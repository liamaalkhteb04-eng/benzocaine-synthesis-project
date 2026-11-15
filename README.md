# AI synthesis report pipeline - reproducible source package

This package includes target-neutral route, condition and yield adapters; report-writing skill; benzocaine example inputs and evidence; and the current verified report. Saved benzocaine predictions are examples only and are never reused for a different target.

## Unified report skill

[`skill/SKILL.md`](skill/SKILL.md) is the single current entrypoint for Solar Pro 4 report writing and the pipeline workflow. New report requests default to a complete report from the selected target and verified evidence. Section- or sentence-only edits apply only when the user explicitly requests a narrow revision. Historical prompts and exact skill files used in prior calls are preserved with hashes and run IDs in [`provenance/skills/PATH-MAP.md`](provenance/skills/PATH-MAP.md); they are not injected into new full-report requests.

The standard flow is: create `inputs/<target_id>.json` from `inputs/input-template.json`, validate and preflight it, execute `scripts/run_pipeline.py` with a new run ID, review raw outputs and additional analyses, prepare or execute the explicitly authorized Solar Pro 4 request through `scripts/generate_report.py`, then export and validate DOCX/PDF. Saved-response document rebuilds use the archived response and do not make a new model request. See `skill/SKILL.md` for the full evidence and page-limit rules.


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

```powershell
$targetId = 'my-compound'
Copy-Item inputs/input-template.json "inputs/$targetId.json"
# Edit inputs/my-compound.json, then validate structure and public identity:
py -3.13 -B -X utf8 scripts/prepare_target.py `
  --input "inputs/$targetId.json" `
  --output "validation/$targetId-identity.json"
```

`prepare_target.py` validates SMILES/formula with RDKit and makes a PubChem PUG REST identity request. This is an identity check, not synthesis inference.

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

The fresh Solar call is a separate, potentially billable action. `configs/report-plan.json` pins model snapshot `solar-pro4-260806`, temperature 0 and a 10,000-token response ceiling; it has both paid-call gates disabled. Keep them disabled unless a budget has been explicitly approved. For a fresh Solar-authored report, use a new attempt ID and run:

```powershell
# Only after setting both report-plan authorization flags under explicit approval
# and providing UPSTAGE_API_KEY through a local secret manager/session (never commit it):
$attemptId = "$runId-solar-01"
py -3.13 -B -X utf8 scripts/build_submission_report.py `
  --run-dir "results/$runId" `
  --output-dir "reports/$runId-report" `
  --attempt-id $attemptId `
  --execute-solar
```

The script calls `generate_report.py`, validates Solar's response against the run evidence, exports DOCX, asks Word to generate PDF, and checks the result. Fresh model predictions and fresh Solar authorship are separate from conversion of any saved response.

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
## 6. Sources, limitations and reproducibility

Official model repositories, versions, checkpoint requirements and setup instructions are listed above and in `skill/SKILL.md`. Model weights, local environments, private API keys, and large derived stock buckets are excluded. The package retains the asset lock/checksum metadata and stock generation instructions.

The report is based on the saved Benzocaine evidence; its displayed values remain tied to the listed run IDs. A fresh local rerun with the submission entrypoint succeeded on this same PC for the same Benzocaine input at `results/benzocaine-live-repro-20261105-01/`. The route/condition/yield integrity and reuse comparison records are included there and under `validation/`. This does not verify another molecule or a clean computer. For a new molecule, prepare its own JSON, install isolated runtimes, obtain matching model assets and full AiZynthFinder stock buckets, run preflight, and then use `scripts/run_pipeline.py` as described above. Never reuse Benzocaine predictions for a different target.

Saved-response DOCX/PDF rebuilding is distinct from fresh model inference and a new Solar-authored report. The saved-response build was verified locally with the existing external report environment and Word 16.0; no new installation, inference, Solar request, GitHub push, or school submission was part of this curation.