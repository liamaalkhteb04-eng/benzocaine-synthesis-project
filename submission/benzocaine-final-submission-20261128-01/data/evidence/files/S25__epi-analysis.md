# EPI Suite MPBPWIN results and interpretation

## Tool and execution status

EPA's current EPI Suite page says the downloadable v4.11 has technical execution difficulties and directs users to the EPI Suite Web beta. The EPI Web endpoint returned HTTP 200 for both the SMILES-only estimate batch and the five CAS-confirmed data queries. The API health document nevertheless reported `degraded` and `requestHandling.healthy=false`; results are saved with this service limitation. No local EPI Suite installation was made.

EPA identifies MPBPWIN as estimating melting point, boiling point, and vapor pressure for organic chemicals using a combination of techniques. EPA describes EPI Suite as screening-level; these estimates should not replace suitable measured values.

## Model estimates and EPI database evidence

The `estimatedValue` is the MPBPWIN v1.44 model estimate. It is shown separately from `experimentalValues` / EpiUnified evidence. EPI's `selectedValue` can select a database evidence row instead of the model estimate; it must not be called a prediction without checking its source metadata. All temperatures below are in deg C.

| Substance (formula) | MPBPWIN MP estimate | EPI Unified MP record | MP record classification | MPBPWIN BP estimate | EPI Unified BP record | BP record classification |
|---|---:|---:|---|---:|---:|---|
| Ethyl 4-nitrobenzoate (C9H9NO4) | 80.66 | — | No EPI Unified record returned | 297.25 | — | No EPI Unified record returned |
| Benzocaine (C9H11NO2) | 66.17 | — | No EPI Unified record returned | 279.90 | — | No EPI Unified record returned |
| 4-Aminobenzoic acid (C7H7NO2) | 94.08 | 188.5 | derived_or_analogue_database_entry_not_direct_measurement | 307.70 | — | No EPI Unified record returned |
| Ethanol (C2H6O) | -87.84 | -114.1 | derived_or_analogue_database_entry_not_direct_measurement | 65.11 | 78.2 | epi_database_evidence_provenance_insufficient_to_claim_direct_experiment |
| Acetic acid (C2H4O2) | -21.26 | 16.635 | literature_cited_epi_evidence_not_independently_verified_as_measurement | 122.30 | 117.9 | epi_database_evidence_provenance_insufficient_to_claim_direct_experiment |
| Tetrahydrofuran (C4H8O) | -84.89 | -108.44 | derived_or_analogue_database_entry_not_direct_measurement | 69.36 | 65.0 | epi_database_evidence_provenance_insufficient_to_claim_direct_experiment |
| Diethyl ether (C4H10O) | -101.15 | -116.3 | derived_or_analogue_database_entry_not_direct_measurement | 47.02 | 34.6 | epi_database_evidence_provenance_insufficient_to_claim_direct_experiment |

All seven model estimates are EPI responses marked `ESTIMATED`; they are not measured properties. The EPI search database had exact-structure records for five substances (4-aminobenzoic acid, ethanol, acetic acid, tetrahydrofuran, and diethyl ether). Benzocaine and ethyl 4-nitrobenzoate had no EPI search match, so their reported values are model-only.

The EPI Unified field is not uniformly a laboratory measurement: four melting-point records explicitly say `slope analogy` or `calculated based upon VP / Water Sol data`; these are derived/analogue entries, not direct observations. The acetic-acid MP record carries a 1992 author string but not the underlying paper or method in the API; its author metadata needs caution. The other boiling-point records are tagged as EpiUnified evidence but return no author/year/pressure, so their measurement provenance cannot be independently checked from this response. The API's `experimentalValues` field name alone is not enough to call every entry an experiment.

For a separate cross-check, the Australian Government National Pollutant Inventory lists acetic acid MP 16.7 deg C and BP 118 deg C, close to the EpiUnified database entries 16.635 deg C and 117.9 deg C. This source does not validate the MPBPWIN predictions; the MPBPWIN estimates for acetic acid were -21.26 deg C and 122.30 deg C.

## Structure and support review

The seven submitted structures are neutral organic compounds with net formal charge zero and are represented as the same structures used in the preparation CSV. Three inputs were not submitted: `[Pd]` is an elemental atom token rather than a defined catalyst material; `[Al+3].[H-]...[Li+]` is a disconnected ionic LiAlH4 representation rather than a defined pure neutral organic compound; and `FB(F)F` is inorganic BF3 rather than an organic chemical within MPBPWIN's stated scope. No values were fabricated for these entries.

## Reaction-condition limits

The selected Parrot condition predictions do not specify reaction temperature, pressure, or full mixture composition/amounts. The Web API returned pure-compound BP/MP estimates and database records, not mixture phase equilibria. Do not infer whether route materials precipitate, melt, boil, or react from these values alone. To assess operational phase, obtain the actual temperature and pressure, solvent/reagent equivalents and concentrations, water content, chemical forms/salts, atmosphere, and mixture vapor-liquid/solid-liquid behavior or solubility data. A pure-compound MP or BP is not evidence of reaction feasibility or yield.

## Reproducibility and files

- Input structures: `analyses/preparation/epi-suite-inputs.csv`.
- Reproduction script: `analyses/epi-suite/run_epi_web_suite.py` (SMILES-only estimates and CAS/reference resolution) and `analyses/epi-suite/run_epi_cas_confirmed.py` (CAS-identified EpiUnified lookup).
- API specification and degraded health snapshot: `raw/api-openapi.json`, `run-metadata.json`.
- Exact request and raw result payloads: `request.json`, `response.raw.json`, `raw/items/`, and `cas-confirmed-run-02/`.
- Structure/CAS audit: `input-review-final.json`; provenance-aware classification: `classified-results.json`.
- Query time and request/response hashes are in each run metadata file.

Sources: [EPA EPI Suite page and current beta notice](https://www.epa.gov/tsca-screening-tools/epi-suitetm-estimation-program-interface); [EPA EPI Suite v4.11 download notice](https://www.epa.gov/tsca-screening-tools/download-epi-suitetm-estimation-program-interface-v411); [EPI Suite Web beta](https://episuite.dev/EpiWebSuite/#/); [Australian Government acetic acid properties](https://www.dcceew.gov.au/environment/protection/npi/substances/acetic-acid-ethanoic-acid).
