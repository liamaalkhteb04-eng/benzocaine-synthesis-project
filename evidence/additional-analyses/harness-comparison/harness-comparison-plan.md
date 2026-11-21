# 하네스 비교 준비 계획 (benzocaine)

작성/공식 문서 확인일: 2026-11-01 (Asia/Seoul)
최신 상태: 공식 CLI를 프로젝트 로컬 설치하고 API 설정 템플릿과 비교 요청문을 준비했다. 인증·Solar 호출은 하지 않았고, 무료 크레딧/무과금 조건 미확인으로 실제 비교 초안은 보류 중이다. 이전 준비안과 이번 실행 업데이트를 함께 기록했다.

## 선정된 비교군

| 하네스 | 공식 프로젝트 | Solar Pro 4 연결 평가 | 동일 Skill 적용 | 비교 적합성 |
|---|---|---|---|---|
| OpenCode | https://github.com/anomalyco/opencode ; 문서 https://opencode.ai/docs/providers/ | 가능성이 높음. 사용자 지정 OpenAI 호환 provider/model과 base URL을 설정할 수 있고, 공식 provider 안내는 `/v1/chat/completions`에 `@ai-sdk/openai-compatible`를, `/v1/responses`에는 `@ai-sdk/openai` runtime을 안내한다. Upstage가 두 API와 `solar-pro4-260806` snapshot을 공식 제공한다. 실제 조합 확인은 아직 안 함. | 프로젝트 skill 디렉터리에서 동일 본문을 명시적으로 활성화. 프런트매터/로더 처리 여부와 system wrapper를 기록한다. | 선정. 범용 coding-agent harness이며 custom provider를 공식 지원한다. |
| Pi Coding Agent | https://github.com/earendil-works/pi (원래 `badlogic/pi-mono` 저장소가 이 공식 저장소로 이동됨); 공식 문서 https://github.com/earendil-works/pi/tree/main/packages/coding-agent/docs | 가능성이 높음. 공식 Pi 문서는 사용자 정의 모델/provider 설정을 지원하고 Upstage Chat Completions가 지원하는 OpenAI 호환 API 형식과 맞출 수 있다. Solar 모델 ID, base URL, API 형식은 Pi `models.json`에 명시해야 함. 실제 호출 테스트는 아직 안 함. | 동일 skill 파일을 경로로 지정/불러오고, 명령으로 명시적 활성화를 강제한다. 자동 스킬 검색과 기본 prompt injection은 기록한다. | 선정. OpenCode와 별도 CLI/harness 구현이며 skill 및 custom model/provider 확장 구조가 공식 문서화되어 있다. |
| Feynman | https://github.com/Companion-Inc/feynman ; 문서 https://www.feynman.is/docs/ | 현재 비교군에서 제외. 공식 설정 문서는 Pi 기반 custom OpenAI-compatible provider를 설명하지만, 같은 문서는 `Pro-class model IDs`가 `model set`/`--model`에서 거부된다고 명시한다. Solar Pro 4 ID는 Pro 모델이므로 공식 경로에서 연결 가능하다고 확정할 수 없다. 연구용 에이전트·웹검색/하위 에이전트도 기본 설계에 포함되어 혼입 변수가 더 많다. | 동일 skill을 붙이는 것은 가능해 보이나, 위 Solar 모델 제약 때문에 이번 동일 모델 비교에서는 제외. | 별도 탐색 비교 후보. Solar Pro 4 모델 ID 허용 여부가 공식적으로 바뀌고, 도구/하위 에이전트를 끌 수 있음을 확인한 뒤 포함한다. |

최소 비교는 OpenCode와 Pi 두 개다. 모델이 실제로 동일 API ID에 수렴하는지 각 실행의 반환 `model`/응답 메타데이터로 기록해야 한다. 둘 중 하나가 400/404 또는 provider format 오류를 내면, 이를 실패 결과로 보존하고 다른 모델로 바꾸어 성공 결과처럼 비교하지 않는다.

## 공통 입력 및 동등성 통제

1. Skill source: `skill/synthesis_report_skill.md` (원본 수정 금지). 실행 시 두 harness에 같은 바이트의 지침을 전달하고 SHA-256을 기록한다. Harness 전용 폴더에 필요한 경우 byte-identical `SKILL.md` 사본을 만들되, 본문이나 frontmatter를 각자 다르게 고치지 않는다. Pi/OpenCode의 로더가 skill을 자동 주입하는 방식과 harness 기본 system prompt 차이는 완전히 같게 만들 수 없으므로 숨기지 않고 별도 변수로 기록한다.
2. Input evidence: `results/benzocaine-live-20261031-04/report-evidence.json` 및 해당 run의 `routes.json`, `conditions-parrot.json`, `yields-rxn_yields.json`, `validation_notes.json`; 추가분석 근거는 `analyses/mopac/results-interpretation.md`, `analyses/epi-suite/analysis.md`, `analyses/visualizer/visualizer-measurement-interpretation.md`와 실제 측정 CSV/캡처 인덱스를 사용한다. 원본 파일 경로와 SHA-256을 실행 manifest에 기록하고 두 호출 모두 동일한 snapshot을 읽는다. 과거 aspirin 기록을 입력에 섞지 않는다.
3. User task: 동일한 한국어 지시문을 각각 전달하고 skill을 실제 읽게 한다. 이번 비교 출력은 최종 제출 보고서가 아니라 구조화된 초안/본문 비교 산출물이다. 실제 최종 문서 편집은 별도 승인 이후 수행한다.
4. Model/API: `solar-pro4-260806` snapshot을 고정하고 `https://api.upstage.ai/v1`의 **Chat Completions**를 두 harness에서 공통 사용한다. Chat API는 현재 Solar Pro 4 snapshot과 `reasoning_effort`를 명시적으로 지원한다. 제안 설정: `temperature=0`, `reasoning_effort=none`(reasoning off), 동일 `max_tokens=10000`, 동일 system/task/skill/evidence 텍스트. OpenCode/Pi가 동일 파라미터를 wire request에 전달하지 못하면 실제 request config 차이를 기록하고 완전 동등 비교라고 표현하지 않는다. 웹 검색, 도구, MCP, subagent는 비활성화 또는 호출하지 않는 프로토콜로 제한하고, 도구 사용 시 해당 run은 별도 조건으로 분류한다.
5. Call order: 순서 효과를 줄이기 위해 A/B 순서를 기록하고, 가능하면 두 번의 초기 호출 순서를 동전 던지기 등 사전 규칙으로 정한다. 각 harness 1회, 총 2회의 새 Solar 모델 호출이 최소안이다. 변동성 평가가 필요하면 각 3회(총 6회)가 권장되지만 비용/실험 수가 증가한다.

## 모델 호출과 저장 응답 렌더링 구분

- 새 모델 비교: 각 harness에서 Solar API를 실제 호출하여 원문 응답과 usage/응답 ID/모델 snapshot/타임스탬프를 저장. 최소 2 API calls (OpenCode 1 + Pi 1).
- 저장 응답 재렌더링: 이미 저장한 원문 텍스트를 같은 DOCX/PDF 변환기로 내보내는 작업. Solar 호출 0회이며 harness가 작성한 문체나 모델 품질 결과가 아니다. 재렌더링은 문서 조판 검증으로만 보고하고 harness 성능 표에는 포함하지 않는다.
- 재시도는 API 실패가 명확한 경우에도 새 호출 수/비용에 포함하며, 최초 실패 JSON과 로그를 보존한다. 모델 후편집 또는 응답 합성은 비교 결과를 오염시키므로 평가 전 금지한다.

## 필요한 설치/접근 및 인증

이번 작업에서는 아무것도 설치/인증하지 않았다. 다음 실행 단계에서 필요:

- OpenCode: 공식 설치 방식으로 CLI 설치(미수행), project-scoped provider 설정 파일 작성, Upstage API key를 환경 변수로 주입. provider format은 Chat Completions로 고정. `opencode` 버전과 설정 스키마 보존.
- Pi: Node.js 지원 버전 확인 및 공식 `@earendil-works/pi-coding-agent` 설치(미수행), project/user custom `models.json` 작성, 동일 API key를 환경 변수로 주입. 모델 ID와 API protocol 명시.
- Solar: 현재 API key 상태를 새로 조회하지 않았고, 유료 호출하지 않았다. 실제 실행 전 키 접근 상태와 계정 크레딧/가격을 확인해야 한다. key 값은 로그·manifest에 절대 기록하지 않는다.
- Feynman: 이번 최소 비교에는 설치 불필요. 추후 모델 ID 거부 문제를 공식 문서로 재확인한 뒤 별도 검토.

## 호출 수와 예상 비용

Upstage 공식 API 가격표(확인일 2026-11-01)에는 Solar Pro 4 입력 1M token당 0.30, cached input 0.06, 출력 1M token당 1.20이 표시된다(가격표의 현재 통화/세금/계정 조건은 실행 직전 console에서 재확인). 이 프로젝트의 evidence JSON은 약 161 KB이고 skill/지침/메타데이터가 추가된다. 토크나이저 실측 전이므로 대략 입력 40k–70k tokens, 출력 5k–10k tokens를 가정하면 1회 약 0.018–0.033, 2회 약 0.036–0.066 (표시 통화 기준, 세금 및 재시도 제외)이다. 출력 최대치가 10k이며 실제 usage를 받아 비용을 사후 확정한다. 무료 크레딧 여부나 가격 변경을 가정하지 않는다.

| 설계 | 새 Solar 호출 | 대략 비용 범위 | 용도 |
|---|---:|---:|---|
| 최소 비교 (OpenCode 1, Pi 1) | 2 | 0.036–0.066 | 서로 다른 harness 1회 비교 |
| 반복 비교 (각 3회) | 6 | 0.108–0.198 | 출력 변동성/안정성 확인 |
| 저장 응답 문서 변환 | 0 | 0 | DOCX/PDF 조판·페이지 확인 |

비용은 예상치일 뿐이다. 실제 입력 토큰 수가 70k보다 크거나 출력 상한/재시도 설정이 다르면 다시 계산한다.

## 평가 기준

각 응답을 익명 A/B로 고정 rubric으로 평가한다(가능하면 평가자는 harness 이름을 가린다):

1. 근거 정확성: 파일/모델 결과의 수치, route/step 연결, 예측/실험 구분, 출처 충실도.
2. 과장/환각: 없는 조건·수율·실험 사실·Visualizer 측정을 만들어 냈는지, MOPAC/EPI/정적 geometry를 수율이나 반응 성공으로 오해했는지.
3. 단계 정합성: 각 route의 reaction SMILES, 중간체, 조건 및 수율이 같은 route_id/step_id에 연결되는지.
4. 필수 항목 완전성 및 적용 한계: 성공/실패/미실행을 그대로 표시하고 빠진 내용을 정직하게 공개하는지.
5. 한국어 가독성: 자연스러운 문체, 중복·템플릿 문구, 표/그림 참조 정확성.
6. 형식/재현성: 요청된 출력 구조, 페이지 예산, 인용 가능한 출처, 실행 메타데이터.
7. 운용 지표: API 성공/실패, latency, input/output/cached/reasoning token, retries, tool invocation.

각 항목 0–4점(0=오류/누락, 2=부분 충족, 4=근거 연결이 명확하고 오류 없음)과 근거 인용을 남기며, 과학적 과장 항목은 별도 치명 오류로 센다. 평균 점수 하나로 모델 우열을 단정하지 않는다.

## 공식 출처

- OpenCode repository: https://github.com/anomalyco/opencode/
- OpenCode provider docs: https://opencode.ai/docs/providers/
- Pi official repository: https://github.com/earendil-works/pi (기존 `badlogic/pi-mono`에서 redirect)
- Pi provider docs: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md
- Pi model docs: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md
- Pi skill docs: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md
- Feynman official repository: https://github.com/Companion-Inc/feynman
- Feynman setup: https://www.feynman.is/docs/getting-started/setup/
- Feynman configuration: https://www.feynman.is/docs/getting-started/configuration/
- Upstage Chat Completions API: https://console.upstage.ai/api/chat
- Upstage Responses API: https://console.upstage.ai/api/responses
- Upstage Solar Pro 4 reasoning settings: https://console.upstage.ai/docs/capabilities/generate/reasoning
- Upstage API pricing: https://www.upstage.ai/pricing/api

공식 문서 확인은 연결/기능 지원성 검토다. 실제 local install, API key authentication, request acceptance, Solar response, output quality는 아직 검증되지 않았다.
## 실행 업데이트 (2026-11-01)

OpenCode 2.2.5와 Pi 1.4.0을 공식 npm 패키지로 프로젝트 로컬 설치하고 CLI 버전을 확인했다. Node 24.22.1을 사용했다. Solar endpoint/model 설정은 `configs/opencode.solar.template.json`, `../../tools/harnesses/pi-agent-config/models.json`에 key 없는 template으로 준비했다. Pi custom model을 `PI_OFFLINE=1`와 일회성 placeholder env key로 읽기만 하여 모델 등록을 확인했다; placeholder는 실제 key가 아니며 network/API call은 하지 않았다. OpenCode config parse/help/version은 확인했으나 custom model 인식/연결은 인증 없이 검증되지 않았다.

현재 프로세스에 실제 UPSTAGE_API_KEY는 없고 프로젝트 `.env`도 없다. Upstage Console에 접근해 무료 잔액·만료·모델 적용범위·초과 과금/자동충전 차단을 확인할 수 없었다. 따라서 실제 비교 호출 0회. 또한 OpenCode 문서의 timeout 자동 재시도 정책과 Pi CLI의 provider retry 비활성화 미확인 때문에 “추가 호출 0회 보장” 조건은 현재 충족되지 않는다. 두 실행 모두 credit 및 retry controls 검증 전에는 보류한다.
## 2026-11-03 update: guarded execution readiness

- The nonempty `UPSTAGE_API_KEY` setting was found in the pre-existing `<historical external model/runtime root; not included>\.env`. Its value was never displayed, copied, or written in the benzocaine project. `scripts/run_guarded_harness.ps1` reads it only after a credit-eligibility gate and exposes it to child processes through their environment for the local proxy to forward.
- `scripts/harness_request_guard.py` is now the only configured upstream path. It pins `solar-pro4-260806`, forces temperature 0/reasoning off/tools off/one response, caps output at 10,000 tokens, rejects oversized prompts, reserves one upstream attempt per harness and two total before sending, disallows redirects, and never retries upstream. Client retry attempts are answered locally with 409.
- Four local loopback mock tests passed. They verified one accepted upstream request per harness, total cap two, replay/restart retry denial, request/output size rejection, missing-key denial, parameter normalization, and no dummy credential in artifacts. Mock responses are test fixtures only, not model comparison outputs.
- A frozen 198,918-byte payload was built from 11 evidence sources; both harnesses will use the same attachment and pinned snapshot. No Solar request has been made, no real draft exists, and usage remains $0 credits / $0 cash.
- Upstage's public pricing page lists Solar Pro 4 API rates of $0.30/M input and $1.20/M output (exclusive of 10% VAT); the guard's conservative cap estimates at most $0.132 per request including VAT and $0.264 for both. The page also says API use may continue after credits run out and bill a registered payment method. Therefore auto-recharge-off alone is not sufficient to establish the user's no-cash condition.
- The user's credit screen details cannot be inspected in this environment. Public pages do not establish whether the specific Welcome coupon and Survey Credit Reward apply to direct Solar Pro 4 API requests. Live calls remain gated until the user verifies that in the authenticated Console.
