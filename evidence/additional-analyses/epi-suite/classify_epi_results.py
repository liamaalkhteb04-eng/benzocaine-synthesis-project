"""Create a provenance-aware final review without changing raw EPI responses."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "analyses" / "epi-suite"
INPUT = ROOT / "analyses" / "preparation" / "epi-suite-inputs.csv"


def classify_data_record(record):
    author = (record.get("author") or "").strip()
    low = author.casefold()
    if "analogy" in low or "calculated" in low or "based upon" in low:
        return {
            "classification": "derived_or_analogue_database_entry_not_direct_measurement",
            "reason": f"EPI record author/method label is {author!r}.",
        }
    if author and record.get("year") not in (None, 0):
        return {
            "classification": "literature_cited_epi_evidence_not_independently_verified_as_measurement",
            "reason": f"The record carries a literature author/year ({author}, {record['year']}) but does not expose the underlying paper or measurement method here.",
        }
    return {
        "classification": "epi_database_evidence_provenance_insufficient_to_claim_direct_experiment",
        "reason": "The API labels this EpiUnified evidence, but author, year, pressure, and underlying experimental protocol are absent.",
    }


def main():
    estimates = json.loads((BASE / "response.json").read_text(encoding="utf-8"))
    casrun = json.loads((BASE / "cas-confirmed-run-02" / "results.json").read_text(encoding="utf-8"))
    review = json.loads((BASE / "input-review.json").read_text(encoding="utf-8"))
    sources = {x["species_id"]: x for x in casrun}
    rows = {x["species_id"]: x for x in csv.DictReader(INPUT.open(encoding="utf-8-sig", newline=""))}
    review_items = {x["species_id"]: dict(x) for x in review["items"]}
    for sid, source in sources.items():
        if sid in review_items:
            review_items[sid]["experimental_lookup_cas"] = source["cas_used"]
            review_items[sid]["experimental_lookup_status"] = "CAS-identified EpiUnified data query; see CAS-confirmed-run-02/results.json"
            review_items[sid]["cas_normalization_correction"] = "Leading zeroes in EPI CAS were normalized before intersecting with PubChem's canonical CAS synonyms."
    final_review = {
        "status": "reviewed",
        "input_source": str(INPUT.relative_to(ROOT)),
        "input_source_sha256": review["source_sha256"],
        "structure_validation": "RDKit 2026.03.2; formulas, canonical structures and net formal charges recorded.",
        "supported_submitted_count": 7,
        "skipped_count": 3,
        "skipped_reason_summary": "Palladium atom token (not a defined metal catalyst material), disconnected LiAlH4 ions, and inorganic BF3 token are outside MPBPWIN's organic-compound scope or do not define pure substances.",
        "cas_lookup": "Five exact EPI structure-search records intersected with PubChem CAS synonyms after removal of EPI's leading zero padding; the five CAS-confirmed responses are preserved separately.",
        "items": list(review_items.values()),
        "cas_confirmed_items": [{"species_id": x["species_id"], "cas": x["cas_used"], "structure_match": True,
                                 "EPI_search_raw": x["search_raw"], "PubChem_synonyms_raw": x["pubchem_raw"]}
                                for x in casrun],
    }
    (BASE / "input-review-final.json").write_text(json.dumps(final_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    classified = []
    for estimate in estimates:
        sid = estimate["species_id"]
        evidence_source = sources.get(sid, {})
        property_records = {}
        for prop, exp_key, est_key in (("melting_point", "mp_experimental_values", "estimated_mp"),
                                       ("boiling_point", "bp_experimental_values", "estimated_bp")):
            records = evidence_source.get(exp_key, [])
            property_records[prop] = {
                "model_estimate": estimate[est_key],
                "model_estimate_type": "MPBPWIN v1.44 estimated; EPI API valueType ESTIMATED",
                "epi_unified_records": [{**r, **classify_data_record(r)} for r in records],
                "selected_value": evidence_source.get("mp_selected_value" if prop == "melting_point" else "bp_selected_value"),
            }
        classified.append({"species_id": sid, "name": estimate["name"], "smiles": estimate["smiles"],
                           "formula": estimate["formula"], "formal_charge": estimate["formal_charge"],
                           "cas": estimate["cas"] or (evidence_source.get("cas_used") if evidence_source else None),
                           "properties": property_records,
                           "raw_smiles_only_response": estimate["raw_item"],
                           "raw_cas_response": evidence_source.get("raw_item"),
                           "epiunified_provenance": {"source_database": "EpiUnified", "measurement_conditions_returned": False,
                                                       "pressure_mmHg": None, "temperature_c": None}})
    (BASE / "classified-results.json").write_text(json.dumps(classified, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# EPI Suite MPBPWIN results and interpretation",
        "",
        "## Tool and execution status",
        "",
        "EPA's current EPI Suite page says the downloadable v4.11 has technical execution difficulties and directs users to the EPI Suite Web beta. The EPI Web endpoint returned HTTP 200 for both the SMILES-only estimate batch and the five CAS-confirmed data queries. The API health document nevertheless reported `degraded` and `requestHandling.healthy=false`; results are saved with this service limitation. No local EPI Suite installation was made.",
        "",
        "EPA identifies MPBPWIN as estimating melting point, boiling point, and vapor pressure for organic chemicals using a combination of techniques. EPA describes EPI Suite as screening-level; these estimates should not replace suitable measured values.",
        "",
        "## Model estimates and EPI database evidence",
        "",
        "The `estimatedValue` is the MPBPWIN v1.44 model estimate. It is shown separately from `experimentalValues` / EpiUnified evidence. EPI's `selectedValue` can select a database evidence row instead of the model estimate; it must not be called a prediction without checking its source metadata. All temperatures below are in deg C.",
        "",
        "| Substance (formula) | MPBPWIN MP estimate | EPI Unified MP record | MP record classification | MPBPWIN BP estimate | EPI Unified BP record | BP record classification |",
        "|---|---:|---:|---|---:|---:|---|",
    ]
    for row in classified:
        sid = row["species_id"]
        mp = row["properties"]["melting_point"]
        bp = row["properties"]["boiling_point"]
        mp_ev = mp["epi_unified_records"]
        bp_ev = bp["epi_unified_records"]
        mp_value = mp_ev[0].get("value") if mp_ev else None
        bp_value = bp_ev[0].get("value") if bp_ev else None
        mp_class = mp_ev[0]["classification"] if mp_ev else "No EPI Unified record returned"
        bp_class = bp_ev[0]["classification"] if bp_ev else "No EPI Unified record returned"
        lines.append(f"| {row['name']} ({row['formula']}) | {mp['model_estimate']['value']:.2f} | {mp_value if mp_value is not None else '—'} | {mp_class} | {bp['model_estimate']['value']:.2f} | {bp_value if bp_value is not None else '—'} | {bp_class} |")

    lines += [
        "",
        "All seven model estimates are EPI responses marked `ESTIMATED`; they are not measured properties. The EPI search database had exact-structure records for five substances (4-aminobenzoic acid, ethanol, acetic acid, tetrahydrofuran, and diethyl ether). Benzocaine and ethyl 4-nitrobenzoate had no EPI search match, so their reported values are model-only.",
        "",
        "The EPI Unified field is not uniformly a laboratory measurement: four melting-point records explicitly say `slope analogy` or `calculated based upon VP / Water Sol data`; these are derived/analogue entries, not direct observations. The acetic-acid MP record carries a 1992 author string but not the underlying paper or method in the API; its author metadata needs caution. The other boiling-point records are tagged as EpiUnified evidence but return no author/year/pressure, so their measurement provenance cannot be independently checked from this response. The API's `experimentalValues` field name alone is not enough to call every entry an experiment.",
        "",
        "For a separate cross-check, the Australian Government National Pollutant Inventory lists acetic acid MP 16.7 deg C and BP 118 deg C, close to the EpiUnified database entries 16.635 deg C and 117.9 deg C. This source does not validate the MPBPWIN predictions; the MPBPWIN estimates for acetic acid were -21.26 deg C and 122.30 deg C.",
        "",
        "## Structure and support review",
        "",
        "The seven submitted structures are neutral organic compounds with net formal charge zero and are represented as the same structures used in the preparation CSV. Three inputs were not submitted: `[Pd]` is an elemental atom token rather than a defined catalyst material; `[Al+3].[H-]...[Li+]` is a disconnected ionic LiAlH4 representation rather than a defined pure neutral organic compound; and `FB(F)F` is inorganic BF3 rather than an organic chemical within MPBPWIN's stated scope. No values were fabricated for these entries.",
        "",
        "## Reaction-condition limits",
        "",
        "The selected Parrot condition predictions do not specify reaction temperature, pressure, or full mixture composition/amounts. The Web API returned pure-compound BP/MP estimates and database records, not mixture phase equilibria. Do not infer whether route materials precipitate, melt, boil, or react from these values alone. To assess operational phase, obtain the actual temperature and pressure, solvent/reagent equivalents and concentrations, water content, chemical forms/salts, atmosphere, and mixture vapor-liquid/solid-liquid behavior or solubility data. A pure-compound MP or BP is not evidence of reaction feasibility or yield.",
        "",
        "## Reproducibility and files",
        "",
        "- Input structures: `analyses/preparation/epi-suite-inputs.csv`.",
        "- Reproduction script: `analyses/epi-suite/run_epi_web_suite.py` (SMILES-only estimates and CAS/reference resolution) and `analyses/epi-suite/run_epi_cas_confirmed.py` (CAS-identified EpiUnified lookup).",
        "- API specification and degraded health snapshot: `raw/api-openapi.json`, `run-metadata.json`.",
        "- Exact request and raw result payloads: `request.json`, `response.raw.json`, `raw/items/`, and `cas-confirmed-run-02/`.",
        "- Structure/CAS audit: `input-review-final.json`; provenance-aware classification: `classified-results.json`.",
        "- Query time and request/response hashes are in each run metadata file.",
        "",
        "Sources: [EPA EPI Suite page and current beta notice](https://www.epa.gov/tsca-screening-tools/epi-suitetm-estimation-program-interface); [EPA EPI Suite v4.11 download notice](https://www.epa.gov/tsca-screening-tools/download-epi-suitetm-estimation-program-interface-v411); [EPI Suite Web beta](https://episuite.dev/EpiWebSuite/#/); [Australian Government acetic acid properties](https://www.dcceew.gov.au/environment/protection/npi/substances/acetic-acid-ethanoic-acid).",
    ]
    (BASE / "analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote final EPI structure/evidence classification and analysis to", BASE)


if __name__ == "__main__":
    main()
