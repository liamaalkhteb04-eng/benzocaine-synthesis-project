"""Validate target identity locally with RDKit; never queries PubChem or another service."""
import argparse
from pathlib import Path
import sys

from _runtime import digest, load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--compare", type=Path,
                        help="Optional prepared run input that must describe the same target")
    args = parser.parse_args()

    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors

    target = load(args.input)
    required = ("target_id", "name", "smiles", "expected_formula", "chemical_form")
    missing = [key for key in required if not target.get(key)]
    if missing:
        raise ValueError("Missing required target fields: " + ", ".join(missing))
    molecule = Chem.MolFromSmiles(target["smiles"])
    if molecule is None:
        raise ValueError("RDKit could not parse the supplied SMILES")
    formula = rdMolDescriptors.CalcMolFormula(molecule)
    if formula != target["expected_formula"]:
        raise ValueError(f"Formula mismatch: supplied={target['expected_formula']} RDKit={formula}")

    result = {
        "status": "passed",
        "scope": "Local JSON/schema, SMILES and formula validation only; no network, model, or Solar calls.",
        "target_id": target["target_id"],
        "name": target["name"],
        "canonical_smiles": Chem.MolToSmiles(molecule, canonical=True),
        "formula": formula,
        "formal_charge": Chem.GetFormalCharge(molecule),
        "input_sha256": digest(args.input),
        "network_requests": 0,
        "model_calls": 0,
    }
    if args.compare:
        prepared = load(args.compare)
        prepared_molecule = Chem.MolFromSmiles(prepared["smiles"])
        if prepared_molecule is None:
            raise ValueError("Prepared run has invalid SMILES")
        same = (Chem.MolToSmiles(prepared_molecule, canonical=True) == result["canonical_smiles"]
                and prepared.get("expected_formula", prepared.get("formula")) == formula
                and prepared.get("chemical_form") == target.get("chemical_form"))
        result["prepared_run_comparison"] = {
            "status": "matched" if same else "mismatch",
            "prepared_input_sha256": digest(args.compare),
        }
        if not same:
            raise ValueError("Input target does not match the prepared evidence target")

    save(args.output, result)
    print("passed; network_requests=0; model_calls=0")


if __name__ == "__main__":
    main()
