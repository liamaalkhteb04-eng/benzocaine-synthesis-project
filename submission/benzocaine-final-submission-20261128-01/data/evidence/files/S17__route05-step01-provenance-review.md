# route-05/step-01 provenance review

작성일: 2026-11-24  
범위: 읽기 전용 route tree·selected route·template·evidence join 확인

기존 수율 적용성 검토, Parrot 조건 검토, 수율 보완 검토 파일은 수정하지 않았다.

## 결론

`CC(=O)O>>CCO`는 수율 adapter가 무작위로 만든 문자열이라고 볼 근거는 없다. 원시 선택 경로에는 **최종 esterification의 retrosynthetic tree에서 ethanol(`CCO`)을 precursor로 만들기 위해 acetic acid(`CC(=O)O`)까지 내려간 branch**가 실제로 존재한다. 다만 tree의 reaction edge는 retrosynthesis 방향인 `CCO>>CC(=O)O`로 기록되어 있고, yield evidence는 forward prediction 입력으로 `CC(=O)O>>CCO`로 기록되어 있다. 따라서 확인되는 것은 “route/tree edge를 forward yield 입력으로 뒤집어 연결한 것”이지, Parrot이 acetic acid→ethanol의 실험 합성을 독립적으로 제안했다는 사실이 아니다.

route-05에서는 이 edge가 최종 단계의 ethanol precursor로 연결되므로 **순차 경로에 포함된 공급 branch**이다. 그러나 그 branch가 실험적으로 유효한 ethanol 제조 단계라는 근거는 없다. `CC(=O)O`는 tree에서 `in_stock: true`인 terminal precursor이고, step-02에는 `depends_on: [step-01]` 및 precursor `CCO`가 기록되어 있다.

따라서 현재 `77.5889%`는 모델이 forward SMILES `CC(=O)O>>CCO`에 대해 출력한 숫자일 뿐, route-05의 실제 ethanol 공급 수율이나 benzocaine 합성 단계 수율로 비교할 수 없다. 이 단계는 원본 route/template 의미가 해결되기 전까지 수율 비교 대상에서 제외하는 것이 타당하다.

## 직접 확인한 증거

| 확인 항목 | 저장소 근거 | 관찰 |
|---|---|---|
| 선택 route root | `reports/benzocaine-final/evidence-run/latest-route-reproduction/routes-selected-raw.json`, `route-05` | root `smiles`는 benzocaine `CCOC(=O)c1ccc(N)cc1`; `number of reactions: 2`, `number of pre-cursors: 2`, `is_solved: true` |
| 최종 retrosynthetic edge | 같은 파일 `route-05.children[0]` | reaction edge는 `[C](=O)(CH3)OCH3 >> acetic acid + alcohol`의 mapped/template 표현이며, mapped reaction은 PABA ester에서 PABA + ethanol로 분해하는 방향이다. 저장된 canonical reaction은 `CCO.Nc1ccc(C(=O)O)cc1>>benzocaine`로 evidence에 materialized된다. |
| ethanol branch | 같은 파일의 first child `smiles: CCO` | `CCO`가 최종 esterification edge의 precursor child로 존재한다. |
| branch source | 같은 파일 `CCO.children[0]` | tree reaction edge는 `[C]([CH3])[OH]>>O=[C]([CH3])[OH]`, 즉 **CCO → CC(=O)O** 방향이다. child terminal은 `smiles: CC(=O)O`, `in_stock: true`다. |
| template provenance | 같은 branch metadata | `template_code: 32658`; `template_hash: c42f96a0658c03bc12dc20efce06e66daaeccc675d73631eea24ea610a7227b8`; `classification: 0.0 Unrecognized`; `library_occurrence: 3921`; `policy_probability: 0.09149999916553497`; `policy_probability_rank: 0`. |
| yield join | `reports/benzocaine-final/evidence-run/report-evidence.json`, route-05 steps | step-01 `reaction_smiles: CC(=O)O>>CCO`, `yield_percent: 77.58890327412914`, `predicted_not_validated`; step-02 `depends_on: [step-01]`, precursor `CCO`, product benzocaine. |
| output/route distinction | `reports/benzocaine-final/evidence-run/report-evidence.json` limitations | `overall_yield_percent: null`; independently predicted steps are not combined; route/template stock membership does not prove practical feasibility and omitted agents may exist. |

## 실제 모델 제안인가, 정규화 문제인가

### 확인된 부분

1. Route search가 benzocaine root에서 retrosynthetic disconnection을 만들었다.
2. 그 disconnection의 ethanol precursor를 다시 tree에서 찾았고, terminal stock precursor로 acetic acid가 연결되었다.
3. tree edge는 retrosynthesis 방향 `CCO>>CC(=O)O`로 보존되어 있다.
4. yield adapter/evidence는 forward reaction 형식 `CC(=O)O>>CCO`를 사용했다.

### 확인되지 않은 부분

- Yield 모델이 acetic acid를 실제로 ethanol로 합성할 수 있다고 독립 판단했다는 증거
- step-01이 실제 forward synthesis proposal인지, retrosynthetic route edge의 방향 전환 후 부여된 yield query인지
- `template_code 32658`이 route generator에서 의도한 chemical transformation인지
- omitted reagent/agent, reaction conditions, yield label의 실험 정의

따라서 “정규화 과정의 단순 오류”라고 단정할 수 없고, 반대로 “모델이 유효한 acetic acid→ethanol 합성을 제안했다”고도 말할 수 없다. 가장 정확한 설명은 **retrosynthetic tree edge가 forward yield query로 방향 변환되었고, 그 결과가 route step-01로 materialized되었지만, 해당 edge의 실험적 정당성은 검증되지 않음**이다.

## 에탄올 공급 branch인가, 표적까지 이어지는 순차 단계인가

두 표현을 구분하면 다음과 같다.

- **그래프 구조상:** route-05 step-01은 step-02의 `CCO` precursor를 공급하는 branch이며, `depends_on`으로 순차 연결되어 있다.
- **화학적 의미상:** tree가 acetic acid terminal을 ethanol precursor로 연결한 것은 확인되지만, 그 변환의 유효한 forward synthesis 조건은 확인되지 않았다.
- **표적 연결상:** step-02는 PABA + CCO → benzocaine으로 target까지 이어진다. 그러나 step-01의 실제 수율을 곱해 route overall yield를 만드는 것은 저장소도 하지 않았고, 현재 근거로도 정당화되지 않는다.

## 생략 성분 복원 가능성

현재 저장소에서 복원 가능한 것은 template metadata와 tree의 mapped reaction뿐이다. `classification: 0.0 Unrecognized`, `caveat: Template-derived disconnection; omitted agents were not reconstructed.`가 있어, 촉매·용매·산화제·환원제·압력·온도·시간을 기록으로 복원할 수 없다.

`routes-selected-raw.json`의 mapped reaction은 ethanol→acetic acid 방향을 보여 주지만, 이는 원자 mapping/template 표현이지 실험 protocol이 아니다. 누락 성분은 추정으로 추가하지 않았다.

## 수율 비교 대상 여부

**현재 비교 대상에서 제외:**

- 정확한 forward reaction의 실험 문헌 수율이 없다.
- tree edge의 방향은 retrosynthetic이고, yield query는 역방향이다.
- template classification이 `Unrecognized`이며 omitted agents가 복원되지 않았다.
- `CC(=O)O`가 stock이라는 것은 출발물질 접근성일 뿐 변환 성공성의 근거가 아니다.
- 77.5889%는 predicted_not_validated이고 route overall yield와 결합되지 않았다.

## 남은 확인 방법

추가 실행 없이 가능한 다음 확인은 원본 route generator의 edge-direction/step materialization 코드와 해당 run의 `routes.log`, `routes.metadata.json`, `pipeline.log`를 대조하는 것이다. 이 자료에서도 forward experimental protocol이 없으면, 이 단계는 수율 benchmark가 아니라 **route-search artifact/precursor-branch provenance 사례**로만 기록한다.

## 보고서에서의 수율 의미 정리

| 수치 | 보고서에서 허용되는 의미 | 쓰면 안 되는 의미 |
|---|---|---|
| 82.95% | `route-01/step-01` reaction SMILES에 대한 USPTO gram-scale checkpoint의 역정규화 예측값 | 해당 nitro reduction의 실험 수율, 문헌 조건에서의 예상값, 모델 정확도 |
| 77.70% | `route-02/step-01` reaction SMILES에 대한 동일 checkpoint 예측값 | deacetylation 실험 수율 또는 target-specific confidence |
| 77.59% | route tree에서 acetic acid terminal을 ethanol precursor로 연결한 forward yield query의 예측값 | 실제 ethanol 공급 수율, route-05 step yield, benzocaine 전체 수율 |
| 79.80% | `route-05/step-02` PABA+ethanol→benzocaine reaction SMILES에 대한 예측값 | 문헌 esterification 수율의 대체값, 조건부 실험 수율, overall route yield |

공통 한계: 모델 입력은 reaction SMILES이고 Parrot 조건이 들어가지 않았으며, 네 값 모두 `predicted_not_validated`/`applicability: not_assessed`이다. 문헌 수율은 별도의 substrate·조건·workup·수율 정의를 가진 비교 근거이지, 프로젝트 실험 결과가 아니다.

