"""Execute a configured yield checkpoint with explicit normalization provenance."""
from pathlib import Path
import sys
from _runtime import ROOT, cli, digest, execute, load, require, save, steps_from


def handler(args, payload, config, result, log):
    steps = steps_from(payload)
    result["input_step_mapping"] = steps
    if args.model == "drfp":
        estimator = Path(config.get("estimator", ROOT / "models/drfp/yield_regressor.joblib"))
        require(estimator.is_file(), "missing_trained_DRFP_yield_regressor; fingerprint_is_not_a_yield_model")
    else:
        require(config.get("checkpoint"), "missing_rxn_yields_checkpoint_and_normalization_metadata")
        estimator = Path(config["checkpoint"]) / "pytorch_model.bin"
        require(estimator.is_file(), "missing_rxn_yields_pytorch_model_bin")
    require(config.get("metadata"), "missing_checkpoint_training_domain_and_normalization_manifest")
    metadata = load(config["metadata"])
    require(metadata.get("checkpoint_sha256") == digest(estimator), "checkpoint_checksum_mismatch")
    require(metadata.get("training_data_reference"), "missing_training_data_reference")
    require(metadata.get("output_scale") in {"percent", "fraction", "standardized_percent", "standardized_fraction", "standardized_unknown"}, "unsupported_or_missing_yield_scale")
    python = Path(config.get("python", sys.executable))
    require(python.is_file(), "missing_yield_model_python_environment")
    raw = args.output.with_suffix(".raw.json")
    # Pass the already-expanded configuration to the worker. Re-reading the
    # template there leaves ${RXN_YIELDS_CHECKPOINT} unresolved on clean PCs.
    materialized_runtime = args.output.parent / "rxn_yields.runtime.materialized.json"
    save(materialized_runtime, {args.model: config})
    command = [python, "-X", "utf8", Path(__file__).resolve(), "--worker", args.model,
               args.input.resolve(), materialized_runtime.resolve(), raw]
    result.update(command=list(map(str, command)), checkpoint_sha256=digest(estimator),
                  checkpoint_metadata=metadata)
    result["materialized_runtime_configuration"] = str(materialized_runtime.resolve())
    result["runtime_configuration_sha256"] = digest(materialized_runtime)
    execute(command, log, timeout=600)
    result.update(status="success", inference_executed=True, predictions=load(raw), raw_path=str(raw),
                  applicability="not_assessed; numeric inference does not establish target-specific validity")
    if metadata["output_scale"] == "standardized_unknown":
        result.update(status="not_implemented", reason="raw_inference_executed_but_training_mean_std_unavailable; percent_yield_not_implemented")


def worker(model_name, input_path, config_path, raw_path):
    import math
    config = load(config_path)[model_name]
    metadata = load(config["metadata"])
    steps = steps_from(load(input_path))
    reactions = [s["reaction_smiles"] for s in steps]
    if model_name == "drfp":
        import joblib
        from drfp import DrfpEncoder
        estimator = joblib.load(config["estimator"])
        features = DrfpEncoder.encode(reactions, **metadata["encoding"])
        values = estimator.predict(features)
    else:
        # RXNFP's older wrapper lacks loss_fct expected by newer SimpleTransformers.
        # Invoke the same trained BERT regression head directly, with its SMILES tokenizer.
        import torch
        from transformers import BertForSequenceClassification
        from rxnfp.models import SmilesTokenizer
        torch.set_num_threads(2)
        checkpoint = config["checkpoint"]
        tokenizer = SmilesTokenizer.from_pretrained(checkpoint)
        model = BertForSequenceClassification.from_pretrained(checkpoint, local_files_only=True)
        if model.config.num_labels != 1:
            raise ValueError("Checkpoint is not a single-output yield regressor")
        model.eval()
        model_args = load(Path(checkpoint) / "model_args.json")
        values = []
        token_counts = [len(tokenizer.encode(r,add_special_tokens=True)) for r in reactions]
        with torch.no_grad():
            for start in range(0, len(reactions), 8):
                encoded = tokenizer(reactions[start:start+8], return_tensors="pt",
                                    padding="max_length", truncation=True,
                                    max_length=int(model_args["max_seq_length"]))
                output = model(**encoded, return_dict=True).logits
                values.extend(output.squeeze(-1).cpu().tolist())
    records = []
    for step, value in zip(steps, values):
        raw_value = float(value)
        if not math.isfinite(raw_value):
            raise ValueError("Non-finite yield output")
        scale = metadata["output_scale"]
        percent = raw_value
        if scale == "fraction":
            percent *= 100
        elif scale == "standardized_percent":
            percent = raw_value * float(metadata["training_yield_std"]) + float(metadata["training_yield_mean"])
        elif scale == "standardized_fraction":
            # USPTO TSV labels are /100 before z-scoring; reverse both operations.
            mean = float(metadata["training_yield_mean"])
            std = float(metadata["training_yield_std"])
            if metadata.get("training_yield_units") != "fraction" or not (0 <= mean <= 1) or not math.isfinite(std) or std <= 0:
                raise ValueError("Invalid or ambiguous fraction-scale normalization metadata")
            percent = 100.0 * (raw_value * std + mean)
        elif scale == "standardized_unknown":
            percent = None
        records.append({"route_id": step["route_id"], "step_id": step["step_id"],
                        "reaction_smiles": step["reaction_smiles"], "raw_value": raw_value,
                        "yield_percent": percent,
                        "raw_output_scale": scale,
                        "yield_status": "not_implemented" if percent is None else "predicted_not_validated",
                        "within_physical_bounds": (0 <= percent <= 100) if percent is not None else None,
                        "input_tokens": token_counts[len(records)] if model_name != "drfp" else None,
                        "max_input_tokens": int(model_args["max_seq_length"]) if model_name != "drfp" else None,
                        "input_truncated": token_counts[len(records)] > int(model_args["max_seq_length"]) if model_name != "drfp" else None,
                        "applicability": "not_assessed", "conditions_in_input": False})
    if len(records) != len(steps):
        raise ValueError("Prediction count does not match actual input reactions")
    save(raw_path, records)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        worker(*sys.argv[2:])
    else:
        raise SystemExit(cli("yields", ["rxn_yields", "drfp"], handler))
