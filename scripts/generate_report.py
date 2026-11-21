"""Prepare a target-neutral Solar report request and require a current budget gate before one paid POST."""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from _runtime import ROOT, load, save, digest
from harness_request_guard import API_KEY_ENV, API_ORIGIN, MODEL_ID, MAX_BODY_BYTES, PRICE_INPUT, PRICE_OUTPUT, VAT, UsageLedger, _NoRedirect

REPORT_MAX_INPUT_TOKENS = 380_000
REPORT_MAX_OUTPUT_TOKENS = 35_000
REPORT_RESERVED_COST = ((REPORT_MAX_INPUT_TOKENS * PRICE_INPUT) + (REPORT_MAX_OUTPUT_TOKENS * PRICE_OUTPUT)) / 1_000_000 * (1 + VAT)
BUDGET_SNAPSHOT_MAX_AGE_SECONDS = 24 * 60 * 60
LOCAL_PATH_RE = re.compile(r'(?i)(?:[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"<>]+(?:[\\/]+[^\\/\s\"<>]+)*|/(?:home|Users)/[^/\s\"<>]+(?:/[^/\s\"<>]+)*)')


def redact_local_paths(value):
    """Return a copy with workstation profile paths anonymized before model transmission."""
    count = 0
    def visit(item):
        nonlocal count
        if isinstance(item, dict): return {k: visit(v) for k, v in item.items()}
        if isinstance(item, list): return [visit(v) for v in item]
        if isinstance(item, str):
            result, n = LOCAL_PATH_RE.subn('<LOCAL_PATH>', item)
            count += n
            return result
        return item
    return visit(value), count


def build_request(run: Path, plan: dict) -> tuple[dict, Path]:
    evidence = load(run / 'report-evidence.json')
    for name, expected in evidence['source_hashes'].items():
        if digest(run / name) != expected:
            raise ValueError(f'Evidence source changed: {name}')
    skill = ROOT / plan.get('report_writing_skill_path', 'skill/report-writing/SKILL.md')
    if not skill.is_file():
        raise FileNotFoundError(f'Report-writing skill is missing: {skill.relative_to(ROOT)}')
    manifest = load(run / 'manifest.json')
    if manifest.get('artifact_type') == 'public_curated_evidence_derivative_not_execution_record':
        evidence['execution_record'] = {
            'artifact_type': manifest['artifact_type'],
            'source_run_id': manifest['source_run_id'],
            'source_execution_manifest_sha256': manifest['source_execution_manifest_sha256'],
            'prediction_statuses_from_source_run': manifest['prediction_statuses_from_source_run'],
            'new_inference_executed': False,
            'solar_call_executed': False,
        }
        evidence['public_derivation_record'] = load(run / 'public-derivation.json')
    else:
        evidence['execution_record'] = manifest
    evidence, local_path_redactions = redact_local_paths(evidence)
    figures = evidence.get('report_figure_assets', [])
    figure_index = json.dumps([{'figure_id': x['figure_id'], 'path': x['path'], 'sha256': x['sha256'], 'caption': x['caption']} for x in figures], ensure_ascii=False, indent=2)
    figure_markers = "\n".join(f"[figure: {x['figure_id']}]" for x in figures)
    user_content = (
        '보고서 작성 스킬과 실제 실행 근거에 따라 전체 한국어 보고서 원고를 작성하세요. 근거에 없는 값은 만들지 말고 누락 사항을 표시하세요.\n'
        + json.dumps(evidence, ensure_ascii=False)
        + '\n\n아래 figure manifest의 각 ID를 해당 설명 뒤에 정확히 한 번 표시하세요. 로컬 렌더러는 ID와 해시가 일치하는 파일만 삽입합니다. 그림을 본 것처럼 새 관찰을 주장하지 마세요.\n'
        + '--- BEGIN REPORT_FIGURE_ASSET_INDEX ---\n' + figure_index + '\n--- END REPORT_FIGURE_ASSET_INDEX ---\n'
        + '--- BEGIN MANDATORY_FIGURE_MARKERS ---\n' + figure_markers + '\n--- END MANDATORY_FIGURE_MARKERS ---'
    )
    request = {
        'model': plan['model'],
        'temperature': plan['temperature'],
        'reasoning_effort': 'none',
        'max_tokens': int(plan['max_tokens']),
        'n': 1,
        'stream': False,
        'messages': [
            {'role': 'system', 'content': skill.read_text(encoding='utf-8')},
            {'role': 'user', 'content': user_content},
        ],
    }
    validate_request(request)
    return request, skill, local_path_redactions


def validate_request(request: dict) -> int:
    if request.get('model') != MODEL_ID:
        raise ValueError('Request model does not match the pinned Solar snapshot')
    if request.get('n') != 1 or request.get('stream') is not False or request.get('tools'):
        raise ValueError('Only one non-streaming text completion without tools is allowed')
    if request.get('reasoning_effort') != 'none':
        raise ValueError('Report requests must keep reasoning_effort=none')
    output_limit = request.get('max_tokens')
    if not isinstance(output_limit, int) or not 1 <= output_limit <= REPORT_MAX_OUTPUT_TOKENS:
        raise ValueError('Output token limit is outside the report guard')
    messages = request.get('messages')
    if not isinstance(messages, list) or len(messages) != 2 or [m.get('role') for m in messages] != ['system', 'user']:
        raise ValueError('Request must contain exactly one system and one user message')
    if any(not isinstance(m.get('content'), str) for m in messages):
        raise ValueError('Only text messages are supported')
    content_bytes = sum(len(m['content'].encode('utf-8')) for m in messages)
    body = json.dumps(request, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if len(body) > MAX_BODY_BYTES:
        raise ValueError(f'Request body {len(body)} exceeds {MAX_BODY_BYTES} bytes')
    if content_bytes + 30_000 > REPORT_MAX_INPUT_TOKENS:
        raise ValueError(f'Conservative token ceiling {content_bytes + 30_000} exceeds {REPORT_MAX_INPUT_TOKENS}')
    return content_bytes


def verified_budget(plan: dict) -> tuple[dict, float, float]:
    if plan.get('paid_calls_authorized') is not True or plan.get('report_generation_authorized') is not True:
        raise ValueError('Paid calls and report generation are not currently authorized')
    snapshot = plan.get('live_budget_snapshot')
    if not isinstance(snapshot, dict) or snapshot.get('verified') is not True or snapshot.get('free_credit_only_confirmed') is not True:
        raise ValueError('A current verified free-credit-only budget snapshot is required')
    try:
        baseline = float(snapshot['project_cumulative_usd'])
        cap = float(snapshot['project_cap_usd'])
        stamp = datetime.fromisoformat(str(snapshot['as_of_utc']).replace('Z', '+00:00'))
    except (KeyError, TypeError, ValueError):
        raise ValueError('Budget snapshot needs numeric cumulative/cap values and ISO UTC timestamp') from None
    if stamp.tzinfo is None:
        raise ValueError('Budget snapshot timestamp must include a UTC offset')
    age = (datetime.now(timezone.utc) - stamp.astimezone(timezone.utc)).total_seconds()
    if age < 0 or age > BUDGET_SNAPSHOT_MAX_AGE_SECONDS or not snapshot.get('verification_source'):
        raise ValueError('Budget snapshot is stale, future-dated, or lacks its verification source')
    if baseline < 0 or cap <= 0 or baseline + REPORT_RESERVED_COST > cap + 1e-9:
        raise ValueError('Worst-case VAT-inclusive reservation exceeds the approved project cap')
    return snapshot, baseline, cap


def load_local_api_key() -> str:
    value = os.environ.get(API_KEY_ENV, '').strip()
    if value:
        return value
    env = ROOT / '.env'
    if env.is_file():
        for raw in env.read_text(encoding='utf-8-sig').splitlines():
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            name, candidate = line.split('=', 1)
            if name.strip() == API_KEY_ENV:
                return candidate.strip().strip('"\'')
    return ''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--attempt-id', required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prepare-only', action='store_true')
    group.add_argument('--execute-solar', action='store_true')
    args = parser.parse_args()
    if Path(args.attempt_id).name != args.attempt_id or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)+', args.attempt_id):
        parser.error('Use a simple lowercase dash-separated attempt ID')
    plan = load(ROOT / 'configs/report-plan.json')
    if args.execute_solar:
        try:
            snapshot, baseline, cap = verified_budget(plan)
        except ValueError as exc:
            parser.error(str(exc) + '; no API request was sent')
    run = args.run_dir.resolve()
    attempt = run / 'solar-attempts' / args.attempt_id
    if args.prepare_only:
        attempt.mkdir(parents=True, exist_ok=False)
        request, skill, local_path_redactions = build_request(run, plan)
        request_path = attempt / 'solar-request.json'
        serialized = json.dumps(request, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        request_path.write_bytes(serialized)
        content_bytes = validate_request(request)
        save(attempt / 'solar-prepare-status.json', {
            'status': 'prepared_not_executed', 'external_requests': 0, 'inference_executed': False,
            'model': plan['model'], 'report_writing_skill_path': skill.relative_to(ROOT).as_posix(),
            'skill_sha256': digest(skill), 'request_sha256': digest(request_path),
            'request_body_bytes': len(serialized), 'content_utf8_bytes': content_bytes,
            'local_path_redactions': local_path_redactions,
            'reserved_max_cost_usd_including_vat': round(REPORT_RESERVED_COST, 8),
        })
        print(json.dumps({'status': 'prepared_not_executed', 'external_requests': 0, 'request_body_bytes': len(serialized), 'content_utf8_bytes': content_bytes, 'local_path_redactions': local_path_redactions, 'worst_case_reservation_usd_including_vat': round(REPORT_RESERVED_COST, 8), 'key_value_printed': False}, ensure_ascii=False))
        return 0

    request_path = attempt / 'solar-request.json'
    prepare_path = attempt / 'solar-prepare-status.json'
    if not attempt.is_dir() or not request_path.is_file() or not prepare_path.is_file():
        parser.error('Execute requires a prepared request in this attempt directory')
    for name in ('solar-response.raw.json', 'solar-status.json', 'solar-execution-started.json'):
        if (attempt / name).exists():
            parser.error('Attempt already has an execution artifact; automatic retries are blocked')
    request = load(request_path)
    skill = ROOT / plan.get('report_writing_skill_path', 'skill/report-writing/SKILL.md')
    if request.get('messages', [{}])[0].get('content') != skill.read_text(encoding='utf-8'):
        parser.error('Prepared request does not contain the current report-writing skill')
    try:
        content_bytes = validate_request(request)
    except ValueError as exc:
        parser.error(str(exc))
    if digest(request_path) != load(prepare_path).get('request_sha256'):
        parser.error('Prepared request hash changed; no API request was sent')
    key = load_local_api_key()
    if not key:
        parser.error('UPSTAGE_API_KEY is missing; no key value is logged')
    try:
        run_manifest = load(run / 'manifest.json')
        run_id = str(run_manifest.get('run_id') or run.name)
    except Exception:
        run_id = run.name
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)+', run_id):
        parser.error('Run ID is invalid')
    state_dir = run / 'execution' / 'solar-budget-state'
    state_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = state_dir / 'usage-ledger.json'
    if not ledger_path.exists():
        save(ledger_path, {'max_external_posts': 1, 'calls': [], 'baseline_usage_usd': baseline, 'baseline_source': snapshot['verification_source'], 'baseline_recorded_at': snapshot['as_of_utc'], 'cumulative_cap_usd': cap, 'free_credit_only_confirmed': True})
    else:
        state = load(ledger_path)
        if float(state.get('baseline_usage_usd', -1)) != baseline or float(state.get('cumulative_cap_usd', -1)) != cap:
            parser.error('Existing run ledger disagrees with the current budget snapshot; no API request was sent')
    ledger = UsageLedger(state_dir, max_total_posts=1, max_per_harness=1, cumulative_budget_usd=cap, reserved_max_cost_usd_including_vat=REPORT_RESERVED_COST)
    try:
        reservation = ledger.reserve('solar-report', run_id)
    except Exception as exc:
        parser.error(f'Budget ledger refused the request ({type(exc).__name__}); no API request was sent')
    save(attempt / 'solar-execution-started.json', {'status': 'single_request_reserved', 'run_id': run_id, 'request_sha256': digest(request_path), 'reserved_max_cost_usd_including_vat': reservation['reserved_max_cost_usd_including_vat'], 'automatic_retries': 0, 'key_logged': False})
    req = urllib.request.Request(API_ORIGIN + '/v1/chat/completions', data=request_path.read_bytes(), headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json', 'Accept': 'application/json'}, method='POST')
    started = time.perf_counter(); http_status = None; raw = b''; transport_error = None
    try:
        with urllib.request.build_opener(_NoRedirect).open(req, timeout=300) as response:
            http_status = response.status; raw = response.read()
    except urllib.error.HTTPError as exc:
        http_status = exc.code; raw = exc.read()
    except Exception as exc:
        transport_error = type(exc).__name__; raw = json.dumps({'transport_error_type': transport_error}).encode('utf-8')
    latency_ms = round((time.perf_counter() - started) * 1000, 1)
    response_path = attempt / 'solar-response.raw.json'; response_path.write_bytes(raw)
    try: decoded = json.loads(raw.decode('utf-8'))
    except Exception: decoded = {}
    usage = decoded.get('usage', {}) if isinstance(decoded, dict) else {}
    input_tokens = usage.get('prompt_tokens', usage.get('input_tokens')) if isinstance(usage, dict) else None
    output_tokens = usage.get('completion_tokens', usage.get('output_tokens')) if isinstance(usage, dict) else None
    cached = ((usage.get('prompt_tokens_details') or {}).get('cached_tokens', 0)) if isinstance(usage, dict) else 0
    actual = None
    if isinstance(input_tokens, (int,float)) and isinstance(output_tokens, (int,float)):
        actual = round((max(0,input_tokens-(cached or 0))*PRICE_INPUT + (cached or 0)*0.06 + output_tokens*PRICE_OUTPUT)/1_000_000, 8)
    choice = (decoded.get('choices') or [{}])[0] if isinstance(decoded, dict) else {}
    content = (choice.get('message') or {}).get('content') if isinstance(choice, dict) else None
    finish = choice.get('finish_reason') if isinstance(choice, dict) else None
    success = http_status == 200 and isinstance(decoded,dict) and decoded.get('model') == MODEL_ID and finish == 'stop' and isinstance(content,str) and bool(content.strip())
    metadata = {'status':'success' if success else 'failed_after_single_request','run_id':run_id,'upstream_model':decoded.get('model') if isinstance(decoded,dict) else None,'http_status':http_status,'finish_reason':finish,'latency_ms':latency_ms,'usage':usage,'estimated_api_cost_usd_including_vat':round(actual*(1+VAT),8) if actual is not None else None,'reserved_max_cost_usd_including_vat':REPORT_RESERVED_COST,'retry_count':0,'api_key_logged':False,'transport_error_type':transport_error}
    save(attempt / 'solar-status.json', metadata)
    ledger.update_last('solar-report',run_id,{'state':'completed_success' if success else 'completed_failed_after_single_request','completed_at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z'),'http_status':http_status,'latency_ms':latency_ms,'input_tokens':input_tokens,'output_tokens':output_tokens,'actual_cost_usd_including_vat':round(actual*(1+VAT),8) if actual is not None else None,'transport_error_type':transport_error})
    if success:
        output = ROOT/'reports'/(run.name+'-'+args.attempt_id); output.mkdir(parents=True,exist_ok=False); (output/'report.md').write_text(content,encoding='utf-8')
    print(json.dumps({k:metadata[k] for k in ['status','upstream_model','http_status','finish_reason','latency_ms','usage','estimated_api_cost_usd_including_vat','retry_count']},ensure_ascii=False,indent=2))
    return 0 if success else 1

if __name__ == '__main__':
    raise SystemExit(main())
