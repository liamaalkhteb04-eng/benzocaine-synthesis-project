"""Sequential CPU inference using upstream Parrot weights, not its Linux parallel CLI."""
import json
from pathlib import Path
import sys
from _runtime import digest, load, save, steps_from


def main(repo, config_path, input_path, output_path):
    sys.path.insert(0, repo)
    import pandas as pd
    import torch
    import yaml
    from models.parrot_model import ParrotConditionPredictionModel
    from models.utils import caonicalize_rxn_smiles
    torch.set_num_threads(2)
    config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    args = config["model_args"]
    checkpoint = Path(args["best_model_dir"])
    if not checkpoint.is_absolute():
        checkpoint = Path(repo) / checkpoint
    trained_config = load(checkpoint / "config.json")
    idx2label, label2idx = trained_config["condition_label_mapping"]
    # JSON stringifies dictionary keys; restore the actual trained index mapping.
    labels = ({int(k): v for k, v in idx2label.items()},
              {k: int(v) for k, v in label2idx.items()})
    use_temperature = bool(trained_config["use_temperature"])
    args["use_temperature"] = use_temperature
    args["decoder_args"].update(tgt_vocab_size=len(labels[0]), condition_label_mapping=labels)
    args.update(use_multiprocessing=False, use_multiprocessing_for_evaluation=False,
                process_count=1, dataloader_num_workers=0, thread_count=2,
                wandb_project=None, output_dir=str(Path(output_path).parent/"parrot-runtime"),
                cache_dir=str(Path(output_path).parent/"parrot-cache"),
                tensorboard_dir=str(Path(output_path).parent/"parrot-tensorboard"),
                best_model_dir=str(checkpoint), pretrained_path=str(checkpoint), no_cache=True)
    model = ParrotConditionPredictionModel("bert", str(checkpoint), args=args,
                                           use_cuda=False, cuda_device=-1)
    steps = steps_from(load(input_path))
    # Deduplicate actual reactions, retaining all route/step mappings.
    reactions = list(dict.fromkeys(s["reaction_smiles"] for s in steps))
    canonical = [caonicalize_rxn_smiles(s) for s in reactions]
    if any(not s for s in canonical):
        raise ValueError("Parrot rejected an actual route reaction; no silent input deletion")
    frame = pd.DataFrame({"text": canonical, "labels": [[0] * (8 if use_temperature else 7)] * len(canonical)})
    conditions, temperatures = model.condition_beam_search(
        frame, output_dir=str(Path(output_path).parent/"parrot-runtime"), beam={int(k):int(v) for k,v in config["inference_args"]["beam"].items()},
        test_batch_size=1, calculate_topk_accuracy=False)
    if len(conditions) != len(reactions):
        raise ValueError("Parrot prediction count mismatch")
    predictions = []
    for index, candidates in enumerate(conditions):
        rows = []
        # Upstream label order follows catalyst1, solvent1, solvent2, reagent1, reagent2. Do not infer roles from the SMILES tokens.
        for rank, (agents, score) in enumerate(candidates, 1):
            rows.append({"rank": rank, "catalyst1": agents[0], "solvent1": agents[1],
                         "solvent2": agents[2], "reagent1": agents[3], "reagent2": agents[4],
                         "sequence_score": float(score)})
        predictions.append({
            "reaction_smiles": reactions[index], "canonical_reaction_smiles": canonical[index],
            "steps": [{"route_id": s["route_id"], "step_id": s["step_id"]}
                      for s in steps if s["reaction_smiles"] == reactions[index]],
            "candidates": rows,
            "temperature": float(temperatures[index]) if use_temperature and temperatures else None,
            "temperature_status": "provided" if use_temperature else "not_provided_by_checkpoint",
            "time": None, "yield_percent": None,
        })
    save(output_path, {"predictions": predictions, "checkpoint": str(checkpoint),
                       "checkpoint_sha256": digest(checkpoint / "pytorch_model.bin"),
                       "label_mapping_source": "trained checkpoint config.json; no synthesized labels",
                       "label_mapping_config_sha256": digest(checkpoint / "config.json"),
                       "execution_mode": "sequential CPU; upstream model API; no pandarallel",
                       "use_temperature": use_temperature,
                       "slot_order": ["catalyst1", "solvent1", "solvent2", "reagent1", "reagent2"]})


if __name__ == "__main__":
    main(*sys.argv[1:])

