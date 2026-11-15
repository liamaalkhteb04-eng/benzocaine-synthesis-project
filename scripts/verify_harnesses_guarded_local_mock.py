"""End-to-end local-only verification through the real request guard.

The installed OpenCode and Pi CLIs talk only to the loopback guard. The guard
forwards only to an in-process mock server; no Upstage request is possible.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.harness_request_guard import MODEL_ID, make_server

COMPARISON = ROOT / "analyses" / "harness-comparison"
PAYLOAD = COMPARISON / "comparison-input-payload.md"
SYSTEM_PROMPT = COMPARISON / "comparison-system-prompt.txt"
MANIFEST = COMPARISON / "comparison-input-payload-manifest.json"
OUT = COMPARISON / "local-harness-verification-02"
USER_PROMPT = "Create the Korean comparison draft requested in the attached frozen payload."
MOCK_TEXT = "LOCAL_MOCK_ONLY: SYNTHETIC_RESPONSE_NOT_A_REPORT_RESULT"
ALLOWED_FIELDS = {
    "model", "messages", "temperature", "reasoning_effort", "max_tokens", "n", "stream",
    "prompt_cache_key", "top_p", "frequency_penalty", "presence_penalty", "stop",
}


class MockHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length).decode("utf-8"))
        self.server.received.append(body)  # type: ignore[attr-defined]
        response = {
            "id": "local-mock-chat-completion",
            "object": "chat.completion",
            "created": 1793700000,
            "model": MODEL_ID,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": MOCK_TEXT}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 17, "completion_tokens": 8, "total_tokens": 25},
        }
        raw = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        self.send_error(404)

    def log_message(self, *args: Any) -> None:
        pass


def text_content(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(part.get("text", "") for part in value if isinstance(part, dict))
    return ""


def run_harness(command: list[str], env: dict[str, str], log_file: Path) -> int:
    proc = subprocess.run(command, cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=100)
    captured = (proc.stdout + "\n" + proc.stderr).replace("LOCAL_GUARD_PLACEHOLDER", "[LOCAL_PLACEHOLDER]")
    log_file.write_text(captured, encoding="utf-8")
    return proc.returncode


def validate_forwarded(body: dict[str, Any], source_paths: list[str]) -> dict[str, Any]:
    messages = body.get("messages", [])
    user_text = "\n".join(text_content(m.get("content")) for m in messages if m.get("role") == "user")
    top_unknown = sorted(set(body) - ALLOWED_FIELDS)
    missing_sources = [p for p in source_paths if f"BEGIN SOURCE: {p}" not in user_text]
    problems: list[str] = []
    if body.get("model") != MODEL_ID:
        problems.append("wrong_model")
    if USER_PROMPT not in user_text:
        problems.append("first_request_not_report_writing_prompt")
    if missing_sources:
        problems.append("missing_payload_sources")
    if top_unknown:
        problems.append("unsupported_fields_forwarded:" + ",".join(top_unknown))
    if body.get("store") is not None:
        problems.append("unsupported_store_field_forwarded")
    if body.get("stream") is not False:
        problems.append("guard_did_not_normalize_streaming")
    if body.get("temperature") != 0 or body.get("reasoning_effort") != "none" or body.get("max_tokens") != 10000 or body.get("n") != 1:
        problems.append("generation_settings_not_normalized")
    return {
        "model": body.get("model"),
        "fields_forwarded": sorted(body),
        "removed_unsupported_fields": top_unknown,
        "store_absent_upstream": "store" not in body,
        "stream_normalized_false_upstream": body.get("stream") is False,
        "report_prompt_present_in_first_request": USER_PROMPT in user_text,
        "source_blocks_expected": len(source_paths),
        "source_blocks_present": len(source_paths) - len(missing_sources),
        "missing_sources": missing_sources,
        "user_content_bytes": len(user_text.encode("utf-8")),
        "user_content_sha256": hashlib.sha256(user_text.encode("utf-8")).hexdigest().upper(),
        "problems": problems,
        "pass": not problems,
    }


def main() -> int:
    if OUT.exists():
        raise SystemExit(f"Verification output already exists; refusing overwrite: {OUT}")
    payload = PAYLOAD.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    source_paths = [item["path"] for item in manifest["inputs"]]
    state_root = OUT / "temporary_guard_state"
    run_root = OUT / "temporary_guard_runs"
    OUT.mkdir(parents=True)
    upstream = ThreadingHTTPServer(("127.0.0.1", 0), MockHandler)
    upstream.received = []  # type: ignore[attr-defined]
    upstream_thread = threading.Thread(target=upstream.serve_forever, daemon=True)
    upstream_thread.start()
    old_key = os.environ.get("UPSTAGE_API_KEY")
    os.environ["UPSTAGE_API_KEY"] = "LOCAL_GUARD_PLACEHOLDER"
    servers = []
    results: dict[str, Any] = {
        "classification": "LOCAL_MOCK_ONLY_NOT_SOLAR_OUTPUT",
        "external_solar_requests": 0,
        "fixture_response": MOCK_TEXT,
        "base_payload_sha256": hashlib.sha256(PAYLOAD.read_bytes()).hexdigest().upper(),
        "source_count": len(source_paths),
        "harnesses": {},
    }
    try:
        for harness in ("opencode", "pi"):
            run_id = f"local-{harness}-mock-01"
            guard = make_server(
                harness,
                0,
                state_root / harness,
                run_root,
                f"http://127.0.0.1:{upstream.server_address[1]}",
                timeout_seconds=15,
                run_id=run_id,
                max_total_posts=1,
                max_per_harness=1,
                cumulative_budget_usd=1.0,
            )
            servers.append(guard)
            threading.Thread(target=guard.serve_forever, daemon=True).start()
            local_base = f"http://127.0.0.1:{guard.server_address[1]}/v1"
            start = len(upstream.received)  # type: ignore[attr-defined]

            if harness == "opencode":
                config = {
                    "$schema": "https://opencode.ai/config.json",
                    "update": "disable",
                    "share": "disabled",
                    "experimental": {"openTelemetry": False},
                    "provider": {"upstage": {
                        "npm": "@ai-sdk/openai-compatible",
                        "name": "Loopback guard",
                        "options": {"baseURL": local_base, "apiKey": "LOCAL_GUARD_PLACEHOLDER"},
                        "models": {MODEL_ID: {"name": "Solar Pro 4 pinned", "limit": {"context": 512000, "output": 10000}}},
                    }},
                    "agent": {"comparison-draft": {
                        "mode": "primary",
                        "prompt": SYSTEM_PROMPT.read_text(encoding="utf-8").strip(),
                        "tools": {"*": False},
                        "steps": 1,
                        "temperature": 0,
                    }},
                }
                config_path = OUT / "opencode.mock.json"
                config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
                env = os.environ.copy()
                env.update({"OPENCODE_CONFIG": str(config_path), "OPENCODE_PURE": "1", "OPENCODE_DISABLE_AUTOUPDATE": "1"})
                exe = ROOT / "tools" / "harnesses" / "opencode" / "node_modules" / ".bin" / "opencode.cmd"
                cmd = ["cmd.exe", "/c", str(exe), "run", "--standalone", "--title", "Benzocaine comparison draft", "--agent", "comparison-draft", "--model", "upstage/" + MODEL_ID, "--file", str(PAYLOAD), USER_PROMPT]
            else:
                pi_dir = OUT / "pi-config"
                pi_dir.mkdir()
                pi_models = {
                    "$schema": "https://pi.dev/schemas/models.schema.json",
                    "providers": {"upstage": {
                        "name": "Loopback guard",
                        "baseUrl": local_base,
                        "api": "openai-completions",
                        "apiKey": "LOCAL_GUARD_PLACEHOLDER",
                        "compat": {"supportsStore": False, "supportsDeveloperRole": False, "supportsReasoningEffort": True, "supportsUsageInStreaming": False, "maxTokensField": "max_tokens"},
                        "models": [{"id": MODEL_ID, "name": "Solar Pro 4 pinned", "reasoning": False, "maxTokens": 10000, "samplingParams": {"temperature": 0}}],
                    }},
                }
                (pi_dir / "models.json").write_text(json.dumps(pi_models, ensure_ascii=False, indent=2), encoding="utf-8")
                env = os.environ.copy()
                env.update({"PI_CODING_AGENT_DIR": str(pi_dir), "PI_OFFLINE": "1", "PI_TELEMETRY": "0", "PI_SKIP_VERSION_CHECK": "1"})
                exe = ROOT / "tools" / "harnesses" / "pi" / "node_modules" / ".bin" / "pi.cmd"
                system_prompt = SYSTEM_PROMPT.read_text(encoding="utf-8").strip()
                cmd = ["cmd.exe", "/c", str(exe), "--no-tools", "--no-extensions", "--no-mcp", "--no-context-files", "--no-skills", "--no-prompt-templates", "--no-themes", "--offline", "--no-session", "--thinking", "off", "--provider", "upstage", "--model", MODEL_ID, "--system-prompt", system_prompt, "--print", "@" + str(PAYLOAD), USER_PROMPT]

            exit_code = run_harness(cmd, env, OUT / f"{harness}.log")
            bodies = upstream.received[start:]  # type: ignore[attr-defined]
            meta_file = run_root / run_id / "metadata.json"
            request_file = run_root / run_id / "request.redacted.json"
            meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}
            forwarded = json.loads(request_file.read_text(encoding="utf-8")) if request_file.exists() else {}
            check = validate_forwarded(bodies[0], source_paths) if bodies else {"pass": False, "problems": ["no_upstream_mock_post"]}
            removed = meta.get("request_controls", {}).get("removed_unsupported_request_fields", [])
            if harness == "pi" and "store" in removed:
                check["problems"].append("Pi_provider_compat_did_not_omit_store_before_guard")
                check["pass"] = False
            if len(bodies) != 1:
                check["problems"].append("expected_one_mock_upstream_post")
                check["pass"] = False
            if exit_code != 0:
                check["problems"].append("harness_nonzero_exit_after_mock_stream_adapter")
                check["pass"] = False
            results["harnesses"][harness] = {
                "run_id": run_id,
                "exit_code": exit_code,
                "mock_upstream_posts": len(bodies),
                "first_post": check,
                "guard_removed_request_fields": removed,
                "forwarded_fields": sorted(forwarded),
                "local_stream_adapter_used": meta.get("request_controls", {}).get("tools") == "disabled",
            }
        results["all_passed"] = all(v["first_post"]["pass"] for v in results["harnesses"].values())
        results["external_solar_requests"] = 0
        (OUT / "verification.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"all_passed": results["all_passed"], "classification": results["classification"], "opencode_mock_posts": results["harnesses"].get("opencode", {}).get("mock_upstream_posts"), "pi_mock_posts": results["harnesses"].get("pi", {}).get("mock_upstream_posts"), "external_solar_requests": 0, "artifacts": str(OUT.relative_to(ROOT))}, ensure_ascii=False))
        return 0 if results["all_passed"] else 1
    finally:
        for server in servers:
            server.shutdown()
            server.server_close()
        upstream.shutdown()
        upstream.server_close()
        if old_key is None:
            os.environ.pop("UPSTAGE_API_KEY", None)
        else:
            os.environ["UPSTAGE_API_KEY"] = old_key


if __name__ == "__main__":
    raise SystemExit(main())
