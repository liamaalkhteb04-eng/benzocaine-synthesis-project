"""Render only reaction structures obtained from an actual route prediction."""
import argparse
from pathlib import Path
from _runtime import load, save, digest


def main():
    from rdkit import Chem, rdBase
    from rdkit.Chem import Draw, rdChemReactions
    from PIL import Image, ImageDraw, ImageFont
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    payload = load(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    records = []
    if payload.get("status") == "success":
        for route in payload.get("predictions", []):
            for step in route.get("steps", []):
                label = f"{route['route_id']}-{step['step_id']}"
                record = {"route_id": route["route_id"], "step_id": step["step_id"],
                          "reaction_smiles": step["reaction_smiles"]}
                try:
                    reaction = rdChemReactions.ReactionFromSmarts(step["reaction_smiles"], useSmiles=True)
                    if reaction is None:
                        raise ValueError("Invalid predicted reaction SMILES")
                    path = args.output_dir / (label + ".png")
                    molecules = [Chem.MolFromSmiles(s) for s in step["precursor_smiles"] + [step["product_smiles"]]]
                    if any(mol is None for mol in molecules):
                        raise ValueError("Invalid molecule in predicted step")
                    # Draw native molecular panels separately; reserve empty columns for symbols.
                    picture = Image.new("RGB", (len(molecules) * 500 + (len(molecules)-1) * 100, 450), "white")
                    canvas = ImageDraw.Draw(picture)
                    try:
                        font = ImageFont.truetype("arial.ttf", 24)
                    except OSError:
                        font = ImageFont.load_default()
                    for i, mol in enumerate(molecules):
                        x = i * 600
                        picture.paste(Draw.MolToImage(mol, size=(500, 380)), (x, 0))
                        text = "Product" if i == len(molecules)-1 else f"Reactant {i+1}"
                        canvas.text((x+250, 405), text, fill="black", font=font, anchor="mm")
                        if i:
                            center = x-50
                            if i == len(molecules)-1:
                                canvas.line((center-35, 190, center+30, 190), fill="black", width=3)
                                canvas.polygon([(center+35,190),(center+21,182),(center+21,198)], fill="black")
                            else:
                                canvas.line((center-12,190,center+12,190), fill="black", width=3)
                                canvas.line((center,178,center,202), fill="black", width=3)
                    picture.save(path)
                    record.update(status="success", image_path=str(path.resolve()), sha256=digest(path))
                    for i, mol in enumerate(molecules):
                        if mol:
                            Draw.MolToFile(mol, str(args.output_dir / f"{label}-molecule-{i+1}.png"), size=(600, 450))
                except Exception as exc:
                    record.update(status="failed", reason=f"{type(exc).__name__}: {exc}")
                records.append(record)
    save(args.output_dir / "manifest.json", {
        "rdkit_version": rdBase.rdkitVersion,
        "source_routes_sha256": digest(args.input),
        "note": "Forward depictions of actual retrosynthetic edges; no missing agents added.",
        "figures": records,
    })
    print(f"Rendered {sum(r['status']=='success' for r in records)} actual predicted reaction figures")


if __name__ == "__main__":
    main()
