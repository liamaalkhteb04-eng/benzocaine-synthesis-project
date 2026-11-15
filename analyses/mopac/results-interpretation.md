# MOPAC PM7 result interpretation

## What was calculated

MOPAC 23.2.5 performed PM7 isolated-molecule geometry optimizations for five neutral species. For each molecule, five RDKit ETKDGv3 conformers were first minimized with MMFF94s; all five were independently optimized with MOPAC. Inputs explicitly set `CHARGE=0 MS=0`, so the specified state is neutral singlet. MOPAC output confirms closed-shell RHF, SCF completion, normal job termination, and a final gradient norm below the requested `GNORM=0.5 kcal mol⁻¹ Å⁻¹` for all **25/25** jobs.

The primary input conformer was the one with the lowest MMFF94s starting energy among the five. Because every start was calculated, the geometry saved as `*-pm7-optimized.sdf` is instead the converged geometry with the lowest PM7 heat of formation among those five starts **for that same molecular formula and charge**. It is a best-of-five search, not a proven global minimum or a frequency-verified minimum.

All jobs were gas-phase, with no solvent, catalyst, hydrogen, counterion, reaction partner, or transition state. The calculated heats below are listed per molecule as output records. They are not compared across different formulas and are not a reactivity or stability ranking.

| Species | Formula | Converged starts | Best-of-five PM7 heat of formation (kcal/mol) | Final gradient norm (kcal mol⁻¹ Å⁻¹) | Dipole (D) | Heat spread within this species' five starts (kcal/mol) |
|---|---:|---:|---:|---:|---:|---:|
| Ethyl 4-nitrobenzoate | C9H9NO4 | 5/5 | -72.22692 | 0.42843 | 4.508 | 0.51989 |
| Benzocaine | C9H11NO2 | 5/5 | -73.05519 | 0.39984 | 4.100 | 0.49850 |
| 4-Aminobenzoic acid | C7H7NO2 | 5/5 | -70.47009 | 0.48101 | 4.785 | 0.00225 |
| Ethanol | C2H6O | 5/5 | -57.85665 | 0.38440 | 2.064 | 1.98718 |
| Acetic acid | C2H4O2 | 5/5 | -102.19677 | 0.31766 | 1.990 | 0.00047 |

The within-species spread highlights starting-geometry sensitivity in this small ensemble: ethanol's five optimized starts span about 1.99 kcal/mol, while the 4-aminobenzoic-acid and acetic-acid starts converge to nearly identical heats. This is not a thermodynamic population calculation. A narrow five-start spread does not prove global convergence.

## Structural and charge observations

Selected optimized bond distances are calculated from the final MOPAC ARC Cartesian coordinates using the input molecular graph. Distances are in Å. The charge values are MOPAC's population-derived net atomic charges in units of electron charge; they are model partitions, not directly observable atomic properties.

- **Ethyl 4-nitrobenzoate:** ester C=O 1.2050; ester C–O 1.3528; aryl C–nitro N 1.4603; the two N–O distances are 1.2198 and 1.2198. The selected conformer's N charge is +0.6117 and the two O charges are -0.3904 and -0.3888. The nearly equal N–O distances are consistent with the delocalized nitro representation in this optimized PM7 structure; they do not describe the reduction process.
- **Benzocaine:** aryl C–NH2 N 1.3772; ester C=O 1.2080; ester C–O 1.3613. The amino N charge is -0.6321; carbonyl and alkoxy O charges are -0.4421 and -0.5283.
- **4-Aminobenzoic acid:** aryl C–NH2 N 1.3760; carboxyl C=O 1.2071; carboxyl C–O 1.3654. The amino N charge is -0.6274; carboxyl O charges are -0.5262 and -0.5700.
- **Ethanol:** C–O 1.4142; O charge -0.5507.
- **Acetic acid:** C=O 1.2021; C–O 1.3612; O charges -0.5065 and -0.5675.

These geometries and charge distributions characterize the computed isolated molecules. They do not establish reactant accessibility, a reaction pathway, an activation barrier, experimental conditions, yield, or synthetic success. In particular, this work does not model Pd catalysis or the missing reducing conditions in route-01's highest-ranked Parrot condition slots.

## Output files

- `run-manifest.json`: all 25 job statuses, hashes, return codes, and output paths.
- `*/conformer-*/<species>-conf-*.out`: full raw MOPAC outputs; matching `.arc` files hold the optimized geometries and charge columns.
- `analysis-summary.json`: extracted energy, gradient, dipole, convergence and conformer-sensitivity results.
- `net-atomic-charges.csv` and `optimized-bond-lengths.csv`: per-atom population charges and bond lengths from the selected best-of-five geometry for each species, plus charge rows for all starts.
- `optimized-structures/*-pm7-optimized.sdf`: selected optimized structures for visualization.
- `validation/mopac-input-review.json`: formula/charge/spin preflight and output consistency checks.

MOPAC documentation: [PM7](https://openmopac.net/Manual/pm7.html), [geometry optimization precision and GNORM](https://openmopac.net/Manual/precision.html), [MS=0 singlet](https://openmopac.net/Manual/ms.html), and [basic usage and output files](https://openmopac.net/guides/basics/).
