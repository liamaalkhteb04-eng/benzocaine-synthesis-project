#!/usr/bin/env python3
"""Build a route/step comparison matrix from verified saved project evidence.

This is a formatting/join utility. It does not infer conditions, explain chemistry,
or combine condition candidates. Candidate rows preserve Parrot's original slots.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SLOT_FIELDS = ("catalyst1", "solvent1", "solvent2", "reagent1", "reagent2")
SELECTED = {"route-01", "route-02", "route-05"}
DEFAULT_CANDIDATE_RANKS = (1, 2, 3)
ROUTE01_CANDIDATE_RANKS = (1, 2, 3, 4)  # Separate alternatives retained as separate rows.


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def md_cell(value: Any) -> str:
    if value is None:
        return "미제공"
    text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence-dir", type=Path, required=True)
    ap.add_argument("--base-report", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    evidence = args.evidence_dir.resolve()
    report_evidence_path = evidence / "report-evidence.json"
    conditions_path = evidence / "latest-route-reproduction" / "conditions-parrot.raw.json"
    yields_path = evidence / "latest-route-reproduction" / "yields-rxn_yields.raw.json"
    literature_path = evidence / "literature-validation" / "route-01-primary-comparison-20261114" / "comparison.json"
    literature_md_path = evidence / "literature-validation" / "route-01-primary-comparison-20261114" / "literature-comparison.md"
    course_path = evidence / "course-evidence-summary.md"
    citation_map_path = evidence / "citation-source-map.json"
    required = (report_evidence_path, conditions_path, yields_path, literature_path, literature_md_path, course_path, citation_map_path, args.base_report.resolve())
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        raise SystemExit("Missing required evidence: " + "; ".join(missing))

    report = read_json(report_evidence_path)
    condition_doc = read_json(conditions_path)
    yield_rows = read_json(yields_path)
    literature = read_json(literature_path)
    literature_md = literature_md_path.read_text(encoding="utf-8")
    course_text = course_path.read_text(encoding="utf-8")
    citation_map = read_json(citation_map_path)
    base_text = args.base_report.read_text(encoding="utf-8")

    route_meta = {r["route_id"]: r for r in report["route_summary"]}
    report_steps = [s for s in report["report_steps"] if s["route_id"] in SELECTED]
    if not report_steps:
        raise SystemExit("No selected report steps found")

    # Use already authored route headings only as labels; do not invent transformation prose.
    headings: dict[str, str] = {}
    step_headings: dict[tuple[str, str], str] = {}
    for line in base_text.splitlines():
        if line.startswith("### "):
            for route_id in SELECTED:
                if re.search(rf"\b{re.escape(route_id)}\b", line) and route_id not in headings:
                    headings[route_id] = line[4:].strip()
        step_match = re.match(r"^#{3,6}\s+.*?\b(route-\d+)/(step-\d+):\s*(.+)$", line)
        if step_match and step_match.group(1) in SELECTED:
            step_headings[(step_match.group(1), step_match.group(2))] = line.lstrip("# ").strip()
    missing_headings = SELECTED - headings.keys()
    if missing_headings:
        raise SystemExit("No existing base-report headings for: " + ", ".join(sorted(missing_headings)))

    cond_by_rxn: dict[str, dict[str, Any]] = {}
    for prediction in condition_doc.get("predictions", []):
        cond_by_rxn[prediction.get("reaction_smiles", "")] = prediction
    yield_by_key = {(y["route_id"], y["step_id"]): y for y in yield_rows}
    lit_rxn = literature.get("reaction_smiles")
    lit_refs = literature.get("literature", [])
    lit_route_step = literature.get("ai_evidence", {}).get("route_step", [])
    lit_applies = lit_route_step == [{"route_id": "route-01", "step_id": "step-01"}]
    if not lit_applies:
        raise SystemExit("Literature comparison route/step mapping did not match its declared route-01 scope")
    source_ids = citation_map.get("sources", {})
    if not all(key in source_ids for key in ("17", "D1", "D9")):
        raise SystemExit("Required project/course source-map entries are missing")
    # Reuse the previously checked human-readable source transcription for display;
    # the machine JSON's en dash was already replaced by '?' in that earlier record.
    literature_table_rows = [line for line in literature_md.splitlines() if line.startswith("|") and ("Organic Syntheses" in line or "US 3,037,046" in line)]
    if len(literature_table_rows) != 2:
        raise SystemExit("Expected the two previously verified route-01 literature rows")
    literature_yield_cells = [line.strip().strip("|").split("|")[-1].strip() for line in literature_table_rows]
    if "91–100%" not in literature_md or "분리/재결정 후 수율" not in literature_md:
        raise SystemExit("Verified Organic Syntheses yield statement is missing from the literature comparison")
    if "약 100% of theory" not in literature_md or "Example IV는 수율법을 별도 정의하지 않는다" not in literature_md:
        raise SystemExit("Verified patent yield/basis statement is missing from the literature comparison")

    rows: list[dict[str, Any]] = []
    for step in report_steps:
        route_id, step_id, reaction = step["route_id"], step["step_id"], step["reaction_smiles"]
        cond = cond_by_rxn.get(reaction)
        yp = yield_by_key.get((route_id, step_id))
        if cond is None or yp is None:
            raise SystemExit(f"Missing exact reaction evidence for {route_id}/{step_id}")
        if yp.get("reaction_smiles") != reaction:
            raise SystemExit(f"Yield reaction mismatch for {route_id}/{step_id}")
        cond_steps = cond.get("steps", [])
        if not any(s.get("route_id") == route_id and s.get("step_id") == step_id for s in cond_steps):
            raise SystemExit(f"Parrot route/step mismatch for {route_id}/{step_id}")
        embedded = step.get("yield_prediction", {})
        if embedded.get("reaction_smiles") != reaction or embedded.get("yield_percent") != yp.get("yield_percent"):
            raise SystemExit(f"report-evidence yield mismatch for {route_id}/{step_id}")

        wanted = ROUTE01_CANDIDATE_RANKS if route_id == "route-01" and step_id == "step-01" else DEFAULT_CANDIDATE_RANKS
        candidates = {c.get("rank"): c for c in cond.get("candidates", [])}
        for rank in wanted:
            candidate = candidates.get(rank)
            if candidate is None:
                raise SystemExit(f"Missing Parrot rank {rank} for {route_id}/{step_id}")
            slots = {field: candidate.get(field, "") for field in SLOT_FIELDS}
            # Compare all fields exactly with the corresponding normalized evidence candidate.
            normalized_candidates = {c.get("rank"): c for c in step.get("conditions", {}).get("candidates", [])}
            normalized = normalized_candidates.get(rank)
            if normalized is None or any(normalized.get(k, "") != v for k, v in slots.items()):
                raise SystemExit(f"Parrot slot mismatch at {route_id}/{step_id}, rank {rank}")
            rows.append({
                "route_id": route_id,
                "route_step_count": route_meta[route_id]["step_count"],
                "step_id": step_id,
                "existing_report_heading": headings[route_id],
                "reaction_smiles": reaction,
                "parrot_rank": rank,
                "parrot_sequence_score": candidate.get("sequence_score"),
                "parrot_original_slots": slots,
                "temperature": cond.get("temperature"),
                "temperature_status": cond.get("temperature_status"),
                "time": cond.get("time"),
                "yield_percent": yp.get("yield_percent"),
                "yield_status": yp.get("yield_status"),
                "conditions_in_yield_input": yp.get("conditions_in_input"),
                "literature_evidence": (
                    [{"key": item.get("key"), "location": item.get("location"), "source_yield_cell": literature_yield_cells[i]}
                     for i, item in enumerate(lit_refs)]
                    if reaction == lit_rxn and route_id == "route-01" and step_id == "step-01" else []
                ),
                "course_evidence_scope": (
                    "PDF 80–81: benzocaine disconnection and sulfuric-acid Fischer example; PDF 90–95: general methanol/acetic-acid Fischer mechanism (teaching example, not route-specific experiment)"
                    if route_id == "route-05" and step_id == "step-02" and "PDF 80–81" in course_text
                    else "No matching experimental literature/course comparison mapped in this evidence packet"
                ),
                "evidence_ids": (["D1", "D9"] if route_id == "route-01" and step_id == "step-01" else (["D1", "17"] if route_id == "route-05" and step_id == "step-02" else ["D1"])),
                "checks_recorded_in_sources": [
                    "temperature/time are not provided by Parrot" if cond.get("temperature") is None and cond.get("time") is None else "temperature/time fields present",
                    "yield model input excludes conditions" if yp.get("conditions_in_input") is False else "yield conditions-input status requires review",
                    "equivalents/pressure are not included in the saved Parrot output",
                ],
            })

    # Explicitly ensure the literature evidence is attached only to its exact route-01 reaction.
    for row in rows:
        if row["reaction_smiles"] != lit_rxn and row["literature_evidence"]:
            raise SystemExit("Literature evidence was attached to a nonmatching reaction")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    md_path = args.output_dir / "route-comparison-matrix.md"
    json_path = args.output_dir / "route-comparison-matrix.audit.json"
    summary_rows = []
    unique_steps = {}
    for row in rows:
        unique_steps.setdefault((row["route_id"], row["step_id"]), row)
    for (route_id, step_id), row in unique_steps.items():
        if row["route_id"] == "route-01":
            evidence_scope = "[D9][D1] 동일 변환의 직접 문헌 사례. Org. Synth. 분리·재결정 후 질량 수율 91–100%; 특허 약 100% 이론량(측정법 별도 정의 없음). 세부 조건은 §6.1."
        elif route_id == "route-05" and step_id == "step-02":
            evidence_scope = "[17, PDF pp. 80–81][D1] 벤조카인 교육 예시; [17, PDF pp. 90–95] 일반 메커니즘 교육자료. 실험 수율 근거 아님."
        else:
            evidence_scope = "[D1] 이 증거 묶음에는 동일 단계의 문헌·강의 사례가 매핑되지 않음."
        summary_rows.append({
            "route_id": route_id,
            "step_id": step_id,
            "route_step_count": row["route_step_count"],
            "transformation_label": step_headings.get((route_id, step_id), row["existing_report_heading"]),
            "evidence_scope": evidence_scope,
            "checks": "Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음.",
        })

    lines = [
        "# 경로 비교 매트릭스 (검증 원자료의 코드 조인)",
        "",
        "경로 개요와 조건 후보의 상세 슬롯을 분리했다. 아래 후보 표는 각 Parrot 후보를 별도 행으로 보존하며, route-01 rank 1과 rank 4도 합치지 않는다. 문헌은 반응 변환의 선례이지 개별 Parrot 후보를 검증한 결과가 아니다. 수율은 반응 구조만 입력한 단계별 모델 예측값이며 조건별 실험 수율이 아니다.",
        "",
        "## 경로 요약",
        "",
        "| 경로·단계 (전체 단계 수) | 기존 보고서의 변환 표기 | 문헌·강의 근거 및 확인 사항 |",
        "|---|---|---|",
    ]
    for row in summary_rows:
        lines.append("| " + " | ".join([
            md_cell(f"{row['route_id']} / {row['step_id']} ({row['route_step_count']}단계)"),
            md_cell(row["transformation_label"]),
            md_cell(row["evidence_scope"] + "<br>" + row["checks"]),
        ]) + " |")
    lines += [
        "",
        "## Parrot 후보·단계별 예측 수율",
        "",
        "| Route / step (경로 단계 수) | Parrot rank | sequence_score | Parrot 원래 슬롯 | Yield-BERT 예측값 / 상태 |",
        "|---|---:|---:|---|---|",
    ]
    for row in rows:
        slots = "; ".join(f"{k}=`{v}`" for k, v in row["parrot_original_slots"].items())
        lines.append("| " + " | ".join([
            md_cell(f"{row['route_id']} / {row['step_id']} ({row['route_step_count']}단계) [D1]"),
            str(row["parrot_rank"]),
            str(row["parrot_sequence_score"]),
            md_cell(slots),
            md_cell(f"{row['yield_percent']:.2f}% / {row['yield_status']} (conditions_in_input={row['conditions_in_yield_input']})"),
        ]) + " |")
    lines += [
        "",
        "## 입력·검증 자료",
        "",
        "- `report-evidence.json`: selected routes, route/step reaction mapping, step counts, normalized yield and candidates.",
        "- `latest-route-reproduction/conditions-parrot.raw.json`: original Parrot slots, rank, score, reaction and route/step links.",
        "- `latest-route-reproduction/yields-rxn_yields.raw.json`: raw/normalized yield record, status and conditions-input flag.",
        "- `literature-validation/route-01-primary-comparison-20261114/comparison.json`: route-01 direct literature comparison only.",
        "- `course-evidence-summary.md`: course page summary; educational evidence is not experimental validation.",
        "",
        "미제공 온도·시간은 Parrot 출력 기준이다. 당량·압력 미기재는 이 결과 묶음의 Parrot 원시 출력에 해당 필드가 없다는 뜻이다. 표의 route-01 문헌은 route-01과 동일 반응 SMILES에 매핑된 사례만 표시한다. route-05의 강의 비교는 교육 예시로 표시하며 실험 문헌으로 취급하지 않는다.",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    input_paths = {
        "report_evidence": report_evidence_path,
        "parrot_raw": conditions_path,
        "yield_raw_normalized_records": yields_path,
        "route01_literature_comparison": literature_path,
        "route01_literature_comparison_text": literature_md_path,
        "course_evidence_summary": course_path,
        "citation_source_map": citation_map_path,
        "base_report_headings_source": args.base_report.resolve(),
    }
    audit = {
        "status": "passed",
        "generator": "scripts/build_route_comparison_matrix.py",
        "scope": "data join and formatting only; no new scientific interpretation",
        "row_count": len(rows),
        "unique_route_step_count": len(summary_rows),
        "summary_rows": summary_rows,
        "selected_route_step_counts": {route: route_meta[route]["step_count"] for route in sorted(SELECTED)},
        "rows": rows,
        "input_files": {name: {"path": str(path), "sha256": sha256(path)} for name, path in input_paths.items()},
        "outputs": {"markdown": md_path.name, "markdown_sha256": sha256(md_path)},
        "assertions": {
            "yield_join_exact_by_route_step_and_reaction": True,
            "parrot_slots_equal_raw_and_normalized": True,
            "route01_rank1_and_rank4_separate_rows": True,
            "candidate_rows_separate_not_combined": True,
            "literature_only_on_matching_route01_reaction": True,
            "no_route_total_yield_calculated": True,
            "course_evidence_not_treated_as_experimental_yield": True,
        },
    }
    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    audit["outputs"]["audit_json_sha256_excluding_self_hash"] = "not_applicable"
    # Write finalized audit after recording markdown digest; audit is intentionally not self-hashed.
    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "passed", "rows": len(rows), "markdown": str(md_path), "audit": str(json_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
