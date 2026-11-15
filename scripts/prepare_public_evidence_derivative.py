"""Create a lineage-tracked, path-anonymized public copy of an existing result bundle."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

from _runtime import ROOT, digest, load, save


PATH_FIELDS = {
    "input_path", "log_path", "raw_path", "checkpoint", "command", "image_path",
    "path", "source_path",
}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def walk_differences(old, new, pointer=""):
    if pointer == "/asset_sha256" and isinstance(old, dict) and isinstance(new, dict):
        if sorted(old.values()) == sorted(new.values()):
            return [(pointer, "path_keyed_asset_hash_map", "path_metadata_only")]
        return [(pointer, "path_keyed_asset_hash_map", "non_path_value_changed")]
    if isinstance(old, dict) and isinstance(new, dict):
        differences = []
        for key in sorted(set(old) | set(new)):
            if key not in old or key not in new:
                differences.append((pointer + "/" + key, key, "missing_or_added"))
            else:
                differences.extend(walk_differences(old[key], new[key], pointer + "/" + key))
        return differences
    if isinstance(old, list) and isinstance(new, list):
        differences = []
        if len(old) != len(new):
            differences.append((pointer + "/length", "length", "changed"))
        for index, (left, right) in enumerate(zip(old, new)):
            differences.extend(walk_differences(left, right, pointer + "/" + str(index)))
        return differences
    if old == new:
        return []
    leaf = pointer.rsplit("/", 1)[-1]
    # The asset hash map keys are filesystem paths; their digest values must be identical.
    if pointer.startswith("/asset_sha256/"):
        return [] if old == new else [(pointer, "asset_path_key_or_hash", "changed")]
    if leaf in PATH_FIELDS:
        return [(pointer, leaf, "path_metadata_only")]
    if (isinstance(old, str) and isinstance(new, str)
            and re.match(r"^[A-Za-z]:[\\/]", old)
            and (re.match(r"^[A-Za-z]:[\\/]", new) or new.startswith((".\\", "./", "<")))):
        return [(pointer, "path_value", "path_metadata_only")]
    return [(pointer, leaf, "non_path_value_changed")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--published-source", type=Path, required=True,
                        help="Existing path-anonymized result bundle in this package")
    parser.add_argument("--historical-source", type=Path, required=True,
                        help="Read-only original run, used only to verify anonymization lineage")
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if Path(args.run_id).name != args.run_id or args.run_id in {".", ".."}:
        parser.error("run-id must be a simple directory name")
    published = args.published_source.resolve()
    historical = args.historical_source.resolve()
    destination = ROOT / "results" / args.run_id
    if destination.exists():
        parser.error(f"Destination already exists: results/{args.run_id}")
    for source in (published, historical):
        for required in ("input.json", "routes.json", "conditions-parrot.json",
                         "yields-rxn_yields.json", "figures/manifest.json", "manifest.json"):
            if not (source / required).is_file():
                raise FileNotFoundError(f"Missing {required} in supplied source bundle")

    old_manifest = load(historical / "manifest.json")
    old_evidence = load(historical / "report-evidence.json")
    source_pairs = ["input.json", "routes.json", "conditions-parrot.json",
                    "yields-rxn_yields.json", "figures/manifest.json"]
    anonymization = {}
    for rel in source_pairs:
        old_path, public_path = historical / rel, published / rel
        expected_old = old_manifest.get("files", {}).get(rel)
        evidence_expected = old_evidence.get("source_hashes", {}).get(rel)
        actual_old = sha(old_path)
        if expected_old and actual_old != expected_old:
            raise ValueError(f"Historical execution manifest mismatch for {rel}")
        if evidence_expected != expected_old:
            raise ValueError(f"Historical evidence/manifest hash disagreement for {rel}")
        entry = {
            "historical_execution_sha256": actual_old,
            "published_path_anonymized_sha256": sha(public_path),
            "byte_identical": actual_old == sha(public_path),
        }
        if rel != "input.json":
            old_json = json.loads(old_path.read_text(encoding="utf-8"))
            public_json = json.loads(public_path.read_text(encoding="utf-8"))
            diffs = walk_differences(old_json, public_json)
            non_path = [item for item in diffs if item[2] != "path_metadata_only"]
            if non_path:
                raise ValueError(f"Non-path result changes found in {rel}: {non_path[:5]}")
            entry["changed_json_pointer_count"] = len(diffs)
            entry["changed_json_pointers"] = [item[0] for item in diffs]
            entry["semantic_non_path_differences"] = 0
        elif actual_old != sha(public_path):
            raise ValueError("Target input differs between historical and public source")
        anonymization[rel] = entry

    # Preserve prediction/evidence files, but omit stale request attempts and old manifests
    # that claim hashes for the pre-anonymized bytes.
    def omit_stale_root_records(directory, names):
        if Path(directory).resolve() != published:
            return set()
        return {name for name in names if name in {
            "solar-attempts", "manifest.json", "report-evidence.json",
            "validation_notes.json", "step-validation.json", "public-derivation.json",
        }}

    shutil.copytree(published, destination, ignore=omit_stale_root_records)

    sys.path.insert(0, str(ROOT / "scripts"))
    import build_evidence
    evidence = build_evidence.build(destination)
    for item in evidence.get("report_figure_assets", []):
        path = Path(item["path"]).resolve()
        try:
            item["path"] = path.relative_to(ROOT).as_posix()
        except ValueError:
            raise ValueError("Report figure is outside the portable package")
    evidence["condition_results_file"] = (destination / "conditions-parrot.json").relative_to(ROOT).as_posix()
    evidence["source_hash_scope"] = "Exact bytes of this path-anonymized public derivative; historical model-input hashes remain in the original prediction outputs and public-derivation.json."
    evidence["public_derivation_record"] = (destination / "public-derivation.json").relative_to(ROOT).as_posix()
    save(destination / "report-evidence.json", evidence)
    save(destination / "validation_notes.json", {
        "artifact_type": "deterministic_checks_not_a_Solar_report",
        "target_id": evidence["target"]["target_id"],
        "notes": evidence["limitations"],
        "applicability": "not_assessed",
        "source_hashes": evidence["source_hashes"],
        "source_hash_scope": evidence["source_hash_scope"],
    })
    save(destination / "step-validation.json", {
        "status": "passed",
        "route_count": len(evidence["route_summary"]),
        "step_count": len(evidence["steps"]),
        "multi_step_route_count": sum(r["step_count"] > 1 for r in evidence["route_summary"]),
        "conditions_joined": sum(s["conditions"] is not None for s in evidence["steps"]),
        "yields_joined": sum(s["yield_prediction"] is not None for s in evidence["steps"]),
        "scope": "Exact route/step/reaction joins for this public derivative; not chemical feasibility validation.",
    })

    derivation = {
        "status": "passed",
        "artifact_type": "public_path_anonymized_evidence_derivative",
        "source_run_id": historical.name,
        "source_execution_manifest_sha256": sha(historical / "manifest.json"),
        "source_manifest_statuses": old_manifest.get("statuses"),
        "new_inference_executed": False,
        "report_generated": False,
        "network_requests": 0,
        "parity_scope": "The four model/figure JSON files were structurally compared with the original run. Changed fields were limited to local paths, commands, checkpoints, path-keyed asset-hash labels, and image paths; scientific values were unchanged.",
        "source_files": anonymization,
    }
    save(destination / "public-derivation.json", derivation)

    # This manifest describes this derivative, not a historical execution. Keep the
    # original execution manifest hash and source file digests above for provenance.
    derivative_files = {}
    for path in sorted((p for p in destination.rglob("*") if p.is_file()),
                       key=lambda p: p.relative_to(destination).as_posix()):
        if path.name == "manifest.json" or "solar-attempts" in path.parts:
            continue
        derivative_files[path.relative_to(destination).as_posix()] = sha(path)
    derivative_manifest = {
        "artifact_type": "public_curated_evidence_derivative_not_execution_record",
        "source_run_id": historical.name,
        "source_execution_manifest_sha256": derivation["source_execution_manifest_sha256"],
        "prediction_statuses_from_source_run": old_manifest.get("statuses"),
        "new_inference_executed": False,
        "solar_call_executed": False,
        "files_scope": "SHA-256 of each file in this derivative before any solar-attempts are prepared; original execution hashes are in public-derivation.json.",
        "files": derivative_files,
    }
    save(destination / "manifest.json", derivative_manifest)
    print(json.dumps({"status": "passed", "run_id": args.run_id,
                      "source_files_verified": len(anonymization),
                      "routes": len(evidence["route_summary"]),
                      "steps": len(evidence["steps"]),
                      "network_requests": 0, "model_calls": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
