"""Copy saved Solar Markdown and repair the known corrupted lecture page-range dash."""
import argparse
import hashlib
import json
from pathlib import Path


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.manifest.exists():
        parser.error("Output exists; use a fresh rebuild folder")
    original = args.input.read_text(encoding="utf-8")
    old = "PDF pp. 90?95"
    new = "PDF pp. 90–95"
    count = original.count(old)
    if count > 1:
        raise ValueError("Unexpected repeated corrupted page-range token")
    corrected = original.replace(old, new)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(corrected, encoding="utf-8")
    record = {
        "status": "success",
        "source_path": str(args.input.resolve()),
        "source_sha256": sha256(args.input),
        "output_path": str(args.output.resolve()),
        "output_sha256": sha256(args.output),
        "text_authoring_or_model_call": False,
        "typographic_repairs": [{"from": old, "to": new, "count": count}],
    }
    args.manifest.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": record["status"], "repairs": count, "output_sha256": record["output_sha256"]}))


if __name__ == "__main__":
    main()
