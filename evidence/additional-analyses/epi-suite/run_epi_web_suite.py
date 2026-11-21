"""Query EPA-recommended EPI Suite web beta for prepared neutral organic inputs.

This script sends no proprietary data, installs nothing, and writes all evidence
under analyses/epi-suite. It separates API estimates from available experimental
database values and skips non-organic/ionic species rather than inventing data.
"""
import csv
import datetime as dt
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "analyses" / "epi-suite"
INPUT = ROOT / "analyses" / "preparation" / "epi-suite-inputs.csv"
API = "https://episuite.dev"
PUBCHEM = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name"

ELIGIBLE = {
    "ethyl-4-nitrobenzoate", "benzocaine", "p-aminobenzoic-acid", "ethanol",
    "acetic-acid", "tetrahydrofuran-condition-slot", "diethyl-ether-condition-slot",
}
PUBCHEM_NAMES = {
    "ethyl-4-nitrobenzoate": "ethyl 4-nitrobenzoate",
    "benzocaine": "benzocaine",
    "p-aminobenzoic-acid": "4-aminobenzoic acid",
    "ethanol": "ethanol",
    "acetic-acid": "acetic acid",
    "tetrahydrofuran-condition-slot": "tetrahydrofuran",
    "diethyl-ether-condition-slot": "diethyl ether",
}


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def get_json(url):
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "BenzocaineCourseProject/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        raw = response.read()
        return response.status, response.headers.get("Content-Type", ""), raw, json.loads(raw)


def post_json(url, payload):
    raw_request = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(url, data=raw_request, method="POST", headers={
        "Accept": "application/json", "Content-Type": "application/json",
        "User-Agent": "BenzocaineCourseProject/1.0",
    })
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read()
            return response.status, response.headers.get("Content-Type", ""), raw, json.loads(raw), raw_request
    except urllib.error.HTTPError as error:
        raw = error.read()
        raise RuntimeError(f"EPI estimate request failed with HTTP {error.code}: {raw[:1000]!r}") from error


def cas_numbers(synonyms):
    pattern = re.compile(r"^\d{2,7}-\d{2}-\d$")
    return sorted({value for value in synonyms if pattern.fullmatch(value)})


def main():
    (BASE / "raw" / "search").mkdir(parents=True, exist_ok=True)
    (BASE / "raw" / "pubchem").mkdir(parents=True, exist_ok=True)
    (BASE / "raw" / "items").mkdir(parents=True, exist_ok=True)
    for filename in ("request.json", "response.raw.json", "run-metadata.json", "input-review.json", "results.json", "analysis.md"):
        if (BASE / filename).exists():
            raise FileExistsError(f"Refusing to overwrite existing EPI result: {BASE / filename}")

    rows = list(csv.DictReader(INPUT.open(encoding="utf-8-sig", newline="")))
    openapi_status, openapi_type, openapi_raw, openapi = get_json(API + "/api")
    (BASE / "raw" / "api-openapi.json").write_bytes(openapi_raw)
    (BASE / "raw" / "api-openapi.http.json").write_text(json.dumps({
        "http_status": openapi_status, "content_type": openapi_type,
        "sha256": sha_bytes(openapi_raw), "url": API + "/api",
        "captured_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }, indent=2) + "\n", encoding="utf-8")

    review_rows = []
    eligible_rows = []
    reference_rows = []
    for row in rows:
        mol = Chem.MolFromSmiles(row["smiles"])
        if mol is None:
            review_rows.append({**row, "status": "not_supported", "reason": "RDKit could not parse input SMILES"})
            continue
        charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
        formula = rdMolDescriptors.CalcMolFormula(mol)
        canonical = Chem.MolToSmiles(mol, canonical=True)
        reviewed = {**row, "canonical_smiles": canonical, "formula": formula,
                    "net_formal_charge": charge, "rdkit_parse_status": "success"}
        if row["species_id"] not in ELIGIBLE:
            reason = {
                "palladium-condition-slot": "Elemental metal atom token; MPBPWIN is described by EPA as estimating organic chemicals; the token is not a Pd/C surface or a defined material.",
                "lithium-aluminium-hydride-condition-slots": "Disconnected multicomponent ionic reagent representation; a single-compound BP/MP estimate would not represent the commercial reagent formulation.",
                "boron-trifluoride-condition-slot": "Inorganic BF3 token; outside the intended organic-compound scope of MPBPWIN; also not the actual concentration/etherate formulation.",
            }.get(row["species_id"], "Not selected for this EPI run.")
            review_rows.append({**reviewed, "status": "not_submitted", "reason": reason})
            continue
        if charge != 0:
            review_rows.append({**reviewed, "status": "not_submitted", "reason": "Non-neutral structure: this planned EPI input set only covers neutral compounds."})
            continue

        name = PUBCHEM_NAMES[row["species_id"]]
        # Search the EPI Suite experimental-data catalog; preserve the exact reply.
        search_url = API + "/api/search?" + urllib.parse.urlencode({"query": name, "limit": 20})
        search_status, search_type, search_raw, search = get_json(search_url)
        search_path = BASE / "raw" / "search" / f"{row['species_id']}.json"
        search_path.write_bytes(search_raw)

        # Validate the registry number independently in PubChem's public synonym
        # response, then intersect it with EPI search entries for the identical structure.
        pub_url = PUBCHEM + "/" + urllib.parse.quote(name, safe="") + "/synonyms/JSON"
        cas_status, cas_type, cas_raw, cas_data = get_json(pub_url)
        cas_path = BASE / "raw" / "pubchem" / f"{row['species_id']}-synonyms.json"
        cas_path.write_bytes(cas_raw)
        information = cas_data.get("InformationList", {}).get("Information", [])
        pubchem_cas = cas_numbers(information[0].get("Synonym", [])) if information else []

        exact_entries = []
        for entry in search if isinstance(search, list) else []:
            entry_mol = Chem.MolFromSmiles(entry.get("smiles", ""))
            if entry_mol and Chem.MolToSmiles(entry_mol, canonical=True) == canonical:
                exact_entries.append(entry)
        matching_cas = [entry.get("cas") for entry in exact_entries if entry.get("cas") in pubchem_cas]
        chosen_cas = matching_cas[0] if matching_cas else None
        reference_rows.append({
            "species_id": row["species_id"], "search_query": name,
            "epi_search_url": search_url, "epi_search_http_status": search_status,
            "epi_search_raw": str(search_path.relative_to(ROOT)), "exact_structure_matches": exact_entries,
            "pubchem_synonym_url": pub_url, "pubchem_synonyms_raw": str(cas_path.relative_to(ROOT)),
            "pubchem_http_status": cas_status, "pubchem_cas_candidates": pubchem_cas,
            "cas_used_for_experimental_lookup": chosen_cas,
            "cas_resolution": "exact canonical-structure match plus PubChem synonym intersection" if chosen_cas else "no independently verified EPI experimental-data CAS; model-only SMILES request",
        })
        item = {"modules": ["physicalProperties"], "smiles": row["smiles"], "chemicalName": row["name"]}
        if chosen_cas:
            item["cas"] = chosen_cas
        eligible_rows.append((row, reviewed, item, chosen_cas))
        review_rows.append({**reviewed, "status": "submitted", "experimental_lookup_cas": chosen_cas,
                            "experimental_lookup_status": "CAS-identified" if chosen_cas else "SMILES-only; no measured-data lookup"})

    requests = [item for _, _, item, _ in eligible_rows]
    request_doc = {
        "source_csv": str(INPUT.relative_to(ROOT)),
        "source_csv_sha256": sha_bytes(INPUT.read_bytes()),
        "api_url": API + "/api/submit/batch",
        "http_method": "POST",
        "modules": ["physicalProperties"],
        "requests": requests,
        "note": "Neutral organic compounds only. CAS included only when EPI search's exact canonical structure matched and PubChem synonyms independently validated the CAS.",
    }
    (BASE / "request.json").write_text(json.dumps(request_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    status, content_type, raw_response, response, raw_request = post_json(API + "/api/submit/batch", requests)
    (BASE / "raw" / "request-body.json").write_bytes(raw_request)
    (BASE / "response.raw.json").write_bytes(raw_response)
    if status != 200 or not response.get("success"):
        raise RuntimeError(f"EPI batch response did not report success; see saved raw response ({status})")
    if len(response.get("results", [])) != len(eligible_rows):
        raise RuntimeError("EPI batch result count does not match submitted items")

    curated = []
    for (source, reviewed, request, cas), result in zip(eligible_rows, response["results"]):
        result_path = BASE / "raw" / "items" / f"{source['species_id']}.json"
        result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        entry = {"species_id": source["species_id"], "name": source["name"], "smiles": source["smiles"],
                 "formula": reviewed["formula"], "formal_charge": reviewed["net_formal_charge"],
                 "cas": cas, "source_kind": "model_estimate", "raw_item": str(result_path.relative_to(ROOT)),
                 "estimated_mp": result.get("meltingPoint", {}).get("estimatedValue"),
                 "experimental_mp_values": result.get("meltingPoint", {}).get("experimentalValues", []),
                 "selected_mp": result.get("meltingPoint", {}).get("selectedValue"),
                 "estimated_bp": result.get("boilingPoint", {}).get("estimatedValue"),
                 "experimental_bp_values": result.get("boilingPoint", {}).get("experimentalValues", []),
                 "selected_bp": result.get("boilingPoint", {}).get("selectedValue"),
                 "mpbpwin_output": result.get("meltingPoint", {}).get("output"),
                 "module_errors": result.get("errors", [])}
        if entry["experimental_mp_values"] or entry["experimental_bp_values"]:
            entry["source_kind"] = "model_estimate_plus_experimental_database_values"
        curated.append(entry)

    (BASE / "response.json").write_text(json.dumps(curated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (BASE / "input-review.json").write_text(json.dumps({
        "source": str(INPUT.relative_to(ROOT)), "source_sha256": sha_bytes(INPUT.read_bytes()),
        "rdkit": Chem.rdBase.rdkitVersion, "items": review_rows,
        "cas_references": reference_rows,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (BASE / "run-metadata.json").write_text(json.dumps({
        "captured_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "official_epa_parent_page": "https://www.epa.gov/tsca-screening-tools/epi-suitetm-estimation-program-interface",
        "officially_recommended_web_beta": "https://episuite.dev/EpiWebSuite/#/",
        "engine_api": API + "/api", "service_info": openapi.get("info"),
        "runtime_status": openapi.get("x-epi-status"), "runtime_health": openapi.get("x-epi-health"),
        "api_spec_sha256": sha_bytes(openapi_raw), "request_http_status": status,
        "response_content_type": content_type, "request_body_sha256": sha_bytes(raw_request),
        "response_sha256": sha_bytes(raw_response), "submitted_count": len(requests),
        "experimental_values_available": sum(bool(x["experimental_mp_values"] or x["experimental_bp_values"]) for x in curated),
        "estimated_values_returned": sum(bool(x["estimated_mp"] or x["estimated_bp"]) for x in curated),
        "interpretation": "EPA describes MPBPWIN as screening-level estimation. This web API returned estimated values. Experimental result arrays are preserved separately; no results are labeled as measured unless present there.",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"EPI web batch: HTTP {status}; submitted {len(requests)}; estimates returned {sum(bool(x['estimated_mp'] or x['estimated_bp']) for x in curated)}; entries with experimental results {sum(bool(x['experimental_mp_values'] or x['experimental_bp_values']) for x in curated)}")
    for item in curated:
        print(item["species_id"], "MP", item["estimated_mp"], "BP", item["estimated_bp"],
              "experimental", len(item["experimental_mp_values"]), len(item["experimental_bp_values"]))
    print("EPI runtime status:", openapi.get("x-epi-status"), "health:", openapi.get("x-epi-health", {}).get("requestHandling"))


if __name__ == "__main__":
    main()
