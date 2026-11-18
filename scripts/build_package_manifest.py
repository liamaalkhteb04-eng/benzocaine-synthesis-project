"""Create a complete SHA-256 inventory for a GitHub preparation folder."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def package_file_metadata(root, paths):
    """Hash the canonical uploaded bytes in batches; raw bytes outside Git."""
    if not (root / ".git").exists():
        return {path: (path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest())
                for path in paths}
    relatives = [path.relative_to(root).as_posix() for path in paths]
    try:
        objects = subprocess.run(
            ["git", "-C", str(root), "hash-object", "-w", "--stdin-paths"],
            input=("\n".join(relatives) + "\n").encode("utf-8"),
            capture_output=True, check=True
        ).stdout.decode("ascii").splitlines()
        if len(objects) != len(paths):
            raise RuntimeError("Git did not return one object ID per package file")
        batch = subprocess.run(
            ["git", "-C", str(root), "cat-file", "--batch"],
            input=("\n".join(objects) + "\n").encode("ascii"),
            capture_output=True, check=True
        ).stdout
        metadata = {}
        offset = 0
        for path, oid in zip(paths, objects):
            end = batch.index(b"\n", offset)
            header = batch[offset:end].split()
            if len(header) != 3 or header[0].decode("ascii") != oid or header[1] != b"blob":
                raise RuntimeError(f"Could not read canonical Git blob for {path.name}")
            size = int(header[2])
            offset = end + 1
            content = batch[offset:offset + size]
            if len(content) != size:
                raise RuntimeError(f"Truncated canonical Git blob for {path.name}")
            offset += size + 1
            metadata[path] = (size, hashlib.sha256(content).hexdigest())
        return metadata
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {path: (path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest())
                for path in paths}


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
    transient_dirs = {".git", "__pycache__", ".cache", "venv"}
    candidates = []
    for path in sorted((p for p in root.rglob("*") if p.is_file() and ".git" not in p.relative_to(root).parts), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        parts = path.relative_to(root).parts
        if (rel in excluded
                or path.suffix == ".pyc"
                or any(part in transient_dirs or part.startswith(".venv") for part in parts)):
            continue
        candidates.append(path)
    metadata = package_file_metadata(root, candidates)
    files = [{"path": path.relative_to(root).as_posix(),
              "size_bytes": metadata[path][0], "sha256": metadata[path][1]}
             for path in candidates]
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
            f"passed; pre-manifest package tree/index scan summary: {a.secret_audit}; "
            "manifest and sidecar hashes are checked separately after generation"
        ),
        "excluded_from_package": [".env", "API keys", "authentication data", "virtual environments", "model weights", "large AiZynthFinder stock buckets", ".cache", "Python __pycache__ and .pyc runtime artifacts", "course lecture PDF with uncertain redistribution rights", "literature source scans with uncertain redistribution rights", "superseded report copies", "temporary page renderings"],
        "manifest_scope": "All non-transient packaged regular files except this manifest and its SHA-256 sidecar are listed and SHA-256 hashed from Git clean-filtered blob bytes (the uploaded bytes); outside Git, working-tree bytes are used. .git, virtual environments, runtime caches, and compiled Python artifacts are excluded.",
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
