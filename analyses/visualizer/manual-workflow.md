# Discovery Studio Visualizer: manual analysis handoff

## Status

No Discovery Studio Visualizer installation or running process was detected in the checked locations. This session has no interactive desktop-control channel. Therefore no Visualizer file was opened, no accessibility observation or measurement was completed, and no Visualizer screen capture exists. The project status is **not analyzed / awaiting user installation and GUI work**. Do not cite the prepared SDFs or this workflow as a Discovery Studio result.

## Official download and user steps

BIOVIA/Dassault Systèmes offers Discovery Studio Visualizer as a free download for molecular viewing/basic analysis. Download access is provided through its official registration form:

- https://discover.3ds.com/discovery-studio-visualizer-download
- Product overview: https://www.3ds.com/products/biovia/discovery-studio/visualization

The user must open the official download page, complete its registration form, select/download the Windows installer, install the supplied Visualizer package, launch it, and record the version from **Help > About** (menu label can differ by release). No installer was downloaded or run here. Avoid downloading third-party repacks. The free Visualizer is distinct from the licensed full Discovery Studio product.

## Prepared structures

Open the multi-record SDFs under `inputs/`. Each contains five existing MOPAC PM7 conformer geometries copied from the corresponding `.arc` final geometry into the selected structure's atom/bond graph. These are conversion files for viewing, not new calculations. The selected conformer is identified in each record's `selected_pm7_geometry` property. The first four original MOPAC selected-geometry SDFs remain preserved under `analyses/mopac/optimized-structures/`.

For the nitro structure, the copied graph had lost atom-level formal charge annotations in the source SDF. The preparation script restores the input-SMILES nitro charges using an SDF `M  CHG` record on atom 10 (+1) and atom 12 (-1), without changing coordinates. Confirm the atom labels after opening. See `atom-serial-crosswalk.csv` for SDF serial, element, and source atom map correspondence.

## GUI sequence

1. In Discovery Studio Visualizer, use **File > Open** (or the equivalent open command) to load the SDF for one species. If the file importer opens the records separately, choose each conformer entry from the document/structure hierarchy; keep the conformer index visible in the record name or property table.
2. Set a 3D stick or ball-and-stick view, fit the molecule, and display atom labels or atom indices. The exact display-label controls can vary by version. Use `atom-serial-crosswalk.csv` to resolve the heavy-atom map numbers and hydrogen SDF serials.
3. For each selected MOPAC conformer, rotate to at least three distinct directions (front/side/oblique). Record qualitative observations only, such as whether an atom is visibly flanked by neighboring atoms in that isolated geometry. Do not call this a computed solvent-accessible area or catalyst approach trajectory.
4. Use the version's **Measure** tool (or the equivalent structure-monitor measurement command) to record the distances/angles/torsion listed in `measurement-plan.csv`. Save the value, atom labels, SDF filename, conformer index, and units exactly as displayed. Use Å for distances and degrees for angles/torsions.
5. For route-05 only, if an explanatory picture places PABA next to ethanol, label it prominently **illustrative manual placement; not a calculated/optimized reaction complex**. Measure C6···O3 only as a layout descriptor. Do not infer binding, reaction progress, or a reaction pathway from that placement.
6. Save screenshots with the molecule, selected reaction-site labels, displayed measurement and value, conformer index, and application/version visible where practical. Do not crop away the atom labels or measurement annotations.

## Selected routes and requested screen captures

Route and atom-number selection rationale is in `route-selection.json`.

- `route-01`: representative one-step nitro-to-amine predicted route. Capture the para nitro region from three orientations and the two N10-to-ortho-H distances plus the C8-C9-N10 and C13-C9-N10 angles. Repeat for conformers 1–5, or document why a record could not be opened.
- `route-05`: comparison route using PABA and ethanol. Capture PABA carboxyl C6/O7/O8 and ethanol O3 in three orientations, with the local geometry measurements in the CSV. Repeat for conformers 1–5. If showing a manually placed pair, save a separate explicitly illustrative capture with C6···O3 annotated.
- Save at least these file names under `screenshots/`: `route-01-nitro-site-conformer-1-front.png`, `route-01-nitro-site-conformer-1-side.png`, `route-01-nitro-site-measurements.png`, `route-05-paba-site-measurements.png`, `route-05-ethanol-site-measurements.png`, and (only if used) `route-05-illustrative-pair-not-complex.png`. Add conformer index to every capture used for cross-conformer comparison.

## Interpretation limits

MOPAC structures are isolated neutral-molecule PM7 gas-phase minima; there is no solvent, catalyst surface, hydrogen source, intermolecular encounter geometry, or transition state. Static geometry and manual measurements cannot establish activation barriers, rates, reaction success, or yield. The route labels are AiZynthFinder predictions and do not validate the reaction chemistry.
