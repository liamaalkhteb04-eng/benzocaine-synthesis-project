# AI 유기합성 보고서 작성 스킬

## 역할과 원칙

제공된 물질 입력, 원시 예측, 검증 기록, 계산 결과, GUI 관찰, 분석 계획, 출처를 읽고 자연스러운 한국어 학술 보고서를 작성한다. 보고서는 검토 가능한 과학적 근거를 설명하며 실험 프로토콜을 임의로 완성하지 않는다. 프로젝트의 보고서 본문은 Solar Pro 4가 작성한다. 문체나 해석을 고칠 때는 이 스킬과 보고서별 브리프를 보완하고 모델이 다시 작성하게 한다. DOCX/PDF의 표·그림 배치, 글꼴, 구조식 표시 오류는 변환 코드에서 고친다. 이미 저장된 Solar 응답을 문서로 변환하는 일은 새 모델 호출로 표시하지 않는다.

`success`는 어댑터가 결과 파일을 만들고 형식 검사를 통과했다는 상태다. 그 자체로 반응 예측의 정확도, 물질의 실험 합성, 수율 또는 모델의 외부 검증을 의미하지 않는다. 모델이 실제 실행되지 않았거나 적용 범위가 확인되지 않았으면 그 상태를 그대로 쓴다.

## 근거 선택과 충돌 처리

1. 물질의 이름, 구조, 분자식, 전하 상태는 사용자가 제공한 입력과 검증된 구조 일치 기록으로 확인한다. 보고 대상 SMILES를 원시 반응 SMILES, 구조 그림, 문서의 표·본문과 대조한다.
2. 보고서별 브리프에 `current` 권위 파일과 충돌 해결 기록이 있으면, 과거 상태 파일보다 이를 우선한다. 과거 하네스 입력과 초안은 당시의 사례를 설명하는 자료로만 쓴다.
3. 모든 경로, 반응 단계, 조건, 수율은 `route_id`, `step_id`, 반응 SMILES가 모두 맞는 원자료끼리 연결한다. 다단계 경로에서는 각 중간체와 의존 관계를 보존한다.
4. 계산·모델 출력, 데이터베이스 레코드, 문헌값, GUI에서 직접 읽은 측정값, 정성 관찰, 미수행 항목을 구분한다. 누락값·실패값을 추정으로 채우지 않는다.
5. 근거가 없는 메커니즘, 전자 이동, 활성화 장벽, 속도, 반응 성공, 실험 수율, 용액 내 상 상태를 모델 결과처럼 쓰지 않는다.

## 문체와 전문용어

자연스러운 한국어 학술 문체를 사용한다. 독자가 “왜 이 물질을 다루는가 → 각 후보 경로에서 구조가 어떻게 달라지는가 → 조건·수율 예측을 어디까지 신뢰할 수 있는가 → 어떤 경로를 어떤 이유로 먼저 검토할 것인가”를 따라가게 구성한다. 작성 방법이나 과제 지시를 본문에 노출하지 않는다.

전문용어는 실제 결과를 설명하는 문장에서 처음 쓸 때 한국어와 영어를 함께 쓴다. 예: 역합성 분석(retrosynthetic analysis), 전구체(precursor), 배좌(conformer), 기하 최적화(geometry optimization), 부분전하(partial charge). 이후 같은 개념에는 하나의 한국어 용어를 일관되게 사용한다. 약어는 처음에 풀어 쓰고, 화학종·반응물·용매·촉매·시약을 혼동하지 않는다.

SMILES, 전하, 결합 표기에서 `[N+]`, `[O-]`, 괄호, `>>`, 점으로 연결된 조각을 정확히 보존한다. 긴 원시 문자열은 좁은 표 셀에 반복하지 말고 별도 코드 문단이나 저장소 원자료로 연결한다. 구조 그림은 원시 SMILES로 나타낸 분자와 일치해야 한다. 모든 그림에는 필요한 경우 물질명, 경로·단계 번호, 작용기 변화가 표시되어야 한다.

## 보고서 구성

물질과 증거에 맞게 절 제목과 분량을 조정하되, 참고문헌·부록을 포함해 20쪽 이내로 작성한다.

1. 표적 물질 및 선정 근거: 입력 구조의 눈에 띄는 작용기·구조 특징이 후보 경로 비교와 가능한 추가 분석에 어떤 질문을 제공하는지 설명한다. 사용자가 선택했다는 사실만으로 화학적 우수성을 주장하지 않는다.
2. 입력·모델·실행 범위: 모델마다 입력과 출력, 실행 버전·설정, 실제 성공/실패, 검증된 범위와 미검증 범위를 설명한다. 사용하지 않은 도구는 실행 결과처럼 쓰지 않는다.
3. 전체 탐색 결과와 경로 선정: 모든 탐색 후보 수, 해결 상태, 단계 수, 점수의 의미와 한계를 원시 결과로 확인한다. 전체 후보, 검토 shortlist, 자세히 설명한 대표 경로를 구분한다. 선정은 검색 순위·다양성 등 기록된 기준에 한정하며 실행 가능성을 암시하지 않는다.
4. 대표 경로의 단계별 구조 변화: 출발물질·생성물 이름, 동일 경로/단계 번호, 변화한 작용기, 보존된 구조를 그림과 설명으로 연결한다. retrosynthetic edge가 실험적인 정방향 반응으로 확인된 것이 아니면 명시한다.
5. 통합 조건·수율 표: 실제 경로 단계당 한 행을 두고, 반응물/생성물 및 작용기 변화, 상위 조건 후보와 모델 점수, 온도·시간·당량·조건 수율, 수율 모델의 단계별 예측과 검증 상태를 연결한다. 누락값은 정확히 `NOT SUPPLIED`로 표기한다. 모델이 빈 문자열을 반환했다면 “모델 출력 슬롯이 비어 있음”으로 쓰며, 실험에서 성분이 없었다고 단정하지 않는다. 조건 후보 점수는 수율·확률·실험 성공률이 아니다. 중복 수율 표를 만들지 않는다.
6. 모델의 성능과 한계: 이번 실행에서 검증한 파싱, 구조 일치, 경로/단계 연결, 출력 범위 및 수렴 여부와 실제 정확도 검증을 구분한다. 타깃별 시험 데이터가 없으면 성능 수치나 일반화 성능을 만들지 않는다.
7. 추가 분석: MOPAC, EPI Suite, Visualizer, 하네스 비교 등 제공된 실제 증거만 보고한다. 아래의 각 전용 원칙을 따른다.
8. 종합 결론: 어떤 경로를 우선 검토할지 조건부로 답한다. 근거가 되는 구조 변화·조건 출력·누락 정보·추가 분석을 함께 언급한다. 우선 검토는 실험 권고나 최적 경로 판정이 아니다. 결론을 바꿀 수 있는 문헌·시약·조건·적용 범위 정보와 실험 전 확인 사항을 명시한다.
9. 재현 방법, 외부 참고문헌, 프로젝트 증거 목록 및 간결한 부록. 환경 변수, 모델 저장소, 가중치·재고 준비, 입력 예시, 실제로 기록된 명령을 설명한다. 키나 다른 비밀 값을 공개하지 않는다. 저장된 예측을 이용한 문서 재생성과 새 물질의 새 추론을 구분한다.

## 전용 해석 원칙

### 경로·조건·수율

- 경로 탐색기는 구조를 입력받아 template/정책 또는 탐색 기반 전구체 분해를 출력한다. `solved`, 재고 플래그, 점수는 벤더 재고의 현재성이나 실험 가능성을 보증하지 않는다. 생략된 시약, 부산물, 보호기, 선택성 문제가 있으면 설명한다.
- 조건 모델이 촉매·용매·시약 슬롯만 출력하면 이를 후보 조합으로 부른다. 온도·시간·당량이 출력되지 않으면 빠진 정보로 남긴다. 이상한 SMILES 토큰은 화학적 형태를 임의로 바꾸지 않는다.
- 수율 모델이 반응 SMILES만 받았다면 조건별 실험 수율이 아니다. 정규화 복원에 사용한 체크포인트와 훈련 통계, 적용 범위 평가 여부를 설명한다. 독립 단계 예측을 곱해 검증된 전체 수율로 만들지 않는다.
- 오픈소스 모델에 관한 공식 저장소와 필요한 가중치/입력 형태를 인용한다. 이번에 실제 실행하지 않은 모델의 결과를 채워 넣지 않는다.

### MOPAC 및 양자 계산

- 실제 원시 입력·출력, 사용 버전, 방법, 전하, 다중도, 시작 배좌, 수렴 판정과 단위를 기록한다. 부분전하를 관찰 가능한 전하처럼 설명하지 않는다.
- 서로 다른 분자식·전하·조성의 총에너지를 비교해 안정성이나 반응성 순위를 매기지 않는다. 고립 분자 구조·결합 길이·부분전하는 반응성 기작, 전이상태, 활성화 장벽, 속도, 수율의 증거가 아니다.
- 진동수 분석이 없으면 최적화 구조가 진정한 국소 최소점으로 확인되었다고 단정하지 않는다.

### EPI Suite 및 물성

- MPBPWIN 모델 추정과 데이터베이스/문헌 출처가 있는 레코드를 분리한다. 실험 기원과 압력 조건을 확인할 수 없으면 직접 실험값으로 부르지 않는다.
- 순물질의 녹는점·끓는점만으로 반응 혼합물의 석출·기화·반응 상태를 확정하지 않는다. 판단에 필요한 온도, 압력, 용매·농도·당량, 염/수화 상태, 용해도 및 혼합물 자료를 적는다.
- 서비스 오류 또는 degraded 상태, 구조 지원 범위 밖 입력, 응답하지 않은 값은 그대로 보고한다.

### Discovery Studio Visualizer 및 3차원 관찰

- 실제 GUI 화면의 물질, 원자 번호, 배좌, 프로그램 버전, 거리/각도, 단위를 원본 측정 기록과 대조한다. 화면 확대·자르기는 화면 캡처 가공임을 구분하고 원본 캡처를 보존한다.
- 분자 내부 거리·결합각과 서로 다른 반응물 사이의 접근 거리·공격각을 혼동하지 않는다. 별도 분자를 함께 놓지 않았으면 반응물 접근을 측정했다고 쓰지 않는다.
- 여러 방향 화면은 단일 분자의 투영에서 본 정성적 노출/가림으로만 설명한다. 구조 정렬·고정 회전 복사본은 새 배좌가 아니다.
- Visualizer 정적 구조로 활성화 장벽, 반응 속도, 합성 성공이나 수율을 확정하지 않는다. 미완료 측정과 화면 오류를 숨기지 않는다.

### 하네스 비교

- 실제로 저장된 각 초안의 구체적 누락·모순·과장 사례를 인용 가능한 원문과 대조한다. 저장된 응답을 재문서화한 작업은 새 모델 호출 비교가 아니다.
- 동일 skill/input/model/settings를 썼더라도 실제 요청 페이로드의 시스템 메시지, 래퍼, 도구, 재시도 차이를 기록한다. 1회 실행은 사례 비교이며 일반 성능의 우열 증거가 아니다.
- 사실 일치, 근거 인용, 필수 내용, 읽기 쉬움, 누락과 과장을 중심으로 비교한다. 토큰·시간·비용은 보조 지표다.

## 그림·표·출처 검증

- 원시 구조/반응 SMILES, 경로 ID와 단계 번호, 반응 그림의 원자 연결·전하·결합 기호를 서로 대조한다. 그림의 강조색은 식별 가능한 구조 변화만 표시한다.
- `report_figure_assets`에 등록된 각 그림을 캡션과 함께 본문에 한 번씩 배치한다. 그림은 실제 생성된 자산만 사용한다.
- 모든 정량 사실과 외부 자료에는 인접 인용을 둔다. 외부 문헌 번호는 실제 URL로 연결한다. 생성된 프로젝트 증거는 `[D1]` 등 파일 식별자로 연결하고 해당 파일 목록을 제공한다.
- 작성 지시문, `TODO`, 가짜 인용, 알 수 없는 주소, 미제공 수치, placeholder를 최종 본문에 노출하지 않는다.

## 최종 품질 게이트

보고서 Markdown을 DOCX로 변환하기 전에 대상 이름·SMILES, 모든 선택 단계, 숫자와 단위, 표의 행 연결, 필수 그림, 출처 URL, D 증거 목록, 미수행 상태를 결정적으로 검사한다. DOCX/PDF 변환 뒤 실제 전체 페이지 수를 확인하고 20쪽을 넘으면 글을 직접 고치지 말고 이 스킬 또는 보고서 브리프의 편집 지침을 고쳐 Solar로 다시 작성한다. 변환 문제는 코드에서 해결한다. 전체 PDF 페이지를 렌더링해 글자·그림·표 잘림, 작은 글씨, 불필요한 공백, 중복, 지시문 노출을 확인한다. DOCX의 이미지·표와 Solar 원문 일치도 확인하고, 저장 응답 재사용 검증과 새 물질 추론 검증의 범위를 구분해 기록한다.

## Final Korean copy and condition-slot fidelity
- Use ?normalization output? or a precise description of the cited training script; never use an unnatural phrase such as ?normalization launch script.?
- For Parrot tables, preserve each returned field exactly: `catalyst1`, `solvent1`, `solvent2`, `reagent1`, `reagent2`. Do not merge solvent and reagent slots into an ambiguous label. For route-05/step-02, raw rank 1 has empty catalyst1, solvent1 `CCO` (ethanol), empty solvent2, reagent1 `CCOCC` (diethyl ether token), and reagent2 `FB(F)F` (BF3 token). State that these are model slots, not validated experimental roles. Verify the raw and normalized files with the Parrot slot audit before describing them.
- When reporting numerical MOPAC geometry, charges, or heat values, cite the calculation-specific result summary `[D5]` as well as general method references where useful.
- Ensure headings remain with the first paragraph/table they introduce. Remove orphan headings and authoring/meta instructions from the final document.

## Citation source scope and prevention rules

- Treat a repository or official manual as evidence for what a tool implements and how its method is intended to work. It does not verify this project's outputs. Cite the matching project evidence file beside every run-specific number, status, model slot, computed value, or observation.
- Use this project map when preparing a report: AiZynthFinder method [2] plus route outputs [D1]; Parrot method [5] plus conditions [D1]; rxn_yields method [6], normalization implementation [8], training data [9] / data exploration [15], and predictions [D1] with validation [D4]; MOPAC method [10], GNORM documentation [11], and actual calculation outputs [D5]; EPA EPI Suite scope/method [12], Web beta endpoint [13], returned results and provenance [D6], and external acetic-acid reference values [14]; course mechanism claims cite reference [17] with the exact PDF page range; Visualizer observations/measurements cite [D7]; harness executions and comparisons cite [D8].
- Never use [5] (Parrot) to support MOPAC calculations or [6] (rxn_yields) to support EPI Suite values. A model repository cannot support a reported run value unless the run's project evidence is also cited.
- Keep each bibliography number bound to its listed URL or file. When adding, removing, or renumbering references, update citations by claim paragraph, then verify every in-text number exists, every cited source supports that claim, and each [D#] resolves to the matching evidence-list entry. Do not bulk replace citation numbers across the report.
- Run `scripts/audit_citations.py` before document conversion. Treat its claim-to-source checks as a minimum gate; review the underlying official source and referenced project file for each cited claim, not just the citation number.

## Primary-literature comparison and replay scope

- When a direct primary source reports the same starting material and product, compare it as experimental literature evidence separate from model output. Record source locator (DOI/URL, page and procedure/example), catalyst, hydrogen source/reductant, solvent, temperature, time, pressure, isolated or analytical yield, yield definition, and every unreported condition. Never infer a missing condition.
- Keep each Parrot candidate rank as its own row. Preserve `catalyst1`, `solvent1`, `solvent2`, `reagent1`, and `reagent2` exactly; do not combine a hydrogen token from one rank with another rank. Distinguish the model slot from a chemical interpretation.
- A Yield-BERT value from reaction SMILES alone is not conditioned on cited literature conditions. If numerically juxtaposed to a literature yield, label the arithmetic difference in percentage points, state yield-definition/condition differences, and say dataset overlap is unknown unless established. A single example is neither an accuracy estimate nor experimental validation.
- Use primary-source evidence for experimental claims and the matching project evidence file for model outputs. Keep the bibliography references and evidence IDs distinct.
- Report reruns with exact molecule, run ID, counts, mapping checks, and environment scope. A same-PC rerun of the same molecule does not establish portability to another molecule or computer.
- Use only the run-specific evidence paths and corrected validation artifacts explicitly identified in the current task. Do not reuse evidence pointers from an earlier request when a newer corrected record is identified. Preserve original runs and reports.


- Before authoring any route/step condition sentence, filter the raw candidate by the exact reaction SMILES and exact `(route_id, step_id)` mapping. Verify every named slot against that candidate; never transfer a condition token from another route or shared reaction record. Keep raw model slots distinct from chemical-role interpretation.
- For literature values, distinguish solvent composition (for example, 95% alcohol) from isolated yield. Verify yield basis and reported mass against the primary source record; do not convert a solvent percentage into a yield.

- If the current task authorizes edits to named sections only, follow that narrow scope and do not apply unrelated sections from the general report outline. Use a focused instruction set for section-level revisions.
## Evidence-led route rationale and replay-hash reporting

- When primary-literature comparison is available, distinguish the model-generated route ranking from literature reviewed after inference. State explicitly that post-inference literature research was not part of the model inputs and did not affect model scores.
- Explain a route's conditional priority using directly matching transformation evidence, while retaining alternatives/comparison routes for their stated roles. Do not convert literature conditions into model predictions or merge distinct model candidates.
- For execution-asset reproducibility, compute comparisons from saved run-specific manifests and file SHA-256 values. Do not copy an inconsistent summary boolean without checking its source.
- Report separately: model binary, reaction-template archive, source stock and derived stock-file hashes; materialized configuration byte hashes; and semantic configuration comparison after documented path normalization. A matching prediction is not evidence that assets match.
- If a historical temporary configuration is missing, say that the byte-level difference is unresolved; do not attribute it to path separators unless the exact hashed bytes are available. If the historical config-template hash is absent, mark that comparison unavailable.
- Preserve run roles: identify which run produced route search, which representative bundle supplied successful conditions/yields, and which rerun is compared. Never conflate copied route artifacts with newly executed stages.
- Keep the original conflicting validation artifact unchanged. Create a separate corrected record from evidence, compute pass/fail checks, and preserve failed checks as failures. Never edit values merely to obtain a passing status.
