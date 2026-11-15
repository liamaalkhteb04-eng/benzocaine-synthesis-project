"""Prepare conformers and optional, explicitly reviewed MOPAC inputs from any actual route run.

No MOPAC, EPI Suite, Visualizer, or AI inference is executed here.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def safe_slug(text):
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return text[:36] or "compound"


def write_mopac(path, mol, conformer_id, title, state):
    conf = mol.GetConformer(conformer_id)
    lines = [state["keywords"], title, "Prepared geometry only; MOPAC not run"]
    for atom in mol.GetAtoms():
        p = conf.GetAtomPosition(atom.GetIdx())
        lines.append(f"{atom.GetSymbol():<3} {p.x: .8f} 1 {p.y: .8f} 1 {p.z: .8f} 1")
    path.write_text("\n".join(lines)+"\n", encoding="ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path,
                        help="prediction run containing input.json and report-evidence.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT/"analyses"/"preparation")
    parser.add_argument("--conformers", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20261104)
    parser.add_argument("--mopac-state-map", type=Path,
                        help="optional JSON mapping canonical SMILES to reviewed MOPAC keywords")
    args = parser.parse_args()
    run = args.run_dir.resolve()
    evidence_path = run/"report-evidence.json"
    if not evidence_path.is_file():
        raise FileNotFoundError("Build and validate actual report-evidence.json first")
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    target = json.loads((run/"input.json").read_text(encoding="utf-8"))
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise FileExistsError(f"Output folder is non-empty; choose a new folder: {args.output_dir}")
    out = args.output_dir.resolve()
    (out/"structures").mkdir(parents=True, exist_ok=True)
    (out/"mopac-inputs").mkdir(exist_ok=True)
    state_map = json.loads(args.mopac_state_map.read_text(encoding="utf-8")) if args.mopac_state_map else {}

    target_mol = Chem.MolFromSmiles(target["smiles"])
    if target_mol is None:
        raise ValueError("Target SMILES is invalid")
    target_canonical = Chem.MolToSmiles(target_mol, canonical=True)
    selected_routes = set(evidence.get("selected_route_ids", []))
    steps = [s for s in evidence.get("steps", []) if s["route_id"] in selected_routes]
    structures = {}
    def add(smiles, route_ref, role):
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid participant SMILES in {route_ref}")
        canonical = Chem.MolToSmiles(mol, canonical=True)
        rec = structures.setdefault(canonical, {"smiles": canonical, "routes": set(), "roles": set()})
        rec["routes"].add(route_ref); rec["roles"].add(role)
    add(target["smiles"], "target", "target")
    for step in steps:
        ref = f"{step['route_id']}/{step['step_id']}"
        for smiles in step["precursor_smiles"]: add(smiles, ref, "precursor")
        add(step["product_smiles"], ref, "product")
    labels = {target_canonical: {"name": target.get("name", target.get("target_id", "target")),
                                "name_ko": target.get("name_ko", "")}}
    labels_path = run/"molecule-labels.json"
    if labels_path.is_file(): labels.update(json.loads(labels_path.read_text(encoding="utf-8")))

    manifest = {"status":"preparation_only_not_calculated", "source_run":str(run),
        "source_evidence_sha256":sha(evidence_path), "random_seed":args.seed,
        "conformers_per_species":args.conformers,
        "mopac":{"input_decks_written":0,"mopac_invoked":False,
                 "state_policy":"No default charge or multiplicity is assumed. A reviewed --mopac-state-map is required to write executable input decks."},
        "species":[]}
    atom_rows=[]; epi_rows=[]
    for canonical, record in structures.items():
        mol = Chem.AddHs(Chem.MolFromSmiles(canonical))
        formula = rdMolDescriptors.CalcMolFormula(mol)
        name = labels.get(canonical, {}).get("name", "")
        species_id = safe_slug(name or formula) + "-" + hashlib.sha256(canonical.encode()).hexdigest()[:8]
        formal_charge = Chem.GetFormalCharge(Chem.MolFromSmiles(canonical))
        radicals = sum(a.GetNumRadicalElectrons() for a in Chem.MolFromSmiles(canonical).GetAtoms())
        params = AllChem.ETKDGv3(); params.randomSeed=args.seed; params.numThreads=1
        conformer_ids = list(AllChem.EmbedMultipleConfs(mol, numConfs=args.conformers, params=params))
        if len(conformer_ids) != args.conformers:
            raise RuntimeError(f"Conformer generation incomplete for {species_id}")
        props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant="MMFF94s")
        if props is None: raise RuntimeError(f"MMFF94s parameters unavailable for {species_id}")
        energies=[]
        for conf_id in conformer_ids:
            ff=AllChem.MMFFGetMoleculeForceField(mol, props, confId=conf_id)
            ff.Minimize(maxIts=500); energies.append((float(ff.CalcEnergy()), conf_id))
        for atom in mol.GetAtoms():
            atom.SetAtomMapNum(atom.GetIdx()+1 if atom.GetAtomicNum()>1 else 0)
        sdf=out/"structures"/(species_id+".sdf")
        writer=Chem.SDWriter(str(sdf))
        for rank, conf_id in enumerate(conformer_ids,1):
            mol.SetProp("species_id", species_id); mol.SetProp("conformer_index", str(rank))
            mol.SetProp("geometry_status", "RDKit starting conformer; not experimental or QM optimized")
            writer.write(mol, confId=conf_id)
        writer.close()
        state = state_map.get(canonical)
        mop_path=None
        if state:
            if not state.get("keywords") or "CHARGE=" not in state["keywords"]:
                raise ValueError(f"Reviewed MOPAC keywords with explicit CHARGE are required: {species_id}")
            best_conf=min(energies)[1]
            mop=out/"mopac-inputs"/(species_id+".mop")
            write_mopac(mop,mol,best_conf,name or species_id,state)
            mop_path=str(mop.relative_to(out)); manifest["mopac"]["input_decks_written"]+=1
        for atom in mol.GetAtoms():
            if atom.GetAtomicNum()==1: continue
            atom_rows.append({"species_id":species_id,"atom_index_rdkit_0based":atom.GetIdx(),
                "atom_number_1based":atom.GetIdx()+1,"atom_map_number":atom.GetAtomMapNum(),"element":atom.GetSymbol()})
        item={"id":species_id,"name":name or species_id,"name_ko":labels.get(canonical,{}).get("name_ko",""),
            "smiles":canonical,"formula":formula,"formal_charge":formal_charge,"radical_electrons":radicals,
            "routes":sorted(record["routes"]),"roles":sorted(record["roles"]),
            "conformers_written":len(conformer_ids),"lowest_mmff94s_conformer_index":conformer_ids.index(min(energies)[1])+1,
            "sdf_file":str(sdf.relative_to(out)),"sdf_sha256":sha(sdf),
            "mopac_keywords":state.get("keywords") if state else None,
            "mopac_input":mop_path,"mopac_input_status":"prepared_not_run" if mop_path else "not_written_state_not_supplied"}
        manifest["species"].append(item)
        epi_rows.append({"species_id":species_id,"name":item["name"],"smiles":canonical,
            "formal_charge":formal_charge,"chemical_form":target.get("chemical_form", "review structure-specific form"),
            "route_context":";".join(sorted(record["routes"])),"source":"selected actual route participant","EPI_Suite_execution":"not_run"})

    for step in steps:
        for pred in (step.get("conditions") or {}).get("candidates",[])[:1]:
            for slot in ("catalyst1","solvent1","solvent2","reagent1","reagent2"):
                token=pred.get(slot)
                if token:
                    epi_rows.append({"species_id":"condition-"+hashlib.sha256(token.encode()).hexdigest()[:10],
                        "name":slot+" model token","smiles":token,"chemical_form":"exact model output token; speciation not inferred",
                        "route_context":step["route_id"]+"/"+step["step_id"],"source":"Parrot rank-1 candidate",
                        "EPI_Suite_execution":"not_run; validate model support first"})
    for filename, rows in [("atom-numbers.csv",atom_rows),("epi-suite-inputs.csv",epi_rows)]:
        with (out/filename).open("w",newline="",encoding="utf-8-sig") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    manifest["species_count"]=len(manifest["species"])
    manifest["atom_numbering_csv"]="atom-numbers.csv"
    manifest["epi_suite_smiles_input_table"]="epi-suite-inputs.csv"
    manifest["discovery_studio_visualizer"]={"prepared":True,"structure_files":[s["sdf_file"] for s in manifest["species"]],
        "GUI_opened":False,"measurements_performed":False,"note":"Preparing files alone is not a Visualizer observation."}
    (out/"structure-preparation.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":manifest["status"],"species":len(manifest["species"]),
        "mopac_input_decks":manifest["mopac"]["input_decks_written"],"mopac_invoked":False},ensure_ascii=False))

if __name__=="__main__": main()
