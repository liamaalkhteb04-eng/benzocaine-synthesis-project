"""Repeat eligible EPI lookups with CAS numbers verified against structure + PubChem."""
import csv
import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "analyses" / "epi-suite"
INPUT = ROOT / "analyses" / "preparation" / "epi-suite-inputs.csv"
API = "https://episuite.dev"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def cas_norm(value):
    # EPI data uses zero-padded CAS strings; PubChem returns canonical form.
    parts = value.split("-")
    if len(parts) != 3:
        return value
    return f"{int(parts[0])}-{parts[1]}-{parts[2]}"


def main():
    out = BASE / "cas-confirmed-run-02"
    raw_dir = out / "raw"
    items_dir = raw_dir / "items"
    items_dir.mkdir(parents=True, exist_ok=False)
    rows = {r["species_id"]: r for r in csv.DictReader(INPUT.open(encoding="utf-8-sig", newline=""))}
    review = json.loads((BASE / "input-review.json").read_text(encoding="utf-8"))
    refs = {r["species_id"]: r for r in review["cas_references"]}
    body = []
    provenances = []
    for sid, row in rows.items():
        ref = refs.get(sid)
        if not ref:
            continue
        epi_cas = {cas_norm(e["cas"]): e["cas"] for e in ref["exact_structure_matches"] if e.get("cas")}
        pubchem_cas = {cas_norm(c): c for c in ref.get("pubchem_cas_candidates", [])}
        shared = sorted(set(epi_cas) & set(pubchem_cas))
        if not shared:
            continue
        normalized = shared[0]
        request_cas = pubchem_cas[normalized]
        body.append({"modules": ["physicalProperties"], "cas": request_cas,
                     "smiles": row["smiles"], "chemicalName": row["name"]})
        provenances.append({"species_id": sid, "name": row["name"], "smiles": row["smiles"],
                            "epi_search_exact_structure_matches": ref["exact_structure_matches"],
                            "pubchem_synonym_cas_candidates": ref["pubchem_cas_candidates"],
                            "cas_used": request_cas,
                            "normalization_rule": "Strip leading zeros in first CAS field for comparison; preserve canonical PubChem CAS in request.",
                            "structure_identity_basis": "EPI experimental catalog exact structure match and PubChem CAS synonym list.",
                            "search_raw": ref["epi_search_raw"], "pubchem_raw": ref["pubchem_synonyms_raw"]})
    if len(body) != 5:
        raise RuntimeError(f"Expected 5 independently CAS-confirmed compounds, found {len(body)}")
    raw_body = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(API + "/api/submit/batch", data=raw_body, method="POST", headers={
        "Accept": "application/json", "Content-Type": "application/json",
        "User-Agent": "BenzocaineCourseProject/1.0",
    })
    with urllib.request.urlopen(req, timeout=180) as response:
        raw_response = response.read()
        status = response.status
        content_type = response.headers.get("Content-Type", "")
    parsed = json.loads(raw_response)
    (out / "request.json").write_text(json.dumps({"api_url": API + "/api/submit/batch", "requests": body,
                                                    "cas_provenance": provenances}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (raw_dir / "request-body.json").write_bytes(raw_body)
    (out / "response.raw.json").write_bytes(raw_response)
    if status != 200 or not parsed.get("success") or len(parsed.get("results", [])) != len(body):
        raise RuntimeError("CAS-confirmed EPI batch returned errors or wrong count; inspect saved raw response")

    structured = []
    for provenance, result in zip(provenances, parsed["results"]):
        sid = provenance["species_id"]
        result_raw = json.dumps(result, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
        result_path = items_dir / f"{sid}.json"
        result_path.write_bytes(result_raw)
        structured.append({
            **provenance,
            "mp_estimated_value": result.get("meltingPoint", {}).get("estimatedValue"),
            "mp_experimental_values": result.get("meltingPoint", {}).get("experimentalValues", []),
            "mp_selected_value": result.get("meltingPoint", {}).get("selectedValue"),
            "bp_estimated_value": result.get("boilingPoint", {}).get("estimatedValue"),
            "bp_experimental_values": result.get("boilingPoint", {}).get("experimentalValues", []),
            "bp_selected_value": result.get("boilingPoint", {}).get("selectedValue"),
            "mpbpwin_output": result.get("meltingPoint", {}).get("output"),
            "raw_item": str(result_path.relative_to(ROOT)),
        })
    (out / "results.json").write_text(json.dumps(structured, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    openapi = json.loads((BASE / "raw" / "api-openapi.json").read_text(encoding="utf-8"))
    (out / "run-metadata.json").write_text(json.dumps({
        "captured_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "http_status": status, "content_type": content_type, "runtime_status_at_session": openapi.get("x-epi-status"),
        "runtime_health_at_session": openapi.get("x-epi-health"), "api_spec_sha256": sha((BASE / "raw" / "api-openapi.json").read_bytes()),
        "request_sha256": sha(raw_body), "response_sha256": sha(raw_response), "submitted": len(body),
        "experimental_mp_records": sum(bool(r["mp_experimental_values"]) for r in structured),
        "experimental_bp_records": sum(bool(r["bp_experimental_values"]) for r in structured),
        "estimated_values_returned": sum(bool(r["mp_estimated_value"] or r["bp_estimated_value"]) for r in structured),
        "note": "This CAS-confirmed request supplements, and does not overwrite, the original SMILES-only estimate response. Experimental values are reported only from the API experimentalValues arrays.",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"CAS-confirmed HTTP {status}: {len(structured)} items; measured MP {sum(bool(r['mp_experimental_values']) for r in structured)}; measured BP {sum(bool(r['bp_experimental_values']) for r in structured)}")
    for r in structured:
        print(r["species_id"], "CAS", r["cas_used"], "MP exp", len(r["mp_experimental_values"]), "BP exp", len(r["bp_experimental_values"]), "selected MP", r["mp_selected_value"], "selected BP", r["bp_selected_value"])


if __name__ == "__main__":
    main()
