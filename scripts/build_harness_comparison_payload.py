"""Create one identical, read-only evidence attachment for both harnesses."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "analyses/harness-comparison/comparison-system-prompt.txt",
    "skill/report-writing/SKILL.md",
    "results/benzocaine-live-20261031-04/report-evidence.json",
    "results/benzocaine-live-20261031-04/validation_notes.json",
    "analyses/mopac/results-interpretation.md",
    "analyses/epi-suite/analysis.md",
    "analyses/visualizer/visualizer-measurement-interpretation.md",
    "analyses/visualizer/visualizer-measurements.csv",
    "analyses/visualizer/route-selection.json",
    "analyses/visualizer/visualizer-session-status.json",
    "results/benzocaine-live-20261031-04/additional-analysis-status.json",
]
TASK = "analyses/harness-comparison/comparison-task.md"
OUT = "analyses/harness-comparison/comparison-input-payload-report-writing-v1.md"
MANIFEST = "analyses/harness-comparison/comparison-input-payload-report-writing-v1-manifest.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true", help="rebuild to memory and compare with existing payload")
    args = parser.parse_args()
    source_paths = [TASK, *FILES]
    contents: dict[str, bytes] = {}
    for relative in source_paths:
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"Missing required fixed input: {relative}")
        contents[relative] = path.read_bytes()
    chunks = [
        b"# Solar Pro 4 harness comparison: single-call draft request\n\n",
        b"Create one Korean comparison draft from this single attachment. No tools, external search, file operations, or follow-up requests. This is not the final submission report. Preserve uncertainty and report only evidence included below. The eventual final report must be authored by Solar Pro 4 from the skill and actual results, include additional analyses, and remain within 20 pages including references.\n\n",
    ]
    for relative in source_paths:
        raw = contents[relative]
        text = raw.decode("utf-8-sig").rstrip()
        if relative == TASK:
            # The source task is a preserved historical artifact; new payloads
            # route its skill reference to the report-only Solar prompt.
            text = text.replace("skill/synthesis_report_skill.md", "skill/report-writing/SKILL.md")
        chunks.extend([
            f"\n\n--- BEGIN SOURCE: {relative} ---\n".encode("utf-8"),
            text.encode("utf-8"),
            f"\n--- END SOURCE: {relative} ---\n".encode("utf-8"),
        ])
    payload = b"".join(chunks)
    out_path = ROOT / OUT
    if args.verify:
        if not out_path.is_file() or out_path.read_bytes() != payload:
            raise SystemExit("Payload verification failed: source inputs changed or payload differs.")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(payload)
    entries = []
    for relative in source_paths:
        data = contents[relative]
        rendered = data.decode("utf-8-sig").rstrip()
        if relative == TASK:
            rendered = rendered.replace("skill/synthesis_report_skill.md", "skill/report-writing/SKILL.md")
        entry = {"path": relative, "sha256": sha256(data), "bytes": len(data),
                 "rendered_payload_text_sha256": sha256(rendered.encode("utf-8"))}
        if relative == TASK and rendered.encode("utf-8") != data.decode("utf-8-sig").rstrip().encode("utf-8"):
            entry["payload_transform"] = "redirect historical skill path to skill/report-writing/SKILL.md; source task remains unchanged"
        entries.append(entry)
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "payload_path": OUT,
        "payload_sha256": sha256(payload),
        "payload_bytes": len(payload),
        "inputs": entries,
        "same_byte_payload_for_both_harnesses": True,
        "model_calls": 0,
        "images_embedded": False,
        "visualizer_measurement_text_and_capture_references_included": True,
    }
    manifest_path = ROOT / MANIFEST
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"payload_path": OUT, "payload_bytes": len(payload), "payload_sha256": sha256(payload), "input_count": len(entries), "model_calls": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
