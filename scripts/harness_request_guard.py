"""Single-pass, local OpenAI-compatible proxy for the two Solar harness trials.

It forwards at most one Chat Completions POST per harness and two total. The
claim is persisted before forwarding, so a client retry or proxy restart cannot
create another paid upstream attempt. No credentials are written to disk/logs.
"""
from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
API_KEY_ENV = "UPSTAGE_API_KEY"
MODEL_ID = "solar-pro4-260806"
API_ORIGIN = "https://api.upstage.ai"
MAX_TOTAL_POSTS = 2
MAX_POSTS_PER_HARNESS = 1
MAX_BODY_BYTES = 350_000
MAX_INPUT_TOKENS = 360_000
MAX_OUTPUT_TOKENS = 10_000
MAX_MESSAGES = 8
PRICE_INPUT = 0.30
PRICE_OUTPUT = 1.20
VAT = 0.10
RESERVED_COST_PER_CALL = ((MAX_INPUT_TOKENS * PRICE_INPUT) + (MAX_OUTPUT_TOKENS * PRICE_OUTPUT)) / 1_000_000 * (1 + VAT)
HARNESS_PORTS = {"opencode": 18710, "pi": 18711}
RUN_IDS = {"opencode": "opencode-trial-01", "pi": "pi-trial-01"}
NEW_TRIAL_RUN_IDS = {"opencode": "opencode-trial-02", "pi": "pi-trial-02"}
UPSTREAM_FIELDS = {
    "model", "messages", "temperature", "reasoning_effort", "max_tokens",
    "n", "stream", "prompt_cache_key", "top_p", "frequency_penalty",
    "presence_penalty", "stop",
}
MAX_CUMULATIVE_BUDGET_USD = 1.0


class GuardError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # A redirect must never create a second external request or forward data.
        return None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


class UsageLedger:
    """Small cross-process ledger protected by a Windows/POSIX file lock."""

    def __init__(self, state_dir: Path, max_total_posts: int = MAX_TOTAL_POSTS,
                 max_per_harness: int = MAX_POSTS_PER_HARNESS,
                 cumulative_budget_usd: float = MAX_CUMULATIVE_BUDGET_USD,
                 reserved_max_cost_usd_including_vat: float | None = None):
        self.state_dir = state_dir
        self.max_total_posts = max_total_posts
        self.max_per_harness = max_per_harness
        self.cumulative_budget_usd = cumulative_budget_usd
        self.reserved_max_cost_usd_including_vat = reserved_max_cost_usd_including_vat or RESERVED_COST_PER_CALL
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.path = state_dir / "usage-ledger.json"
        self.lock_path = state_dir / "usage-ledger.lock"

    def _lock(self):
        handle = open(self.lock_path, "a+b")
        handle.seek(0, os.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        return handle

    @staticmethod
    def _unlock(handle) -> None:
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()

    def reserve(self, harness: str, run_id: str) -> dict[str, Any]:
        lock = self._lock()
        try:
            if self.path.exists():
                state = json.loads(self.path.read_text(encoding="utf-8"))
            else:
                state = {"max_external_posts": self.max_total_posts, "calls": [], "baseline_usage_usd": 0.0}
            calls = state.get("calls", [])
            if any(c.get("run_id") == run_id for c in calls):
                raise GuardError(409, f"The external request slot for run {run_id} is already consumed.")
            if sum(c.get("harness") == harness for c in calls) >= self.max_per_harness:
                raise GuardError(409, f"The cumulative request allowance for {harness} is exhausted.")
            if len(calls) >= self.max_total_posts:
                raise GuardError(409, "The cumulative external-request cap is exhausted.")
            def call_cost_for_budget(call: dict[str, Any]) -> float:
                # Explicit null means usage was not returned; retain the reservation.
                value = call.get("actual_cost_usd_including_vat")
                if value is None:
                    value = call.get("estimated_actual_cost_usd_including_vat")
                if value is None:
                    value = call.get("reserved_max_cost_usd_including_vat", 0.0)
                return float(value or 0.0)
            cumulative_reserved = float(state.get("baseline_usage_usd", 0.0)) + sum(call_cost_for_budget(c) for c in calls)
            if cumulative_reserved + self.reserved_max_cost_usd_including_vat > self.cumulative_budget_usd + 1e-9:
                raise GuardError(409, "The cumulative $1 credit-use budget would be exceeded.")
            record = {
                "harness": harness,
                "run_id": run_id,
                "reserved_at_utc": utc_now(),
                "reserved_max_cost_usd_including_vat": round(self.reserved_max_cost_usd_including_vat, 8),
                "state": "reserved_before_upstream_send",
            }
            state["max_external_posts"] = self.max_total_posts
            state["max_per_harness"] = self.max_per_harness
            state["cumulative_budget_usd"] = self.cumulative_budget_usd
            state["calls"] = calls + [record]
            temp = self.path.with_suffix(".json.tmp")
            temp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(temp, self.path)
            return record
        finally:
            self._unlock(lock)

    def update_last(self, harness: str, run_id: str, changes: dict[str, Any]) -> None:
        lock = self._lock()
        try:
            if not self.path.exists():
                return
            state = json.loads(self.path.read_text(encoding="utf-8"))
            for call in reversed(state.get("calls", [])):
                if call.get("harness") == harness and call.get("run_id") == run_id:
                    call.update(changes)
                    break
            temp = self.path.with_suffix(".json.tmp")
            temp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(temp, self.path)
        finally:
            self._unlock(lock)


def _extract_text_and_validate(messages: Any) -> int:
    if not isinstance(messages, list) or not messages or len(messages) > MAX_MESSAGES:
        raise GuardError(413, f"Request must contain 1–{MAX_MESSAGES} messages.")
    total_bytes = 0
    for message in messages:
        if not isinstance(message, dict) or message.get("role") not in {"system", "developer", "user", "assistant"}:
            raise GuardError(400, "Only text chat messages are permitted; tool/result roles are disabled.")
        if message.get("tool_calls") or message.get("function_call"):
            raise GuardError(400, "Tool/function calls are disabled for the one-request comparison.")
        content = message.get("content")
        if isinstance(content, str):
            total_bytes += len(content.encode("utf-8"))
        elif isinstance(content, list):
            for item in content:
                if not isinstance(item, dict) or item.get("type") != "text" or not isinstance(item.get("text"), str):
                    raise GuardError(400, "Only text content is permitted.")
                total_bytes += len(item["text"].encode("utf-8"))
        else:
            raise GuardError(400, "Every message must contain plain text.")
    # BPE tokens cannot exceed ordinary UTF-8 content bytes; reserve a generous
    # 10k-token allowance for role/message framing and service serialization.
    if total_bytes + 10_000 > MAX_INPUT_TOKENS:
        raise GuardError(413, f"Estimated input exceeds the {MAX_INPUT_TOKENS}-token safety ceiling.")
    return total_bytes


def prepare_request(raw: bytes) -> tuple[dict[str, Any], int, list[str], bool]:
    if len(raw) > MAX_BODY_BYTES:
        raise GuardError(413, f"Serialized request exceeds {MAX_BODY_BYTES} bytes.")
    try:
        body = json.loads(raw.decode("utf-8"))
    except Exception:
        raise GuardError(400, "Request body must be UTF-8 JSON.") from None
    if not isinstance(body, dict):
        raise GuardError(400, "Request body must be a JSON object.")
    client_wants_stream = body.get("stream") is True
    if body.get("model") not in {MODEL_ID, "upstage/" + MODEL_ID}:
        raise GuardError(400, f"Only the pinned model {MODEL_ID} is allowed.")
    messages = body.get("messages")
    content_bytes = _extract_text_and_validate(messages)
    for key in ("max_tokens", "max_completion_tokens"):
        if key in body:
            try:
                value = int(body[key])
            except (ValueError, TypeError):
                raise GuardError(400, f"{key} must be an integer.") from None
            if value <= 0 or value > MAX_OUTPUT_TOKENS:
                raise GuardError(400, f"Output limit must be between 1 and {MAX_OUTPUT_TOKENS} tokens.")
    for forbidden in ("api_key", "authorization"):
        if forbidden in body:
            raise GuardError(400, "Credentials are accepted only through the process environment.")
    # Keep only fields verified against Upstage Chat Completions. In particular,
    # Pi's default `store` field is not accepted by Upstage.
    removed_fields = sorted(set(body) - UPSTREAM_FIELDS)
    body = {key: value for key, value in body.items() if key in UPSTREAM_FIELDS}
    # Normalize safety-critical settings identically, regardless of harness defaults.
    body["model"] = MODEL_ID
    body["temperature"] = 0
    body["reasoning_effort"] = "none"
    body["max_tokens"] = MAX_OUTPUT_TOKENS
    body["n"] = 1
    body["stream"] = False
    for key in ("max_completion_tokens", "tools", "tool_choice", "functions", "function_call", "parallel_tool_calls", "stream_options"):
        body.pop(key, None)
    return body, content_bytes, removed_fields, client_wants_stream


def encode_sse_completion(response: dict[str, Any]) -> bytes | None:
    """Adapt the guard's single non-stream upstream result for streaming clients."""
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        return None
    message = choices[0].get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        return None
    base = {"id": response.get("id"), "object": "chat.completion.chunk", "created": response.get("created"), "model": response.get("model", MODEL_ID)}
    chunks = [
        {**base, "choices": [{"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}]},
        {**base, "choices": [{"index": 0, "delta": {"content": message["content"]}, "finish_reason": None}]},
        {**base, "choices": [{"index": 0, "delta": {}, "finish_reason": choices[0].get("finish_reason", "stop")}]},
    ]
    return b"".join(b"data: " + json.dumps(chunk, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n\n" for chunk in chunks) + b"data: [DONE]\n\n"


class GuardHandler(BaseHTTPRequestHandler):
    server_version = "BenzocaineHarnessGuard/1.0"
    sys_version = ""
    config: dict[str, Any]

    def log_message(self, fmt: str, *args) -> None:
        # Request paths are safe; never log headers, body, API keys, or prompts.
        self.config["logger"](f"{self.config['harness']} local {self.command} {self.path} {args[1] if len(args)>1 else ''}".strip())

    def _reply(self, status: int, payload: bytes, content_type: str = "application/json") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def _json_error(self, status: int, message: str) -> None:
        payload = json.dumps({"error": {"type": "request_guard", "message": message}}).encode("utf-8")
        self._reply(status, payload)

    def do_GET(self) -> None:
        if self.path.rstrip("/") in {"/v1/models", "/models"}:
            payload = json.dumps({"object": "list", "data": [{"id": MODEL_ID, "object": "model", "owned_by": "upstage"}]}).encode()
            return self._reply(200, payload)
        self._json_error(404, "Only local model-list discovery is available.")

    def do_POST(self) -> None:
        if self.path.rstrip("/") not in {"/v1/chat/completions", "/chat/completions"}:
            return self._json_error(404, "Only Chat Completions is allowed.")
        if not os.environ.get(API_KEY_ENV):
            return self._json_error(503, f"{API_KEY_ENV} is not available to the guarded process.")
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            return self._json_error(400, "Invalid Content-Length.")
        if length < 0 or length > MAX_BODY_BYTES:
            return self._json_error(413, f"Request body must be at most {MAX_BODY_BYTES} bytes.")
        raw = self.rfile.read(length)
        try:
            body, content_bytes, removed_fields, client_wants_stream = prepare_request(raw)
        except GuardError as exc:
            return self._json_error(exc.status, str(exc))
        run_dir: Path = self.config["output_root"] / self.config["run_id"]
        if run_dir.exists():
            return self._json_error(409, "Run output already exists; overwrite/replay is blocked.")
        try:
            run_dir.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            return self._json_error(409, "Run output already exists; overwrite/replay is blocked.")
        try:
            reservation = self.config["ledger"].reserve(self.config["harness"], self.config["run_id"])
        except GuardError as exc:
            return self._json_error(exc.status, str(exc))
        request_bytes = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        (run_dir / "request.redacted.json").write_bytes(request_bytes)
        self.config["logger"](f"{self.config['harness']} reserved its single upstream request; input_bytes={content_bytes}; request_body_bytes={len(request_bytes)}")
        start = time.perf_counter()
        status = 502
        response_body = b""
        response_headers: dict[str, str] = {}
        error = None
        upstream_url = self.config["upstream_base_url"].rstrip("/") + "/v1/chat/completions"
        headers = {
            "Authorization": "Bearer " + os.environ[API_KEY_ENV],
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Content-Length": str(len(request_bytes)),
        }
        req = urllib.request.Request(upstream_url, data=request_bytes, headers=headers, method="POST")
        try:
            # urllib does not retry; the durable ledger also blocks any client retry.
            opener = urllib.request.build_opener(_NoRedirect)
            with opener.open(req, timeout=self.config["timeout_seconds"]) as response:
                status = response.status
                response_headers = {"content-type": response.headers.get("Content-Type", "application/json")}
                response_body = response.read()
        except urllib.error.HTTPError as exc:
            status = exc.code
            response_headers = {"content-type": exc.headers.get("Content-Type", "application/json")}
            response_body = exc.read()
        except Exception as exc:  # do not include exception repr; it may contain request details
            error = type(exc).__name__
            response_body = json.dumps({"error": {"type": "upstream_transport", "message": error}}).encode("utf-8")
        elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
        (run_dir / "response.raw.json").write_bytes(response_body)
        try:
            decoded = json.loads(response_body.decode("utf-8"))
        except Exception:
            decoded = None
        usage = decoded.get("usage", {}) if isinstance(decoded, dict) else {}
        input_tokens = usage.get("prompt_tokens", usage.get("input_tokens"))
        output_tokens = usage.get("completion_tokens", usage.get("output_tokens"))
        cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0) if isinstance(usage, dict) else 0
        actual_cost = None
        if isinstance(input_tokens, (int, float)) and isinstance(output_tokens, (int, float)):
            uncached = max(0, input_tokens - (cached or 0))
            actual_cost = round((uncached * PRICE_INPUT + (cached or 0) * 0.06 + output_tokens * PRICE_OUTPUT) / 1_000_000, 8)
        meta = {
            "harness": self.config["harness"],
            "run_id": self.config["run_id"],
            "timestamp_utc": utc_now(),
            "upstream_model": decoded.get("model") if isinstance(decoded, dict) else None,
            "upstream_status": status,
            "latency_ms": elapsed_ms,
            "usage": usage,
            "estimated_api_cost_usd_ex_vat": actual_cost,
            "estimated_api_cost_usd_including_vat": round(actual_cost * (1 + VAT), 8) if actual_cost is not None else None,
            "cached_input_tokens": cached,
            "input_utf8_bytes": content_bytes,
            "serialized_request_bytes": len(request_bytes),
            "request_controls": {"upstream_posts_total_max": self.config["max_total_posts"], "upstream_posts_this_harness_max": self.config["max_per_harness"], "cumulative_budget_usd": self.config["cumulative_budget_usd"], "max_input_tokens_estimate": MAX_INPUT_TOKENS, "max_output_tokens": MAX_OUTPUT_TOKENS, "temperature": 0, "reasoning_effort": "none", "tools": "disabled", "retries_to_upstream": 0, "removed_unsupported_request_fields": removed_fields},
            "reserved_max_cost_usd_including_vat": round(self.reserved_max_cost_usd_including_vat, 8),
            "transport_error_type": error,
            "api_key_logged": False,
            "auto_retry": False,
        }
        (run_dir / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        self.config["ledger"].update_last(self.config["harness"], self.config["run_id"], {"completed_at_utc": utc_now(), "http_status": status, "latency_ms": elapsed_ms, "input_tokens": input_tokens, "output_tokens": output_tokens, "actual_cost_usd_ex_vat": actual_cost, "actual_cost_usd_including_vat": round(actual_cost * (1 + VAT), 8) if actual_cost is not None else None, "transport_error_type": error})
        if status == 200 and client_wants_stream and isinstance(decoded, dict):
            stream_body = encode_sse_completion(decoded)
            if stream_body is not None:
                return self._reply(status, stream_body, "text/event-stream; charset=utf-8")
        self._reply(status, response_body or b"{}", response_headers.get("content-type", "application/json"))


def make_server(harness: str, port: int, state_dir: Path, output_root: Path, upstream_base_url: str = API_ORIGIN, timeout_seconds: int = 180, run_id: str | None = None, max_total_posts: int = MAX_TOTAL_POSTS, max_per_harness: int = MAX_POSTS_PER_HARNESS, cumulative_budget_usd: float = MAX_CUMULATIVE_BUDGET_USD) -> ThreadingHTTPServer:
    if harness not in HARNESS_PORTS:
        raise ValueError("harness must be opencode or pi")
    if not re.fullmatch(r"https?://(?:127\.0\.0\.1|localhost)(?::\d+)?", upstream_base_url) and upstream_base_url != API_ORIGIN:
        raise ValueError("Custom upstream URL must be loopback for mock tests or the official Upstage API origin.")
    run_id = run_id or RUN_IDS[harness]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+", run_id):
        raise ValueError("run_id must be a lowercase alphanumeric dash-separated identifier")
    if max_total_posts < 1 or max_per_harness < 1 or not 0 < cumulative_budget_usd <= MAX_CUMULATIVE_BUDGET_USD:
        raise ValueError("request/budget caps are invalid or exceed the hard $1 cumulative ceiling")
    logger = lambda message: print(message, flush=True)
    config = {"harness": harness, "run_id": run_id, "ledger": UsageLedger(state_dir, max_total_posts, max_per_harness, cumulative_budget_usd), "output_root": output_root, "upstream_base_url": upstream_base_url, "timeout_seconds": timeout_seconds, "logger": logger, "max_total_posts": max_total_posts, "max_per_harness": max_per_harness, "cumulative_budget_usd": cumulative_budget_usd}
    handler = type(f"{harness.title()}GuardHandler", (GuardHandler,), {"config": config})
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def main() -> int:
    parser = argparse.ArgumentParser(description="One-request-per-harness Upstage proxy; no retry or secret logging.")
    parser.add_argument("--harness", choices=sorted(HARNESS_PORTS), required=True)
    parser.add_argument("--port", type=int)
    parser.add_argument("--state-dir", type=Path, default=ROOT / "analyses" / "harness-comparison" / "guard-state")
    parser.add_argument("--output-root", type=Path, default=ROOT / "results" / "harness-comparison" / "runs")
    parser.add_argument("--upstream-base-url", default=API_ORIGIN, help=argparse.SUPPRESS)
    parser.add_argument("--run-id")
    parser.add_argument("--max-total-posts", type=int, default=MAX_TOTAL_POSTS)
    parser.add_argument("--max-per-harness", type=int, default=MAX_POSTS_PER_HARNESS)
    parser.add_argument("--cumulative-budget-usd", type=float, default=MAX_CUMULATIVE_BUDGET_USD)
    parser.add_argument("--allow-live", action="store_true", help="required to permit upstream forwarding; never set by tests")
    parser.add_argument("--dry-run", action="store_true", help="show non-secret configuration only")
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps({"harness": args.harness, "run_id": args.run_id or RUN_IDS[args.harness], "port": args.port or HARNESS_PORTS[args.harness], "model": MODEL_ID, "max_external_posts_total": args.max_total_posts, "max_per_harness": args.max_per_harness, "cumulative_budget_usd": args.cumulative_budget_usd, "max_input_tokens_estimate": MAX_INPUT_TOKENS, "max_output_tokens": MAX_OUTPUT_TOKENS, "max_cost_per_call_including_vat_usd": round(RESERVED_COST_PER_CALL, 6), "secret_value_printed": False, "network_started": False}, indent=2))
        return 0
    if not args.allow_live:
        parser.error("live proxy start requires --allow-live; tests must use a loopback mock upstream")
    if args.run_id != NEW_TRIAL_RUN_IDS[args.harness]:
        parser.error("live trial requires the unique approved run ID for this harness")
    if args.max_total_posts != 4 or args.max_per_harness != 2 or abs(args.cumulative_budget_usd - MAX_CUMULATIVE_BUDGET_USD) > 1e-9:
        parser.error("live trial caps are fixed at 4 lifetime posts, 2 per harness, and $1 cumulative")
    port = args.port or HARNESS_PORTS[args.harness]
    if args.run_id in NEW_TRIAL_RUN_IDS.values() and NEW_TRIAL_RUN_IDS[args.harness] != args.run_id:
        parser.error("run id does not match the selected harness")
    server = make_server(args.harness, port, args.state_dir, args.output_root, args.upstream_base_url, run_id=args.run_id, max_total_posts=args.max_total_posts, max_per_harness=args.max_per_harness, cumulative_budget_usd=args.cumulative_budget_usd)
    print(json.dumps({"status": "listening_loopback", "harness": args.harness, "run_id": args.run_id or RUN_IDS[args.harness], "port": port, "secret_value_printed": False, "forwarding_enabled": True}), flush=True)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
