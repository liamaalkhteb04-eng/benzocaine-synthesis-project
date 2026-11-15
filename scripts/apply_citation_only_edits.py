"""Apply the two reviewed source-citation additions; no scientific prose is edited."""
import argparse
from collections import Counter
import hashlib
import json
import re
from pathlib import Path

CITATION = re.compile(r"\[(D\d+|\d+)(?:,\s*PDF\s+pp\.[^\]]+)?\]")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True, help="Solar-merged Markdown before citation-only edits")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--log", type=Path, required=True)
    a = p.parse_args()
    if a.output.exists() or a.log.exists():
        raise SystemExit("Refusing to overwrite an existing output or log")
    original = a.input.read_text(encoding="utf-8-sig")
    lines = original.splitlines(keepends=True)
    s21 = [i for i, line in enumerate(lines) if "Organic Syntheses Procedure 1 [18]" in line and line.rstrip().endswith("[18][19][D9]")]
    comparison = [i for i, line in enumerate(lines) if "Organic Syntheses" in line and "91" in line and line.rstrip().endswith("[18][19][D9]")]
    if len(s21) != 1 or len(comparison) != 1 or s21 == comparison:
        raise SystemExit("Expected citation targets were not uniquely identified")
    lines[s21[0]] = lines[s21[0]].replace("[18][19][D9]", "[18][19][D9][D1]")
    lines[comparison[0]] = lines[comparison[0]].replace("[18][19][D9]", "[18][19][D9][6][D1]")
    revised = "".join(lines)
    if CITATION.sub("", revised) != CITATION.sub("", original):
        raise SystemExit("The patch changed non-citation text")
    delta = Counter(CITATION.findall(revised)) - Counter(CITATION.findall(original))
    if delta != Counter({"D1": 2, "6": 1}) or Counter(CITATION.findall(original)) - Counter(CITATION.findall(revised)):
        raise SystemExit("Unexpected citation-token changes")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.log.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(revised, encoding="utf-8", newline="\n")
    record = {
        "status": "passed",
        "input_path": str(a.input.resolve()), "input_sha256": sha(a.input),
        "output_path": str(a.output.resolve()), "output_sha256": sha(a.output),
        "added_citations": dict(delta), "removed_citations": {},
        "scientific_prose_or_values_changed": False,
        "scope": "section 2.1 adds D1; the route-01 model-vs-literature numeric comparison adds [6][D1]",
    }
    a.log.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": record["status"], "added_citations": record["added_citations"], "output": str(a.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
