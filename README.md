# 벤조카인 AI 유기합성 보고서 재현 패키지

이 폴더는 교수님이 벤조카인 보고서의 근거와 생성 절차를 확인하고, 저장된 증거로 새 Solar 보고서를 작성하거나 문서 파일만 다시 만들 수 있도록 정리한 패키지입니다. **최종 후보 보고서의 본문·수치·그림·표는 고정되어 있습니다.** PDF와 DOCX는 이름만 정리해 복사했으며 원본 파일의 SHA-256과 복사본의 SHA-256이 일치합니다.

## 먼저 볼 두 스킬

- [전체 실행 스킬](skill/SKILL.md): 입력 구조 확인, 모델 사전검사, 경로·조건·수율 실행, 증거 취합, 보고서 작성 요청과 문서 검증 흐름을 안내합니다.
- [Solar 보고서 작성 스킬](skill/report-writing/SKILL.md): Solar Pro 4가 근거를 읽고 한국어 보고서 원고를 작성할 때 적용할 규칙입니다.

스킬만 별도로 복사해도 모델 실행이나 문서 생성이 되지는 않습니다. 이 패키지의 코드, 설정, 증거, Python 의존성, 외부 모델 런타임·가중치·재고 데이터, 로컬 Solar API 키와 Windows PDF 변환 환경이 각각 필요합니다.

## 제출 후보 파일

- [최종 보고서 PDF](reports/benzocaine-final/벤조카인_AI유기합성_최종보고서.pdf)
- [최종 보고서 DOCX](reports/benzocaine-final/벤조카인_AI유기합성_최종보고서.docx)
- 보고서 원고와 실행 증거는 같은 폴더의 `report-source.md`, `evidence-run/`, `final-document-validation.json`, `citation-audit.json`, `content-validation.json`에서 확인합니다.
- 제출 후보 PDF SHA-256: `4d5521f3594706453ee413f0c7cfc1edf952ca4ae44b66eb9f1ddb6e27cf7445`
- 제출 후보 DOCX SHA-256: `b8b408829f833848bfcd422697f7ca0035f9be11d299fc30fe4c757a43dee926`
- 문서 검증 기록은 20쪽, 그림 10개, 표 4개, 페이지 렌더링 및 잘림 검사 통과를 기록합니다. 원본 보고서 폴더도 저장소의 기존 위치에 그대로 보존되어 있습니다.

## 실행 전 준비

### 보고서 환경과 Solar 연결

Windows에서 Python 3.13 보고서 환경을 별도로 준비하고 Microsoft Word 데스크톱을 사용해 PDF를 만듭니다. 기존 검증용 가상환경은 이 패키지 밖에 두며, 새 PC에서는 아래처럼 구성합니다.

```powershell
py -3.13 -m venv .venv-report
& .\.venv-report\Scripts\python.exe -m pip install -r requirements-report.txt
```

`requirements-driver.txt`는 RDKit과 파이프라인 증거·그림 생성 라이브러리용이며, `requirements-report.txt`는 Markdown 검증과 DOCX 조판용입니다. AiZynthFinder, Parrot, Yield-BERT는 각 공식 저장소의 런타임·체크포인트를 별도로 준비하고 `configs/model-assets.lock.json`의 환경변수에 연결합니다. PDF 변환에는 Microsoft Word 데스크톱이 필요합니다.

Solar 요청은 `configs/report-plan.json`에서 모델 스냅샷 `solar-pro4-260806`, temperature `0`, 최대 출력 토큰 `35000`을 사용합니다. API 키는 저장소에 넣지 마세요. 현재 이 패키지의 라이브 호출 설정은 비활성 상태입니다. 실제 호출을 승인받은 경우에만 `UPSTAGE_API_KEY`를 프로세스 환경변수에 설정하고, 직전 Console 잔액·크레딧 적용·이번 달 비용 및 최신 프로젝트 원장을 확인한 뒤 `report-plan.json`의 승인 및 `live_budget_snapshot`을 로컬에서 갱신합니다. 호출 가드는 현재 누적액, 프로젝트 상한, VAT 포함 최악 예약액을 비교하며 한 번만 요청하고 자동 재시도하지 않습니다. Console의 자동 충전 미설정은 후불 청구 차단을 뜻하지 않습니다.

```powershell
$env:UPSTAGE_API_KEY = [System.Net.NetworkCredential]::new('', (Read-Host -AsSecureString 'Upstage API key')).Password
```

### 화학 모델과 자산

체크포인트·토크나이저·재고 가중치는 용량과 배포 조건 때문에 이 패키지에 포함하지 않았습니다. 버전, 필요한 파일 유형, 기준 체크섬은 [모델 자산 잠금 파일](configs/model-assets.lock.json), [수율 정규화 메타데이터](configs/yield-normalization.json), `skill/SKILL.md`와 아래의 공식 프로젝트 안내를 기준으로 준비해야 합니다.

| 단계 | 공식 프로젝트 | 준비 항목 |
|---|---|---|
| 경로 | [AiZynthFinder](https://github.com/MolecularAI/aizynthfinder) | Python 3.12 계열의 격리 환경, ONNX 정책 모델·템플릿, 전체 공개 ZINC stock HDF 데이터와 변환된 stock bucket. `AIZYNTH_PYTHON`, `AIZYNTH_MODEL_DIR`, `AIZYNTH_STOCK_BUCKETS`를 로컬에서 지정합니다. `scripts/prepare_stock_buckets.py`는 공식 전체 HDF에서 bucket을 만들며 입력 일부만으로 만든 재고를 전체 재고처럼 취급하지 않습니다. |
| 조건 | [Parrot](https://github.com/wangxr0526/Parrot) | 공식 저장소의 문서에 맞춘 Conda 환경과 내려받은 학습 체크포인트(`pytorch_model.bin`). `PARROT_PYTHON`, `PARROT_REPOSITORY`, `PARROT_CHECKPOINT`를 지정합니다. |
| 수율 | [rxn_yields](https://github.com/rxn4chemistry/rxn_yields), [rxn-models](https://github.com/rxn4chemistry/rxn-models) | 일치하는 RXN 체크포인트·토크나이저·모델 설정과 정규화 메타데이터. `RXN_YIELDS_PYTHON`, `RXN_YIELDS_CHECKPOINT`를 지정하고 체크포인트 해시가 정규화 기록과 일치하는지 사전검사합니다. |
| 대안/추가 | [SynthEx](https://github.com/schwallergroup/synthex/tree/submission), [ASKCOS context recommender](https://gitlab.com/mlpds_mit/askcosv2/context_recommender), [DRFP](https://github.com/reymond-group/drfp) | 이 패키지에서 실행 어댑터 또는 회귀 헤드가 확인되지 않은 기능은 실행하지 않고 `not_implemented`/미실행으로 둡니다. DRFP 자체는 수율 회귀 모델이 아닙니다. |

설치·다운로드 명령과 데이터 출처는 각 공식 프로젝트의 현재 문서를 먼저 확인하세요. 모델 자산 준비 후 실행 전에 `scripts/preflight_models.py`가 런타임·설정·체크포인트·stock hash를 검사하게 합니다. 가중치가 없거나 해시가 다르면 임의 대체하지 않습니다. 기존 PC에서 확인한 경로는 다른 PC에 적용되는 보증이 아닙니다.

## A. 저장된 벤조카인 증거에서 새 Solar 보고서 작성

이 절차는 저장된 벤조카인 예측·추가 분석 자료로 Solar Pro 4가 **새 보고서 원고를 작성**합니다. 화학 모델은 다시 실행하지 않습니다. 과거 최종 원고를 Solar의 템플릿이나 정답으로 요청에 넣지 않습니다. 문헌 비교, 강의 근거 요약, MOPAC·EPI·Visualizer·하네스 결과, route/step별 원시 출력, figure manifest와 보고서별 citation source map의 **파일 내용**을 요청에 넣는 구성은 로컬 `scripts/generate_solar_report_from_bundle.py`가 수행합니다.

먼저 보고서 의존성을 준비한 뒤 저장 증거를 새 실행 폴더에 복사하고, 외부 호출 없는 준비 모드로 요청과 메시지를 검토합니다.

```powershell
$py = '.\.venv-report\Scripts\python.exe'
$reportDir = 'reports\reproduction\benzocaine-authoring-01'
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
Copy-Item -LiteralPath 'reports\benzocaine-final\evidence-run' `
  -Destination (Join-Path $reportDir 'evidence-run') -Recurse
& $py -B -X utf8 scripts\generate_solar_report_from_bundle.py `
  --report-dir $reportDir --attempt-id solar-author-01 `
  --run-id benzocaine-authoring-01 --prepare-only
```

준비된 `reports/reproduction/benzocaine-authoring-01/execution/attempts/solar-author-01/solar-request.redacted.json`과 `request-input-manifest.json`에서 system 메시지의 보고서 스킬 해시, user 메시지의 실제 증거 블록, 원시 데이터 해시, figure ID·캡션을 확인합니다. 문헌 비교 파일은 AI 예측 뒤에 조사한 자료라는 점도 입력 근거에서 구별합니다. 현재 패키지 복사본으로 같은 준비 절차를 외부 호출 없이 확인한 기록은 [오프라인 요청 검사](validation/offline-authoring-request-check.json)입니다. 이 기록은 요청 내용과 입력 해시 연결만 검사하며 Solar 응답 품질을 보증하지 않습니다.

새 Solar 보고서 작성은 외부 유료 요청입니다. 이 패키지의 기본 설정은 호출 비활성입니다. **새 호출을 실행하라는 별도 승인이 있고**, Console의 크레딧 적용과 현금 청구 위험, 최신 누적 원장, 입력·출력 상한의 VAT 포함 예약액을 확인한 뒤에만 config 승인과 최신 `live_budget_snapshot`을 입력합니다. 해당 snapshot이 없거나 상한을 보장하지 못하면 코드는 요청을 보내지 않습니다. 승인 후 명령 형식은 아래와 같고, 한 번만 전송하며 실패해도 재시도하지 않습니다.

```powershell
& $py -B -X utf8 scripts\generate_solar_report_from_bundle.py `
  --report-dir $reportDir --attempt-id solar-author-01 `
  --run-id benzocaine-authoring-01 `
  --authorize-credit-only --execute-solar
```

호출이 실제 성공하면 저장 응답을 근거·요구사항으로 검증한 후에만 문서 렌더러를 실행합니다. 현재 스킬 버전은 이번 정리 과정에서 새 Solar 호출로 품질 검증하지 않았습니다.

## B. 새 물질의 예측 후 Solar 보고서 작성

새 물질마다 물질 ID와 구조가 일치하는 새 JSON, 새 run ID, 새 출력 디렉터리를 사용합니다. 벤조카인의 예측·MOPAC·EPI·Visualizer·하네스 결과는 자동 재사용하지 않습니다.

```powershell
$driver = '.\.venv-driver\Scripts\python.exe'
$py = '.\.venv-report\Scripts\python.exe'
$target = 'my-target'
$runId = 'my-target-live-YYYYMMDD-01'
Copy-Item inputs\input-template.json "inputs\$target.json"
# inputs/<target>.json에 이름, canonical SMILES, 분자식, 구조 출처를 직접 입력
& $driver -B -X utf8 scripts\prepare_target.py `
  --input "inputs\$target.json" --output "validation\$target-identity.json"
& $driver -B -X utf8 scripts\preflight_models.py `
  --input "inputs\$target.json" --output "validation\$target-preflight.json"
& $driver -B -X utf8 scripts\run_pipeline.py `
  --input "inputs\$target.json" --run-id $runId
& $py -B -X utf8 scripts\generate_report.py `
  --run-dir "results\$runId" --attempt-id solar-author-01 --prepare-only
```

`results/<run-id>/`에 생성된 경로·조건·수율의 원시/정규화 결과, 실패 상태, 그림과 증거 manifest를 먼저 확인합니다. 요청 준비만 한 결과를 모델 추론 성공이나 Solar 작성 성공으로 부르지 않습니다. `generate_report.py --execute-solar`도 현재 config의 승인 플래그, 24시간 이내의 검증된 무료 크레딧 전용 예산 snapshot, VAT 포함 예약액의 프로젝트 누적 한도 통과, 키의 로컬 설정이 모두 있어야 단일 POST를 허용합니다. 새 snapshot이 없거나 오래됐거나 여유가 부족하면 API 요청 전에 중단합니다. 자동 재시도와 redirect는 차단됩니다. 실제 upstream 비용 상한은 API가 보장하는 청구 상한이 아니므로 호출 전 공식 단가와 계정 상태를 다시 확인해야 합니다. 이 패키지의 기본 config는 호출 비활성입니다. 승인을 받은 경우 실행은 아래와 같이 별도 명령으로 하며, 현재 snapshot과 worst-case reservation gate를 통과하지 않으면 API 요청 전에 중지합니다.

```powershell
& $py -B -X utf8 scripts\generate_report.py `
  --run-dir "results\$runId" --attempt-id solar-author-01 --execute-solar
```

문서 변환은 보고서 스킬의 검증 절차와 `scripts/render_report_evidence.py`, `scripts/export_report_docx.py`, `scripts/convert_docx_to_pdf.ps1`로 진행합니다. 예산 가드의 로컬 단위 검사는 `python -B -X utf8 -m unittest discover -s tests -p test_generate_report_budget_gate.py -v`로 실행할 수 있습니다.

## C. 저장된 응답으로 DOCX/PDF만 재생성

이 절차는 Solar나 화학 모델을 호출하지 않습니다. 저장된 조립 완료 원고 `reports/benzocaine-final/report-source.md`와 검증된 figure manifest·증거를 사용해 새 위치에서 DOCX/PDF를 재생성합니다. 과거 부분 응답을 새로 조립하거나 최종 후보 파일을 덮어쓰지 않습니다. 이 원고의 여러 Solar 블록 조립 이력은 `provenance/report-assembly/ASSEMBLY-PROVENANCE.md`와 실행별 원시 응답·해시 기록에 연결되어 있습니다.

```powershell
$py = '.\.venv-report\Scripts\python.exe'
$out = 'reports\rebuild-local-01'
New-Item -ItemType Directory -Path $out | Out-Null
Copy-Item -LiteralPath 'reports\benzocaine-final\report-source.md' `
  -Destination (Join-Path $out 'report.md')
& $py -B -X utf8 scripts\export_report_docx.py `
  --run-dir 'reports\benzocaine-final\evidence-run' `
  --markdown (Join-Path $out 'report.md') `
  --solar-status 'reports\benzocaine-final\solar-status.json' `
  --verified-edits-validation 'reports\benzocaine-final\verified-edits-validation.json' `
  --compact-layout
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\convert_docx_to_pdf.ps1 `
  -DocxPath (Join-Path $out 'report.docx') `
  -PdfPath (Join-Path $out 'report.pdf') `
  -MetadataPath (Join-Path $out 'word-export.json')
```

조립된 원고에는 그림 참조와 검증된 표가 이미 반영되어 있으므로, 이 절차에서는 `render_report_evidence.py`를 다시 적용하지 않습니다. 해당 렌더러는 원시 Solar 원고에 manifest 기반 그림과 정규화 표를 넣을 때 사용하는 단계이며, 이미 렌더링된 통합표를 다시 발견하면 중복 생성을 막기 위해 거부합니다. 위 저장 응답 기반 직접 DOCX/PDF 재생성은 `reports/rebuild-check-02/document-rebuild-validation-corrected.json`과 20쪽 미리보기로 확인했습니다. 보존된 `document-rebuild-validation-initial-failed.json`은 PDF 한글 텍스트 추출을 잘못 판정 기준으로 사용한 최초 검사 기록입니다. DOCX 본문·표 비교와 PDF 추출 텍스트의 원본 동등성을 확인한 정정 검증을 함께 참조하세요. 이 검증은 저장 원고의 재조판을 확인한 것이며 새 Solar 작성 품질을 검증한 것이 아닙니다.

최종 후보 PDF/DOCX의 바이트 해시는 위에 고정된 값과 동일해야 합니다. C 절차의 산출물은 별도 출력 폴더에서 검사한 뒤에만 후보로 검토하세요.

## 근거, 인용과 공개 자료

- 벤조카인 선택 경위·물질 확인·경로별 근거는 `reports/benzocaine-final/evidence-run/`의 `report-context.json`, `input.json`, `report-evidence.json`, `latest-route-reproduction/`, `token-identity-evidence.json`, `chemical-token-audit.csv`에서 확인합니다.
- Parrot 슬롯과 구조 이름, 실험 역할은 서로 구분합니다. 모델이 반환한 `catalyst1`, `solvent1`, `solvent2`, `reagent1`, `reagent2`, 후보 rank, 점수 및 반응 SMILES를 그대로 보존하고, 물질 정체성과 실험 역할은 별도 확인 근거가 있을 때만 연결합니다.
- 주장은 report-specific `citation-source-map.json`과 프로젝트 증거 ID를 연결합니다. 모델 방법 인용과 이 실행의 원시 출력 인용을 구분합니다.
- 강의 원문 PDF와 논문·특허 원문 파일은 재배포 권한을 확인하지 못해 포함하지 않았습니다. 공개 가능한 자체 강의 요약과 LMS에서 원문을 확보하는 안내, 논문·특허의 식별 정보·원문 접근 경로는 evidence 폴더의 `course-evidence-summary.md`, `course-material-acquisition.md`, literature validation 자료에 있습니다. 수강 권한이 있는 사용자는 LMS에서 강의 원문을 별도로 확보합니다.
- 공개용 익명화가 필요한 텍스트는 패키지 복사본에서만 처리했습니다. 원본과 파생본의 파일별 해시는 `provenance/package-redaction-map.json`과 `provenance/package-source-map.json`에서 구분합니다. 이 패키지의 매니페스트는 복사 후 바이트에 대한 해시입니다.

## 확인 범위와 한계

- 기존 PC에서 벤조카인 파이프라인 실행이 확인되었고, 아세트아미노펜도 해당 PC의 기존 환경에서 실제 경로·조건·수율 추론과 저장 응답 기반 DOCX/PDF 렌더링이 확인된 회귀 사례입니다. 아세트아미노펜의 추가 분석 결과를 벤조카인에 적용하지 않습니다.
- 최신 벤조카인 후보 PDF/DOCX의 20쪽·그림·표·인용·잘림 검증은 보고서 폴더의 해당 기록에 보존되어 있습니다. 이 패키지에서는 파일 해시와 사본 동일성도 다시 확인합니다.
- Solar 요청 오프라인 검사는 메시지 구성과 근거 포함 여부만 확인하며 새 통합 스킬의 Solar 응답 품질은 검증하지 않았습니다.
- 별도 새 PC에 설치해 처음부터 실행한 검증은 없습니다. 모델 가중치, 전체 AiZynthFinder stock 원본, Solar API 키, Word와 재배포 불명확한 원문은 패키지에 없습니다.

## 매니페스트 및 개인정보

`PACKAGE-MANIFEST.json`은 패키지 파일의 상대 경로·크기·SHA-256을 기록하며 `PACKAGE-MANIFEST.sha256`은 매니페스트 자체의 체크섬입니다. `.env`, API 키, 가상환경, 모델 가중치와 불필요한 원문 파일은 패키지에서 제외합니다. 경로 링크 점검 및 비밀정보 검사를 `SUBMISSION-PACKAGE-VALIDATION.md`에 기록합니다. 패키지를 수정한 뒤 공개 준비 매니페스트를 다시 만들려면 Python 환경에서 `python -B -X utf8 scripts/build_professor_package_manifest.py .`을 실행합니다. 실제 `.env`, 모델 가중치 확장자, 50 MiB 초과 파일은 생성기가 거부합니다.


?????? ??? ?? ??? Git? ??? ??? ??? ??? ????, ????? ?? ??? ?????. ????? ???? ??? ??? ?? ??? ??? ??? ??? ?? ??? ??? ?????? ????.
