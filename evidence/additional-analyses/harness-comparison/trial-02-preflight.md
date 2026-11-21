# Trial 02 preflight and compatibility fixes (2026-11-03)

## OpenCode title request

The installed official OpenCode CLI's `opencode run --help` exposes `--title`. Trial 02 passes a fixed `--title "Benzocaine comparison draft"`, so the first model request is reserved for the report prompt instead of generated session metadata. `OPENCODE_PURE=1` and the local config disable updates, sharing, and OpenTelemetry; no extension/web tools are enabled. The explicit-title behavior passed the end-to-end loopback test with exactly one upstream mock POST.

Official CLI docs: https://dev.opencode.ai/docs/cli/

## Pi and Upstage request compatibility

The prior real Pi request included `store:false`, and Upstage returned HTTP 400 for that field. The active Pi `models.json` now sets `compat.supportsStore:false`; it also pins `maxTokensField:"max_tokens"`, disables streaming-usage options, leaves developer-role mapping off, and retains supported Solar reasoning control. The real request also contained only standard `model`, `messages`, `max_tokens`, `n`, `reasoning_effort`, `stream`, and `temperature` fields besides `store`. The guard now strips all fields outside an explicit Upstage Chat Completions allowlist, including `store`, `tools`, `tool_choice`, `stream_options`, and `max_completion_tokens`.

Official Pi compatibility docs: https://pi.dev/docs/latest/models-configuration
Upstage Chat Completions docs: https://console.upstage.ai/api/chat

## Streaming adapter and local-only verification

Both harnesses request streaming at their client boundary. The guard still forwards exactly one non-streaming request to Upstage, then adapts a successful JSON completion into a short SSE response for the harness. This avoids a response-mode mismatch that caused local retries in the previous attempt. The real installed OpenCode and Pi programs were run through the guard to a loopback mock server. Both exited successfully with exactly one mock upstream POST, the report-writing prompt and all 12 source blocks present, no unsupported field forwarded, and the same pinned model plus temperature 0, reasoning `none`, `max_tokens` 10,000, `n` 1. This fixture response is marked `LOCAL_MOCK_ONLY` and is not a real draft.

The first direct-to-mock test remains preserved at `analyses/harness-comparison/local-harness-verification/`; it demonstrated streaming-client retries when bypassing the guard. The corrected guarded test is `analyses/harness-comparison/local-harness-verification-02/` and passed.

## Cumulative $1 hard limit

A new ledger was initialized at `analyses/harness-comparison/guard-state-cumulative/usage-ledger.json`. The earlier failed ledger was left untouched and its two reservations were imported. The $0.08 prior user-reported Solar Pro 4 credit transaction was also counted as baseline usage. Each new request reserves at most $0.132 including VAT. Worst-case cumulative exposure is therefore $0.08 + $0.264 prior attempts + $0.264 new attempts = $0.608, below the $1 ceiling. Unique live run IDs are `opencode-trial-02` and `pi-trial-02`; each may reserve once, total four lifetime POSTs including the two imported historical attempts. No automatic retry can forward another request.
