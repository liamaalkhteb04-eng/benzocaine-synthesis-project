"""Package existing MOPAC PM7 conformers as multi-record SDF for DS Visualizer.

This only converts coordinates already present in MOPAC .arc outputs. It does
not run a calculation, optimize a geometry, measure anything, or create images.
"""
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analyses" / "visualizer"
MOPAC = ROOT / "analyses" / "mopac"
MAP_CSV = ROOT / "analyses" / "preparation" / "atom-numbers.csv"
SPECIES = [
    "ethyl-4-nitrobenzoate",
    "benzocaine",
    "p-aminobenzoic-acid",
    "ethanol",
]
FORMAL_CHARGE_RECORDS = {
    "ethyl-4-nitrobenzoate": [(10, 1), (12, -1)],
}
FLOAT = r"[+-]?(?:\d+\.\d*|\.\d+)(?:[Ee][+-]?\d+)?"
ARC_ATOM = re.compile(rf"^\s*([A-Z][a-z]?)\s+({FLOAT})\s+\+1\s+({FLOAT})\s+\+1\s+({FLOAT})\s+\+1\s+({FLOAT})")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_sdf(path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    natoms, nbonds = int(lines[3][:3]), int(lines[3][3:6])
    atom_lines = lines[4:4 + natoms]
    bond_lines = lines[4 + natoms:4 + natoms + nbonds]
    elements = [line[31:34].strip() for line in atom_lines]
    return natoms, nbonds, atom_lines, bond_lines, elements, lines[3]


def arc_geometry(path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    start = next(i for i, line in enumerate(lines) if "FINAL GEOMETRY OBTAINED" in line)
    atoms = []
    for line in lines[start + 1:]:
        m = ARC_ATOM.match(line)
        if m:
            atoms.append((m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4))))
        elif atoms and not line.strip():
            break
    if not atoms:
        raise ValueError(f"No final geometry parsed from {path}")
    return atoms


def main():
    inputs = OUT / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    atom_maps = list(csv.DictReader(MAP_CSV.open(encoding="utf-8-sig", newline="")))
    crosswalk, files = [], []
    summary = json.loads((MOPAC / "analysis-summary.json").read_text(encoding="utf-8"))

    for sid in SPECIES:
        base = MOPAC / "optimized-structures" / f"{sid}-pm7-optimized.sdf"
        n_atoms, n_bonds, atom_lines, bond_lines, elements, counts_line = read_sdf(base)
        species_dir = MOPAC / sid
        records, conf_meta = [], []
        detail = summary["species"][sid]
        conf_results = {x["conformer_index"]: x for x in detail["all_conformer_results"]}
        for conf_index in range(1, 6):
            arc = species_dir / f"conformer-{conf_index:02d}" / f"{sid}-conf-{conf_index:02d}.arc"
            coords = arc_geometry(arc)
            if len(coords) != n_atoms or [a[0] for a in coords] != elements:
                raise ValueError(f"Atom order mismatch: {sid} conformer {conf_index}")
            out_atoms = []
            for old, (_, x, y, z) in zip(atom_lines, coords):
                out_atoms.append(f"{x:10.4f}{y:10.4f}{z:10.4f}{old[30:]}")
            result = conf_results[conf_index]
            props = [
                f">  <species_id>\n{sid}\n",
                f">  <geometry_source>\nMOPAC PM7 optimized .arc final geometry\n",
                f">  <mopac_version>\n{summary['mopac_version']}\n",
                f">  <method>\n{summary['method']}\n",
                f">  <conformer_index>\n{conf_index}\n",
                f">  <heat_of_formation_kcal_mol>\n{result['heat_of_formation_kcal_mol']}\n",
                f">  <selected_pm7_geometry>\n{str(conf_index == detail['lowest_pm7_heat_conformer_index_among_five_starts']).lower()}\n",
            ]
            charge_lines = []
            charges = FORMAL_CHARGE_RECORDS.get(sid, [])
            if charges:
                charge_lines.append("M  CHG" + f"{len(charges):3d}" + "".join(f"{idx:4d}{charge:4d}" for idx, charge in charges))
            records.append("\n".join([f"{sid} | MOPAC PM7 conformer {conf_index}", "     MOPAC PM7      3D", "", counts_line, *out_atoms, *bond_lines, *charge_lines, "M  END", *props, "$$$$", ""]))
            conf_meta.append({
                "conformer_index": conf_index,
                "arc_source": str(arc.relative_to(ROOT)),
                "arc_sha256": digest(arc),
                "heat_of_formation_kcal_mol": result["heat_of_formation_kcal_mol"],
                "selected_lowest_pm7_heat_among_five": conf_index == detail["lowest_pm7_heat_conformer_index_among_five_starts"],
            })
        out_sdf = inputs / f"{sid}-mopac-pm7-conformers.sdf"
        out_sdf.write_text("".join(records), encoding="utf-8", newline="\n")
        files.append({"species_id": sid, "source_selected_sdf": str(base.relative_to(ROOT)), "source_selected_sdf_sha256": digest(base), "multi_conformer_sdf": str(out_sdf.relative_to(ROOT)), "sha256": digest(out_sdf), "atom_count": n_atoms, "bond_count": n_bonds, "conformers": conf_meta})
        for i, element in enumerate(elements, 1):
            mapped = next((x for x in atom_maps if x["species_id"] == sid and int(x["atom_number_1based"]) == i), None)
            crosswalk.append({
                "species_id": sid,
                "sdf_atom_serial_1based": i,
                "element": element,
                "atom_map_number": int(mapped["atom_map_number"]) if mapped else 0,
                "input_atom_index_0based": int(mapped["atom_index_rdkit_0based"]) if mapped else None,
                "numbering_note": "Heavy-atom map numbers follow preparation atom-numbers.csv; added hydrogens have map 0 and retain SDF serials.",
            })

    with (OUT / "atom-serial-crosswalk.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(crosswalk[0]))
        w.writeheader()
        w.writerows(crosswalk)
    (OUT / "prepared-input-manifest.json").write_text(json.dumps({
        "status": "prepared_for_manual_DS_Visualizer_import_only",
        "created_by": "prepare_visualizer_inputs.py",
        "created_utc": "2026-11-01",
        "source_run": "benzocaine-live-20261031-04",
        "geometry_provenance": "Existing converged PM7 optimized MOPAC .arc final geometries; no new calculation.",
        "mopac_version": summary["mopac_version"],
        "method": summary["method"],
        "conversion": "MOPAC .arc final coordinates copied into the atom/bond graph from the corresponding selected MOPAC SDF. Formal charges from the source SMILES are written as M  CHG records for the nitro group because the source SDF omitted its formal N+/O- charge annotations. No geometry edits or measurements.",
        "structures": files,
        "limitations": ["This package is not a Discovery Studio result.", "No Visualizer screen was opened or captured.", "No GUI distance/angle measurements or accessibility observations have been made.", "Independent molecules are not arranged as a reaction complex."],
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Prepared {len(files)} multi-conformer SDF inputs and atom crosswalk in {OUT}")


if __name__ == "__main__":
    main()
