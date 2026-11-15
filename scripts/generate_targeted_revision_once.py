"""One-shot, credit-bounded Solar Pro 4 authoring call for targeted report edits."""
import argparse, hashlib, json, os, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

MODEL = "solar-pro4-260806"
API_URL = "https://api.upstage.ai/v1/chat/completions"
PRICE_INPUT = 0.30
PRICE_OUTPUT = 1.20
VAT = 0.10
MAX_CUMULATIVE_USD = 1.00
RESERVED_USD = 0.02
MAX_INPUT_BYTE_BOUND = 44_000
MAX_OUTPUT_TOKENS = 4_000
RUN_ID = "benzocaine-integrated-conclusion-20261110-01"


def load_env_key(path):
    if "UPSTAGE_API_KEY" in os.environ and os.environ["UPSTAGE_API_KEY"].strip():
        return os.environ["UPSTAGE_API_KEY"].strip()
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        if name.strip() == "UPSTAGE_API_KEY":
            value = value.strip().strip("\"'")
            if value:
                return value
    return ""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--skill", type=Path, required=True)
    p.add_argument("--user-prompt", type=Path, required=True)
    p.add_argument("--env-file", type=Path, required=True)
    p.add_argument("--prior-ledger", type=Path, required=True)
    p.add_argument("--execute-live", action="store_true")
    a = p.parse_args()
    out = a.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    attempt = out / "solar-call"
    attempt.mkdir(exist_ok=True)
    status_path = attempt / "solar-status.json"
    if status_path.exists() or (attempt / "solar-response.raw.json").exists():
        raise FileExistsError("Refusing to repeat or overwrite a Solar attempt")
    skill = a.skill.read_text(encoding="utf-8")
    user = a.user_prompt.read_text(encoding="utf-8")
    content_bytes = len(skill.encode("utf-8")) + len(user.encode("utf-8"))
    input_byte_bound = content_bytes + 2048
    budget = json.loads(a.prior_ledger.read_text(encoding="utf-8"))
    cumulative = float(budget["conservative_cumulative_after_usd"])
    est_uncached_cost = (input_byte_bound * PRICE_INPUT + MAX_OUTPUT_TOKENS * PRICE_OUTPUT) / 1_000_000
    estimate_inc_vat = round(est_uncached_cost * (1 + VAT), 8)
    if cumulative + RESERVED_USD > MAX_CUMULATIVE_USD + 1e-9:
        raise SystemExit("Budget guard: cumulative cap would be exceeded; no request sent.")
    if input_byte_bound > MAX_INPUT_BYTE_BOUND or estimate_inc_vat > RESERVED_USD:
        raise SystemExit("Token/cost guard: prepared request exceeds the reserved $0.02; no request sent.")
    request = {
        "model": MODEL,
        "messages": [{"role": "system", "content": skill}, {"role": "user", "content": user}],
        "temperature": 0,
        "reasoning_effort": "none",
        "max_tokens": MAX_OUTPUT_TOKENS,
        "n": 1,
        "stream": False,
    }
    body = json.dumps(request, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    request_hash = hashlib.sha256(body).hexdigest()
    (attempt / "solar-request.redacted.json").write_bytes(body)
    pre = {
        "status": "prepared",
        "run_id": RUN_ID,
        "model": MODEL,
        "request_sha256": request_hash,
        "request_content_bytes": content_bytes,
        "conservative_input_token_upper_bound": input_byte_bound,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "max_external_posts": 1,
        "retries": 0,
        "estimated_max_cost_including_vat_usd": estimate_inc_vat,
        "reserved_max_cost_including_vat_usd": RESERVED_USD,
        "prior_conservative_cumulative_usd": cumulative,
        "conservative_cumulative_with_reservation_usd": round(cumulative + RESERVED_USD, 8),
        "remaining_under_cap_after_reservation_usd": round(MAX_CUMULATIVE_USD - cumulative - RESERVED_USD, 8),
        "api_key_value_logged": False,
        "solar_request_sent": False,
    }
    (attempt / "pre-call-budget.json").write_text(json.dumps(pre, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not a.execute_live:
        print(json.dumps(pre, ensure_ascii=False, indent=2))
        return 0
    key = load_env_key(a.env_file)
    if not key:
        status_path.write_text(json.dumps({**pre, "status": "blocked_missing_key", "api_key_present": False}, indent=2), encoding="utf-8")
        print("Solar call not sent: UPSTAGE_API_KEY is not configured.")
        return 2
    if status_path.exists():
        raise FileExistsError("Solar status already exists; one request maximum")
    status_path.write_text(json.dumps({**pre, "status": "reserved_before_send", "api_key_present": True}, indent=2), encoding="utf-8")
    start = time.perf_counter()
    http_status = None
    error_type = None
    raw = b""
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }, method="POST")
    try:
        opener = urllib.request.build_opener(NoRedirect)
        with opener.open(req, timeout=180) as response:
            http_status = response.status
            raw = response.read()
    except urllib.error.HTTPError as exc:
        http_status = exc.code
        raw = exc.read()
    except Exception as exc:
        error_type = type(exc).__name__
        raw = json.dumps({"transport_error_type": error_type}).encode("utf-8")
    elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
    (attempt / "solar-response.raw.json").write_bytes(raw)
    try:
        decoded = json.loads(raw.decode("utf-8"))
    except Exception:
        decoded = {}
    usage = decoded.get("usage") if isinstance(decoded, dict) else None
    input_tokens = (usage or {}).get("prompt_tokens", (usage or {}).get("input_tokens")) if isinstance(usage, dict) else None
    output_tokens = (usage or {}).get("completion_tokens", (usage or {}).get("output_tokens")) if isinstance(usage, dict) else None
    cached = ((usage or {}).get("prompt_tokens_details") or {}).get("cached_tokens", 0) if isinstance(usage, dict) else 0
    actual_ex_vat = None
    if isinstance(input_tokens, (int, float)) and isinstance(output_tokens, (int, float)):
        actual_ex_vat = round(((max(0, input_tokens - (cached or 0)) * PRICE_INPUT) + (cached or 0) * 0.06 + output_tokens * PRICE_OUTPUT) / 1_000_000, 8)
    choice = (decoded.get("choices") or [{}])[0] if isinstance(decoded, dict) else {}
    message = choice.get("message") or {} if isinstance(choice, dict) else {}
    content = message.get("content") if isinstance(message, dict) else None
    finish = choice.get("finish_reason") if isinstance(choice, dict) else None
    returned_model = decoded.get("model") if isinstance(decoded, dict) else None
    ok = http_status == 200 and returned_model == MODEL and finish == "stop" and isinstance(content, str) and bool(content.strip())
    actual_inc_vat = round(actual_ex_vat * (1 + VAT), 8) if actual_ex_vat is not None else None
    post_cumulative = round(cumulative + (actual_inc_vat if actual_inc_vat is not None else RESERVED_USD), 8)
    final = {
        **pre,
        "status": "success" if ok else "failed_after_single_request",
        "http_status": http_status,
        "returned_model": returned_model,
        "finish_reason": finish,
        "latency_ms": elapsed_ms,
        "usage": usage,
        "actual_cost_usd_ex_vat": actual_ex_vat,
        "actual_cost_usd_including_vat": actual_inc_vat,
        "conservative_cumulative_after_usd": post_cumulative,
        "remaining_under_cap_after_usd": round(MAX_CUMULATIVE_USD - post_cumulative, 8),
        "retry_count": 0,
        "api_key_value_logged": False,
        "solar_request_sent": True,
        "transport_error_type": error_type,
        "response_sha256": hashlib.sha256(raw).hexdigest(),
    }
    status_path.write_text(json.dumps(final, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if ok:
        (attempt / "solar-revision-blocks.md").write_text(content, encoding="utf-8")
    ledger = {
        "previous_cumulative_usd": cumulative,
        "new_call_reserved_usd": RESERVED_USD,
        "new_call_actual_including_vat_usd": actual_inc_vat,
        "cumulative_after_usd": post_cumulative,
        "cap_usd": MAX_CUMULATIVE_USD,
        "cash_payment_or_topup": False,
        "calls": [{"run_id": RUN_ID, "request_sha256": request_hash,
                   "status": final["status"], "input_tokens": input_tokens,
                   "output_tokens": output_tokens, "actual_cost_usd_including_vat": actual_inc_vat,
                   "retry_count": 0}]
    }
    (out / "cost-ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: final[k] for k in ["status", "run_id", "http_status", "returned_model", "finish_reason", "latency_ms", "usage", "estimated_max_cost_including_vat_usd", "actual_cost_usd_including_vat", "conservative_cumulative_after_usd", "remaining_under_cap_after_usd", "retry_count", "api_key_value_logged"]}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
