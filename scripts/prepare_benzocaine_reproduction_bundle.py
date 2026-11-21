"""Build a self-contained public report-authoring evidence bundle from verified records.

This copies evidence only; it does not run chemistry models or rewrite the historical report.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from _runtime import ROOT

SOURCE = ROOT / "reports/benzocaine-page-layout-and-instruction-cleanup-20261115/evidence-run"
DEST = ROOT / "reports/benzocaine-reproduction-validation-20261119-07/evidence-run"
REPORT_ROOT = SOURCE.parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_rel(rel: str, target: Path | None = None) -> dict:
    src = SOURCE / rel
    if not src.is_file():
        raise FileNotFoundError(src)
    dst = target or (DEST / rel)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"path": dst.relative_to(DEST).as_posix(), "source_path": src.relative_to(SOURCE).as_posix(), "sha256": sha(dst), "bytes": dst.stat().st_size}


def main() -> int:
    if DEST.exists():
        raise FileExistsError(f"Refusing to replace evidence bundle: {DEST}")
    DEST.mkdir(parents=True)
    copied = []
    required = [
        "input.json", "manifest.json", "validation_notes.json", "course-material-acquisition.md",
        "additional-analysis-status-current.json", "evidence-conflict-resolution.md",
        "mopac-results-interpretation.md", "epi-analysis.md",
        "visualizer-observation-index.csv",
        "visualizer-measurements.csv", "reproducibility-manifest.json",
        "harness-trial-02-comparison-evaluation.md", "harness-trial-02-status.json",
        "harness-trial-02-budget.json", "route05-step02-parrot-rank1-audit.json",
        "figures/figure-index.json", "target/target.png",
        "figures/route-01-step-01.png", "figures/route-02-step-01.png",
        "figures/route-05-step-01.png", "figures/route-05-step-02.png",
        "figures/visualizer-route01-conf1-angle.png", "figures/visualizer-route01-conf1-distance.png",
        "figures/visualizer-route05-ethanol-conf2.png", "figures/visualizer-route05-paba-conf4.png",
        "figures/visualizer-route05-paba-edge.png",
        "literature-validation/route-01-primary-comparison-20261114/literature-comparison.md",
        "literature-validation/route-01-primary-comparison-20261114/comparison.json",
        "literature-validation/route-01-primary-comparison-20261114/validation.json",
        "literature-validation/route-01-primary-comparison-20261114/source-integrity.json",
        "literature-validation/route-01-primary-comparison-20261114/source-acquisition.md",
        "literature-validation/route-01-primary-comparison-20261114/evidence/routes.raw.json",
        "literature-validation/route-01-primary-comparison-20261114/evidence/conditions-parrot.raw.json",
        "literature-validation/route-01-primary-comparison-20261114/evidence/yields-rxn_yields.raw.json",
    ]
    for rel in required:
        copied.append(copy_rel(rel))
    copied.append(copy_rel("target/target.png", DEST / "figures/target.png"))
    # The public accessibility prose copy contains question-mark corruption.
    # Include the intact original measurement interpretation and machine-readable
    # observation/measurement records instead; do not repair or overwrite history.
    visualizer_source = Path(r"<ASPIRIN_TEST_PROJECT>\analyses\visualizer\visualizer-measurement-interpretation.md")
    if not visualizer_source.is_file():
        raise FileNotFoundError("Intact Visualizer measurement interpretation is unavailable")
    visualizer_dst = DEST / "visualizer-measurement-interpretation.md"
    shutil.copy2(visualizer_source, visualizer_dst)
    copied.append({"path": visualizer_dst.relative_to(DEST).as_posix(), "source_path": "local project analyses/visualizer/visualizer-measurement-interpretation.md (read-only copy)", "sha256": sha(visualizer_dst), "bytes": visualizer_dst.stat().st_size})

    # Add exact run-level raw data for all route IDs and a separately indexed subset for detailed routes.
    latest = SOURCE / "latest-route-reproduction"
    raw_rel = ["routes.raw.json", "routes.json", "conditions-parrot.raw.json", "conditions-parrot.json", "yields-rxn_yields.raw.json", "yields-rxn_yields.json", "manifest.json", "reproduction-validation.json", "step-validation.json", "pipeline.log"]
    for rel in raw_rel:
        src = latest / rel
        if not src.is_file():
            raise FileNotFoundError(src)
        dst = DEST / "latest-route-reproduction" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append({"path": dst.relative_to(DEST).as_posix(), "source_path": src.relative_to(SOURCE).as_posix(), "sha256": sha(dst), "bytes": dst.stat().st_size})

    # The raw AiZynthFinder tree has many alternatives. Preserve an exact slice
    # of the three report routes and record the parent raw file hash and indices.
    raw_routes_path = latest / "routes.raw.json"
    raw_routes = json.loads(raw_routes_path.read_text(encoding="utf-8"))
    selected_raw = {
        "source_path": raw_routes_path.relative_to(SOURCE).as_posix(),
        "source_sha256": sha(raw_routes_path),
        "selection_method": "exact complete route-tree objects selected by target-root child template and precursor SMILES; no content rewritten",
        "source_list_indices_zero_based": {"route-01": 0, "route-02": 1, "route-05": 4},
        "routes": {"route-01": raw_routes[0], "route-02": raw_routes[1], "route-05": raw_routes[4]},
    }
    selected_raw_path = DEST / "latest-route-reproduction/routes-selected-raw.json"
    write_json(selected_raw_path, selected_raw)
    copied.append({"path": selected_raw_path.relative_to(DEST).as_posix(), "source_path": raw_routes_path.relative_to(SOURCE).as_posix(), "source_sha256": sha(raw_routes_path), "sha256": sha(selected_raw_path), "bytes": selected_raw_path.stat().st_size, "derivative": "selected complete raw route trees; indices preserved"})

    # Make a separate report-authoring derivative whose figure paths point to the
    # exact public bytes copied into this bundle. Historical source manifests remain intact.
    evidence_path = DEST / "report-evidence.json"
    shutil.copy2(SOURCE / "report-evidence.json", evidence_path)
    source_evidence_sha = sha(evidence_path)
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    figure_manifest = json.loads((DEST / "figures/figure-index.json").read_text(encoding="utf-8"))
    by_name = {item["basename"]: item for item in figure_manifest}
    for item in evidence.get("report_figure_assets", []):
        basename = Path(item["path"].replace("\\", "/")).name
        if basename not in by_name:
            raise ValueError(f"report figure absent from copied figure manifest: {basename}")
        asset = DEST / "figures" / basename
        item["path"] = f"figures/{basename}"
        item["sha256"] = sha(asset)
    evidence.pop("steps", None)
    write_json(evidence_path, evidence)
    copied.append({"path": "report-evidence.json", "source_path": "evidence-run/report-evidence.json with figure paths rebound to exact copied assets and redundant unselected step detail omitted", "source_sha256": source_evidence_sha, "sha256": sha(evidence_path), "bytes": evidence_path.stat().st_size, "derivative": True})

    # Report-specific source map is versioned beside the historical report, not global.
    citation_src = REPORT_ROOT / "citation-source-map.json"
    citation_dst = DEST / "citation-source-map.json"
    shutil.copy2(citation_src, citation_dst)
    citation_map = json.loads(citation_dst.read_text(encoding="utf-8"))
    citation_map["sources"]["16"]["files"] = ["evidence-run/manifest.json", "evidence-run/reproducibility-manifest.json"]
    citation_map["sources"]["17"] = {
        "type": "course",
        "supports": "Course-only claims summarized from the specified original lecture pages; original PDF excluded from redistribution.",
        "files": ["evidence-run/course-evidence-summary.md", "evidence-run/course-material-acquisition.md"],
        "url": "User obtains the course file from the course LMS."
    }
    citation_map["sources"]["D7"]["files"] = ["evidence-run/visualizer-measurement-interpretation.md", "evidence-run/visualizer-observation-index.csv", "evidence-run/visualizer-measurements.csv"]
    citation_dst.write_text(json.dumps(citation_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    copied.append({"path": citation_dst.relative_to(DEST).as_posix(), "source_path": "../citation-source-map.json", "sha256": sha(citation_dst), "bytes": citation_dst.stat().st_size})

    # Provenance is a user-provided fact for this run, not a reusable target-specific skill rule.
    context = {
        "target_id": "benzocaine",
        "selection_provenance": {"selected_by": "user", "basis": "The user explicitly selected Benzocaine as the final project target in the conversation; this fact is task provenance, not a model inference."},
        "identity": {"name": "Benzocaine", "name_ko": "벤조카인", "smiles": "CCOC(=O)c1ccc(N)cc1", "formula": "C9H11NO2", "pubchem_cid": 2337, "identity_url": "https://pubchem.ncbi.nlm.nih.gov/compound/2337"},
        "no_reuse_rule": "This additional analysis evidence applies only to the recorded Benzocaine structures and runs. Do not attach it to another target or a new run unless separately performed."
    }
    context_path = DEST / "report-context.json"
    write_json(context_path, context)
    copied.append({"path": context_path.relative_to(DEST).as_posix(), "source_path": "current task user instruction and inputs/benzocaine.json", "sha256": sha(context_path), "bytes": context_path.stat().st_size})

    # Self-authored factual course note derived from specified pages; no lecture PDF is redistributed.
    course_text = """# 강의 근거 메모(원문 PDF 미포함)\n\n출처: `02_반응과_전자이동_개선_v2.pdf`, 수업 LMS에서 수강자가 확보. 공개 패키지는 재배포 권한이 확인되지 않은 원문을 포함하지 않는다. 원문 확보 안내는 `course-material-acquisition.md` 참조. 이 메모는 지정 쪽을 직접 확인해 핵심 사실만 자체 요약한 것이며 강의 원문을 대체하지 않는다.\n\n- PDF 80–81쪽(인쇄 쪽수 78–79): 벤조카인 역합성 예시는 에틸 에스터 결합을 끊어 4-아미노벤조산과 에탄올을 전구체로 제시하고, 정방향으로 황산 촉매 피셔 에스터화를 든다.\n- PDF 83–84쪽(인쇄 쪽수 81–82): 과제는 단계별 새 결합·작용기 변화, 전자쌍의 출발·도착, 형식전하, 시약·촉매·용매 역할 설명을 요구한다.\n- PDF 90–95쪽(인쇄 쪽수 88–93): 피셔 에스터화 그림은 카보닐 산소 양성자화, 알코올 산소의 비공유전자쌍이 카보닐 탄소로 이동하며 새 C–O 결합 형성, 카보닐 π 전자 이동, 양성자 이동, 물 이탈과 C=O 재형성, 촉매 재생 순서를 제시한다. 예시는 메탄올/아세트산 계열 그림이며 이를 벤조카인 반응의 직접 실험조건으로 오인하지 않는다.\n\n원문 URL/확보: 수강 권한이 있는 사용자는 강의 LMS에서 파일을 확보한다. 원문 전체는 업로드하지 않는다. 페이지 인용은 PDF 쪽수 기준이다.\n"""
    course_path = DEST / "course-evidence-summary.md"
    course_path.write_text(course_text, encoding="utf-8", newline="\n")
    copied.append({"path": course_path.relative_to(DEST).as_posix(), "source_path": "user-provided course PDF, pages 80-81, 83-84, 90-95; derived summary", "sha256": sha(course_path), "bytes": course_path.stat().st_size})

    # Preserve both historical conflicting record and corrected record in bundle.
    rerun = SOURCE / "rerun/benzocaine-live-repro-20261105-01"
    for name in ["reproduction-validation-corrected.json", "reproduction-validation-original-conflicting.json", "verification.json", "manifest.json", "reproduction-validation.json"]:
        src = rerun / name
        if src.is_file():
            dst = DEST / "rerun/benzocaine-live-repro-20261105-01" / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append({"path": dst.relative_to(DEST).as_posix(), "source_path": src.relative_to(SOURCE).as_posix(), "sha256": sha(dst), "bytes": dst.stat().st_size})

    # Link every figure against bytes and descriptions actually copied.
    fig_index = json.loads((DEST / "figures/figure-index.json").read_text(encoding="utf-8"))
    for item in fig_index:
        asset = DEST / "figures" / item["basename"]
        if not asset.is_file():
            raise FileNotFoundError(f"figure manifest asset absent: {item['path']}")
        item["sha256_actual"] = sha(asset)
        item["exists"] = True
    write_json(DEST / "figures/figure-index-verified.json", fig_index)
    copied.append({"path": "figures/figure-index-verified.json", "source_path": "derived from copied figure-index.json and exact asset bytes", "sha256": sha(DEST / "figures/figure-index-verified.json"), "bytes": (DEST / "figures/figure-index-verified.json").stat().st_size})

    manifest = {"schema_version": 1, "bundle_id": DEST.parent.name, "source_report_bundle": "reports/benzocaine-page-layout-and-instruction-cleanup-20261115/evidence-run", "report_is_not_included_as_authoring_input": True, "course_original_pdf_included": False, "sources": copied}
    write_json(DEST / "authoring-evidence-manifest.json", manifest)
    print(json.dumps({"bundle": str(DEST.relative_to(ROOT)), "files": len(copied) + 1, "bytes": sum(x["bytes"] for x in copied), "figure_assets": len(fig_index), "course_original_included": False}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
