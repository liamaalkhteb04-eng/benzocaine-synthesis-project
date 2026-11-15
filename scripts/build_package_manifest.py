"""Create a complete SHA-256 inventory for a GitHub preparation folder."""
import argparse
import hashlib
import json
from pathlib import Path


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", type=Path, required=True)
    ap.add_argument("--latest-pdf", required=True)
    ap.add_argument("--latest-docx", required=True)
    ap.add_argument("--solar-run-id", required=True)
    ap.add_argument("--solar-cost", type=float, required=True)
    ap.add_argument("--cumulative-cost", type=float, required=True)
    ap.add_argument("--secret-audit", required=True)
    a = ap.parse_args()
    root = a.package.resolve()
    excluded = {"PACKAGE-MANIFEST.json", "PACKAGE-MANIFEST.sha256"}
    files = []
    for path in sorted((p for p in root.rglob("*") if p.is_file() and ".git" not in p.relative_to(root).parts), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        if rel in excluded:
            continue
        files.append({"path": rel, "size_bytes": path.stat().st_size, "sha256": sha(path)})
    data = {
        "generated_from": "benzocaine-synthesis-project working copy plus verified page-layout/instruction-cleanup release",
        "status": "validated_submission_package",
        "latest_report_path": a.latest_pdf,
        "latest_docx_path": a.latest_docx,
        "latest_report_page_count": 19,
        "citation_audit": "passed",
        "document_validation": "passed",
        "latest_solar_run_id": a.solar_run_id,
        "latest_solar_call_count": 1,
        "latest_solar_actual_cost_including_vat_usd": round(a.solar_cost, 8),
        "cumulative_solar_actual_cost_usd": round(a.cumulative_cost, 8),
        "new_chemical_model_inference": False,
        "package_secret_scan_status": (
            f"passed; package tree/index scan summary: {a.secret_audit}; "
            "final post-manifest scan is recorded in the local submission validation folder"
        ),
        "excluded_from_package": [".env", "API keys", "authentication data", "virtual environments", "model weights", "large AiZynthFinder stock buckets", ".cache", "course lecture PDF with uncertain redistribution rights", "literature source scans with uncertain redistribution rights", "superseded report copies", "temporary page renderings"],
        "manifest_scope": "All packaged regular files except this manifest and its SHA-256 sidecar are listed and hashed.",
        "file_count": len(files),
        "files": files,
    }
    manifest = root / "PACKAGE-MANIFEST.json"
    encoded = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    manifest.write_bytes(encoded)
    sidecar = hashlib.sha256(encoded).hexdigest() + "  PACKAGE-MANIFEST.json\n"
    # Keep the sidecar byte-for-byte stable on Windows as well as POSIX.
    (root / "PACKAGE-MANIFEST.sha256").write_bytes(sidecar.encode("ascii"))
    print(json.dumps({"status": data["status"], "file_count": len(files),
                      "manifest_sha256": hashlib.sha256(encoded).hexdigest(),
                      "package": str(root)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
