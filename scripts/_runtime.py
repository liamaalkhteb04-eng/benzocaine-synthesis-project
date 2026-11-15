"""Shared provenance, subprocess execution and adapter CLI. No synthetic predictions."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def expand_runtime_values(value, defaults=None):
    """Expand ${NAME} in runtime configuration without exposing secret values."""
    defaults = defaults or {}
    pattern = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
    if isinstance(value, str):
        return pattern.sub(lambda match: os.environ.get(match.group(1), defaults.get(match.group(1), match.group(0))), value)
    if isinstance(value, list):
        return [expand_runtime_values(item, defaults) for item in value]
    if isinstance(value, dict):
        return {key: expand_runtime_values(item, defaults) for key, item in value.items()}
    return value


def load_runtime_config(path):
    return expand_runtime_values(load(path), {"PROJECT_ROOT": str(ROOT)})


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def digest(path):
    sha = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def local_artifact(recorded_path, local_directory):
    """Prefer a relocated submission's copy over a historical absolute filename."""
    name = str(recorded_path).replace("\\", "/").rsplit("/", 1)[-1]
    local = Path(local_directory) / name
    if local.is_file():
        return local.resolve()
    recorded = Path(recorded_path)
    if recorded.is_file():
        return recorded.resolve()
    raise FileNotFoundError(f"Artifact unavailable: {name}")


class Unavailable(Exception):
    """Inference did not start; detailed reason must be retained."""


def require(condition, reason):
    if not condition:
        raise Unavailable(reason)


def execute(command, log, cwd=ROOT, timeout=300):
    env = os.environ.copy()
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1",
               HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", WANDB_MODE="disabled",
               HF_HOME=str(ROOT/".cache/huggingface"), TRANSFORMERS_CACHE=str(ROOT/".cache/transformers"),
               MPLCONFIGDIR=str(ROOT/".cache/matplotlib"), TORCH_HOME=str(ROOT/".cache/torch"))
    for name in ["UPSTAGE_API_KEY", "GEMINI_API_KEY", "WANDB_API_KEY"]:env.pop(name,None)
    with Path(log).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps({"command": list(map(str, command)), "cwd": str(cwd)}) + "\n")
        stream.flush()
        proc = subprocess.run(list(map(str, command)), cwd=cwd, env=env,
                              stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
    if proc.returncode:
        raise RuntimeError(f"Process exited {proc.returncode}; see {log}")


def steps_from(payload):
    require(payload.get("status") == "success", "upstream_routes_not_successful")
    steps = [dict(step, route_id=route["route_id"])
             for route in payload.get("predictions", []) for step in route.get("steps", [])]
    require(bool(steps), "no_actual_predicted_reactions_available")
    return steps


def cli(task, models, handler):
    parser = argparse.ArgumentParser(description=f"Real {task} adapters; no mock fallback")
    parser.add_argument("--model", required=True, choices=models)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--runtime", type=Path, default=ROOT / "configs/runtime.json")
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        parser.error("Output exists; use a new run directory")
    payload = load(args.input)
    config = load_runtime_config(args.runtime) if args.runtime.exists() else {}
    result = {
        "schema_version": "0.2", "task": task, "model": args.model,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "not_implemented", "inference_executed": False,
        "input_path": str(args.input.resolve()), "input_sha256": digest(args.input),
        "adapter_sha256": digest(Path(sys.argv[0])), "predictions": None,
        "reason": None,
    }
    log = args.output.with_suffix(".log")
    try:
        handler(args, payload, config.get(args.model, {}), result, log)
    except Unavailable as exc:
        result["reason"] = str(exc)
    except Exception as exc:
        result.update(status="failed", reason=f"{type(exc).__name__}: {exc}")
        with log.open("a", encoding="utf-8") as stream:
            traceback.print_exc(file=stream)
    result["completed_at"] = datetime.now(timezone.utc).isoformat()
    if not log.exists():
        log.write_text(f"{result['status']}: {result['reason']}\n", encoding="utf-8")
    result["log_path"] = str(log)
    save(args.output, result)
    print(f"{args.model}: {result['status']}; {args.output}")
    return 0 if result["status"] == "success" else 2
