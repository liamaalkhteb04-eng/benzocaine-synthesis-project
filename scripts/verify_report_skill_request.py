"""Offline-check that both report request builders send the report-writing skill."""
from __future__ import annotations
import hashlib
import json
import shutil
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from _runtime import ROOT, load
from scripts.generate_solar_report_from_bundle import make_request


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, help="Optional real run outside the package, for read-only request-construction validation")
    parser.add_argument("--output", type=Path, default=ROOT / "validation/report-writing-skill-request-offline-check-final-03.json",
                        help="New verification record path; existing records are never overwritten")
    args = parser.parse_args()
    config = load(ROOT / "configs/report-plan.json")
    execution_path = ROOT / config["execution_skill_path"]
    writing_path = ROOT / config["report_writing_skill_path"]
    execution_text = execution_path.read_text(encoding="utf-8")
    writing_text = writing_path.read_text(encoding="utf-8")
    if "report-writing/SKILL.md" not in execution_text:
        raise SystemExit("The full-run skill does not route to the report-writing skill.")

    run_source = args.run_dir.resolve() if args.run_dir else ROOT / "results/benzocaine-live-20261031-04"
    bundle_source = ROOT / "reports/benzocaine-page-layout-and-instruction-cleanup-20261115"
    evidence_for_run = load(run_source / "report-evidence.json")
    bad_hashes = [name for name, sha in evidence_for_run.get("source_hashes", {}).items()
                  if not (run_source / name).is_file() or hashlib.sha256((run_source / name).read_bytes()).hexdigest() != sha]
    checks: dict[str, object] = {
        "status": "passed",
        "scope": "Offline request construction only; no network request, Solar call, or chemical inference.",
        "execution_skill_path": str(execution_path.relative_to(ROOT)),
        "execution_skill_sha256": hashlib.sha256(execution_path.read_bytes()).hexdigest(),
        "report_writing_skill_path": str(writing_path.relative_to(ROOT)),
        "report_writing_skill_sha256": hashlib.sha256(writing_path.read_bytes()).hexdigest(),
        "run_id": run_source.name,
        "run_dir_origin": "packaged run" if run_source.is_relative_to(ROOT) else "external read-only existing run; absolute path omitted",
        "source_hash_mismatch_count": len(bad_hashes),
        "modes": {},
    }
    if bad_hashes:
        raise SystemExit("Refusing to construct a request from changed evidence sources: " + ", ".join(bad_hashes))
    forbidden_historical_instructions = [
        "Create one Korean comparison draft",
        "Return exactly the two replacement blocks requested",
        "targeted-benzocaine-section-revision-v1.md",
    ]
    with tempfile.TemporaryDirectory(prefix="report-skill-request-check-") as temp_dir:
        temp = Path(temp_dir)
        copied_run = temp / "run"
        shutil.copytree(run_source, copied_run)
        attempt_id = "offline-report-skill-check"
        proc = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(ROOT / "scripts/generate_report.py"),
             "--run-dir", str(copied_run), "--attempt-id", attempt_id, "--prepare-only"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        if proc.returncode:
            raise SystemExit("Generic request preparation failed offline: " + proc.stderr[-1200:])
        generic_request_path = copied_run / "solar-attempts" / attempt_id / "solar-request.json"
        generic = json.loads(generic_request_path.read_text(encoding="utf-8"))
        generic_messages = generic.get("messages", [])
        generic_user = "\n".join(m.get("content", "") for m in generic_messages if m.get("role") == "user")
        generic_ok = (
            bool(generic_messages)
            and generic_messages[0].get("role") == "system"
            and generic_messages[0].get("content") == writing_text
            and '"target":' in generic_user
            and '"steps":' in generic_user
            and not any(x in generic_user for x in forbidden_historical_instructions)
        )
        if not generic_ok:
            raise SystemExit("Generic Solar request does not contain the expected skill and evidence.")
        checks["modes"]["general_run"] = {
            "prepared_request": True,
            "system_message_exactly_matches_report_skill": True,
            "target_evidence_in_user_message": True,
            "source_hashes_validated_before_request": True,
            "external_requests": 0,
        }

        attempt = temp / "bundle-attempt"
        attempt.mkdir()
        bundle_request, source_manifest = make_request(bundle_source, attempt)
        messages = bundle_request.get("messages", [])
        bundle_user = "\n".join(m.get("content", "") for m in messages if m.get("role") == "user")
        labels = {x.get("label") for x in source_manifest}
        required_labels = {
            "EVIDENCE_RUN_REPORT_EVIDENCE_JSON", "CURRENT_STATUS", "VALIDATION_NOTES",
            "MOPAC_RESULTS", "EPI_RESULTS", "VISUALIZER_OBSERVATIONS",
            "VISUALIZER_ATOM_AND_SCREEN_INDEX", "VISUALIZER_MEASUREMENTS",
            "REPRODUCIBILITY_MANIFEST", "HARNESS_COMPARISON_EVALUATION",
        }
        bundle_ok = (
            bool(messages)
            and messages[0].get("role") == "system"
            and messages[0].get("content") == writing_text
            and "EVIDENCE_RUN_REPORT_EVIDENCE_JSON" in bundle_user
            and required_labels.issubset(labels)
            and len(source_manifest) >= 12
            and "EXPLICIT_FULL_REPORT_BRIEF" not in labels
        )
        if not bundle_ok:
            raise SystemExit("Evidence-bundle request does not contain the expected skill/evidence.")
        stale_in_system = [x for x in forbidden_historical_instructions if x in messages[0]["content"]]
        stale_in_user = [x for x in forbidden_historical_instructions if x in bundle_user]
        if stale_in_system or stale_in_user:
            raise SystemExit("Historical task instruction leaked into the default full-report request.")
        checks["modes"]["evidence_bundle"] = {
            "request_built_without_send": True,
            "system_message_exactly_matches_report_skill": True,
            "verified_evidence_blocks": sorted(labels),
            "historical_ab_or_targeted_task_instruction_in_default_request": False,
            "external_requests": 0,
        }

    output = args.output if args.output.is_absolute() else ROOT / args.output
    if output.exists():
        raise SystemExit(f"Refusing to overwrite prior verification: {output.relative_to(ROOT)}")
    output.write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "passed", "verification": output.relative_to(ROOT).as_posix(), "external_requests": 0}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
