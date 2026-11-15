# MOPAC analysis bundle

MOPAC portable distribution and version record: [installation manifest](../../tools/mopac-installation.json). All model runs, output parsing, optimized SDF exports, and interpretation are under this directory.

`analyses/preparation/structure-preparation.json` is a historical record of the earlier structure-preparation stage. Its `mopac_invoked: false` means no MOPAC work had been done at the time that preparation snapshot was created. Actual calculations are recorded here in `run-manifest.json` and `analysis-summary.json`; the earlier snapshot and frozen prediction run were left unchanged.

The 25 independent starts consist of five conformers each for ethyl 4-nitrobenzoate, benzocaine, 4-aminobenzoic acid, ethanol, and acetic acid. Each run directory retains its `.mop` input, raw `.out`, `.arc` optimized archive, stdout, and stderr log. `run-manifest.json` holds SHA256 hashes for executable, official archive, inputs, and all raw output files.

The first validation attempt was stopped before launching MOPAC because a preflight helper counted heavy-atom electrons without hydrogens. The next batch completed the first five ethyl 4-nitrobenzoate conformers, then stopped at a target identity comparison that included atom-map labels. Both helper issues were corrected; the first five output files were hash-checked and reused, and the other twenty calculations then ran. These orchestration events are recorded in `run-manifest.json` and `validation/mopac-input-review.json`; they did not change the molecular inputs or require changing the system Python/model environment.
