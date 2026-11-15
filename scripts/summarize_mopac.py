"""Extract summaries and optimized structures from saved MOPAC .out/.arc files."""
import csv
import json
import math
import re
from pathlib import Path

from rdkit import Chem
from rdkit.Geometry import Point3D

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analyses" / "mopac"
PREP = ROOT / "analyses" / "preparation"
STRUCTURES = OUT / "optimized-structures"
FLOAT = r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[EeDd][-+]?\d+)?"


def number(value):
    return float(value.replace("D", "E").replace("d", "e"))


def parse_out(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    heat = re.search(r"FINAL HEAT OF FORMATION\s*=\s*(" + FLOAT + r")\s+KCAL/MOL", text)
    grad = re.search(r"GRADIENT NORM\s*=\s*(" + FLOAT + r")\s*=\s*(" + FLOAT + r")\s+PER ATOM", text)
    dipole = re.search(r"^\s*SUM\s+(" + FLOAT + r")\s+(" + FLOAT + r")\s+(" + FLOAT + r")\s+(" + FLOAT + r")\s*$", text, re.M)
    charge_start = text.find("NET ATOMIC CHARGES AND DIPOLE CONTRIBUTIONS")
    charges = []
    if charge_start >= 0:
        heading = "NET ATOMIC CHARGES AND DIPOLE CONTRIBUTIONS"
        tail = text[charge_start + len(heading):].split("\n DIPOLE", 1)[0]
        for line in tail.splitlines():
            match = re.match(r"\s*(\d+)\s+([A-Z][a-z]?)\s+(" + FLOAT + r")", line)
            if match:
                charges.append({"atom_number_1based": int(match.group(1)), "element": match.group(2),
                                "net_atomic_charge_e": number(match.group(3))})
    normal = "* JOB ENDED NORMALLY *" in text and "== MOPAC DONE ==" in text
    scf = "SCF FIELD WAS ACHIEVED" in text
    rhf = "RHF CALCULATION, NO. OF DOUBLY OCCUPIED LEVELS" in text
    return {
        "heat_of_formation_kcal_mol": number(heat.group(1)) if heat else None,
        "gradient_norm_kcal_mol_angstrom": number(grad.group(1)) if grad else None,
        "gradient_norm_per_atom": number(grad.group(2)) if grad else None,
        "dipole_x_debye": number(dipole.group(1)) if dipole else None,
        "dipole_y_debye": number(dipole.group(2)) if dipole else None,
        "dipole_z_debye": number(dipole.group(3)) if dipole else None,
        "dipole_magnitude_debye": number(dipole.group(4)) if dipole else None,
        "net_atomic_charges": charges,
        "net_atomic_charge_sum_e": sum(q["net_atomic_charge_e"] for q in charges) if charges else None,
        "normal_end_markers": normal,
        "scf_field_achieved": scf,
        "closed_shell_rhf_reported": rhf,
        "output_text": text,
    }


def parse_arc_coordinates(path, symbols):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    start = next(i for i, line in enumerate(lines) if "FINAL GEOMETRY OBTAINED" in line)
    coords = []
    for line in lines[start + 1:]:
        tokens = line.split()
        if not tokens or tokens[0] not in {"H", "C", "N", "O", "F", "S", "P", "Cl", "Br", "I", "B"}:
            if coords:
                break
            continue
        if len(tokens) < 7:
            if coords:
                break
            continue
        try:
            row = (tokens[0], number(tokens[1]), number(tokens[3]), number(tokens[5]))
        except (ValueError, IndexError):
            if coords:
                break
            continue
        coords.append(row)
        if len(coords) == len(symbols):
            break
    if len(coords) != len(symbols):
        raise ValueError(f"Expected {len(symbols)} optimized coordinates in {path}, found {len(coords)}")
    if [x[0] for x in coords] != symbols:
        raise ValueError(f"MOPAC optimized atom order does not match input atoms in {path}")
    return [(x[1], x[2], x[3]) for x in coords]


def main():
    manifest_path = OUT / "run-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    prep = json.loads((PREP / "structure-preparation.json").read_text(encoding="utf-8"))
    STRUCTURES.mkdir(parents=True, exist_ok=True)
    by_species = {}
    all_charge_rows = []
    all_bond_rows = []
    for spec in prep["species"]:
        sdf_path = ROOT / spec["sdf_file"]
        mols = list(Chem.SDMolSupplier(str(sdf_path), removeHs=False))
        symbols = [a.GetSymbol() for a in mols[0].GetAtoms()]
        atom_map = {a.GetIdx() + 1: a.GetAtomMapNum() for a in mols[0].GetAtoms() if a.GetAtomicNum() > 1}
        species_jobs = [j for j in manifest["jobs"] if j["species_id"] == spec["id"]]
        if len(species_jobs) != 5:
            raise ValueError(f"Expected five completed MOPAC starts for {spec['id']}")
        parsed = []
        optimized_mols = []
        for job in species_jobs:
            out_path, arc_path = ROOT / job["out"], ROOT / job["arc"]
            result = parse_out(out_path)
            coords = parse_arc_coordinates(arc_path, symbols)
            gradient = result["gradient_norm_kcal_mol_angstrom"]
            converged = bool(job["status"] in ("output_candidate_normal", "reused_output_candidate_normal") and
                             result["normal_end_markers"] and result["scf_field_achieved"] and
                             result["closed_shell_rhf_reported"] and result["net_atomic_charge_sum_e"] is not None and
                             abs(result["net_atomic_charge_sum_e"]) < 0.001 and
                             gradient is not None and gradient <= 0.5 + 1e-6)
            item = {k: v for k, v in result.items() if k not in ("net_atomic_charges", "output_text")}
            item.update({"conformer_index": job["conformer_index"], "is_lowest_mmff94s_start": job["is_lowest_mmff94s_start"],
                         "converged_by_recorded_criteria": converged, "input": job["input"], "out": job["out"], "arc": job["arc"],
                         "elapsed_seconds": job["elapsed_seconds"]})
            parsed.append(item)
            for q in result["net_atomic_charges"]:
                all_charge_rows.append({"species_id": spec["id"], "conformer_index": job["conformer_index"],
                                        "is_selected_lowest_pm7_heat_start": False, **q})
            newmol = Chem.Mol(mols[job["conformer_index"] - 1])
            conf = newmol.GetConformer()
            for i, xyz in enumerate(coords):
                conf.SetAtomPosition(i, Point3D(*xyz))
            for key, value in {"species_id": spec["id"], "conformer_index": str(job["conformer_index"]),
                               "method": "MOPAC 23.2.5 PM7", "geometry_status": "optimized; see raw .out and .arc",
                               "converged": str(converged).lower()}.items():
                newmol.SetProp(key, value)
            optimized_mols.append((job["conformer_index"], newmol, result, item))

        good = [x for x in optimized_mols if x[3]["converged_by_recorded_criteria"] and x[2]["heat_of_formation_kcal_mol"] is not None]
        selected = min(good, key=lambda x: x[2]["heat_of_formation_kcal_mol"]) if good else None
        for row in all_charge_rows:
            if row["species_id"] == spec["id"] and selected and row["conformer_index"] == selected[0]:
                row["is_selected_lowest_pm7_heat_start"] = True
        if selected:
            one = Chem.SDWriter(str(STRUCTURES / f"{spec['id']}-pm7-optimized.sdf"))
            one.write(selected[1]); one.close()
            bestmol = selected[1]
            conf = bestmol.GetConformer()
            for bond in bestmol.GetBonds():
                i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
                a, b = conf.GetAtomPosition(i), conf.GetAtomPosition(j)
                distance = math.dist((a.x, a.y, a.z), (b.x, b.y, b.z))
                all_bond_rows.append({"species_id": spec["id"], "formula": spec["formula"],
                                      "selected_conformer_index": selected[0], "atom_i_1based": i + 1,
                                      "atom_i_map_number": atom_map.get(i + 1), "element_i": bestmol.GetAtomWithIdx(i).GetSymbol(),
                                      "atom_j_1based": j + 1, "atom_j_map_number": atom_map.get(j + 1),
                                      "element_j": bestmol.GetAtomWithIdx(j).GetSymbol(),
                                      "bond_type": str(bond.GetBondType()), "bond_length_angstrom": distance})
        heats = [x[2]["heat_of_formation_kcal_mol"] for x in good]
        by_species[spec["id"]] = {
            "name": spec["name"], "formula": spec["formula"], "formal_charge": 0, "multiplicity": 1,
            "jobs_total": len(parsed), "jobs_converged": len(good),
            "starting_conformer_selection": {"primary_conformer_index": spec["lowest_mmff94s_conformer_index"],
                                              "rationale": "Lowest MMFF94s energy among five RDKit ETKDGv3/MMFF94s-minimized starting conformers."},
            "pm7_conformer_heats_of_formation_kcal_mol": [x[2]["heat_of_formation_kcal_mol"] for x in optimized_mols],
            "within_same_formula_conformer_heat_range_kcal_mol": max(heats) - min(heats) if len(heats) > 1 else (0.0 if heats else None),
            "lowest_pm7_heat_conformer_index_among_five_starts": selected[0] if selected else None,
            "selected_heat_of_formation_kcal_mol": selected[2]["heat_of_formation_kcal_mol"] if selected else None,
            "selected_gradient_norm_kcal_mol_angstrom": selected[2]["gradient_norm_kcal_mol_angstrom"] if selected else None,
            "selected_gradient_norm_per_atom": selected[2]["gradient_norm_per_atom"] if selected else None,
            "selected_dipole_magnitude_debye": selected[2]["dipole_magnitude_debye"] if selected else None,
            "selected_optimized_structure": str((STRUCTURES / f"{spec['id']}-pm7-optimized.sdf").relative_to(ROOT)) if selected else None,
            "all_conformer_results": parsed,
        }

    summary = {
        "status": "summarized",
        "mopac_version": manifest["mopac_version"], "method": manifest["method"], "keywords": manifest["keywords"],
        "calculation_environment": "isolated molecule in gas phase; no implicit solvent keyword used",
        "interpretation_limits": manifest["limitations"],
        "charge_method": "MOPAC output NET ATOMIC CHARGES; population-derived model charges, not observables",
        "energy_comparison_rule": "Compare conformer heat of formation only within same formula, charge, spin, method, and conditions; no cross-formula energy ranking.",
        "species": by_species,
    }
    (OUT / "analysis-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    review = {
        "status": "passed_for_selected_neutral_species",
        "source_structures": str((PREP / "structure-preparation.json").relative_to(ROOT)),
        "source_structures_sha256": __import__("hashlib").sha256((PREP / "structure-preparation.json").read_bytes()).hexdigest(),
        "electronic_settings": {"formal_charge": 0, "spin_multiplicity": 1, "mopac_keyword": "CHARGE=0 MS=0",
                                "method": "PM7", "solvent": "none; gas phase", "coordinate_mode": "all Cartesian coordinates optimized"},
        "review_basis": "RDKit molecular valence, formula, net formal charge, radical electron count, total electron parity, target identity; MOPAC output RHF closed-shell marker, net atomic charge sum, and normal termination.",
        "species": {sid: {
            "name": s["name"], "formula": s["formula"], "formal_charge": s["formal_charge"],
            "radical_electrons": next(j["radical_electrons"] for j in manifest["jobs"] if j["species_id"] == sid),
            "total_electrons": next(j["total_electrons"] for j in manifest["jobs"] if j["species_id"] == sid),
            "multiplicity": s["multiplicity"], "jobs_total": s["jobs_total"],
            "jobs_converged": s["jobs_converged"],
            "charge_spin_consistent": (s["jobs_converged"] == 5 and
                                        next(j["radical_electrons"] for j in manifest["jobs"] if j["species_id"] == sid) == 0 and
                                        next(j["total_electrons"] for j in manifest["jobs"] if j["species_id"] == sid) % 2 == 0),
        } for sid, s in by_species.items()},
        "preflight_script_corrections": manifest.get("execution_notes", []),
        "tool_installation": {"mopac_version": manifest["mopac_version"], "executable": manifest["mopac_executable"],
                              "archive": manifest["official_archive"], "archive_sha256": manifest["official_archive_sha256"]},
    }
    (ROOT / "validation" / "mopac-input-review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
    with (OUT / "net-atomic-charges.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(all_charge_rows[0])); w.writeheader(); w.writerows(all_charge_rows)
    with (OUT / "optimized-bond-lengths.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(all_bond_rows[0])); w.writeheader(); w.writerows(all_bond_rows)
    print("Species convergence:", ", ".join(f"{k} {v['jobs_converged']}/{v['jobs_total']}" for k, v in by_species.items()))
    print("Summary and optimized SDF files saved under", OUT)


if __name__ == "__main__":
    main()
