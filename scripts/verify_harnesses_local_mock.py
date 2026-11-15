"""Run both installed harnesses against a loopback fixture and inspect first POSTs.

This performs no Upstage request. The mock response is explicitly synthetic and
is never written to the real comparison run or counted as a model result.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "analyses" / "harness-comparison" / "comparison-input-payload.md"
SYSTEM_PROMPT = ROOT / "analyses" / "harness-comparison" / "comparison-system-prompt.txt"
MODEL = "solar-pro4-260806"
PROMPT = "Create the Korean comparison draft requested in the attached frozen payload."
MOCK_TEXT = "LOCAL_MOCK_ONLY: BENZOCAINE COMPARISON DRAFT FIXTURE"
ALLOWED_FIELDS = {
    "model", "messages", "temperature", "reasoning_effort", "max_tokens", "n",
    "stream", "prompt_cache_key", "top_p", "frequency_penalty", "presence_penalty", "stop",
}


class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path.rstrip("/") in {"/v1/models", "/models"}:
            data = json.dumps({"object": "list", "data": [{"id": MODEL, "object": "model", "owned_by": "local-mock"}]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_error(404)

    def do_POST(self) -> None:
        n = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(n).decode("utf-8"))
        self.server.requests.append(body)  # type: ignore[attr-defined]
        data = json.dumps({
            "id": "local-mock-only",
            "object": "chat.completion",
            "model": MODEL,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": MOCK_TEXT}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 31, "completion_tokens": 8, "total_tokens": 39},
        }).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args: Any) -> None:
        pass


def flatten_content(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(part.get("text", "") for part in value if isinstance(part, dict))
    return ""


def run_command(args: list[str], env: dict[str, str], cwd: Path, log_path: Path) -> int:
    proc = subprocess.run(args, cwd=str(cwd), env=env, capture_output=True, text=True, timeout=120)
    text = (proc.stdout + "\n" + proc.stderr).replace("LOCAL_MOCK_DUMMY", "[MOCK_KEY_REDACTED]")
    log_path.write_text(text, encoding="utf-8")
    return proc.returncode


def inspect_body(body: dict[str, Any], source_payload: str) -> dict[str, Any]:
    user_text = "\n".join(flatten_content(m.get("content")) for m in body.get("messages", []) if m.get("role") == "user")
    unknown = sorted(set(body) - ALLOWED_FIELDS)
    problems = []
    if body.get("model") != MODEL:
        problems.append("wrong_model")
    if PROMPT not in user_text:
        problems.append("first_request_is_not_the_report_prompt")
    if "Solar Pro 4 harness comparison" not in user_text or "Benzocaine" not in user_text:
        problems.append("frozen_evidence_payload_not_attached")
    if source_payload not in user_text:
        problems.append("full_frozen_payload_not_attached")
    if "synthesis_report_skill.md" not in user_text:
        problems.append("skill_evidence_not_attached")
    if unknown:
        problems.append("unsupported_top_level_fields:" + ",".join(unknown))
    if body.get("store") is not None:
        problems.append("store_field_present")
    if body.get("tools") or body.get("tool_choice"):
        problems.append("tools_not_disabled")
    if body.get("stream") is True:
        problems.append("streaming_unexpected")
    return {
        "model": body.get("model"),
        "top_level_fields": sorted(body),
        "unknown_fields": unknown,
        "user_text_bytes": len(user_text.encode("utf-8")),
        "user_text_sha256": hashlib.sha256(user_text.encode("utf-8")).hexdigest().upper(),
        "full_frozen_payload_present": source_payload in user_text,
        "report_prompt_present": PROMPT in user_text,
        "benzocaine_evidence_present": "Benzocaine" in user_text,
        "skill_filename_present": "synthesis_report_skill.md" in user_text,
        "store_absent": "store" not in body,
        "problems": problems,
        "pass": not problems,
    }


def main() -> int:
    if not PAYLOAD.is_file() or not SYSTEM_PROMPT.is_file():
        raise SystemExit("Frozen input/system prompt missing.")
    payload_text = PAYLOAD.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="benzocaine-harness-mock-") as td:
        temp = Path(td)
        server = ThreadingHTTPServer(("127.0.0.1", 0), MockHandler)
        server.requests = []  # type: ignore[attr-defined]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}/v1"
        results: dict[str, Any] = {"classification": "LOCAL_MOCK_ONLY_NOT_MODEL_OUTPUT", "mock_response": MOCK_TEXT, "payload_sha256": hashlib.sha256(PAYLOAD.read_bytes()).hexdigest().upper(), "harnesses": {}}
        try:
            opencode_config = {
                "$schema": "https://opencode.ai/config.json",
                "update": "disable",
                "share": "disabled",
                "experimental": {"openTelemetry": False},
                "provider": {"upstage": {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": "Local mock only",
                    "options": {"baseURL": base, "apiKey": "LOCAL_MOCK_DUMMY"},
                    "models": {MODEL: {"name": "Solar Pro 4 mock", "limit": {"context": 512000, "output": 10000}}},
                }},
                "agent": {"comparison-draft": {
                    "mode": "primary",
                    "prompt": SYSTEM_PROMPT.read_text(encoding="utf-8").strip(),
                    "tools": {"*": False},
                    "steps": 1,
                    "temperature": 0,
                }},
            }
            oc_cfg = temp / "opencode.mock.json"
            oc_cfg.write_text(json.dumps(opencode_config, ensure_ascii=False, indent=2), encoding="utf-8")
            env = os.environ.copy()
            env.update({"OPENCODE_CONFIG": str(oc_cfg), "OPENCODE_PURE": "1", "OPENCODE_DISABLE_AUTOUPDATE": "1", "OPENCODE_API_KEY": "LOCAL_MOCK_DUMMY"})
            oc = ROOT / "tools" / "harnesses" / "opencode" / "node_modules" / ".bin" / "opencode.cmd"
            oc_args = ["cmd.exe", "/c", str(oc), "run", "--standalone", "--title", "Local mock fixed title", "--agent", "comparison-draft", "--model", "upstage/" + MODEL, "--file", str(PAYLOAD), PROMPT]
            before = len(server.requests)  # type: ignore[attr-defined]
            oc_exit = run_command(oc_args, env, ROOT, temp / "opencode.log")
            oc_bodies = server.requests[before:]  # type: ignore[attr-defined]
            oc_check = inspect_body(oc_bodies[0], payload_text) if oc_bodies else {"pass": False, "problems": ["no_request"]}
            results["harnesses"]["opencode"] = {"exit_code": oc_exit, "post_count": len(oc_bodies), "first_post": oc_check}
            if len(oc_bodies) != 1:
                results["harnesses"]["opencode"]["first_post"]["problems"].append("expected_exactly_one_post_with_fixed_title")
                results["harnesses"]["opencode"]["first_post"]["pass"] = False

            pi_cfg_dir = temp / "pi-config"
            pi_cfg_dir.mkdir()
            pi_models = {"$schema": "https://pi.dev/schemas/models.schema.json", "providers": {"upstage": {
                "name": "Local mock only", "baseUrl": base, "api": "openai-completions", "apiKey": "LOCAL_MOCK_DUMMY",
                "compat": {"supportsStore": False, "supportsDeveloperRole": False, "supportsReasoningEffort": True, "supportsUsageInStreaming": False, "maxTokensField": "max_tokens"},
                "models": [{"id": MODEL, "name": "Solar Pro 4 mock", "reasoning": False, "maxTokens": 10000, "samplingParams": {"temperature": 0}}],
            }}}
            (pi_cfg_dir / "models.json").write_text(json.dumps(pi_models, ensure_ascii=False, indent=2), encoding="utf-8")
            pi_env = os.environ.copy()
            pi_env.update({"PI_CODING_AGENT_DIR": str(pi_cfg_dir), "PI_OFFLINE": "1", "PI_TELEMETRY": "0", "PI_SKIP_VERSION_CHECK": "1"})
            pi = ROOT / "tools" / "harnesses" / "pi" / "node_modules" / ".bin" / "pi.cmd"
            system_prompt = SYSTEM_PROMPT.read_text(encoding="utf-8").strip()
            pi_args = ["cmd.exe", "/c", str(pi), "--no-tools", "--no-extensions", "--no-mcp", "--no-context-files", "--no-skills", "--no-prompt-templates", "--no-themes", "--offline", "--no-session", "--thinking", "off", "--provider", "upstage", "--model", MODEL, "--system-prompt", system_prompt, "--print", "@" + str(PAYLOAD), PROMPT]
            before = len(server.requests)  # type: ignore[attr-defined]
            pi_exit = run_command(pi_args, pi_env, ROOT, temp / "pi.log")
            pi_bodies = server.requests[before:]  # type: ignore[attr-defined]
            pi_check = inspect_body(pi_bodies[0], payload_text) if pi_bodies else {"pass": False, "problems": ["no_request"]}
            results["harnesses"]["pi"] = {"exit_code": pi_exit, "post_count": len(pi_bodies), "first_post": pi_check}
            if len(pi_bodies) != 1:
                results["harnesses"]["pi"]["first_post"]["problems"].append("expected_exactly_one_post")
                results["harnesses"]["pi"]["first_post"]["pass"] = False
            for h in ("opencode", "pi"):
                if results["harnesses"][h]["exit_code"] != 0:
                    results["harnesses"][h]["first_post"]["problems"].append("harness_nonzero_exit")
                    results["harnesses"][h]["first_post"]["pass"] = False
            requests_path = ROOT / "analyses" / "harness-comparison" / "local-harness-verification"
            requests_path.mkdir(parents=True, exist_ok=True)
            for h, bodies in (("opencode", oc_bodies), ("pi", pi_bodies)):
                if bodies:
                    (requests_path / f"{h}.request.json").write_text(json.dumps(bodies[0], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                # Only store sanitized harness logs and synthetic mock result labels.
                for logname in ("opencode", "pi"):
                    source = temp / f"{logname}.log"
                    if source.exists():
                        (requests_path / f"{logname}.log").write_text(source.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
            results["all_passed"] = all(results["harnesses"][h]["first_post"]["pass"] for h in ("opencode", "pi"))
            (requests_path / "verification.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"all_passed": results["all_passed"], "classification": results["classification"], "opencode_posts": len(oc_bodies), "pi_posts": len(pi_bodies), "artifacts": str(requests_path.relative_to(ROOT))}, ensure_ascii=False))
            return 0 if results["all_passed"] else 1
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    raise SystemExit(main())
