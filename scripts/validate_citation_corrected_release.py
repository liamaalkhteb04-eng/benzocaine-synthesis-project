"""Validate a targeted Solar merge followed only by authorized citation additions."""
import argparse
from collections import Counter
import hashlib
import json
import re
from pathlib import Path

from audit_citations import audit

CITATION = re.compile(r"\[(D\d+|\d+)(?:,\s*PDF\s+pp\.[^\]]+)?\]")
MARKERS = ("<<<SECTION_2_1_START>>>", "<<<SECTION_2_1_END>>>",
           "<<<SECTION_8_REPRO_START>>>", "<<<SECTION_8_REPRO_END>>>")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_citations(text):
    return CITATION.sub("", text)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("base", "candidate", "final", "response", "status", "merge_manifest",
                 "citation_log", "source_map", "evidence_dir", "output"):
        p.add_argument("--" + name.replace("_", "-"), required=True,
                       type=Path if name != "evidence_dir" else Path)
    a = p.parse_args()
    base, candidate, final = (x.read_text(encoding="utf-8-sig") for x in (a.base, a.candidate, a.final))
    response_obj = json.loads(a.response.read_text(encoding="utf-8-sig"))
    status = json.loads(a.status.read_text(encoding="utf-8-sig"))
    merge = json.loads(a.merge_manifest.read_text(encoding="utf-8-sig"))
    change = json.loads(a.citation_log.read_text(encoding="utf-8-sig"))
    source_map = json.loads(a.source_map.read_text(encoding="utf-8-sig"))
    raw = response_obj["choices"][0]["message"]["content"]
    markers_ok = all(raw.count(m) == 1 for m in MARKERS)
    solar_blocks_ok = False
    if markers_ok:
        b21 = raw.split(MARKERS[0], 1)[1].split(MARKERS[1], 1)[0].strip()
        b8 = raw.split(MARKERS[2], 1)[1].split(MARKERS[3], 1)[0].strip()
        solar_blocks_ok = strip_citations(b21) in strip_citations(final) and strip_citations(b8) in strip_citations(final)
    added = Counter(CITATION.findall(final)) - Counter(CITATION.findall(candidate))
    removed = Counter(CITATION.findall(candidate)) - Counter(CITATION.findall(final))
    expected_added = Counter({"D1": 2, "6": 1})
    content_without_citations_unchanged = strip_citations(final) == strip_citations(candidate)
    changed_keys = {tuple(sorted(x.keys())) for x in change.get("changes", [])}
    citation_audit = audit(final, a.evidence_dir, source_map)

    # Confirm D10 points to the corrected record, not the preserved contradictory original.
    d10_path = a.evidence_dir / "rerun/benzocaine-live-repro-20261105-01/reproduction-validation.json"
    d10 = json.loads(d10_path.read_text(encoding="utf-8"))
    checks = {
        "Solar_success_single_run_no_retry": status.get("status") == "success" and status.get("retry_count") == 0 and status.get("run_id") == "benzocaine-hash-correction-final-20261115-01",
        "merge_manifest_binds_base_and_response": merge.get("status") == "solar_authored_targeted_replacements_applied" and merge.get("source_report_sha256") == sha(a.base) and merge.get("solar_response_sha256") == sha(a.response) and merge.get("merged_report_sha256") == sha(a.candidate) and merge.get("all_other_report_text_preserved") is True,
        "only_allowed_citation_tokens_added": added == expected_added and not removed,
        "scientific_text_and_numbers_unchanged": content_without_citations_unchanged,
        "Solar_two_target_blocks_present": markers_ok and solar_blocks_ok and merge.get("solar_call_count") == 1,
        "citation_change_log_binds_artifacts": change.get("scientific_text_changed") is False and change.get("edited_report_sha256") == sha(a.final) and change.get("solar_response_sha256") == sha(a.response),
        "citation_audit_passed": citation_audit.get("status") == "passed" and not citation_audit.get("errors"),
        "D10_is_corrected_validation": d10.get("status") == "passed" and d10.get("configuration_comparison", {}).get("byte_hash_same") is False and d10.get("configuration_comparison", {}).get("recorded_configuration_object_same_after_path_separator_normalization") is True and "unresolved" in d10.get("configuration_comparison", {}).get("cause_of_byte_hash_difference", ""),
        "D10_hash_matches_corrected_source": sha(d10_path) == "7087c15ddeabf85006934214fb148f3b3a6bbc173b69502b011a9b3517cef287",
    }
    result = {
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "added_citations": dict(added),
        "removed_citations": dict(removed),
        "citation_audit_status": citation_audit.get("status"),
        "citation_audit_errors": citation_audit.get("errors", []),
        "base_sha256": sha(a.base), "candidate_sha256": sha(a.candidate),
        "final_report_sha256": sha(a.final), "solar_response_sha256": sha(a.response),
        "merge_manifest_sha256": sha(a.merge_manifest),
        "citation_change_log_sha256": sha(a.citation_log),
        "citation_only_changes": content_without_citations_unchanged,
        "solar_targeted_blocks_verified": markers_ok and solar_blocks_ok,
        "no_model_call_or_inference": True,
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "failed_checks": [k for k, v in checks.items() if not v], "output": str(a.output)}, ensure_ascii=False))
    raise SystemExit(0 if result["status"] == "passed" else 2)


if __name__ == "__main__":
    main()
