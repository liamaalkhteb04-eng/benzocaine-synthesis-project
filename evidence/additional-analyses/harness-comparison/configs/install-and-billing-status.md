# Harness 설치/연결 사전 점검 (2026-11-01)

- 공식 배포: OpenCode `@opencode/cli@2.2.5`, Pi `@earendil-works/pi-coding-agent@1.4.0`. 각각 프로젝트 로컬 `tools/harnesses/opencode` 및 `tools/harnesses/pi`에 설치. Node.js 24.22.1 사용. 기존 global PATH/프로그램은 변경하지 않음.
- API 없는 실행 점검: OpenCode `--version` = v2.2.5, Pi `--version` = 1.4.0. Pi `--offline --list-models` 및 OpenCode help/version/catalog 확인은 유료 inference 호출이 아님. 모델 inference/authentication은 하지 않음.
- OpenCode의 npm postinstall은 첫 설치에서 실행되지 않아 placeholder가 생겼다. 공식 패키지의 `postinstall.mjs`를 Node로 실행하여 프로젝트 로컬 Windows 실행파일을 선택하고, 최종 `opencode.exe --version` 성공을 확인.
- Pi 설치 시 lifecycle script를 비활성화하는 공식 권장 방식(`--ignore-scripts`)을 사용. CLI shim 실행 확인.
- 비교 연결 설정 샘플: `analyses/harness-comparison/configs/opencode.solar.template.json`, `tools/harnesses/pi-agent-config/models.json`. 두 파일 모두 Upstage Chat Completions endpoint, `solar-pro4-260806`, temperature 0, output 10,000 기준. API key는 환경변수 `UPSTAGE_API_KEY`에서만 읽도록 했으며 키 값을 넣거나 출력하지 않음. Pi 격리 설정 경로는 `PI_CODING_AGENT_DIR=tools/harnesses/pi-agent-config`.
- 연결 자체는 미검증: 현재 프로젝트 `.env`가 없고 현재 프로세스에 `UPSTAGE_API_KEY`가 설정돼 있지 않음. 계정 API key/과금 상태에 접근하지 않음.
- OpenCode 공식 provider 문서는 timeout 발생 요청을 최대 3회 재시도한다고 한다. 이번 비교의 요구인 재시도 0회를 공식 설정으로 보장하는 방법은 찾지 못했다. 따라서 OpenCode inference는 크레딧이 확인되더라도 retry=0을 보장할 수 있을 때까지 보류한다. 자동 재시도는 추가 과금을 만들 수 있으므로 이 제한은 선결 조건이다.
- API 호출 전에 Upstage Console Billing/Usage에서 무료 credit의 남은 금액, 만료일, 적용 제품/model, `solar-pro4-260806` 적용 여부, 무료 잔액 초과 시 pay-as-you-go/자동충전이 꺼져 있거나 hard spending cap이 0/잔액으로 제한되는지 확인해야 한다. Dashboard를 이 실행 환경에서 읽을 수 없으므로 잔액/정책을 추측하지 않는다. API token/account usage endpoint도 조회하지 않았다.
- 코드/패키지 다운로드 자체에는 Solar 호출이 없고 Solar credit 사용량은 0. Solar inference 호출도 0회.

## 계정에서 확인할 항목

Upstage Console에 로그인해 Billing/Credits 및 Usage/Spending 화면을 확인한다. 아래 항목을 모두 확인할 수 있어야 비교를 실행할 수 있다.

1. 사용 가능한 무료 크레딧 잔액과 만료 시각/날짜.
2. 크레딧이 Generative API inference와 Solar Pro 4 (`solar-pro4-260806`)에 적용된다는 표시.
3. 요청당/분당 제한과 한도 초과 시 동작.
4. 무료 credit 소진 후 유료 과금, 카드 청구, 자동 충전이 발생하지 않게 차단됐다는 명시적인 설정. 단순히 “잔액이 현재 충분함”만으로 자동 과금을 배제하지 못한다.
5. 잔액에서 최소 두 건(요청 최대 output 10,000 tokens × 2, 입력 evidence 포함)의 예상 최대 비용을 감당 가능한지.

화면에서 확인이 불가하거나 account-level hard cap이 없다면 inference를 실행하지 않는다. 이후 비교 시 하네스별 1회, 자동 재시도·fallback·추가 호출은 금지한다. OpenCode의 재시도 제한을 끌 수 없는 경우에는 OpenCode/Pi 동일 1회 호출 비교도 진행하지 않는다.