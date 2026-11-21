---
name: synthesis-pipeline
description: 물질 입력을 확인하고 합성 경로·조건·수율 예측과 실제 분석 자료를 수집한 뒤, 보고서 작성 스킬로 Solar Pro 4 요청을 준비하는 전체 파이프라인 안내.
---

# AI 유기합성 전체 실행 스킬

## 역할

이 스킬은 물질 입력부터 구조 확인, 합성 경로·단계별 조건·수율 예측, 결과 및 추가 분석 근거 취합, 보고서 작성 스킬 호출까지의 파이프라인을 안내한다. 보고서 문체·구성·인용·DOCX/PDF 규칙은 [보고서 작성 스킬](report-writing/SKILL.md)에서 관리한다. Solar Pro 4에 보고서 작성을 요청할 때는 실행 코드가 해당 파일 전체를 system 지침으로 포함해야 한다.

기본 결과물은 전체 보고서다. 특정 절·문장만 수정하는 동작은 사용자가 그 범위를 명시했을 때만 별도로 수행한다. 과거 프롬프트·하네스 비교·수정 요청을 새 보고서 작성 지침에 자동으로 섞지 않는다. 저장된 Solar 응답을 문서로 변환하는 일은 새 모델 호출로 기록하지 않는다.

스킬 파일만 복사해서는 실행할 수 없다. 모델 어댑터, Python 의존성, 모델 코드·가중치·재고 데이터, 입력·결과 파일, 문서 변환 도구가 별도로 필요하다. 설치·호출 전 현재 설정과 명시적 승인을 확인하고, 준비되지 않은 항목을 임의 데이터로 대체하지 않는다.

## 실행 흐름

### 1. 물질 입력과 구조 확인

저장소 전체를 복사해 사용하고 `inputs/input-template.json`을 `inputs/<target_id>.json`으로 복사한다. 이름, 의도한 화학형, 입체화학·염 상태, SMILES, 예상 분자식, PubChem CID 또는 신뢰 가능한 구조 출처를 입력한다. RDKit과 출처 정보로 이름·구조·분자식을 대조한다. 불일치나 모호함이 있으면 추론을 시작하지 말고 검증 기록에 남긴다.

```powershell
py -3.13 -B -X utf8 scripts/prepare_target.py `
  --input inputs/<target_id>.json `
  --output validation/<target_id>-identity.json
```

### 2. 모델 자산·설정 사전검사

모델별 격리 환경, 실행 파일, 체크포인트·토크나이저, 체크섬, AiZynthFinder 설정과 stock bucket이 준비됐는지 검사한다.

```powershell
py -3.13 -B -X utf8 scripts/preflight_models.py `
  --input inputs/<target_id>.json `
  --output validation/<target_id>-preflight.json
```

필요한 공식 모델 출처와 준비 안내:

| 기능 | 공식 저장소·문서 | 운용 원칙 |
|---|---|---|
| 역합성 경로 | [AiZynthFinder](https://github.com/MolecularAI/aizynthfinder) | 모델·stock 설정과 체크섬을 기록한다. 탐색 완료나 점수는 실험 가능성·수율의 증거가 아니다. |
| 경로 대안 | [SynthEx](https://github.com/schwallergroup/synthex/tree/submission) | 이 프로젝트에서 어댑터·실행 검증이 없으면 `not_implemented` 또는 미실행으로 둔다. |
| 조건 대안 | [ASKCOS v2 context recommender](https://gitlab.com/mlpds_mit/askcosv2/context_recommender) | 실제 서비스·모델을 실행하지 않았으면 결과를 만들지 않는다. |
| 조건 추천 | [Parrot](https://github.com/wangxr0526/Parrot) | 슬롯 필드·순위·반응 SMILES를 원시 출력과 연결한다. |
| 수율 예측 | [rxn_yields](https://github.com/rxn4chemistry/rxn_yields) | 체크포인트, 정규화, 적용 범위를 기록한다. 반응 구조만 입력했다면 조건별 실험 수율이 아니다. |
| 반응 지문 | [DRFP](https://github.com/reymond-group/drfp) | DRFP 자체는 수율 회귀 모델이 아니다. 별도 회귀기 없이는 수율 예측기로 취급하지 않는다. |

가중치·대용량 재고 데이터는 저장소에 포함하지 않는다. `configs/model-assets.lock.json`, 모델 설정 예시와 README의 공식 다운로드·버전·체크섬 안내에 따라 별도로 준비한다. 지원되지 않는 OS·Python·모델 버전을 확인 없이 호환된다고 가정하지 않는다.

### 3. 경로·조건·수율 예측

사전검사가 통과했을 때만 새로운 run ID를 사용한다.

```powershell
py -3.13 -B -X utf8 scripts/run_pipeline.py `
  --input inputs/<target_id>.json `
  --run-id <target_id>-live-YYYYMMDD-01
```

실제 결과는 `results/<run_id>/`에 저장한다. 원시 요청·응답, 로그, 정규화 결과, 구조 그림, 매니페스트와 검증 결과를 보존하고 기존 run을 덮어쓰지 않는다. 모델 호출·도구 실행에 실패하면 실제 오류와 `not_implemented`, `not_run`, `unsupported` 등 정확한 상태를 기록한다. Mock Data를 실제 결과로 제시하지 않는다.

경로·조건·수율은 `route_id`, `step_id`, 정확한 반응 SMILES로 연결한다. 다단계 경로의 중간체 순서와 각 단계의 반응물을 유지한다. 다른 후보 순위나 단계의 조건 토큰을 옮기지 않는다. 조건 슬롯의 공란은 모델 출력 공란으로 보고하며 해당 성분이 실험에서 사용되지 않았다는 뜻으로 확대 해석하지 않는다. 단계별 모델 수율을 곱해 검증된 전체 수율로 만들지 않는다.

### 4. 실제 추가 분석 결과 취합

추가 분석은 실제 원시 출력·실행 기록·측정 캡처가 있을 때만 결과로 취급한다. 계획·준비 파일은 계산 완료로 표현하지 않는다.

- MOPAC: 입력·출력, 방법, 전하·다중도, 시작 배좌, 수렴, 원자 번호·단위 및 해석 범위를 확인한다. 서로 다른 조성의 총에너지를 직접 순위화하지 않는다.
- EPI Suite: 예측 물성과 측정·참조 자료를 구분한다. 순물질 BP/MP만으로 반응 혼합물의 상태를 단정하지 않는다.
- Discovery Studio Visualizer: 실제 화면·측정 기록만 사용한다. 분자 내부 기하와 반응물 사이 접근성은 구분한다.
- 하네스 비교: 같은 보고서 작성 스킬과 입력을 쓰되 각 하네스의 프롬프트·설정 차이를 기록한다. 소수 실행은 사례 비교이지 일반적인 성능 우열의 증거가 아니다.

도구별 입력·버전·체크섬·출력 및 미완료 사유를 저장하고, 그 증거를 `report-evidence.json`과 해당 분석 파일에 연결한다. 기존 분석 자료가 준비돼 있으면 `scripts/prepare_additional_analyses.py`가 만든 목록과 최신 상태 파일을 검토하되, 오래된 상태 문구보다 실행 ID가 일치하는 최신 원시 기록을 우선한다.

### 5. 보고서 작성 스킬 호출

보고서 생성 요청 전 `configs/report-plan.json`의 `report_writing_skill_path`가 `skill/report-writing/SKILL.md`를 가리키는지 확인한다. 보고서 요청에는 다음 자료를 제공한다.

- 표적 물질 입력 JSON 및 구조 확인 결과
- 실행 ID, manifest, `report-evidence.json`, 정규화 경로·조건·수율, 원시 결과 위치, validation notes와 실패 로그
- 실제 추가 분석의 결과·상태·측정표·캡처·분석 제한
- 출처 목록·인용 매핑·재현 방법
- 구조/경로 그림 파일, 캡션 및 그림 manifest

모델은 현재 `report_writing_skill_path`가 지정한 보고서 작성 지침으로 Solar 요청을 구성한다. 경로 지정이나 필요한 근거가 없으면 값을 추정해 채우지 말고 누락 항목을 고지한다. Solar 작성은 유료 외부 호출일 수 있으므로 키·예산·승인 게이트를 확인한다. API 키를 인쇄하거나 원시 요청 로그에 포함하지 않는다.

실제 호출 전 system message의 스킬 내용이 보고서 작성 스킬과 바이트 단위로 일치하고 user message에 실제 근거가 포함됐는지 오프라인 검사한다. 실행 기록에는 사용한 보고서 작성 스킬 경로·SHA-256, 입력 파일 목록·해시, 모델 snapshot, 토큰 설정, 요청·응답·비용·오류를 연결한다.

**보고서만 생성하는 모드**는 저장된 run을 사용하고 화학 예측기를 재실행하지 않는다. **새 물질 모드**는 입력별 새 run ID를 만들고 그 run의 추가 분석만 연결한다. **저장 응답 문서화 모드**는 Solar나 화학 모델을 호출하지 않고 DOCX/PDF만 다시 만든다. 저장소 README에 정의된 A/B/C 절차를 따른다.

### 6. 문서 생성과 검증

Solar Pro 4는 보고서 원고를 작성하고, 저장소의 코드가 DOCX를 생성하고 Word 또는 문서 변환기로 PDF를 만든다. 문서 작성·인용·그림 삽입·20쪽 제한의 세부 규칙은 [보고서 작성 스킬](report-writing/SKILL.md)을 따른다. DOCX/PDF 파일 각각 참고문헌과 부록을 포함해 20쪽 이하인지 검증하고, 전체 PDF를 렌더링해 표·그림·SMILES·캡션의 잘림과 본문/근거의 일치를 점검한다.

현재 구현 경로는 `scripts/export_report_docx.py`, `scripts/convert_docx_to_pdf.ps1`, `scripts/audit_citations.py` 및 release별 validator다. 저장된 응답 재생성과 새 물질의 전체 추론은 별도 절차로 기록한다.

## 기본 설정

- 파이프라인 안내 스킬: `configs/report-plan.json`의 `execution_skill_path` (`skill/SKILL.md`)
- Solar system message에 포함할 보고서 작성 스킬: `report_writing_skill_path` (`skill/report-writing/SKILL.md`)
- 입력 예시와 의존성·환경·가중치 준비: `README.md`
- 실행 코드: `scripts/`

실패·누락·적용 범위 불확실성을 숨기지 않는다. 성공적인 파일 생성이나 파싱을 화학적 정확도, 실험 재현성, 반응 성공·수율 검증과 같은 뜻으로 표현하지 않는다.
