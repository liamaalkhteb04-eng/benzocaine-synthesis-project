# Visualizer recovery and measurement session (2026-11-01)

## Application and safe state capture

- BIOVIA Discovery Studio Visualizer 2025 Client 25.1.0 was running and responsive (PID recorded in `visualizer-session-status.json`).
- Before recovery, the open route-01 SDF state and SHA-256 hashes were saved in `session-state-before-recovery.json`; `screenshots/before-recovery-session.png` records the app view.
- The installed Help was consulted under `C:\Program Files\BIOVIA\Discovery Studio 2025\share\doc\DSV\content\docds\client`.
- Help confirmed `View > Graphics` (Ctrl+G), `Fit To Screen`, `View > Transform > Reset Rotation`, and the Data Table visibility controls. It documents `Edit > Select…` by Atom Name/ID and `View` toolbar `Measure` for distance/angle/torsion.

## Recovery and visibility check

- The active document was in Data Table view. `View > Graphics` (Ctrl+G) brought back the 3D view with conformer 1 displayed fully; its Visible cell was Yes and rows 2–5 were No.
- Enabling Visible for conformers 1 and 2 at once showed both geometries superimposed in Graphics View (`screenshots/route01-multiconformer-visible-test.png`). Conformer 2 was then hidden again.
- Further switching caused intermittent partial rendering. The original saved SDF was reopened; the app asked whether to revert in-memory edits, and Yes was chosen. This discarded temporary labels/monitor annotations in the open document and restored the saved structure without saving to the SDF. `View > Graphics` then showed a complete single conformer (`screenshots/route01-reopened-single-graphics.png`).

## Measurements actually made in Visualizer

The following were created with the application’s own Select and Measure controls and read from its AngleMonitor/DistanceMonitor Data Table. They are isolated PM7-optimized geometries, not reactant complexes or transition states.

| Conf. | Atoms | Measure | Visualizer value |
|---:|---|---|---:|
| 1 | N10–H21 (SDF atom serials 10 and 21) | Distance | 2.684 Å |
| 1 | C8–C9–N10 (atom IDs 8, 9, 10) | Angle | 119.102° |
| 2 | N10–H21 (SDF atom serials 10 and 21) | Distance | 2.682 Å |
| 2 | C8–C9–N10 (atom IDs 8, 9, 10) | Angle | 119.062° |

Evidence screenshots are named in `visualizer-measurements.csv` and retained under `screenshots/`. Conf. 2 screenshots show its row as the sole visible conformer; the measurements were created after confirming that state. The native app tables, not calculations in another code/library, supplied these values.

A post-reopen angle attempt initially used the default visible conformer 1 again; its 119.102° result was not assigned to conformer 3 and is excluded as a duplicate. Conformers 3–5 and route-05 structures were not measured because view/selection association became ambiguous during switching. They remain incomplete.

## Preservation and interpretation

- Input SDF hashes before and after this session match; see `visualizer-session-status.json`.
- The original SDF was not saved over or edited on disk. Only Visualizer in-memory view/annotation state changed and was reverted.
- Do not interpret these static intramolecular geometries as evidence for reaction rate, activation barrier, reaction success, or yield.
