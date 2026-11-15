"""Merge two verified Solar sentences and approved local presentation/citation edits."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--response", type=Path, required=True)
    ap.add_argument("--status", type=Path, required=True)
    ap.add_argument("--evidence-root", type=Path, required=True)
    ap.add_argument("--source-map", type=Path, required=True)
    ap.add_argument("--output-validation", type=Path, required=True)
    args = ap.parse_args()

    status = json.loads(args.status.read_text(encoding="utf-8-sig"))
    response = json.loads(args.response.read_text(encoding="utf-8-sig"))
    content = response["choices"][0]["message"]["content"]
    markers = ("<<<SENTENCE_A>>>", "<<<END_SENTENCE_A>>>",
               "<<<SENTENCE_B>>>", "<<<END_SENTENCE_B>>>")
    if status.get("status") != "success" or status.get("returned_model") != "solar-pro4-260806":
        raise SystemExit("Solar status/model validation failed")
    if any(content.count(m) != 1 for m in markers):
        raise SystemExit("Expected output markers were absent or duplicated")
    start_a, end_a, start_b, end_b = markers
    a = content.split(start_a, 1)[1].split(end_a, 1)[0].strip()
    b = content.split(start_b, 1)[1].split(end_b, 1)[0].strip()
    outside = re.sub(re.escape(start_a) + r".*?" + re.escape(end_a), "", content, count=1, flags=re.S)
    outside = re.sub(re.escape(start_b) + r".*?" + re.escape(end_b), "", outside, count=1, flags=re.S)
    if outside.strip() or not a.endswith("[2][D1].") or not b.endswith("[2][5][6][7][D1][D2]."):
        raise SystemExit("Unexpected response text or citation set")

    report_path = args.report
    original = report_path.read_text(encoding="utf-8")
    text = original
    pattern_a = re.compile(r"이 간선은 .*?먼저 명시해야 한다\.")
    pattern_b = re.compile(r"각 모델의 공식 저장소,.*?\[2\]\[5\]\[6\]\[7\]\[D1\]\[D2\]\.")
    old_a, n_a = pattern_a.subn(a, text)
    text = old_a
    old_b, n_b = pattern_b.subn(b, text)
    text = old_b
    if n_a != 1 or n_b != 1:
        raise SystemExit(f"Expected one target sentence each; found A={n_a}, B={n_b}")

    display_values = {"82.9537143%": "82.95%", "77.6954919%": "77.70%",
                      "77.5889033%": "77.59%", "79.7983250%": "79.80%"}
    lines = text.splitlines()
    table_changes = []
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        for raw, shown in display_values.items():
            if raw in line:
                lines[index] = lines[index].replace(raw, shown)
                table_changes.append({"line": index + 1, "raw_evidence_value": raw,
                                      "display_value": shown, "scope": "Markdown table cell only"})
    if len(table_changes) != 4:
        raise SystemExit(f"Expected four display-only yield changes; found {len(table_changes)}")
    text = "\n".join(lines) + ("\n" if original.endswith("\n") else "")

    run = "rerun/benzocaine-live-repro-20261105-01"
    corrected_rel = f"evidence-run/{run}/reproduction-validation-corrected.json"
    original_rel = f"evidence-run/{run}/reproduction-validation-original-conflicting.json"
    corrected = args.evidence_root / run / "reproduction-validation-corrected.json"
    conflicting = args.evidence_root / run / "reproduction-validation-original-conflicting.json"
    if not corrected.is_file() or not conflicting.is_file():
        raise SystemExit("Required corrected/original D10 records are missing")
    c_data = json.loads(corrected.read_text(encoding="utf-8-sig"))
    if c_data.get("status") != "passed":
        raise SystemExit("Corrected D10 record is not passed")
    c_hash, o_hash = sha(corrected), sha(conflicting)
    d10_line = (f"- [D10] `{corrected_rel}` (정정 검증본; SHA-256 `{c_hash}`); "
                f"`{original_rel}` (상충 원본 보존; SHA-256 `{o_hash}`); "
                f"`evidence-run/{run}/verification.json`; `evidence-run/{run}/manifest.json`")
    d10_re = re.compile(r"^- \[D10\].*$", re.MULTILINE)
    text, d10_count = d10_re.subn(d10_line, text)
    if d10_count != 1:
        raise SystemExit(f"Expected one D10 evidence-list entry; found {d10_count}")

    source_map = json.loads(args.source_map.read_text(encoding="utf-8-sig"))
    source_map["sources"]["D10"]["files"] = [
        corrected_rel, original_rel,
        f"evidence-run/{run}/verification.json",
        f"evidence-run/{run}/manifest.json",
    ]
    source_map["sources"]["D10"]["supports"] = (
        "Existing-PC rerun and corrected asset/configuration comparison; the corrected validation is distinct from the preserved original conflicting record."
    )

    report_path.write_text(text, encoding="utf-8", newline="\n")
    args.source_map.write_text(json.dumps(source_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    validation = {
        "status": "passed",
        "solar_targeted_blocks_verified": True,
        "approved_local_edits_verified": True,
        "solar_response_sha256": sha(args.response),
        "solar_run_id": status.get("run_id"),
        "solar_model": status.get("returned_model"),
        "source_report_sha256_before": hashlib.sha256(original.encode("utf-8")).hexdigest(),
        "final_report_sha256": sha(report_path),
        "target_sentence_replacements": [
            {"section": "3.3", "old_anchor": "이 간선은 … 먼저 명시해야 한다.", "new_sentence": a,
             "citations": ["2", "D1"], "evidence": ["D1", "2"]},
            {"section": "5.4", "old_anchor": "각 모델의 공식 저장소, … [D2].", "new_sentence": b,
             "citations": ["2", "5", "6", "7", "D1", "D2"], "evidence": ["D1", "D2", "2", "5", "6", "7"]},
        ],
        "local_edits": {
            "yield_display_rounding_only": table_changes,
            "raw_values_preserved_in_source_evidence": True,
            "D10_corrected_path": corrected_rel,
            "D10_corrected_sha256": c_hash,
            "D10_preserved_original_path": original_rel,
            "D10_original_sha256": o_hash,
        },
        "scope": "No other prose, figures, or analysis changed; new report copy only.",
    }
    args.output_validation.parent.mkdir(parents=True, exist_ok=True)
    args.output_validation.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": validation["status"], "final_report_sha256": validation["final_report_sha256"],
                      "solar_run_id": validation["solar_run_id"], "table_yield_cells": len(table_changes),
                      "D10_corrected_sha256": c_hash, "D10_original_sha256": o_hash}, ensure_ascii=False))


if __name__ == "__main__":
    main()
