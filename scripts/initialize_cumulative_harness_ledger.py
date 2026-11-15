"""Create a new cumulative ledger without changing the prior trial ledger."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_BUDGET_USD = 1.0
HISTORICAL_USER_REPORTED_USAGE_USD = 0.08


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="never overwrites an existing cumulative ledger")
    args = parser.parse_args()
    source = ROOT / "analyses" / "harness-comparison" / "guard-state" / "usage-ledger.json"
    target_dir = ROOT / "analyses" / "harness-comparison" / "guard-state-cumulative"
    target = target_dir / "usage-ledger.json"
    if not source.is_file():
        raise SystemExit("Prior trial ledger is missing; refusing to initialize a new cumulative ledger.")
    if target.exists():
        raise SystemExit("Cumulative ledger already exists; refusing reset/replay.")
    old_bytes = source.read_bytes()
    old = json.loads(old_bytes.decode("utf-8-sig"))
    prior_calls = old.get("calls")
    if not isinstance(prior_calls, list) or len(prior_calls) != 2:
        raise SystemExit("Expected exactly two prior upstream attempts; cumulative run remains blocked.")
    if {call.get("run_id") for call in prior_calls} != {"opencode-trial-01", "pi-trial-01"}:
        raise SystemExit("Prior run IDs differ from expected; refusing to guess cumulative exposure.")
    target_dir.mkdir(parents=True, exist_ok=False)
    state = {
        "ledger_version": 2,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source_ledger_path": "analyses/harness-comparison/guard-state/usage-ledger.json",
        "source_ledger_sha256": hashlib.sha256(old_bytes).hexdigest().upper(),
        "baseline_usage_usd": HISTORICAL_USER_REPORTED_USAGE_USD,
        "baseline_usage_basis": "user-reported 2026-11-02 Solar Pro 4 Usage record: $0.08 charged to credits; coupon identity not shown",
        "max_external_posts": 4,
        "max_per_harness": 2,
        "cumulative_budget_usd": MAX_BUDGET_USD,
        "new_run_ids_allowed": {"opencode": "opencode-trial-02", "pi": "pi-trial-02"},
        "calls": prior_calls,
        "account_usage_after_prior_trials": "not independently inspected; previous OpenCode cost estimate $0.0197316 ex VAT; Pi HTTP 400 supplied no usage",
    }
    temp = target.with_suffix(".json.tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, target)
    worst_prior = HISTORICAL_USER_REPORTED_USAGE_USD + sum(float(c.get("reserved_max_cost_usd_including_vat", 0)) for c in prior_calls)
    per_new = 0.132
    worst_all = worst_prior + 2 * per_new
    if worst_all > MAX_BUDGET_USD:
        target.unlink(missing_ok=True)
        target_dir.rmdir()
        raise SystemExit("Prior plus proposed reservations would exceed $1; no live call is permitted.")
    print(json.dumps({
        "new_ledger": str(target.relative_to(ROOT)),
        "prior_ledger_preserved": True,
        "prior_posts_imported": len(prior_calls),
        "user_reported_prior_credit_usage_usd": HISTORICAL_USER_REPORTED_USAGE_USD,
        "prior_reserved_max_usd": round(sum(float(c.get("reserved_max_cost_usd_including_vat", 0)) for c in prior_calls), 6),
        "new_trial_reserved_max_usd": 0.264,
        "cumulative_worst_case_usd": round(worst_all, 6),
        "hard_budget_usd": MAX_BUDGET_USD,
        "secret_value_printed": False,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
