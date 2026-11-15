# Solar Pro 4 free credit and cash-risk gate (2026-11-03)

## Locally verifiable

- The user reports $19.63 in two credits: Welcome coupon $9.63 (expires 2026-11-25 05:05 UTC) and Survey Credit Reward $10.00 (expires 2027-01-28 14:32 UTC), auto-recharge disabled, commitment $0. These are user-reported Console observations; this machine did not authenticate to the user's account.
- Public Upstage pricing lists Solar Pro 4 at $0.30 per million uncached input tokens and $1.20 per million output tokens, excluding 10% VAT. The local guard caps a trial request at 350,000 serialized bytes, a conservative estimated 360,000 input-token envelope, and 10,000 output tokens. Its worst-case estimate is $0.132 including VAT per request, $0.264 total for two requests. This is an estimate; actual billed tokens would be recorded from the API response if a live call is later approved.
- Upstage's public pricing FAQ says API use continues after credits run out and is billed to the registered payment method. Disabled auto-recharge does not establish that post-credit billing is disabled.
- The public pages do not state whether these named coupon credits apply to direct Solar Pro 4 API calls. The authenticated Billing > Credit account view is not accessible to this process, and API calls were not used to probe eligibility.

## Gate status

`BLOCKED_PENDING_USER_ACCOUNT_CHECK`. No Solar request was sent. Solar API credit use is $0.00 and cash charged is $0.00.

## One required account check

In the logged-in Upstage Console, open **Billing > Credit**, open both named credit entries, and confirm that each is eligible for direct **Solar Pro 4 API** usage (not only Studio/other products). Reply only with whether that eligibility is explicitly shown for both. Do not share API keys, payment details, or account identifiers.

If both entries are explicitly eligible, the configured hard cap estimates up to $0.264 including VAT across two calls, below the $1 credit-use ceiling and below the reported $19.63 balance. The launcher still requires an explicit `-CreditEligibilityConfirmed` switch. If eligibility is missing or unclear, calls remain blocked.

## Official sources checked

- API rates, 10% VAT note, prepaid credits, and billing after credits are exhausted: https://www.upstage.ai/pricing/api
- Chat API model snapshot and `max_tokens` field: https://console.upstage.ai/api/chat
- Authenticated account billing URL (not readable by this environment): https://console.upstage.ai/billing

Additional official terms checked: Upstage's Terms define free credits as promotional/event credits usable for company services and state free credits are deducted before paid credits, with earlier-expiring credits used first. The Terms also say promotion/event credits may have separate validity or payment policies. This supports the general credit mechanism but does not reveal eligibility flags for these two account-specific coupon entries; the Console detail check remains necessary.

Official Terms: https://www.upstage.ai/terms-of-service/update-may-06-2026

## User-reported live usage evidence (2026-11-03)

The user checked Upstage Console > Usage and reports a 2026-11-02 Solar Pro 4 record: Cached/Input/Output line-item total $0.08, credits used $0.08, subtotal $0.00, scheduled/current amount due $0.00. The Console showed the account limit as “Unlimited”. The usage view did not identify which coupon was consumed. This is account-screen evidence reported by the user; the assistant did not access the authenticated screen. Combined with the user-reported current free balance of $19.63, this confirms that Solar Pro 4 API usage has in fact been covered by credits, but not which credit entry supplied them. No payment settings were changed.

The two guarded harness trials have a combined conservative maximum estimate of $0.264 including VAT, below the explicitly authorized $1 credit-use cap. The hard guard still restricts the maximum to one upstream request per harness and two total; no retry is allowed.
