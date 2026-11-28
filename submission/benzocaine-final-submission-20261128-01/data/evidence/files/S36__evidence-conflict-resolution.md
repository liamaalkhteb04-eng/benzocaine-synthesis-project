# Evidence reconciliation for final-report authoring

## Current authority

Use `additional-analysis-status-current.json` and the `additional_analyses` object in `results/report-evidence.json` for current completion status. This evidence bundle was assembled on 2026-11-03 after the analyses and harness trial were completed.

## Historical conflicts preserved outside this bundle

- `results/benzocaine-live-20261031-04/additional-analysis-status.json` says harness comparison, MOPAC, EPI Suite, and Discovery Studio are `not_implemented`. It is a preparation-phase snapshot and was not edited.
- The normalized source `results/benzocaine-live-20261031-04/report-evidence.json` contains the same obsolete status block. This bundle's `results/report-evidence.json` is a derived copy where only `additional_analyses` is replaced with evidence-backed current status. The original remains untouched.
- The frozen harness input `analyses/harness-comparison/comparison-input-payload.md` includes that stale status source and states route-05 Visualizer measurements were unrun. It was the actual shared input at trial time and remains untouched. It is excluded from the current authoring evidence.
- The original OpenCode and Pi drafts remain byte-for-byte in `results/harness-comparison/`. They repeat stale status claims; Pi also contradicts itself by later describing completed analyses. Their content-level comparison is summarized in `harness-comparison/trial-02-comparison-evaluation.md`; that evaluation describes the Visualizer scope at harness-trial time, before this later qualitative view supplement. The current Visualizer scope is in `visualizer/accessibility-observations.md` and supersedes only those historical observation-scope statements. Do not use the old drafts as a source of current chemistry facts.

## Updated Visualizer scope

Current Visualizer evidence includes actual screens for route-01 substrate conformer 1 and 2, route-01 product conformer 1, route-05 PABA conformer 4, and separate ethanol conformer 2. The four previous Visualizer measurements remain only the route-01 intramolecular values listed in `visualizer/visualizer-measurements.csv`. Route-05 has qualitative single-molecule screens but no new GUI distance or angle measurements and no intermolecular PABA/ethanol approach observation. No static structure supports claims about a reaction barrier, rate, success, or yield.

## Final authoring constraints

For the evidence-bundle snapshot as originally assembled, no new Solar call or final report had yet been made. The user instruction dated 2026-11-03 now explicitly authorizes Solar Pro 4 final-report generation and one prompt-guided correction if needed, while the cumulative credit ceiling remains $1 and cash payment/top-up are forbidden. A later Solar Pro 4 report must use current evidence, distinguish prediction/observation/measurement, include unresolved limits, and stay within 20 pages including references.
