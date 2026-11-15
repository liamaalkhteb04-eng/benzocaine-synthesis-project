"""Validate target SMILES and render a structure. Route drawing is future work."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        from rdkit import Chem
        from rdkit.Chem import Draw, rdMolDescriptors
    except ImportError:
        parser.exit(2, "RDKit is missing. Install requirements-visuals.txt in a dedicated environment.\n")
    payload = json.loads(args.input.read_text(encoding="utf-8-sig"))
    molecule = Chem.MolFromSmiles(payload["smiles"])
    if molecule is None:
        parser.error("Invalid target SMILES")
    formula = rdMolDescriptors.CalcMolFormula(molecule)
    if payload.get("expected_formula") and formula != payload["expected_formula"]:
        parser.error(f"Formula mismatch: {formula}")
    # mkdir without exist_ok prevents accidental overwrite of an earlier drawing run.
    args.output_dir.mkdir(parents=True)
    Draw.MolToFile(molecule, str(args.output_dir / "target.png"), size=(1000, 700))
    metadata = {
        "name": payload["name"],
        "canonical_smiles": Chem.MolToSmiles(molecule),
        "formula": formula,
        "source": "RDKit input validation; not a synthesis prediction",
    }
    (args.output_dir / "target.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Structure and validation metadata saved to {args.output_dir}")


if __name__ == "__main__":
    main()
