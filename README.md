# AI synthesis report pipeline - reproducible source package

This package includes target-neutral route, condition and yield adapters; report-writing skill; benzocaine example inputs and evidence; and the current verified report. Saved benzocaine predictions are examples only and are never reused for a different target.

## Two skills, two roles

- [`skill/SKILL.md`](skill/SKILL.md) is the **whole-pipeline skill**: enter a target, verify its structure, preflight and run route/condition/yield adapters, collect actual result and analysis evidence, then route report authoring to the report-writing skill.
- [`skill/report-writing/SKILL.md`](skill/report-writing/SKILL.md) is the **Solar report-authoring skill**. The report request builders read this file into the Solar system message. It defines required evidence, scientific/citation rules, missing-data behavior, Markdown output, and DOCX/PDF checks.

The default is a full report. Targeted section/sentence edits require an explicit request and are not included in ordinary full-report requests. Historical prompt files and run IDs are preserved in [`provenance/skills/PATH-MAP.md`](provenance/skills/PATH-MAP.md); they are not treated as current instructions. Old report files were not authored with the new two-skill layout.

### Copying and using the package

Copy or clone the **entire repository**, not only either skill file. The skills explain and route work; executable adapters, Python dependencies, configs, target JSON, raw/normalized results, figure files, validation records, model runtimes/checkpoints/stock buckets, a local Solar API key, and a DOCX/PDF converter are separate requirements. Large/private weights and API secrets are intentionally not included.

**Full pipeline:** create `inputs/<target_id>.json` from `inputs/input-template.json`; run structure identity and model preflight; run `scripts/run_pipeline.py` with a fresh run ID; inspect raw results and additional analyses; then prepare a Solar report request from the prepared run. The full instructions and actual model/weight preparation are in [`skill/SKILL.md`](skill/SKILL.md) and the model setup sections below.

**Report only from prepared results:** point `scripts/generate_report.py` at an existing `results/<run_id>/` directory. This does not rerun chemistry models. The request builder places `skill/report-writing/SKILL.md` in the Solar system message and passes that run's `report-evidence.json` and manifest. `--prepare-only` constructs the request locally and makes no API call. It verifies source hashes first and refuses changed or mismatched evidence rather than silently repairing it. For the portable Benzocaine example, use `results/benzocaine-live-20261031-04-public-curated/`, not the older path-anonymized archival copies. Solar authoring is separate and may be billable; this package's two authorization flags are disabled by default. For a new target, after an authorized Solar response use the generalized renderer procedure below before DOCX/PDF conversion. The saved Benzocaine release predates that rendering contract and follows the separate archived-response rebuild procedure, with no new Solar call.

The historical `benzocaine-live-20261031-04` run and its original execution manifest are preserved. During creation of the public copy, absolute local paths and checkpoint locations were anonymized in four JSON artifacts; their old source hashes therefore no longer matched the public bytes. [The hash audit](validation/public-evidence-hash-repair-20261115.json) records each expected and actual hash and where the expected value was recorded. The separate `benzocaine-live-20261031-04-public-curated` bundle has new derivative hashes, a provenance map back to the historical execution, and a freshly joined report-evidence file. Its derivation check found path/command/checkpoint/image-path changes only and zero changed scientific values. The new `manifest.json` is explicitly a derivative-artifact manifest, not an execution record. Do not rewrite the old run's manifest or model-input hashes to make the archival copy pass.

The report request builders and configured skill paths are `configs/report-plan.json`, `scripts/generate_report.py`, and `scripts/generate_solar_report_from_bundle.py`. Model outputs are not verified merely because a request or document was generated. Exact Solar skill inclusion, actual evidence blocks, and isolation from historical task instructions are covered by [`validation/report-writing-skill-request-offline-check-final-03.json`](validation/report-writing-skill-request-offline-check-final-03.json), [`validation/public-curated-request-offline-20261115.json`](validation/public-curated-request-offline-20261115.json), and [`validation/skill-role-separation-check.json`](validation/skill-role-separation-check.json); they do not evaluate Solar response quality.


## Independent target validation: acetaminophen (2026-11-15)

The submission entry point was exercised with a separate acetaminophen input on the existing PC, using the existing model runtimes and weights. This is a different-molecule run on that computer; it is not a clean-PC installation/reproduction test. The target identity was checked against PubChem and RDKit (SMILES `CC(=O)Nc1ccc(O)cc1`, formula `C8H9NO2`, CID 1983).

AiZynthFinder completed and returned 12 route predictions (16 steps). Parrot completed 14 unique reaction rows mapped to 16 route steps. Yield-BERT completed 16 step predictions; its model input did not include reaction conditions. The structural, route/step join, and artifact-integrity checks passed. These outputs do not establish chemical feasibility or experimental accuracy. Per-target MOPAC, EPI Suite, Discovery Studio Visualizer, and harness comparison remain `not_implemented`.

The redacted public verification summary, run ID, model statuses, output checksums, and test scope are in [`validation/acetaminophen-generalization-20261115.json`](validation/acetaminophen-generalization-20261115.json). Raw prediction payloads and machine-specific logs are not bundled; they remain in the separate local validation workspace. The source run used existing runtime/model assets whose local paths point into the separate Aspirin test installation; no Aspirin or Benzocaine prediction results were used for this target. The Parrot general slot check passed, and the Benzocaine route-05/step-02 regression passed only when explicitly enabled. The generalization corrections are in `scripts/prepare_target.py` and `scripts/audit_parrot_slots.py`.

At the earlier pipeline-validation checkpoint, the Solar request was recorded as `prepared_not_executed`. A later, separately authorized Solar response (`acetaminophen-report-live-20261117-02`) was reused for document-generation validation; the renderer itself made no Solar call. DOCX/PDF regeneration from that saved response is documented below. The report-writing configuration remains disabled by default. The prior Benzocaine report and raw results are unchanged.

## Current verified Benzocaine release (2026-11-15)

The current report is [PDF](reports/benzocaine-page-layout-and-instruction-cleanup-20261115/벤조카인_AI유기합성_최종보고서.pdf) and [DOCX](reports/benzocaine-page-layout-and-instruction-cleanup-20261115/벤조카인_AI유기합성_최종보고서.docx). Each is 19 pages. Microsoft Word 16.0 generated the PDF from the DOCX. The final copy preserves the prior scientific content, figures, analyses and conclusions; only two Solar-authored sentence replacements, the D10 evidence-path correction, table layout, and display rounding of four yield cells were applied. In this curated public copy, references to excluded course/literature PDFs point to source-acquisition notes; no scientific content was changed. Raw model outputs and unrounded values remain in the evidence bundle.

Solar Pro 4 was called once for the two specified sentence replacements only (run `benzocaine-documentation-cleanup-20261115-01`). The raw request, response, status, targeted skill, evidence files and validation are saved under the report folder. Actual call cost including VAT was `$0.00040722`; cumulative recorded Solar cost is `$0.96937284` under the `$1.00` limit. No retry or additional charge occurred. The report text was not rewritten in full, and no chemical model inference was run for this release.

In the report's D10 evidence list, the corrected validation is explicitly linked to `reports/benzocaine-page-layout-and-instruction-cleanup-20261115/evidence-run/rerun/benzocaine-live-repro-20261105-01/reproduction-validation-corrected.json` (SHA-256 `7087c15ddeabf85006934214fb148f3b3a6bbc173b69502b011a9b3517cef287`). The preserved conflicting source is separately identified as `.../reproduction-validation-original-conflicting.json` (SHA-256 `63ab33c238fda07120f87ff9e4024195b12bb68cc689565539f83112dd7db7a8`). Neither record overwrites the other.

The route-overview, literature-comparison and integrated condition/yield tables use 9 pt table text. The integrated-table title is kept with its table. Displayed predicted yields use two decimal places; the raw values remain in report prose and evidence. The actual Parrot slot names and SMILES tokens are retained.

### Rebuild DOCX/PDF from the saved response without another model call

Use the package's declared report dependencies and Microsoft Word desktop. From the repository root, create a new empty work folder and copy the saved Markdown, response/status, validation record and evidence bundle into it. Keep the release folder unchanged. No API key is needed for this document rebuild.

```powershell
$source = 'reports/benzocaine-page-layout-and-instruction-cleanup-20261115'
$work = 'reports/benzocaine-document-rebuild-local'
New-Item -ItemType Directory $work
Copy-Item "$source/report.md" $work
Copy-Item "$source/solar-call" $work -Recurse
Copy-Item "$source/evidence-run" $work -Recurse
Copy-Item "$source/merge-validation.json" $work
Copy-Item "$source/citation-source-map.json" $work
.venv-report/Scripts/python.exe scripts/audit_citations.py `
  --report "$work/report.md" `
  --evidence-dir "$work/evidence-run" `
  --source-map "$work/citation-source-map.json" `
  --output "$work/citation-audit-rebuilt.json"
.venv-report/Scripts/python.exe scripts/export_report_docx.py `
  --markdown "$work/report.md" `
  --run-dir "$work/evidence-run" `
  --solar-status "$work/solar-call/solar-status.json" `
  --verified-edits-validation "$work/merge-validation.json" `
  --compact-layout
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/convert_docx_to_pdf.ps1 `
  -DocxPath "$work/report.docx" `
  -PdfPath "$work/report.pdf" `
  -MetadataPath "$work/word-export.json"
.venv-report/Scripts/python.exe scripts/validate_citation_corrected_documents.py `
  --report-dir "$work" `
  --run-dir "$work/evidence-run" `
  --citation-validation "$work/citation-audit-rebuilt.json"
Move-Item "$work/report.pdf" "$work/벤조카인_AI유기합성_최종보고서.pdf"
Move-Item "$work/report.docx" "$work/벤조카인_AI유기합성_최종보고서.docx"
```

The commands validate the generic build filenames first, then rename the validated binaries for submission. A SHA-256 record confirms the rename did not change either file. This saved-response conversion is different from running `scripts/run_pipeline.py` for a new target and requesting a new Solar-authored report. New-target prediction needs the isolated model runtimes, matching weights and full stock buckets documented below; Solar authoring needs a locally configured Upstage API key. Neither the key nor model weights are packaged. The benzocaine results must not be substituted for another input.

## 1. Prepare a new target

Use 64-bit Windows, Python 3.13 for the driver, and PowerShell. From the repository root, create a new JSON file from the template and replace every placeholder. Set the intended chemical form, an isomeric SMILES, expected formula, name, stable target ID, and PubChem CID (or adjust the identity-check code for a different trusted identifier). Do not use `inputs/benzocaine.json` for another substance.

For an offline structure check, use `scripts/validate_target_offline.py`. It checks the input fields, parses the SMILES with RDKit, verifies the formula and can compare the target to an existing prepared run. It does not contact PubChem. The next section documents `prepare_target.py`, which additionally makes a PubChem identity request; that command is not part of offline verification.

```powershell
$targetId = 'my-compound'
Copy-Item inputs/input-template.json "inputs/$targetId.json"
# Edit inputs/my-compound.json, then validate structure and public identity:
py -3.13 -B -X utf8 scripts/prepare_target.py `
  --input "inputs/$targetId.json" `
  --output "validation/$targetId-identity.json"
```

The PubChem raw response is stored beside the identity record using its output stem (for example, `my-compound-identity-pubchem.raw.json`), so validating multiple targets does not overwrite a shared `pubchem.raw.json`.

`prepare_target.py` validates SMILES/formula with RDKit and makes a PubChem PUG REST identity request. This is an identity check, not synthesis inference.

### Reproduce target validation and request preparation offline

This demonstration validates the example input against the same target in the path-anonymized public derivative, then builds the exact report request locally. It does not rerun AiZynthFinder, Parrot, Yield-BERT, or Solar. Use a new attempt ID if repeating it, because request attempts are immutable.

```powershell
$runId = 'benzocaine-live-20261031-04-public-curated'
$demoId = Get-Date -Format 'yyyyMMdd-HHmmss'
$attemptId = "readme-offline-$demoId"
py -3.13 -B -X utf8 scripts/validate_target_offline.py `
  --input inputs/benzocaine.json `
  --compare "results/$runId/input.json" `
  --output "validation/$runId-target-offline-$demoId.json"
if ($LASTEXITCODE -ne 0) { throw 'Offline target validation failed' }
py -3.13 -B -X utf8 scripts/generate_report.py `
  --run-dir "results/$runId" `
  --attempt-id $attemptId `
  --prepare-only
if ($LASTEXITCODE -ne 0) { throw 'Local request preparation failed' }
```

The expected result is `prepared_not_executed`. Inspect `solar-prepare-status.json` and `solar-request.json`; the request's system message must match `skill/report-writing/SKILL.md`. This validates the packaged example only. It is not a new chemical inference, a Solar response, or a test on another computer. The command and output from this package's offline check are recorded in [the hash-repair validation](validation/public-evidence-hash-repair-20261115.json). The one-time curation utility `scripts/prepare_public_evidence_derivative.py` used a read-only local copy of the original run to verify its path-only changes. Other computers should use the already bundled curated derivative and do not need that private historical source folder.

## 2. Install only the driver dependencies

Install in isolated environments; these commands are instructions. Keep model environments separate because AiZynthFinder and Parrot have different dependency constraints.

```powershell
py -3.13 -m venv .venv-driver
.venv-driver/Scripts/python.exe -m pip install -r requirements-driver.txt
```

AiZynthFinder, Parrot and Yield-BERT require separate environments. AiZynthFinder upstream currently documents Python 3.10-3.12. Parrot's upstream README says its environment was tested on Linux; the Windows settings in this project are an environment-specific compatibility trial, not an upstream Windows guarantee. For AiZynth stock-HDF conversion, use a separate preparation environment outside the package with `requirements-stock-preparation.txt`; do not install preparation packages into an existing model environment. For Yield-BERT, install `requirements-yields.txt`, then run `python -m pip install --no-deps rxnfp==0.1.0` in its dedicated environment to avoid the older transitive pins. Historical checkpoint/runtime environments are not included.

The script/formatting dependencies are separate:

```powershell
py -3.13 -m venv .venv-report
.venv-report/Scripts/python.exe -m pip install -r requirements-report.txt
```

For Word-to-PDF export, Microsoft Word desktop with COM automation is required. The archived Edge-render path is described in Section 5 and uses the installed Microsoft Edge executable. The verification environment was installed outside the package; see `REPRODUCIBILITY-REVIEW.md` for observed results.

## 3. Obtain model code and weights outside Git

Never put weights, private datasets, virtual environments, `.env`, or API keys in this repository. Follow each upstream repository's current instructions and record the chosen commit/checkpoint hashes. The project adapters require these runtime values; use `configs/model-assets.lock.json` for the checked model versions and checkpoint hashes, then configure your own paths in the current PowerShell session. `configs/runtime.json` and `configs/aizynthfinder.json` are templates; do not commit local absolute paths or secrets. The adapter reads `configs/runtime.json`; the AiZynthFinder template also reads `AIZYNTH_MODEL_DIR` and `AIZYNTH_STOCK_BUCKETS`.

| Task | Official source and required local artifacts | Runtime values used by adapter |
| --- | --- | --- |
| Routes | [AiZynthFinder](https://github.com/MolecularAI/aizynthfinder): in its isolated Python 3.10-3.12 environment, set `$dataDir = 'D:\models\aizynth\public-data'` and run `download_public_data $dataDir`; point to the matching `uspto_model.onnx` and `uspto_templates.csv.gz`. This package uses `scripts/disk_stock.py` and requires exact stock buckets generated by `scripts/prepare_stock_buckets.py` from the downloaded HDF stock file. | `AIZYNTH_PYTHON`, `AIZYNTH_MODEL_DIR`, `AIZYNTH_STOCK_BUCKETS` |
| Conditions | [Parrot](https://github.com/wangxr0526/Parrot): clone the official repository, create its documented Conda environment, run its `preprocess_script/download_data.py`, and use the extracted `outputs/Parrot_train_in_USPTO_Condition_enhance` checkpoint directory containing `pytorch_model.bin`. | `PARROT_PYTHON`, `PARROT_REPOSITORY`, `PARROT_CHECKPOINT` |
| Yield | [rxn_yields](https://github.com/rxn4chemistry/rxn_yields) plus its linked pretrained RXN model assets. The inference adapter expects `<checkpoint>/pytorch_model.bin` and a matching tokenizer/config/model_args folder. Obtain the matching official checkpoint; verify its SHA-256 against `configs/yield-normalization.json`. If the checkpoint differs, do not reuse the shipped mean/std: regenerate normalization metadata from the exact training split. | `RXN_YIELDS_PYTHON`, `RXN_YIELDS_CHECKPOINT` |

The successful local run `benzocaine-live-20261031-04` used AiZynthFinder 4.4.1, Python 3.12, ONNX model `uspto_model.onnx`, templates `uspto_templates.csv.gz`, a 120 s search limit, 100 iterations and at most 4 transforms. Its log records 70 route trees generated, 54 solved routes, 12 selected route predictions, and 17,422,831 stock entries (8.43 s search time). The exact generated stock buckets remain at `<benzocaine-project-root>/assets/stock-buckets`; the portable submission copy omits this roughly 0.5 GB derivative along with model weights. The successful run has a stock path because it ran from the project working copy. On this PC, point `AIZYNTH_STOCK_BUCKETS` at the existing project-level directory; on another PC, use the preparation procedure below. On another PC, generate the buckets from the complete official HDF stock file as below; do not use a partial stock silently.

```powershell
# Use a separate environment outside the project/package for stock conversion.
$prepEnv = Join-Path $env:USERPROFILE '.venvs\aizynth-stock-preparation'
py -3.13 -m venv $prepEnv
$prepPython = Join-Path $prepEnv 'Scripts\python.exe'
& $prepPython -m pip install -r requirements-stock-preparation.txt
$dataDir = 'D:\models\aizynth\public-data'
$stockSource = Join-Path $dataDir 'zinc_stock.hdf5'
$stockBuckets = 'D:\models\aizynth\stock-buckets'
# First use AiZynthFinder's documented download_public_data command to get the complete bundle.
& $prepPython -B -X utf8 scripts/prepare_stock_buckets.py `
  --source $stockSource `
  --output-dir $stockBuckets
```

The converter verifies that every original row became a literal InChIKey record, all 26 bucket files match their manifest hashes, and the stock source hash is recorded. It creates the output directory and about 0.5 GB of derived keys; choose an external disk location with adequate free space. The source HDF and generated buckets are not copied into Git.

Set runtime variables for this PowerShell session, for example (replace paths with actual local paths):

```powershell
$env:AIZYNTH_PYTHON = 'D:\models\aizynth\python.exe'
$env:AIZYNTH_MODEL_DIR = 'D:\models\aizynth\public-data'
$env:AIZYNTH_STOCK_BUCKETS = 'D:\models\aizynth\stock-buckets'
$env:PARROT_PYTHON = 'D:\models\parrot\python.exe'
$env:PARROT_REPOSITORY = 'D:\models\Parrot'
$env:PARROT_CHECKPOINT = 'D:\models\Parrot\outputs\Parrot_train_in_USPTO_Condition_enhance'
$env:RXN_YIELDS_PYTHON = 'D:\models\yields\python.exe'
$env:RXN_YIELDS_CHECKPOINT = 'D:\models\yields\checkpoint'
```

Before any model call, run the local preflight. It validates the target SMILES/formula, runtime imports, adapter/checkpoint paths, checkpoint hashes, yield normalization metadata, AiZynth HDF provenance, and every stock bucket hash. It does not load model weights for prediction, make network requests, or run inference. It is safe to run for a new target.

```powershell
py -3.13 -B -X utf8 scripts/preflight_models.py `
  --input inputs/$targetId.json `
  --output validation/$targetId-preflight.json
if ($LASTEXITCODE -ne 0) { throw 'Preflight failed; do not start inference' }
```

For this PC, historical asset locations are recorded in `validation/model-asset-reuse-audit-20261105.json`. Those are optional references to external machine assets, not package dependencies. The portable setup uses the official download and stock-bucket preparation instructions above and does not depend on the Aspirin test project.

The shipped `yield-normalization.json` is tied to one checkpoint hash and training split. The training code documents its setup but the model checkpoint is not bundled; use the official trained-model assets linked from [rxn-models](https://github.com/rxn4chemistry/rxn-models) or retrain from the pinned source/data. Check that the checkpoint SHA, model files, tokenizer, training normalization, and upstream commit agree before inference. Do not use DRFP as a yield model unless a trained regressor and its metadata are supplied. ASKCOS requires a separately configured live service; SynthEx currently has no adapter normalizer in this package and is not executable.

## 4. Run real predictions and prepare Solar input

```powershell
$runId = "$targetId-live-20261105-01"
py -3.13 -B -X utf8 scripts/run_pipeline.py `
  --input "inputs/$targetId.json" `
  --run-id $runId
```

The command creates `results/<run-id>/` and records raw outputs, logs, images, status and checksums. A model without a configured environment/checkpoint remains `not_implemented` or fails with a recorded reason; no mock fallback is used. Verify actual model statuses and inspect `results/<run-id>/report-evidence.json` before preparing a report.

Report authoring is separate from chemical inference and may be billable. `configs/report-plan.json` pins model snapshot `solar-pro4-260806`, temperature 0 and a 10,000-token response ceiling; both Solar authorization flags are disabled. A report-only request uses the already prepared run and the specialized Solar skill `skill/report-writing/SKILL.md`:

```powershell
$attemptId = "$runId-report-01"
py -3.13 -B -X utf8 scripts/generate_report.py `
  --run-dir "results/$runId" `
  --attempt-id $attemptId `
  --prepare-only
```

This creates `results/<run-id>/solar-attempts/<attempt-id>/solar-request.json` and `solar-prepare-status.json` without contacting Solar. Inspect the prepared messages, evidence hashes, skill path and model settings. To send that exact prepared request, first obtain explicit authorization, configure both plan flags and `UPSTAGE_API_KEY` in a local environment, then run the same command with `--execute-solar`. The execution mode requires the prepared attempt, blocks reuse after a response/status exists, and does not automatically retry. The returned Markdown is saved under `reports/<run-id>-<attempt-id>/report.md`.

To create the documents from that Solar-authored Markdown, use the existing run assets and recorded status:

```powershell
$reportDir = "reports/$runId-$attemptId"
$markdown = "$reportDir/report.md"
$solarStatus = "results/$runId/solar-attempts/$attemptId/solar-status.json"
py -3.13 -B -X utf8 scripts/export_report_docx.py `
  --markdown $markdown `
  --run-dir "results/$runId" `
  --solar-status $solarStatus `
  --compact-layout
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/convert_docx_to_pdf.ps1 `
  -DocxPath "$reportDir/report.docx" `
  -PdfPath "$reportDir/report.pdf" `
  -MetadataPath "$reportDir/word-export.json"
```

The report-only path does not rerun AiZynthFinder, Parrot or Yield-BERT. A model prediction request, Solar report-authoring call, and conversion of an already saved response are separate operations. Do not call the prior benzocaine run a prediction for a different target.

### General saved-response rendering for a target with validated results

For a new target, Solar writes scientific prose and places one exact `[figure: <figure_id>]` marker for each supplied report asset. The renderer then verifies the marker against `report-evidence.json`, checks the asset path and SHA-256, joins selected route/step/reaction records to Parrot and yield results, inserts a single conditions/yield table, and converts the markers to local image links. It does not call Solar or rerun a chemistry model. Do not use this path if the response already contains an integrated route/step conditions-yield table: the renderer refuses to replace authored table content.

```powershell
$runId = 'your-validated-run-id'
$attemptId = 'your-successful-solar-attempt-id'
$runDir = "results/$runId"
$attemptDir = "$runDir/solar-attempts/$attemptId"
$sourceMarkdown = "reports/$runId-$attemptId/report.md"
$renderDir = "reports/$runId-$attemptId-rendered"

py -3.13 -B -X utf8 scripts/render_report_evidence.py `
  --run-dir $runDir `
  --attempt-dir $attemptDir `
  --source-markdown $sourceMarkdown `
  --solar-status "$attemptDir/solar-status.json" `
  --output-dir $renderDir
py -3.13 -B -X utf8 scripts/export_report_docx.py `
  --markdown "$renderDir/report.md" `
  --run-dir $runDir `
  --solar-status "$attemptDir/solar-status.json" `
  --layout-validation "$renderDir/layout-validation.json" `
  --compact-layout
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/convert_docx_to_pdf.ps1 `
  -DocxPath "$renderDir/report.docx" `
  -PdfPath "$renderDir/report.pdf" `
  -MetadataPath "$renderDir/word-export.json"
py -3.13 -B -X utf8 scripts/validate_rendered_report.py `
  --run-dir $runDir `
  --attempt-dir $attemptDir `
  --report-dir $renderDir
```

If `report.md` contains an approved Solar-authored edit rather than the exact saved response text, pass its verified provenance using `--source-validation <passed-validation.json>` to the renderer. Keep each output directory new and empty; the scripts refuse to overwrite earlier attempts. This code-rendered path was verified with stored acetaminophen results on the existing PC; it is not a clean-PC or all-target guarantee.

## 5. Rebuild the current report from its saved Solar response (no API request)

This procedure rebuilds the current 19-page report from the saved Solar-authored Markdown and evidence. It does not call Solar or run synthesis models. Microsoft Word desktop is used for DOCX-to-PDF conversion. Start with a new empty work folder; never overwrite the release folder.

```powershell
$source = 'reports/benzocaine-page-layout-and-instruction-cleanup-20261115'
$work = 'reports/document-rebuild-local'
New-Item -ItemType Directory -Path $work
Copy-Item "$source/report.md" $work
Copy-Item "$source/solar-call" $work -Recurse
Copy-Item "$source/evidence-run" $work -Recurse
Copy-Item "$source/merge-validation.json" $work
Copy-Item "$source/citation-source-map.json" $work
.venv-report/Scripts/python.exe -X utf8 scripts/audit_citations.py `
  --report "$work/report.md" `
  --evidence-dir "$work/evidence-run" `
  --source-map "$work/citation-source-map.json" `
  --output "$work/citation-audit.json"
.venv-report/Scripts/python.exe -X utf8 scripts/export_report_docx.py `
  --markdown "$work/report.md" `
  --run-dir "$work/evidence-run" `
  --solar-status "$work/solar-call/solar-status.json" `
  --verified-edits-validation "$work/merge-validation.json" `
  --compact-layout
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/convert_docx_to_pdf.ps1 `
  -DocxPath "$work/report.docx" `
  -PdfPath "$work/report.pdf" `
  -MetadataPath "$work/word-export.json"
.venv-report/Scripts/python.exe -X utf8 scripts/validate_citation_corrected_documents.py `
  --report-dir "$work" `
  --run-dir "$work/evidence-run" `
  --citation-validation "$work/citation-audit.json"
Move-Item "$work/report.docx" "$work/벤조카인_AI유기합성_최종보고서.docx"
Move-Item "$work/report.pdf" "$work/벤조카인_AI유기합성_최종보고서.pdf"
```

The current included run was rebuilt and passed citation/content checks: 19 pages, 10 figures, 4 tables, all referenced URLs present, no detected overflow or authoring instructions. Details are in `reports/benzocaine-page-layout-and-instruction-cleanup-20261115/document-validation.json`. Report source scans and the course PDF are intentionally not bundled; official links and access instructions are in `reports/benzocaine-page-layout-and-instruction-cleanup-20261115/evidence-run/literature-validation/route-01-primary-comparison-20261114/source-acquisition.md` and `evidence-run/course-material-acquisition.md`.


Official model repositories, versions, checkpoint requirements and setup instructions are listed above and in `skill/SKILL.md`. Model weights, local environments, private API keys, and large derived stock buckets are excluded. The package retains the asset lock/checksum metadata and the stock generation instructions.

The report is based on the saved Benzocaine evidence; its displayed values remain tied to the listed run IDs. A fresh local rerun with the submission entrypoint succeeded on this same PC for the same Benzocaine input at `results/benzocaine-live-repro-20261105-01/`. The route/condition/yield integrity and reuse comparison records are included there and under `validation/`. This does not verify another molecule or a clean computer. For a new molecule, prepare its own JSON, install isolated runtimes, obtain matching model assets and full AiZynthFinder stock buckets, run preflight, and then use `scripts/run_pipeline.py` as described above. Never reuse Benzocaine predictions for a different target.

Saved-response DOCX/PDF rebuilding is distinct from fresh model inference and a new Solar-authored report. The saved-response build was verified locally with the existing external report environment and Word 16.0; no new installation, inference, Solar request, GitHub push, or school submission was part of this curation.

## 2026-11-18 document-rendering regression scope

The existing-PC acetaminophen pipeline had already produced real AiZynthFinder, Parrot, and Yield-BERT outputs (12 route predictions/16 steps; 14 unique Parrot reaction rows mapped to 16 route steps; 16 yield predictions). A saved Solar Pro 4 response from attempt `acetaminophen-report-live-20261117-02` was reused; this rendering did not make another Solar call or chemistry-model inference. The generalized renderer matched five figure markers to five exact manifest assets, joined four selected route steps to their conditions and predicted yields, created the single normalized table, and generated DOCX/PDF. The final current-code build passed at 10 PDF pages with five PDF figures, four route/step rows, and no detected clipping. Redacted hashes and preserved prior failure summaries are in [`validation/acetaminophen-document-render-regression-20261118.json`](validation/acetaminophen-document-render-regression-20261118.json).

The benzocaine document-generation regression used the stored report and its report-specific citation map. DOCX/PDF generation and the full document checks passed (19 pages, 10 figures, 4 tables). The existing final Benzocaine DOCX/PDF were not overwritten and their hashes still match the prior release validation. An initial validator run with the package-wide citation map was preserved as a failed attempt; that map assigns `[17]` to the rxn_yields notebook, while this report's own map correctly assigns `[17]` to the course material. The validator now prefers the report-specific map and the corrected run passes. The anonymized summary is [`validation/benzocaine-document-render-regression-20261118.json`](validation/benzocaine-document-render-regression-20261118.json).

Scope: both target workflows were exercised using existing assets on this PC. Acetaminophen had actual model predictions and a saved Solar-authored body; Benzocaine regression used its existing saved report. This does not establish clean-PC setup/reproduction or success for every input molecule. The final project submission target remains Benzocaine; the acetaminophen run is a validation example only.

The renderer's focused offline tests passed (4/4). The earlier broad test run and its six failures remain recorded in [`validation/report-render-code-tests-20261118.json`](validation/report-render-code-tests-20261118.json). Follow-up isolated the two harness failures to a real handler attribute bug, corrected it, and all five request-guard tests now pass against loopback mocks. The four step-graph tests pass with the existing system RDKit environment. The report-validation virtual environment lacks RDKit while the system environment lacks `markdown_it`, so a single-environment full discovery pass is not claimed; see [`validation/harness-request-guard-fix-20261118.json`](validation/harness-request-guard-fix-20261118.json). No Solar or chemistry-model call was made.

`PACKAGE-MANIFEST.json` records SHA-256 over Git clean-filtered blob bytes, so text-file checksums correspond to the bytes stored by GitHub even when a Windows working copy uses different line endings. Its sidecar hashes the manifest itself. Virtual environments, `.git`, runtime caches, `__pycache__`, and `.pyc` files are excluded.
## 6. Sources, limitations and reproducibility

Official model repositories, versions, checkpoint requirements and setup instructions are listed above and in `skill/SKILL.md`. Model weights, local environments, private API keys, and large derived stock buckets are excluded. The package retains the asset lock/checksum metadata and stock generation instructions.

The report is based on the saved Benzocaine evidence; its displayed values remain tied to the listed run IDs. A fresh local rerun with the submission entrypoint succeeded on this same PC for the same Benzocaine input at `results/benzocaine-live-repro-20261105-01/`. The route/condition/yield integrity and reuse comparison records are included there and under `validation/`. This does not verify another molecule or a clean computer. For a new molecule, prepare its own JSON, install isolated runtimes, obtain matching model assets and full AiZynthFinder stock buckets, run preflight, and then use `scripts/run_pipeline.py` as described above. Never reuse Benzocaine predictions for a different target.

Saved-response DOCX/PDF rebuilding is distinct from fresh model inference and a new Solar-authored report. The saved-response build was verified locally with the existing external report environment and Word 16.0; no new installation, inference, Solar request, GitHub push, or school submission was part of this curation.


## Public-copy privacy and hashes

The public upload tree was scanned for workstation-root strings and credential patterns. No workstation-root matches remained and the secret scanner found no credential matches. Earlier execution logs and results were anonymized only in this public copy; `validation/privacy-redaction-log-20261118.json` maps each changed Git blob SHA-256 to its sanitized-copy SHA-256. Original project files and the final Benzocaine PDF/DOCX were preserved. The package manifest covers the bytes intended for GitHub. Historical run-internal hashes continue to describe execution-time originals and are not silently relabeled as hashes of the sanitized derivatives; consult the redaction log when checking a public copy. See [`validation/public-copy-integrity-generalized-renderer-20261118.json`](validation/public-copy-integrity-generalized-renderer-20261118.json) and [`validation/package-secret-audit-generalized-renderer-20261118.json`](validation/package-secret-audit-generalized-renderer-20261118.json).
