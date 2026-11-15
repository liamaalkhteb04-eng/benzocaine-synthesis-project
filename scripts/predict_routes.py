"""Execute AiZynthFinder or check prerequisites for live SynthEx."""
from pathlib import Path
import os
import sys
from _runtime import ROOT, Unavailable, cli, digest, execute, expand_runtime_values, load, require, save


def normalize_trees(trees):
    def solved(node):
        reactions=node.get("children",[])
        if not reactions:return bool(node.get("in_stock",False))
        return all(solved(p) for reaction in reactions for p in reaction.get("children",[]))
    routes = []
    for index, tree in enumerate(trees, 1):
        steps = []

        def walk(molecule):
            produced = None
            for reaction in molecule.get("children", []):
                precursors = reaction.get("children", [])
                dependencies = []
                for precursor in precursors:
                    upstream = walk(precursor)
                    if upstream:dependencies.append(upstream)
                produced = f"step-{len(steps)+1:02d}"
                steps.append({
                    "step_id": produced,
                    "depends_on": dependencies,
                    "precursor_stock_flags": [p.get("in_stock") for p in precursors],
                    "reaction_smiles": ".".join(p["smiles"] for p in precursors)
                                       + ">>" + molecule["smiles"],
                    "precursor_smiles": [p["smiles"] for p in precursors],
                    "product_smiles": molecule["smiles"],
                    "metadata": reaction.get("metadata", {}),
                    "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
                })
            return produced
        walk(tree)
        routes.append({"route_id": f"route-{index:02d}", "steps": steps,
                       "metadata": tree.get("metadata", {}), "is_solved": solved(tree),
                       "scores": tree.get("scores", {})})
    return routes


def handler(args, payload, config, result, log):
    if args.model == "synthex":
        require(os.getenv("GEMINI_API_KEY"), "missing_GEMINI_API_KEY_for_live_SynthEx; replay_demo_disabled")
        require(False, "SynthEx_RouteJSON_normalizer_not_implemented_for_selected_commit")
    python = Path(config.get("python", ROOT / ".venv-aizynth/Scripts/python.exe"))
    cfg_template = Path(config.get("config", ROOT / "configs/aizynthfinder.json"))
    require(python.is_file(), "missing_AiZynthFinder_python_environment")
    require(cfg_template.is_file(), "missing_AiZynthFinder_config_template")
    materialized_config = args.output.parent / "aizynthfinder.materialized.json"
    template = expand_runtime_values(load(cfg_template), {
        "PROJECT_ROOT": str(ROOT),
        "AIZYNTH_MODEL_DIR": config.get("model_dir", "${AIZYNTH_MODEL_DIR}"),
        "AIZYNTH_STOCK_BUCKETS": config.get("stock_buckets", "${AIZYNTH_STOCK_BUCKETS}"),
    })
    missing_refs = sorted({part for value in str(template).split("${")[1:] for part in [value.split("}", 1)[0]]})
    if missing_refs:
        require(False, "unresolved_AiZynthFinder_runtime_variables: " + ", ".join(missing_refs))
    materialized_config.write_text(__import__("json").dumps(template, indent=2) + "\n", encoding="utf-8")
    cfg = materialized_config
    raw = args.output.with_suffix(".raw.json")
    meta = args.output.with_suffix(".metadata.json")
    command = [python, "-X", "utf8", Path(__file__).resolve(), "--worker",
               args.input.resolve(), cfg.resolve(), raw, meta]
    result["command"] = list(map(str, command))
    result["configuration"] = load(cfg)
    result["configuration_template"] = str(cfg_template.resolve())
    result["configuration_template_sha256"] = digest(cfg_template)
    result["configuration_sha256"] = digest(cfg)
    assets = [s.get("path") if isinstance(s,dict) else s for s in result["configuration"].get("stock", {}).values()]
    for policy in result["configuration"].get("expansion", {}).values():
        if isinstance(policy, list):
            assets.extend(policy)
    result["asset_sha256"] = {str(path): digest(path) for path in assets if path and Path(path).is_file()}
    for path in assets:
        if path and Path(path).is_dir() and (Path(path)/"manifest.json").exists():
            result["derived_stock_provenance"]=load(Path(path)/"manifest.json")
    result["execution_attempted"] = True
    try:
        execute(command, log, timeout=config.get("timeout_seconds", 600))
    except RuntimeError as exc:
        text = log.read_text(encoding="utf-8", errors="replace")
        if "ImportError:" in text or "ModuleNotFoundError:" in text:
            raise Unavailable(f"runtime_import_unavailable; see {log}") from exc
        raise
    result.update(load(meta))
    trees = load(raw)
    normalized=normalize_trees(trees)
    limit=int(config.get("inference_route_limit",len(normalized)))
    reserve=int(config.get("multistep_reserve",0))
    selected=normalized[:max(0,limit-reserve)]
    for candidate in [r for r in normalized if len(r['steps'])>1]+normalized:
        if len(selected)>=limit:break
        if candidate not in selected:selected.append(candidate)
    result.update(status="success", inference_executed=True, raw_path=str(raw),
                  predictions=selected, total_raw_routes=len(normalized),
                  selection_policy={"limit":limit,"multistep_reserve":reserve,"note":"Computational budget: initial score-order candidates plus multi-step diversity. Raw routes retained in full; no claim of feasibility."})
    result["reason"] = "search_completed" if trees else "search_completed_without_routes"


def worker(input_path, cfg_path, raw_path, meta_path):
    import importlib.metadata
    import random
    # On this Windows runtime ORT must initialize before Arrow/RDKit DLLs.
    # This changes library loading order, not model weights or inference outputs.
    import onnxruntime
    import numpy as np
    import aizynthfinder.aizynthfinder as finder_module
    from aizynthfinder.aizynthfinder import AiZynthFinder
    from aizynthfinder.utils.logging import setup_logger
    import logging
    setup_logger(logging.DEBUG)
    random.seed(42)
    np.random.seed(42)
    payload = load(input_path)
    finder = AiZynthFinder(configfile=cfg_path)
    finder.expansion_policy.select("uspto")
    finder.stock.select(finder.stock.items)
    finder.target_smiles = payload["smiles"]
    finder.prepare_tree()
    finder.tree_search()
    finder.build_routes()
    finder.routes.compute_scores(*finder.scorers.objects())
    save(raw_path, finder.routes.dict_with_extra(include_metadata=True, include_scores=True))
    save(meta_path, {
        "package_version": importlib.metadata.version("aizynthfinder"),
        "package_versions": {name: importlib.metadata.version(name)
                             for name in ["rdkit", "onnxruntime", "numpy", "pandas", "reaction-utils"]},
        "finder_source_sha256": digest(finder_module.__file__),
        "source_repository": "https://github.com/MolecularAI/aizynthfinder",
        "random_seed": 42, "numpy_seed": 42,
        "filter_policy": "disabled; expansion-policy-only baseline",
        "statistics": finder.extract_statistics(), "stock_info": finder.stock_info(),
        "exclude_target_from_stock": finder.config.search.exclude_target_from_stock,
    })


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        worker(*sys.argv[2:])
    else:
        raise SystemExit(cli("routes", ["aizynthfinder", "synthex"], handler))
