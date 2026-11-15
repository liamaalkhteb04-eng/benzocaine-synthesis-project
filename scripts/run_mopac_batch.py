"""Run PM7 conformer optimizations using the project-local MOPAC portable archive."""
import hashlib
import json
import os
import re
import subprocess
import argparse
import time
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

ROOT = Path(__file__).resolve().parents[1]
PREP = ROOT / "analyses" / "preparation"
OUT = ROOT / "analyses" / "mopac"
MOPAC = ROOT / "tools" / "mopac-23.2.5-win" / "bin" / "mopac.exe"
ZIP = ROOT / "tools" / "downloads" / "mopac-23.2.5-win.zip"
TIMEOUT_SECONDS = 180


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_mop(path, mol, conf_id, title, keywords):
    conf = mol.GetConformer(conf_id)
    lines = [keywords, title, "RDKit ETKDGv3/MMFF94s starting conformer; PM7 optimization requested"]
    for atom in mol.GetAtoms():
        pos = conf.GetAtomPosition(atom.GetIdx())
        lines.append(f"{atom.GetSymbol():<3} {pos.x: .8f} 1 {pos.y: .8f} 1 {pos.z: .8f} 1")
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="target JSON used for structure identity validation")
    parser.add_argument("--preparation-dir", required=True, type=Path, help="output from prepare_additional_structures.py")
    parser.add_argument("--output-dir", required=True, type=Path, help="new, target-specific MOPAC output folder")
    parser.add_argument("--mopac-executable", type=Path, default=Path(os.environ.get("MOPAC_EXECUTABLE", str(MOPAC))) )
    parser.add_argument("--mopac-archive", type=Path, default=Path(os.environ.get("MOPAC_ARCHIVE", str(ZIP))) )
    args=parser.parse_args()
    mopac=args.mopac_executable.resolve(); archive=args.mopac_archive.resolve()
    prep_dir=args.preparation_dir.resolve(); output_dir=args.output_dir.resolve(); input_path=args.input.resolve()
    running_dir=output_dir
    if not mopac.is_file():
        raise FileNotFoundError(f"MOPAC executable not found: {mopac}")
    if not archive.is_file():
        raise FileNotFoundError(f"Official MOPAC archive not found: {archive}")
    if running_dir.exists() and any(running_dir.iterdir()):
        raise FileExistsError(f"Output folder is non-empty: {running_dir}")
    running_dir.mkdir(parents=True, exist_ok=True)
    version = subprocess.run([str(mopac), "--version"], cwd=mopac.parent,
                             capture_output=True, text=True, timeout=30, check=True)
    version_text = (version.stdout + version.stderr).strip()
    if "23.2.5" not in version_text:
        raise RuntimeError(f"Unexpected MOPAC version output: {version_text}")

    prep = json.loads((prep_dir / "structure-preparation.json").read_text(encoding="utf-8"))
    target = json.loads(input_path.read_text(encoding="utf-8"))
    running_path = running_dir / "run-manifest.json"
    prior = json.loads(running_path.read_text(encoding="utf-8")) if running_path.exists() else {}
    prior_by_key = {(j.get("species_id"), j.get("conformer_index")): j for j in prior.get("jobs", [])}
    rows = []
    for spec in prep["species"]:
        keywords=spec.get("mopac_keywords")
        if not keywords:
            raise ValueError(f"No reviewed MOPAC state in preparation manifest for {spec['id']}; prepare with --mopac-state-map")
        sdf_path = prep_dir / spec["sdf_file"]
        mols = list(Chem.SDMolSupplier(str(sdf_path), removeHs=False))
        if len(mols) != prep["conformers_per_species"] or any(m is None for m in mols):
            raise ValueError(f"Invalid or incomplete SDF conformer ensemble: {sdf_path}")
        base = Chem.RemoveHs(Chem.Mol(mols[0]))
        formula = rdMolDescriptors.CalcMolFormula(base)
        formal_charge = sum(a.GetFormalCharge() for a in base.GetAtoms())
        radical_electrons = sum(a.GetNumRadicalElectrons() for a in base.GetAtoms())
        # Include implicit valence hydrogens when checking parity. The MOPAC
        # geometry itself uses explicit hydrogens from the SDF.
        atom_numbers = sum(a.GetAtomicNum() for a in mols[0].GetAtoms())
        total_electrons = atom_numbers - formal_charge
        charge_match=re.search(r"(?:^|\s)CHARGE=([+-]?\d+)(?:\s|$)",keywords,re.I)
        spin_match=re.search(r"(?:^|\s)MS=([^\s]+)",keywords,re.I)
        if formula != spec["formula"] or not charge_match or int(charge_match.group(1)) != formal_charge or radical_electrons != 0:
            raise ValueError(f"Charge/formula/radical preflight failed for {spec['id']}")
        if total_electrons % 2:
            raise ValueError(f"Cannot use closed-shell singlet for odd-electron species {spec['id']}")
        if not spin_match or spin_match.group(1) != "0":
            raise ValueError(f"This runner is validated only for closed-shell singlets (MS=0): {spec['id']}")
        if Chem.MolToSmiles(base, canonical=True) == Chem.MolToSmiles(Chem.MolFromSmiles(target["smiles"]), canonical=True):
            for atom in base.GetAtoms():
                atom.SetAtomMapNum(0)
            if Chem.MolToSmiles(base, canonical=True) != target["smiles"]:
                raise ValueError("Target structure does not match the supplied input record")

        lowest_id = spec["lowest_mmff94s_conformer_index"] - 1
        energies = []
        for conformer_index, mol in enumerate(mols, start=1):
            job = running_dir / spec["id"] / f"conformer-{conformer_index:02d}"
            job.mkdir(parents=True, exist_ok=True)
            inp = job / f"{spec['id']}-conf-{conformer_index:02d}.mop"
            write_mop(inp, mol, 0, f"{spec['name']} conformer {conformer_index}; formal charge {formal_charge}; singlet", keywords)
            input_hash = sha(inp)
            old = prior_by_key.get((spec["id"], conformer_index))
            if (old and old.get("input_sha256") == input_hash and
                    old.get("status") == "output_candidate_normal" and old.get("out") and old.get("arc")):
                old_out, old_arc = Path(old["out"]), Path(old["arc"])
                if (old_out.is_file() and old_arc.is_file() and
                        old.get("out_sha256") == sha(old_out) and old.get("arc_sha256") == sha(old_arc)):
                    reused = dict(old)
                    reused["status"] = "reused_output_candidate_normal"
                    reused["reused_from_partial_attempt"] = True
                    rows.append(reused)
                    print(f"{spec['id']} conformer {conformer_index}: reused prior successful output", flush=True)
                    continue
            started = time.time()
            status = "failed"
            error = None
            stdout = stderr = ""
            returncode = None
            try:
                proc = subprocess.run([str(mopac), inp.name], cwd=job,
                                      capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
                stdout, stderr, returncode = proc.stdout, proc.stderr, proc.returncode
                status = "completed_process" if returncode == 0 else "failed_process"
            except subprocess.TimeoutExpired as exc:
                stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
                stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
                error = f"Timeout after {TIMEOUT_SECONDS} seconds"
                status = "timed_out"
            (job / "stdout.log").write_text(stdout, encoding="utf-8", errors="replace")
            (job / "stderr.log").write_text(stderr, encoding="utf-8", errors="replace")
            out_path = job / f"{spec['id']}-conf-{conformer_index:02d}.out"
            arc_path = job / f"{spec['id']}-conf-{conformer_index:02d}.arc"
            out_text = out_path.read_text(encoding="utf-8", errors="replace") if out_path.exists() else ""
            arc_exists = arc_path.exists()
            normal_markers = [
                bool(re.search(r"MOPAC DONE|JOB ENDED NORMALLY", out_text, re.I)),
                arc_exists,
                not bool(re.search(r"UNABLE TO ACHIEVE SELF-CONSISTENCY|ERROR", out_text, re.I)),
            ]
            if status == "completed_process" and all(normal_markers):
                status = "output_candidate_normal"
            rows.append({
                "species_id": spec["id"], "formula": formula, "formal_charge": formal_charge,
                "radical_electrons": radical_electrons, "total_electrons": total_electrons,
                "multiplicity": 1, "conformer_index": conformer_index,
                "is_lowest_mmff94s_start": conformer_index == lowest_id + 1,
                "input": str(inp.resolve()), "input_sha256": input_hash,
                "stdout": str((job / "stdout.log").resolve()),
                "stderr": str((job / "stderr.log").resolve()),
                "out": str(out_path.resolve()) if out_path.exists() else None,
                "out_sha256": sha(out_path) if out_path.exists() else None,
                "arc": str(arc_path.resolve()) if arc_exists else None,
                "arc_sha256": sha(arc_path) if arc_exists else None,
                "process_return_code": returncode, "status": status,
                "normal_output_markers": {"completion_text": normal_markers[0], "arc_present": arc_exists,
                                           "no_obvious_error_text": normal_markers[2]},
                "error": error, "elapsed_seconds": round(time.time() - started, 3),
            })
            (running_dir / "run-manifest.json").write_text(json.dumps({
                "status": "running", "mopac_version": version_text,
                "mopac_executable": str(mopac), "mopac_executable_sha256": sha(mopac),
                "official_archive": str(archive), "official_archive_sha256": sha(archive),
                "source_preparation_manifest_sha256": sha(prep_dir / "structure-preparation.json"),
                "keywords_by_species": {s["id"]:s.get("mopac_keywords") for s in prep["species"]}, "timeout_seconds_per_job": TIMEOUT_SECONDS,
                "jobs_completed_or_attempted": len(rows), "jobs": rows,
            }, indent=2) + "\n", encoding="utf-8")
            print(f"{spec['id']} conformer {conformer_index}: {status}", flush=True)

    manifest = {
        "status": "complete_with_failures" if any(r["status"] not in ("output_candidate_normal", "reused_output_candidate_normal") for r in rows) else "all_outputs_candidate_normal",
        "mopac_version": version_text,
        "mopac_executable": str(mopac), "mopac_executable_sha256": sha(mopac),
        "official_archive": str(archive), "official_archive_sha256": sha(archive),
        "source_preparation_manifest_sha256": sha(prep_dir / "structure-preparation.json"),
        "keywords_by_species": {s["id"]:s.get("mopac_keywords") for s in prep["species"]}, "method": "PM7 gas-phase isolated-molecule geometry optimization",
        "geometry_optimization": "enabled; all Cartesian coordinates optimized",
        "charge_spin_review": "Each formal charge is matched to the explicitly reviewed CHARGE keyword; only closed-shell MS=0 singlets with even electron count are supported by this runner.",
        "selection": "Five ETKDGv3 conformers per molecule, each MMFF94s-minimized; conformer index with lowest MMFF94s starting energy is designated primary. All five starts were run to expose local-minimum sensitivity.",
        "limitations": [
            "No solvent or temperature model; isolated-molecule gas-phase calculations only.",
            "No catalyst, hydrogen, counterions, products/byproducts, or transition state included.",
            "Convergence of local minima does not establish reaction feasibility, mechanism, rate, or yield.",
            "Only compare heats of formation among conformers of the same molecular formula, charge, spin, and method; do not rank unlike species by total energy.",
        ],
        "jobs_count": len(rows), "jobs": rows,
    }
    (running_dir / "run-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Finished {len(rows)} jobs; manifest status: {manifest['status']}", flush=True)


if __name__ == "__main__":
    main()
