import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.harness_request_guard import MAX_OUTPUT_TOKENS, MODEL_ID, make_server


class MockUpstageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        self.server.received.append(json.loads(raw.decode("utf-8")))
        body = json.dumps({
            "id": "chatcmpl-local-mock",
            "object": "chat.completion",
            "model": MODEL_ID,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "LOCAL_MOCK_ONLY"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 9, "completion_tokens": 4, "total_tokens": 13},
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def post_json(url, body):
    payload = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "Authorization": "Bearer LOCAL_DUMMY_ONLY"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def request_body():
    return {
        "model": "upstage/" + MODEL_ID,
        "temperature": 0.7,
        "max_completion_tokens": 5000,
        "stream": True,
        "store": False,
        "unrecognized_vendor_field": "must_be_removed",
        "tools": [{"type": "function", "function": {"name": "must_be_removed", "parameters": {"type": "object"}}}],
        "messages": [{"role": "user", "content": "Same frozen comparison request."}],
    }


class RequestGuardMockTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.mock = ThreadingHTTPServer(("127.0.0.1", 0), MockUpstageHandler)
        self.mock.received = []
        self.mock_thread = threading.Thread(target=self.mock.serve_forever, daemon=True)
        self.mock_thread.start()
        self.old_key = os.environ.get("UPSTAGE_API_KEY")
        os.environ["UPSTAGE_API_KEY"] = "LOCAL_DUMMY_ONLY"
        self.servers = []

    def tearDown(self):
        for server in self.servers:
            server.shutdown()
            server.server_close()
        self.mock.shutdown()
        self.mock.server_close()
        if self.old_key is None:
            os.environ.pop("UPSTAGE_API_KEY", None)
        else:
            os.environ["UPSTAGE_API_KEY"] = self.old_key
        self.temp.cleanup()

    def start_guard(self, harness):
        server = make_server(
            harness,
            0,
            self.root / "ledger",
            self.root / "runs",
            f"http://127.0.0.1:{self.mock.server_address[1]}",
            timeout_seconds=5,
        )
        self.servers.append(server)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        return f"http://127.0.0.1:{server.server_address[1]}/v1/chat/completions"

    def test_total_two_posts_and_retry_rejection(self):
        opencode_url = self.start_guard("opencode")
        pi_url = self.start_guard("pi")
        status, raw = post_json(opencode_url, request_body())
        self.assertEqual(status, 200)
        self.assertIn(b"LOCAL_MOCK_ONLY", raw)
        status, _ = post_json(opencode_url, request_body())
        self.assertEqual(status, 409)
        status, _ = post_json(pi_url, request_body())
        self.assertEqual(status, 200)
        status, _ = post_json(pi_url, request_body())
        self.assertEqual(status, 409)
        self.assertEqual(len(self.mock.received), 2)
        for forwarded in self.mock.received:
            self.assertEqual(forwarded["model"], MODEL_ID)
            self.assertEqual(forwarded["temperature"], 0)
            self.assertEqual(forwarded["reasoning_effort"], "none")
            self.assertEqual(forwarded["max_tokens"], MAX_OUTPUT_TOKENS)
            self.assertEqual(forwarded["n"], 1)
            self.assertFalse(forwarded["stream"])
            self.assertNotIn("tools", forwarded)
            self.assertNotIn("max_completion_tokens", forwarded)
            self.assertNotIn("store", forwarded)
            self.assertNotIn("unrecognized_vendor_field", forwarded)
        all_bytes = b"".join(p.read_bytes() for p in (self.root / "runs").rglob("*") if p.is_file())
        self.assertNotIn(b"LOCAL_DUMMY_ONLY", all_bytes)
        ledger = json.loads((self.root / "ledger" / "usage-ledger.json").read_text(encoding="utf-8"))
        self.assertEqual(len(ledger["calls"]), 2)
        meta_files = list((self.root / "runs").rglob("metadata.json"))
        for meta_file in meta_files:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            self.assertEqual(meta["reserved_max_cost_usd_including_vat"], 0.132)
            removed = meta["request_controls"]["removed_unsupported_request_fields"]
            self.assertIn("store", removed)
            self.assertIn("unrecognized_vendor_field", removed)
        restarted = make_server(
            "opencode",
            0,
            self.root / "ledger",
            self.root / "retry-runs",
            f"http://127.0.0.1:{self.mock.server_address[1]}",
            timeout_seconds=5,
        )
        self.servers.append(restarted)
        threading.Thread(target=restarted.serve_forever, daemon=True).start()
        status, _ = post_json(f"http://127.0.0.1:{restarted.server_address[1]}/v1/chat/completions", request_body())
        self.assertEqual(status, 409)
        self.assertEqual(len(self.mock.received), 2)

    def test_cumulative_ledger_carries_prior_usage_and_hard_budget(self):
        state_dir = self.root / "cumulative-ledger"
        state_dir.mkdir()
        prior = {
            "baseline_usage_usd": 0.08,
            "max_external_posts": 4,
            "max_per_harness": 2,
            "cumulative_budget_usd": 1.0,
            "calls": [
                {"harness": "opencode", "run_id": "opencode-trial-01", "reserved_max_cost_usd_including_vat": 0.132},
                {"harness": "pi", "run_id": "pi-trial-01", "reserved_max_cost_usd_including_vat": 0.132},
            ],
        }
        (state_dir / "usage-ledger.json").write_text(json.dumps(prior), encoding="utf-8")
        ledger = __import__("scripts.harness_request_guard", fromlist=["UsageLedger"]).UsageLedger(
            state_dir, max_total_posts=4, max_per_harness=2, cumulative_budget_usd=1.0
        )
        accepted = ledger.reserve("opencode", "opencode-trial-02")
        self.assertEqual(accepted["reserved_max_cost_usd_including_vat"], 0.132)
        with self.assertRaises(Exception):
            ledger.reserve("opencode", "opencode-trial-02")
        self.assertEqual(len(json.loads((state_dir / "usage-ledger.json").read_text())["calls"]), 3)

        over = self.root / "over-budget-ledger"
        over.mkdir()
        (over / "usage-ledger.json").write_text(json.dumps({"baseline_usage_usd": 0.9, "calls": []}), encoding="utf-8")
        bounded = __import__("scripts.harness_request_guard", fromlist=["UsageLedger"]).UsageLedger(
            over, max_total_posts=4, max_per_harness=2, cumulative_budget_usd=1.0
        )
        with self.assertRaises(Exception):
            bounded.reserve("opencode", "opencode-trial-02")
        self.assertEqual(json.loads((over / "usage-ledger.json").read_text())["calls"], [])

    def test_oversized_request_rejected_without_consuming_slot(self):
        url = self.start_guard("opencode")
        body = request_body()
        body["messages"][0]["content"] = "x" * 351_000
        status, _ = post_json(url, body)
        self.assertEqual(status, 413)
        self.assertEqual(len(self.mock.received), 0)
        status, _ = post_json(url, request_body())
        self.assertEqual(status, 200)
        self.assertEqual(len(self.mock.received), 1)
        metadata = next((self.root / "runs").rglob("metadata.json"))
        meta = json.loads(metadata.read_text(encoding="utf-8"))
        self.assertEqual(meta["reserved_max_cost_usd_including_vat"], 0.132)

    def test_output_over_cap_rejected_without_upstream(self):
        url = self.start_guard("pi")
        body = request_body()
        body["max_completion_tokens"] = MAX_OUTPUT_TOKENS + 1
        status, _ = post_json(url, body)
        self.assertEqual(status, 400)
        self.assertEqual(len(self.mock.received), 0)

    def test_missing_key_does_not_send_or_reserve(self):
        url = self.start_guard("pi")
        os.environ.pop("UPSTAGE_API_KEY", None)
        status, _ = post_json(url, request_body())
        self.assertEqual(status, 503)
        self.assertEqual(len(self.mock.received), 0)
        self.assertFalse((self.root / "ledger" / "usage-ledger.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
