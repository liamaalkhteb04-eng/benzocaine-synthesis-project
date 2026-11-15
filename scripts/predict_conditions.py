"""Call a real local ASKCOS service or an installed Parrot CLI."""
from pathlib import Path
import json
import urllib.request
from _runtime import ROOT, cli, digest, execute, load, require, save, steps_from


def handler(args, payload, config, result, log):
    steps = steps_from(payload)
    if args.model == "askcos":
        base = config.get("base_url", "http://localhost:9901").rstrip("/")
        try:
            with urllib.request.urlopen(base + "/health", timeout=5) as response:
                health = response.read().decode("utf-8")
        except Exception as exc:
            require(False, f"ASKCOS_service_unavailable: {type(exc).__name__}: {exc}")
        save(args.output.with_suffix(".health.json"), {"body": health})
        predictions = []
        for step in steps:
            request_body = {"smiles": step["reaction_smiles"], "reagents": [], "n_conditions": 5}
            request = urllib.request.Request(
                base + "/api/v2/condition/GRAPH", data=json.dumps(request_body).encode("utf-8"),
                headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(request, timeout=120) as response:
                raw = json.loads(response.read().decode("utf-8"))
            predictions.append({"route_id": step["route_id"], "step_id": step["step_id"],
                                "reaction_smiles": step["reaction_smiles"], "request": request_body,
                                "raw_response": raw, "temperature_unit": config.get("temperature_unit"),
                                "unit_caveat": "Verify service version and temperature unit before interpretation."})
            save(args.output.with_name(args.output.stem + f".{len(predictions):03d}.raw.json"), predictions[-1])
        result.update(status="success", inference_executed=True, predictions=predictions,
                      endpoint=base + "/api/v2/condition/GRAPH")
        return
    repo = Path(config.get("repository", ROOT / "external/Parrot")).resolve()
    python = Path(config.get("python", ROOT / ".venv-parrot/Scripts/python.exe")).resolve()
    cfg_template = Path(config.get("config", ROOT / "configs/parrot.json")).resolve()
    checkpoint_dir = Path(config.get("checkpoint", repo / "outputs/Parrot_train_in_USPTO_Condition_enhance")).resolve()
    checkpoint = checkpoint_dir / "pytorch_model.bin"
    missing = [str(p) for p in [repo / "inference.py", python, cfg_template, checkpoint] if not p.is_file()]
    require(not missing, "missing_Parrot_runtime_or_checkpoint: " + "; ".join(missing))
    template = load(cfg_template)
    template.setdefault("model_args", {})["best_model_dir"] = str(checkpoint_dir)
    cfg = args.output.parent / "parrot.materialized.json"
    cfg.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raw = args.output.with_suffix(".raw.json")
    command = [python, "-X", "utf8", ROOT / "scripts/_parrot_worker.py", repo.resolve(),
               cfg.resolve(), args.input.resolve(), raw]
    result["command"] = list(map(str, command))
    result["checkpoint_sha256"] = digest(checkpoint)
    execute(command, log, cwd=ROOT, timeout=600)
    worker_data = load(raw)
    result.update(worker_data)
    require(bool(result["predictions"]), "Parrot_produced_no_prediction_rows")
    result.update(status="success", inference_executed=True, raw_path=str(raw),
                  input_step_mapping=steps, configuration_sha256=digest(cfg),
                  source_repository="https://github.com/wangxr0526/Parrot",
                  configuration_template=str(cfg_template),
                  configuration_template_sha256=digest(cfg_template),
                  materialized_configuration=str(cfg),
                  checkpoint=str(checkpoint),
                  note="Sequence scores are rankings, not experimental success probabilities.")


if __name__ == "__main__":
    raise SystemExit(cli("conditions", ["askcos", "parrot"], handler))
