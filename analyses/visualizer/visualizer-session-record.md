# Discovery Studio Visualizer session record

## Installation and process

- Product: BIOVIA Discovery Studio Visualizer 2025 Client
- Version: 25.1.0 (file version 25,1,0,24284; build 518165 20241010 2048)
- Install: `C:\Program Files\BIOVIA\Discovery Studio 2025\`
- Executable: `C:\Program Files\BIOVIA\Discovery Studio 2025\bin\DiscoveryStudio2025.exe`
- During this session the process was running and responsive (PID 12132).

## Actions actually observed in Visualizer

- Opened the benzocaine PM7 conformer SDF and saw its five-record conformer table.
- Opened `inputs/ethyl-4-nitrobenzoate-mopac-pm7-conformers.sdf` and saw five conformer records.
- Added atom ID labels in the 3D view and captured labeled benzocaine and route-01 views. The selected route-01 atoms correspond to the SDF atom serials in the measurement plan.
- Screen captures that document the observed UI are in `screenshots/benzocaine-opened-in-visualizer.png`, `screenshots/route01-labeled-view.png`, `screenshots/route01-nitro-zoomed.png`, and `screenshots/route01-reloaded-actual.png`. `route01-reloaded-actual.png` shows the five records in the Visualizer table; the graphics pane had not yet been restored in that particular capture.

## Not completed

- Multiple conformer geometry comparisons and multiple stable viewing orientations were not completed. The graphics view intermittently rendered only part or none of the molecule after view changes.
- No distance, angle, or torsion result has been measured. No screenshot is represented as a measurement capture.
- A native Perl Script Window was opened and a test script was entered. The Output pane remained empty; therefore script execution and numerical extraction are unverified. No script-derived values are reported.
- No intermolecular reactant pair was assembled. Any such manually arranged pair would be illustrative only, not a calculated complex.

## Exact Visualizer measurement operation

The installed Visualizer 2025 Help (`share/doc/DSV/content/docds/client/menu_view_toolbars_view_hw.htm`) describes the Measure tool:

1. In the route-01 document, restore the Graphics view (`View > Graphics`, if the data table is active), select one conformer row, and use `Fit To Screen`.
2. Confirm the whole molecule is drawn. If it is partial/black, do not measure or capture it; reopen the saved SDF and return to the Graphics view.
3. Deselect all objects. Select two target atoms (or one bond) for a distance, then click the View toolbar's `Measure` tool. For an angle, deselect, select three atoms (or two connected bonds), then click `Measure`.
4. Use the atom ID labels and `measurement-plan.csv` serials to choose the specified atoms. Record the actual displayed number, unit, conformer row, and structure filename in a new observation record; take a screenshot with all atoms, labels, and the measurement annotation visible.
5. Repeat per conformer and direction only while the full structure remains visibly rendered. Save screenshots as new files; do not overwrite original MOPAC structures.

The corresponding native scripting API is documented in the installed Help (`CreateDistanceMonitor` / `CreateAngleMonitor`), but this session's test produced no observed output and must be debugged before relying on it.

## Interpretation boundary

These are isolated, PM7-optimized starting conformers. Intramolecular distances/angles and static visual access do not prove a reaction complex, mechanism, reaction feasibility, kinetics, activation energy, or experimental/model yield.


## Update

This earlier record reflects the prior session, when no measurements had yet been made. The 2026-11-01 recovery and actual measurements are documented in [visualizer-recovery-and-measurement-session.md](visualizer-recovery-and-measurement-session.md), [actual-visualizer-measurements.json](actual-visualizer-measurements.json), and [visualizer-measurements.csv](visualizer-measurements.csv).
