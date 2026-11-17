"""Verify Parrot slot preservation from worker output through report prose."""
import argparse
import json
import re
from pathlib import Path

SLOTS = ("catalyst1", "solvent1", "solvent2", "reagent1", "reagent2")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def rows(path):
    obj = load(path)
    return obj.get("predictions", [])


def verify_adapter_contract(adapter_path, parrot_source=None):
    errors = []
    adapter = Path(adapter_path).read_text(encoding="utf-8")
    compact = re.sub(r"\s+", "", adapter)
    expected = '"catalyst1":agents[0],"solvent1":agents[1],"solvent2":agents[2],"reagent1":agents[3],"reagent2":agents[4]'
    if expected not in compact:
        errors.append("adapter field/index order does not match the five-slot contract")
    details = {"adapter_path": str(Path(adapter_path).resolve()), "adapter_order_verified": expected in compact}
    if parrot_source:
        source = Path(parrot_source)
        utils = re.sub(r"\s+", "", (source / "models" / "utils.py").read_text(encoding="utf-8"))
        model = re.sub(r"\s+", "", (source / "models" / "parrot_model.py").read_text(encoding="utf-8"))
        cols = "condition_cols=['catalyst1','solvent1','solvent2','reagent1','reagent2']"
        seq = "condition_to_calculate=['c1','s1','s2','r1','r2']"
        idx = "condition_item2cols={'c1':0,'s1':1,'s2':2,'r1':3,'r2':4}"
        for name, ok in (("upstream_training_column_order", cols in utils),
                         ("upstream_condition_category_order", seq in model),
                         ("upstream_evaluation_index_order", idx in model)):
            details[name + "_verified"] = ok
            if not ok:
                errors.append("upstream Parrot source no longer matches expected slot contract: " + name)
        details["upstream_source"] = str(source.resolve())
    return details, errors


def verify_run(run_dir, adapter_path=None, parrot_source=None, audit_benzocaine_route05=False):
    root = Path(run_dir)
    raw_path = root / "conditions-parrot.raw.json"
    norm_path = root / "conditions-parrot.json"
    raw_rows, norm_rows = rows(raw_path), rows(norm_path)
    errors = []
    def indexed(records):
        result = {}
        for row in records:
            reaction = row.get("reaction_smiles")
            mapping = tuple((x.get("route_id"), x.get("step_id")) for x in row.get("steps", []))
            key = (reaction, mapping)
            if key in result:
                errors.append(f"duplicate reaction/mapping record: {key}")
            result[key] = row
        return result
    raw, norm = indexed(raw_rows), indexed(norm_rows)
    if raw.keys() != norm.keys():
        errors.append("raw/normalized reaction or route-step mappings differ")
    for key in raw.keys() & norm.keys():
        rc = raw[key].get("candidates", [])
        nc = norm[key].get("candidates", [])
        if len(rc) != len(nc):
            errors.append(f"candidate count differs for {key}")
        for a, b in zip(rc, nc):
            for field in ("rank", *SLOTS, "sequence_score"):
                if a.get(field) != b.get(field):
                    errors.append(f"{field} differs between raw and normalized for {key}, rank {a.get('rank')}")
    resolved = None
    if audit_benzocaine_route05:
        target_reaction = "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1"
        target_mapping = ("route-05", "step-02")
        target = [row for row in raw_rows if row.get("reaction_smiles") == target_reaction
                  and target_mapping in [(x.get("route_id"), x.get("step_id")) for x in row.get("steps", [])]]
        if len(target) != 1:
            errors.append(f"expected one route-05/step-02 exact reaction row, found {len(target)}")
        else:
            top = next((x for x in target[0].get("candidates", []) if x.get("rank") == 1), None)
            expected = {"catalyst1": "", "solvent1": "CCO", "solvent2": "", "reagent1": "CCOCC", "reagent2": "FB(F)F"}
            if top is None:
                errors.append("route-05/step-02 rank-1 candidate missing")
            else:
                resolved = {"reaction_smiles": target_reaction, "steps": target[0].get("steps"),
                            "rank": top.get("rank"), "sequence_score": top.get("sequence_score"),
                            **{slot: top.get(slot) for slot in SLOTS}}
                for field, value in expected.items():
                    if top.get(field) != value:
                        errors.append(f"rank-1 {field} expected {value!r}, got {top.get(field)!r}")
    contract, contract_errors = verify_adapter_contract(adapter_path or Path(__file__).with_name("_parrot_worker.py"), parrot_source)
    errors.extend(contract_errors)
    return {"status": "passed" if not errors else "failed", "errors": errors, "slot_contract": contract,
            "target_specific_check": "benzocaine_route05" if audit_benzocaine_route05 else None,
            "raw_sha256": __import__("hashlib").sha256(raw_path.read_bytes()).hexdigest(),
            "normalized_sha256": __import__("hashlib").sha256(norm_path.read_bytes()).hexdigest(),
            "route05_step02_rank1": resolved, "compared_candidate_count": sum(len(r.get("candidates", [])) for r in raw_rows)}


def audit_report_slots(text):
    errors = []
    target_lines = [line for line in text.splitlines()
                    if ("route-05" in line or "route05" in line.lower())
                    and ("step-02" in line or "step 02" in line.lower())
                    and ("CCOCC" in line or "FB(F)F" in line)]
    for line in target_lines:
        if "CCOCC" in line:
            if re.search(r"(?:solvent2|solvent\s*2|용매\s*2)\s*[:=]?\s*`?CCOCC", line, re.I):
                errors.append("route-05/step-02 CCOCC is incorrectly assigned to solvent2")
            if not re.search(r"(?:reagent1|reagent\s*1|시약\s*1)\s*[:=]?\s*`?CCOCC", line, re.I):
                errors.append("route-05/step-02 CCOCC lacks an explicit reagent1 assignment")
        if "FB(F)F" in line:
            if re.search(r"(?:reagent1|reagent\s*1|시약\s*1)\s*[:=]?\s*`?FB\(F\)F", line, re.I):
                errors.append("route-05/step-02 FB(F)F is incorrectly assigned to reagent1")
            if not re.search(r"(?:reagent2|reagent\s*2|시약\s*2)\s*[:=]?\s*`?FB\(F\)F", line, re.I):
                errors.append("route-05/step-02 FB(F)F lacks an explicit reagent2 assignment")
    if not target_lines:
        errors.append("no route-05/step-02 condition statement found for slot audit")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--parrot-source", type=Path)
    parser.add_argument("--adapter", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--audit-benzocaine-route05", action="store_true",
                        help="also require the historical benzocaine route-05/step-02 rank-1 slot assignment")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify_run(args.run_dir, args.adapter, args.parrot_source, args.audit_benzocaine_route05)
    if args.report:
        text = args.report.read_text(encoding="utf-8")
        report_errors = audit_report_slots(text)
        result["report_path"] = str(args.report.resolve())
        result["report_slot_errors"] = report_errors
        result["errors"].extend(report_errors)
        result["status"] = "passed" if not result["errors"] else "failed"
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["status"] == "passed" else 1)


if __name__ == "__main__":
    main()

