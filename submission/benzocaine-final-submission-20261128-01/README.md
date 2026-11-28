# 벤조카인 최종 제출 패키지 — 20251312 리야마

**학번 20251312 · 이름 리야마**

[폴더 구조 변경 전후와 보존 기록](STRUCTURE_CHANGES.md). 과거 시안·실패/수정 이력·중복 자료는 archive로 구분했으며 필요한 근거를 삭제하지 않았다.

확정 제출본은 [PDF](report/20251312_리야마_벤조카인_최종보고서.pdf)와 [DOCX](report/20251312_리야마_벤조카인_최종보고서.docx)다. 사용자 확정 파일을 **바이트 그대로** 복사했다. 기존 검증 결과는 참고문헌 포함20쪽·그림13개이며, 이번 패키징에서 과학 검토나 전체 페이지 검사를 반복하지 않았다. 기존 제출본·원시 기록을 수정하거나 GitHub에 push하지 않았다.

## 포함 자료

| 경로 | 역할 |
|---|---|
| `report/` | 확정PDF/DOCX, 최종 원고, 확정 그림13개·현재 자료 상대 링크 |
| `skill/` | 일반 작성·수정·조판 모드와 참조 문서. 과거 실제 수정 system은 archive로 분리 |
| `data/evidence/` | 기존 근거45건과 현재 대조 사실·출처 레지스트리. 역사 문서의 오류·과거 상태는 최종 정정 근거보다 우선하지 않음 |
| `data/final-facts-overlay.json` | 최종 문헌 압력 정정: 도식H₂3atm과 본문 수소3당량 구별. 공용 스킬이 아닌 사례 근거 |
| `data/extracted-tables/`, `data/mapping/`, `data/harness/` | 저장 추출CSV·원자/결합 대응·하네스 비교 사실. 상세 표를 보고서에 추가했다는 뜻이 아님 |
| `code/` | 저장 원고 재조판·Word변환·원본PNG복원·패키지 점검 코드. 기본 동작에 Solar 호출 없음 |
| `authoring/section-pipeline/` | 기존 절별 새 작성 시험 코드와 고정 근거. **시험용이며 새 작성 반복 재현성 미검증** |
| `configs/` | 보고서 모드/비용 승인 예시와 화학 모델 설정·자산 식별 예시. 모델 가중치·실행 환경은 미포함 |
| `provenance/` | 실제 마지막 요청/응답, 최종 문장 교정·20쪽 검증·비용 기록, 원본→제출 사본 대응 |
| `validation/` | 이번 파일·경로·비밀정보·이동성 점검 결과. 과학 재검증 결과가 아님 |
| `archive/` | 과거 원고·시안·수정 이력·중복 그림 원본. `baselines/`는 재조판 해시 보호에 필요하므로 포함하고 `local-checks/`만 GitHub 대상에서 제외 |

[패키지 점검](validation/package-check.json) · [파일 출처·해시 대응](provenance/package-copy-map.json) · [GitHub 반영 범위](GITHUB_INCLUDE.md) · [기계 판독 파일 목록](GITHUB_FILES.txt) · [전체 파일 해시](PACKAGE-MANIFEST.json)

## 1. 확정 제출본 생성 과정

이번 이동성 점검에서는 공백이 있는 별도 경로에서 저장 원고 렌더러가13개 그림을 찾는 것과, 다른 작업 폴더에서 새 작성 입력 준비가 네트워크 호출 없이 완료되는 것만 확인했다. 기존20쪽 과학·페이지 검사를 반복하지 않았다. [이동성 smoke 기록](validation/portability-smoke.json) · [확정 제출본 동일성](validation/frozen-deliverables.json).

기존20쪽 원고는 여러 Solar 작성·부분 수정, 검증된 문장 재사용, 허용된 삭제·기계적 교정과 조판을 거쳤다. 별도19쪽 절별 작성본으로 대체하지 않았다. 마지막에는 기존20쪽본 §6.1의 압력 설명 한 문장만 Solar1회로 작성하고 검증한 뒤 반영했다. 원문 도식의H₂3atm은 압력, Procedure1의3분자당량은 흡수량으로 구별한다. 온도는 확인된 원문 범위만 서술하고 Parrot 조건에 섞지 않는다.

마지막 응답의 과학적 단어는 그대로 유지했고 프로젝트 인용 표식만 원출처[18]로 정규화했다. 다른 본문은 동일함을 기존 DOCX/XML·PDF 대조로 확인했다. 기존 Word조판 코드를 사용해20쪽·그림13개를 검증했으며, PDF에는 같은 위치에 원본PNG 해상도를 복원했다. [마지막 변경·검증](provenance/final-validation/change-verification.json) · [실제 요청](provenance/pressure-call/request.json) · [원시 응답](provenance/pressure-call/response.raw.json).

따라서 최종 제출본은 **여러 호출과 교정을 거친 작성·조판 검증 결과**다. 한 번의 새 작성으로 완성됐다고 기록하지 않는다.

## 2. 저장 원고 재조판 — Solar 호출 없음

### 실행 위치와 세 가지 작업의 구분

**이 제출 폴더만 복사하지 말고 GitHub 저장소 전체를 내려받는다.** 새 물질 실행에 필요한 `scripts/`·`inputs/`·루트 `configs/`·실행 스킬은 제출 폴더 바깥에 있다. 저장소 루트는 `scripts/run_pipeline.py`와 `inputs/input-template.json`이 있는 폴더이고, 이 README의 위치는 그 아래 `submission/benzocaine-final-submission-20261128-01/`다.

| 작업 | 명령을 실행할 위치 | 입력과 범위 |
|---|---|---|
| 저장 원고 재조판 (§2) | 이 README가 있는 제출 폴더 | 확정 `report/report.md`를 DOCX/PDF로 변환. 새 작성·화학 추론 없음 |
| 벤조카인 저장 근거로 새 작성 (§3) | 같은 제출 폴더 | 고정된 벤조카인 근거로 절별 Solar 요청 준비·승인 후 작성. 새 물질 모델 실행 아님 |
| 새 물질 모델 실행 (§4) | 저장소 루트 | 별도 입력 JSON과 외부 모델 자산으로 경로·조건·수율 결과 생성. Solar 보고서까지 자동 완성하지 않음 |

일반적인 보고서 구성·표현·참조 규칙은 [일반 보고서 스킬](skill/synthesis-report-writing/SKILL.md)에 있다. §3의 실제 system 메시지는 [절별 새 작성 스킬](authoring/section-pipeline/skill/SKILL.md) 전체이며, 일반 스킬과 그 참조 문서를 자동으로 합쳐 읽는 방식은 아니다. 새 물질 입력·모델 운용 안내는 별도의 [루트 실행 스킬](../../skill/SKILL.md)을 따른다.

실제 당시의 단일 호출·입력 준비 코드는 `provenance/pressure-call/dispatch-source.txt`와 `prepare-source.txt`에 읽기 전용 이력으로 보존했다. 당시 작업폴더 구조를 전제로 하므로 현재 재실행 명령으로 사용하지 않는다.

Windows PowerShell에서 이 제출 폴더를 현재 폴더로 연다. Python3.13, Microsoft Word16 및 맑은 고딕이 사용된 환경이다. Python 의존성은 [requirements-report.txt](requirements-report.txt)에 고정했다. 수신자가 별도 가상환경에 준비해야 하며 이번 패키징에서 설치하지 않았다.

```powershell
# 의존성이 준비된 Python 가상환경을 활성화한 뒤 실행
python .\code\check_package.py
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\code\reflow.ps1 -OutDir .\work\reflow-new
```

이 명령은 저장된 `report/report.md`를 읽어 새 경로에DOCX/PDF를 만들 뿐 Solar를 호출하지 않는다. 이미 있는 출력 폴더는 거부한다. `archive/baselines/baseline20.md`, `provenance/final-validation/sentence-edit.json`, 실제 마지막 응답의 해시를 함께 확인한다. 이들은 재조판의 보호 입력이며 새 작성 모델에 제공할 정답이 아니다.

Word/폰트/라이브러리 버전이 다르면 페이지 배치가 달라질 수 있으므로 새 출력의 실제 쪽수는 Word 기록으로 확인한다. 재조판 성공을 새로운 과학적 정확도나 새 작성 재현성으로 해석하지 않는다. 확정PDF/DOCX는 재조판 출력으로 덮어쓰지 않는다.

## 3. 벤조카인 저장 근거로 새 작성 — 별도 승인 필요, 반복 재현성 미검증

다음은 기존 절별 새 작성 시험의 **오프라인 입력 준비** 명령이다. API를 호출하지 않는다.

```powershell
python .\authoring\section-pipeline\report_pipeline.py build --out .\work\new-writing-inputs
```

각 절에 필요한 근거·코드표·그림ID·허용 인용을 요청별로 만든다. 새 작성에는 `authoring/section-pipeline/skill/SKILL.md`와 이 폴더의 `data/`만 사용한다. 해당 데이터에는 최종 승인된 압력 정정과 현재 누적 원장 기준을 반영했다. 원래 근거 사본과 교정 overlay는 구분했다.

**완성 원고, report/·archive/ 전체, 과거 Solar 문장, provenance/ 응답, 보존 목록을 정답으로 새 작성 요청에 넣지 않는다.** `archive/history/skill/used-revision-system.txt`처럼 기존 원고 수정 지시는 새 작성 system에 혼합하지 않는다. 기존 데이터베이스/모델/문헌·그림 근거를 필요 절별로 제공하고, 표·수치는 저장CSV에서 코드로 생성한다.

새 호출은 새 명시 승인, 최신 요금·무료 크레딧·누적 원장, 요청해시·출력한도·합계 상한을 확인한 뒤에만 가능하다. [승인 예시](configs/approval.example.json)는 `approved=false`, 작업 한도0으로 잠겨 있다. 과거 승인은 모두 종료됐으며 남은 누적 금액이 새 호출 승인을 뜻하지 않는다. 키는 로컬 환경변수 `UPSTAGE_API_KEY`로만 제공하고 커밋하지 않는다. 이번에는 `--execute`를 사용하지 않았다.

시험용 실행 형식은 다음과 같다. 실제 승인서가 없으면 실행하면 안 되며, 현재 예시는 실행 승인이 아니다.

```powershell
# 새 승인과 준비된 요청 묶음이 일치할 때만 사용하는 형식 예시
python .\authoring\section-pipeline\report_pipeline.py build --out .\work\approved-new-run --execute --approval .\private\approval.json
```

기존 시험에서는 누락·인용·형식 오류로 중단한 기록과 별도 허용된 교정이 있었다. 제공한 파이프라인을 최종 제출본을 한 번에 다시 쓰는 검증 완료 프로그램으로 표시하지 않는다. 표식 검사를 통과해도 의미·근거·수치·인용·그림 및 절간 모순을 독립 검증해야 하며, 실패하면 중단하고 원시 응답을 보존한다. 자동 재시도는 없다. 통과한 새 원고의 조판은 별도 검증·계약이 필요하며 현재의 보호용 저장원고 조판 계약에 끼워 넣지 않는다.

**새 작성의 반복 재현성은 미검증이다.** 문구가 달라도 핵심 수치·경로 판단·조건 슬롯·문헌·추가 분석·한계가 일치하는지 반복 시험한 결과는 제공하지 않는다. 이번에 새 작성·새 화학 모델 추론은 하지 않았다.

## 4. 새 물질 모델 실행 — 저장소 루트에서 실행

이 절은 실행 안내이며 이번 README 보완 과정에서 설치·모델 실행을 수행했다는 뜻이 아니다. [입력 템플릿](../../inputs/input-template.json), [실행 스킬](../../skill/SKILL.md), [실제 실행 코드](../../scripts/run_pipeline.py)를 사용한다. 아래 명령의 인자는 해당 코드에서 확인했다. 파일명 `new-target.json`은 새 입력을 저장할 이름이며 벤조카인 데이터로 자동 대체되지 않는다.

### 입력 작성과 자산 준비

다음 블록은 **이 README가 있는 제출 폴더에서 시작**하여 저장소 루트로 이동한다. 입력 파일이 이미 있으면 덮어쓰지 않는다.

```powershell
Set-Location ../..
if (Test-Path ./inputs/new-target.json) { throw '기존 new-target.json을 보존하고 별도 입력 파일을 준비하세요.' }
Copy-Item -LiteralPath ./inputs/input-template.json -Destination ./inputs/new-target.json
notepad.exe ./inputs/new-target.json
```

템플릿의 이름·`target_id`·SMILES·`expected_formula`·`pubchem_cid`·의도한 화학형·구조 출처를 실제 대상의 확인된 값으로 입력하고 저장한 뒤에만 다음 단계로 간다. 템플릿의 빈 예시 문자열이나 CID 0은 실제 대상 정보가 아니다. 대상 물질이 지정되지 않았으므로 임의 구조·CID를 채워 제공하지 않는다. `prepare_target.py`는 이름으로 PubChem을 조회하고 CID·분자식·구조를 대조한다. 종료 코드만 보지 말고 출력 JSON의 `pubchem_status`가 `matched`인지 확인한다.

드라이버와 모델별 환경은 별도로 준비해야 한다. [드라이버](../../requirements-driver.txt)·[AiZynthFinder](../../requirements-aizynth.txt)·[Parrot](../../requirements-parrot.txt)·[수율 모델](../../requirements-yields.txt)·[stock 준비](../../requirements-stock-preparation.txt)의 의존성과 [자산 잠금 파일](../../configs/model-assets.lock.json)의 Python·패키지 버전·체크포인트 해시를 확인한다. 6개 모델 공식 출처는 [루트 실행 스킬](../../skill/SKILL.md)의 모델 표에 있으며, 패키지의 [출처 대응표](report/records/source-index.md)에도 보존되어 있다. 가중치·stock·모델 저장소·환경 자체는 제출물에 포함되지 않는다.

실행기는 패키지의 `configs/chemical-model-examples/runtime.json`이 아니라 **루트 [configs/runtime.json](../../configs/runtime.json)**을 기본으로 읽는다. 이 파일에서 참조하는 다음 환경변수에 실제 준비된 로컬 경로를 설정한다. 사용자별 경로를 추정해 명령에 넣지 않는다.

| 환경변수 | 준비할 실제 자산 |
|---|---|
| `AIZYNTH_PYTHON` | AiZynthFinder 환경의 Python 실행 파일 |
| `AIZYNTH_MODEL_DIR` | 잠금 파일과 일치하는 ONNX 모델·템플릿 디렉터리 |
| `AIZYNTH_STOCK_BUCKETS` | 검증된 `manifest.json` 및 A~Z `.keys`가 있는 stock 디렉터리 |
| `PARROT_PYTHON`, `PARROT_REPOSITORY`, `PARROT_CHECKPOINT` | Parrot 환경 Python·공식 코드 저장소·체크포인트 디렉터리 |
| `RXN_YIELDS_PYTHON`, `RXN_YIELDS_CHECKPOINT` | 수율 모델 환경 Python·체크포인트 디렉터리 |

설정은 현재 PowerShell 세션에서 `$env:` 환경변수로 제공한다. 다음은 경로를 직접 입력받아 존재 여부를 확인하는 방법이며 설치·다운로드를 대신하지 않는다.

```powershell
foreach ($assetName in @('AIZYNTH_PYTHON','AIZYNTH_MODEL_DIR','AIZYNTH_STOCK_BUCKETS','PARROT_PYTHON','PARROT_REPOSITORY','PARROT_CHECKPOINT','RXN_YIELDS_PYTHON','RXN_YIELDS_CHECKPOINT')) {
    $assetPath = Read-Host "$assetName 의 준비된 실제 경로"
    $resolvedAssetPath = (Resolve-Path -LiteralPath $assetPath -ErrorAction Stop).Path
    [Environment]::SetEnvironmentVariable($assetName, $resolvedAssetPath, 'Process')
}
```

stock bucket이 아직 없다면 [stock 준비 코드](../../scripts/prepare_stock_buckets.py)는 원본 HDF 파일에서 전체 InChIKey를 추출한다. 원본의 해시·행 수가 잠금 파일과 맞아야 하고 출력 디렉터리는 새 경로여야 한다. 필요할 때만 준비된 stock 환경에서 아래를 실행한 뒤, 생성된 디렉터리를 `AIZYNTH_STOCK_BUCKETS`에 지정한다.

```powershell
$stockPython = (Resolve-Path -LiteralPath (Read-Host 'tables가 준비된 stock 환경 Python 실행 파일 경로') -ErrorAction Stop).Path
$stockSource = (Resolve-Path -LiteralPath (Read-Host '잠금 파일과 일치하는 원본 stock HDF 파일 경로') -ErrorAction Stop).Path
& $stockPython -B -X utf8 ./scripts/prepare_stock_buckets.py --source $stockSource --output-dir ./work/new-target-stock
```

### 구조 확인 → 사전검사 → 결과 생성

다음도 **저장소 루트**에서 실행한다. 첫 두 검사를 통과한 뒤 마지막 블록을 실행한다. 구조 확인은 PubChem 네트워크 조회를 포함하고, 사전검사는 자산·해시·환경 import를 검사하지만 예측은 하지 않는다.

```powershell
py -3.13 -B -X utf8 ./scripts/prepare_target.py --input ./inputs/new-target.json --output ./validation/new-target-identity.json
py -3.13 -B -X utf8 ./scripts/preflight_models.py --input ./inputs/new-target.json --runtime ./configs/runtime.json --output ./validation/new-target-preflight.json
```

`validation/new-target-identity.json`의 구조 일치와 `validation/new-target-preflight.json`의 `status: passed`를 확인한다. 실패·미확인 상태이면 모델 실행으로 진행하지 않는다. 성공 후:

```powershell
$newRunId = 'new-target-live-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff')
py -3.13 -B -X utf8 ./scripts/run_pipeline.py --input ./inputs/new-target.json --run-id $newRunId
```

결과는 `results/` 아래 해당 `$newRunId` 폴더에 저장된다. 실제 코드가 만드는 주요 파일은 `input.json`, `routes.json`, `conditions-parrot.json`, `yields-rxn_yields.json`, `figures/`, `report-evidence.json`, 검증 기록과 `manifest.json`이다. 기존 run은 덮어쓰지 않는다. 경로 탐색·조건·수율의 성공 여부는 각각의 상태와 로그로 확인하며, 실패하면 후속 파일이 모두 생성된다고 보장하지 않는다. 이 진입점은 AiZynthFinder → Parrot → rxn_yields를 연결한다. SynthEx 정규화는 미구현이며, DRFP 자체는 수율 회귀기가 아니다. 다른 모델이나 MOPAC·EPI·Visualizer 분석을 이 명령이 모두 실행한다고 해석하지 않는다.

### 새 물질 결과와 절별 보고서 작성기의 연결 한계

`run_pipeline.py`는 `build_evidence.py`를 통해 새 run의 경로·단계·반응 SMILES로 조건과 수율을 연결한 `report-evidence.json`까지 만든다. 그러나 §3의 [절별 작성기](authoring/section-pipeline/report_pipeline.py)는 이 파일을 인자로 받지 않는다. 현재는 자기 폴더의 `data/evidence-units.json`·`data/citation-registry.json`·`data/figure-manifest.json`과 `config.json`을 읽고, 벤조카인 전용 코드 표를 생성한다. **새 run을 자동으로 가져오는 변환·연결 단계는 구현되어 있지 않다.**

따라서 새 물질 보고서에는 새 run의 원시 근거를 절별 근거 형식으로 변환하고, 대상별 표 생성·인용·그림·절 계약을 준비·검증하는 추가 작업이 필요하다. 벤조카인 고정 데이터의 파일명만 바꾸거나 새 물질 결과 옆에 둔다고 연결되지 않는다. 이후에도 별도 Solar 승인·내용 검증·조판 계약이 필요하며, 새 물질 모델 실행부터 최종 DOCX/PDF까지 자동 실행·검증됐다고 표시하지 않는다. 현재 새 작성기의 벤조카인 고정 근거는 해당 보고서 시험의 범위이며, 새 물질 화학 모델 입력 자체를 벤조카인으로 제한하는 하드코딩과는 구분한다.

## 외부 자료·상대경로·비밀정보

보고서PDF/DOCX 내부의 `records/...` 자료 링크는 바로 옆 `report/records/`에서 열린다. 원고 그림 경로도 확정 그림과 같은 파일로 연결했다. 스킬 참조·실행 코드·설정 예시의 필수 참조는 제출 폴더 상대경로 또는 명시 환경변수를 쓴다. [경로 처리 설명](provenance/portability-notes.md).

일부 과거 기록의 `external-originals/`나 원래 저장소의 `reviews/...` 등 일반 문자열은 출처 이력이며 실행 경로가 아니다. 실제 패키지 파일 링크는 [자료 대응표](report/records/source-index.md)를 사용한다. 홈PC 경로를 표시화한 공개 사본은 원본과 제출본 해시를 구별했다. 원래 프로젝트 파일은 바꾸지 않았다.

실제 `.env`·API키·개인 가상환경·가중치·과거 승인서는 넣지 않았다. [.env.example](.env.example)은 빈 값 예시다. 외부 원문PDF/강의자료·대용량 모델 자산의 미포함 범위와 확보 방법은 [외부 자료 안내](provenance/sources-acquisition.md)에 있다. 이것은 저장 원고 재조판에 필요한 파일 누락이 아니다.

최신 프로젝트 사용량 기준 누적은 $1.38633932, 누적 한도는 $1.50이다. 실제 Console 크레딧 차감액/잔액·Paid with credits·Postpaid는 새로 확인하지 않았다. 이번 정리 비용과 Solar 호출은0이다.
