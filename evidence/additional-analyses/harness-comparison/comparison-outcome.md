# OpenCode and Pi trial outcome — 2026-11-03

## Scope and budget

- Same pinned model: `solar-pro4-260806`; same 12-source frozen input payload (199,634 bytes; SHA-256 `636BE4F7EE73A4BD08682629B95F906EC246A986E07C17348BB4EA93F72A973E`). Temperature, reasoning, tools, response count, and output cap were normalized identically by the proxy.
- The live serialized messages were not byte-identical: OpenCode sent 201,667 content bytes and Pi sent 200,417. Their system messages differed (OpenCode 1,806 bytes, SHA-256 `A8382DB91F60F816E5A7C3057EDC771476AE817E2BD53273577E4BF4AB3ADD02`; Pi 585 bytes, SHA-256 `F4E3EBDD644D62ACE74E5130A25B51903876EE7F432F522E2D1D5CDEC163759D`), and user-message serialization differed by 29 bytes. Both included the same frozen evidence payload and shared instruction, but harness-added prompt framing remains a comparison variable.
- Guard settings: temperature 0, reasoning off, tools off, one completion, 10,000 output-token maximum; one upstream POST per harness and two total. The guard reserved at most $0.132 including VAT for each POST, for a combined ceiling of $0.264, below the user's $1 credit-use cap.
- User-reported account evidence: 2026-11-02 Solar Pro 4 usage $0.08, covered by $0.08 credits, subtotal/due $0; coupon identity not shown. No payment setting, purchase, recharge, or final report action occurred.

## OpenCode — one upstream request, harness draft failed

- The single forwarded POST returned HTTP 200 from the pinned Solar Pro 4 snapshot in 3,773 ms.
- API-reported usage: 65,736 input tokens, 9 output tokens (65,745 total; 0 cached input). Based on the published rates, estimated API cost is $0.0197316 before VAT, approximately $0.02170476 including 10% VAT. The actual credit debit was not independently read from the authenticated account after this run.
- The response was only a short Korean draft title, not the requested comparison draft. OpenCode then issued additional local attempts; the proxy returned 409 for them and forwarded none upstream. The harness process was stopped to prevent further local retry attempts. No full OpenCode draft was created.
- Root cause: OpenCode's automatic title-generation request consumed the one allowed upstream POST before its substantive draft request. A future run would need a fixed `--title` to avoid that extra model request, but this trial is not being replayed.

## Pi — one upstream request, API rejected request

- The single forwarded POST returned HTTP 400 in 308 ms. The response says: `Unrecognized request arguments supplied: store`.
- No usage object or model completion was returned. Billed amount/credit debit for this rejected request is not exposed in the API response; do not infer it as zero.
- No retry was made and no Pi draft was created. The request and error response were retained.

## Comparison

Neither run produced substantive report prose, so factual accuracy, evidence citation quality, style, coverage, exaggeration, and omissions cannot be scored. This trial only demonstrates a harness behavior difference: OpenCode used its one-call allowance for title generation, while Pi's first request contained a `store` field rejected by the endpoint. These two failures do not establish general performance differences between the harnesses.

## Artifacts and remaining state

Raw request/response and usage metadata are in `results/harness-comparison/runs/opencode-trial-01/` and `results/harness-comparison/runs/pi-trial-01/`. The durable ledger records exactly two upstream POSTs (OpenCode 200; Pi 400); the two-request limit is exhausted. No retry or replacement run has been made. To obtain comparable drafts, a new explicitly authorized trial budget would be needed after updating OpenCode to use a fixed title and configuring Pi to omit the unsupported field. The $1 cap and no-cash rule should remain in force.
