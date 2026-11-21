# 벤조카인(Benzocaine) 합성 경로 예측 및 근거 기반 분석 보고서

벤조카인(Benzocaine)은 중성 유리 염기 형태의 C₉H₁₁NO₂ 화합물이며, PubChem CID 2337로 식별된다[1]. 이번 검토는 사용자가 벤조카인을 최종 과정 목표로 지정한 사실에 근거하여 수행되었으며, 이 사실은 모델 추론이 아니라 과제 출처 정보이다[D11]. AiZynthFinder 탐색은 route-01, route-02, route-05를 포함한 12개 경로를 생성했고, 각 모델의 출력은 정상 생성·정규화되었다[D1]. 아래에서는 각 경로의 반응 SMILES, Parrot 조건 후보, 수율 예측, 그리고 추가 분석 결과를 구분하여 서술한다.

## 1. 대상 물질의 구조적 특징과 선정 이유

벤조카인(Benzocaine, 벤조카인)은 분자식 C₉H₁₁NO₂의 중성 유리 염기(neutral free base) 형태로, PubChem CID 2337로 식별된다[1]. 구조는 파라-아미노벤조에이트 골격에 에틸 에스터가 결합된 형태이며, SMILES는 `CCOC(=O)c1ccc(N)cc1`이다[1]. 즉 방향족 고리의 파라 위치에 아미노기(–NH₂)가, 나머지 파라 위치에 에틸 에스터(–COOCH₂CH₃)가 존재한다. 이 두 작용기는 합성 설계에서 각각 다른 변환의 대상이 될 수 있어, 역합성 탐색에서 여러 경로 후보가 나타나는 배경이 된다.

본 보고서에서 벤조카인을 대상 물질로 삼은 이유는 모델 추론이나 문헌 비교의 결과가 아니라, 사용자가 이 물질을 최종 과제 대상으로 명시적으로 선택했기 때문이다[D11]. 따라서 아래 내용은 벤조카인의 구조 자체를 해석한 뒤, 실제 실행된 예측·검증·추가 분석 증거를 바탕으로 경로 후보를 정리하는 순서로 진행한다.

![벤조카인(C9H11NO2) 구조: 파라 아미노기와 에틸 에스터](assets/target.png)

## 2. 탐색 범위와 경로 선정

### 2.1 실행 개요와 모델 상태

이번 실행은 AiZynthFinder[2]를 이용한 역합성 경로 탐색, Parrot[5]을 이용한 반응 조건 후보 추천, rxn_yields[6] 기반 수율 예측의 세 단계로 구성되었다. 실행 요약에서 routes, conditions, yields는 모두 success로 기록되어 있다[D1]. 다만 이 success는 각 파이프라인의 출력 파일이 정상적으로 생성·정규화되었다는 뜻이며, 예측값이 실험적으로 검증되었다는 뜻은 아니다. 모델별 입력·출력·검증 범위는 뒤에서 따로 구분한다.

### 2.2 전체 탐색 결과와 선정 기준

AiZynthFinder 탐색 결과에는 총 12개 경로가 포함되었다[D1]. 이 중 1단계 경로는 route-01, route-02, route-03, route-04이며, 2단계 경로는 route-05부터 route-12까지이다. 각 경로의 상태 점수(state score)와 반응 수, 전구체 수, 재고 내 전구체 수는 보고서 증거에 기록되어 있다[D1].

이 보고서는 그중 route-01, route-02, route-05를 대표 경로로 다룬다. 선정 이유는 화학적 우월성을 주장하기 위한 것이 아니라, 초기 점수 순서상의 shortlist와 검토 범위를 반영한 것이다[D1]. 즉 이 선정은 “실제 합성이 가능하다”는 증명이 아니라, 검토 대상 경로를 좁히는 절차적 선택이다. 경로 점수와 재고 포함 여부는 실용적 실현성을 직접 보증하지 않으며, 검색은 대상 물질을 재고에서 제외하고 수행되었고 작용제(agent)나 부산물(byproduct)이 생략될 수 있다[D4].

### 2.3 대표 경로의 기본 구성

- **route-01**: 1단계. 에틸 4-니트로벤조에이트(ethyl 4-nitrobenzoate)에서 벤조카인으로의 직접 변환이다. 전구체는 1종이며 재고 포함 플래그가 true로 기록되어 있다[D1].
- **route-02**: 1단계. 에틸 4-아세트아미도벤조에이트(ethyl 4-acetamidobenzoate)에서 벤조카인으로의 변환이다. 전구체는 1종이며 재고 포함 플래그가 true이다[D1].
- **route-05**: 2단계. 첫 단계에서 아세트산(acetic acid)에서 에탄올(ethanol)로의 변환이 제시되고, 둘째 단계에서 4-아미노벤조산(4-aminobenzoic acid)과 에탄올로부터 벤조카인이 생성된다. 전구체는 2종이며, 첫째 단계 전구체의 재고 포함 플래그는 false, 둘째 단계 전구체의 재고 포함 플래그는 true로 기록되어 있다[D1].

route-05의 첫 단계는 검색 모델의 경로 간선(pathway edge)으로 나타나며, 실제 순차 합성으로 검증되지는 않았다[D1]. 이 점은 뒤에서 다시 구분한다.



#### 경로 요약

| 경로·단계 (전체 단계 수) | 기존 보고서의 변환 표기 | 문헌·강의 근거 및 확인 사항 |
|---|---|---|
| route-01 / step-01 (1단계) | 3.1 route-01: 에틸 4-니트로벤조에이트 → 벤조카인 | [D9][D1] 동일 변환의 직접 문헌 사례. Org. Synth. 분리·재결정 후 질량 수율 91–100%; 특허 약 100% 이론량(측정법 별도 정의 없음). 세부 조건은 §6.1.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |
| route-02 / step-01 (1단계) | 3.2 route-02: 에틸 4-아세트아미도벤조에이트 → 벤조카인 | [D1] 이 증거 묶음에는 동일 단계의 문헌·강의 사례가 매핑되지 않음.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |
| route-05 / step-01 (2단계) | 3.3.1 route-05/step-01: 아세트산 → 에탄올 | [D1] 이 증거 묶음에는 동일 단계의 문헌·강의 사례가 매핑되지 않음.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |
| route-05 / step-02 (2단계) | 3.3.2 route-05/step-02: 4-아미노벤조산 + 에탄올 → 벤조카인 | [17, PDF pp. 80–81][D1] 벤조카인 교육 예시; [17, PDF pp. 90–95] 일반 메커니즘 교육자료. 실험 수율 근거 아님.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |

#### Parrot 후보·단계별 예측 수율

| Route / step (경로 단계 수) | Parrot rank | sequence_score | Parrot 원래 슬롯 | Yield-BERT 예측값 / 상태 |
|---|---:|---:|---|---|
| route-01 / step-01 (1단계) [D1] | 1 | -1.700762152671814 | catalyst1=`[Pd]`; solvent1=`CCO`; solvent2=``; reagent1=``; reagent2=`` | 82.95% / predicted_not_validated (conditions_in_input=False) |
| route-01 / step-01 (1단계) [D1] | 2 | -2.0481550693511963 | catalyst1=`[Pd]`; solvent1=`CO`; solvent2=``; reagent1=``; reagent2=`` | 82.95% / predicted_not_validated (conditions_in_input=False) |
| route-01 / step-01 (1단계) [D1] | 3 | -2.7931230068206787 | catalyst1=`[Pd]`; solvent1=`CCOC(C)=O`; solvent2=``; reagent1=``; reagent2=`` | 82.95% / predicted_not_validated (conditions_in_input=False) |
| route-01 / step-01 (1단계) [D1] | 4 | -2.878655195236206 | catalyst1=`[Pd]`; solvent1=`CCO`; solvent2=``; reagent1=`[H][H]`; reagent2=`` | 82.95% / predicted_not_validated (conditions_in_input=False) |
| route-02 / step-01 (1단계) [D1] | 1 | -1.3239554166793823 | catalyst1=``; solvent1=`CCO`; solvent2=``; reagent1=`Cl`; reagent2=`` | 77.70% / predicted_not_validated (conditions_in_input=False) |
| route-02 / step-01 (1단계) [D1] | 2 | -2.660543441772461 | catalyst1=``; solvent1=`Cl`; solvent2=``; reagent1=``; reagent2=`` | 77.70% / predicted_not_validated (conditions_in_input=False) |
| route-02 / step-01 (1단계) [D1] | 3 | -3.2928555011749268 | catalyst1=``; solvent1=`CCO`; solvent2=``; reagent1=`[Na+].[OH-]`; reagent2=`` | 77.70% / predicted_not_validated (conditions_in_input=False) |
| route-05 / step-01 (2단계) [D1] | 1 | -1.8564977645874023 | catalyst1=``; solvent1=`C1CCOC1`; solvent2=``; reagent1=`[Al+3].[H-].[H-].[H-].[H-].[Li+]`; reagent2=`` | 77.59% / predicted_not_validated (conditions_in_input=False) |
| route-05 / step-01 (2단계) [D1] | 2 | -2.797421455383301 | catalyst1=``; solvent1=`C1CCOC1`; solvent2=``; reagent1=`O`; reagent2=`[Al+3].[H-].[H-].[H-].[H-].[Li+]` | 77.59% / predicted_not_validated (conditions_in_input=False) |
| route-05 / step-01 (2단계) [D1] | 3 | -2.994331121444702 | catalyst1=``; solvent1=`C1CCOC1`; solvent2=``; reagent1=``; reagent2=`` | 77.59% / predicted_not_validated (conditions_in_input=False) |
| route-05 / step-02 (2단계) [D1] | 1 | -2.1754837036132812 | catalyst1=``; solvent1=`CCO`; solvent2=``; reagent1=`CCOCC`; reagent2=`FB(F)F` | 79.80% / predicted_not_validated (conditions_in_input=False) |
| route-05 / step-02 (2단계) [D1] | 2 | -2.3472180366516113 | catalyst1=``; solvent1=`CCO`; solvent2=``; reagent1=`CC(=O)Cl`; reagent2=`` | 79.80% / predicted_not_validated (conditions_in_input=False) |
| route-05 / step-02 (2단계) [D1] | 3 | -2.6159138679504395 | catalyst1=``; solvent1=`O=S(=O)(O)O`; solvent2=``; reagent1=``; reagent2=`` | 79.80% / predicted_not_validated (conditions_in_input=False) |




## 3. 구조 변화와 단계별 조건·수율 예측

이 절에서는 각 대표 경로의 반응 전후 구조 변화와 작용기 변화를 짧게 서술하고, 단계별 조건 후보와 수율 예측을 정리한다. 온도·시간·당량·압력이 제공되지 않은 값은 `NOT SUPPLIED`로 표기한다. 조건 슬롯은 Parrot이 반환한 필드 그대로(catalyst1, solvent1, solvent2, reagent1, reagent2) 다루며, 서로 다른 rank 후보를 하나로 합치지 않는다.

### 3.1 route-01: 에틸 4-니트로벤조에이트 → 벤조카인

**구조 변화.** 이 단계는 방향족 니트로기(–NO₂)가 아미노기(–NH₂)로 바뀌는 환원 변환이며, 에틸 에스터는 유지된다[D1]. 반응 SMILES는 `CCOC(=O)c1ccc([N+](=O)[O-])cc1 >> CCOC(=O)c1ccc(N)cc1`이다[D1].

![route-01/step-01: 에틸 4-니트로벤조에이트에서 벤조카인으로; 방향족 니트로기(–NO₂)가 아미노기(–NH₂)로 바뀌고 에틸 에스터는 유지됨](assets/route-01-step-01.png)

**템플릿·분류 정보.** 이 단계의 템플릿 해시는 `664f7756f7526ad6c07e82dd3b3c15f7aabccbc99837dd22105068a2cfc385b5`이며, 분류는 “0.0 Unrecognized”로 기록되어 있다[D1]. 라이브러리 출현 횟수는 33350, 정책 확률은 0.4224, 정책 이름은 uspto, 템플릿 코드는 17064이다[D1]. 템플릿은 아미노기 관련 변환을 기술하는 형태이며, 이 보고서에서는 템플릿이 제시한 절단(disconnection) 방향을 그대로 읽되, 생략된 작용제가 재구성되지 않았다는 단서를 함께 둔다[D1].

**조건 후보.** Parrot은 이 반응에 대해 15개 후보를 반환했다[D1]. 상위 3개 후보의 주요 슬롯은 다음과 같다.

- rank 1: catalyst1 `[Pd]`, solvent1 `CCO`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −1.7008
- rank 2: catalyst1 `[Pd]`, solvent1 `CO`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −2.0482
- rank 3: catalyst1 `[Pd]`, solvent1 `CCOC(C)=O`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −2.7931

상위 후보들은 catalyst1에 Pd 원자 토큰을, solvent1에 에탄올 계열 또는 메탄올 계열 토큰을 배치하는 경향을 보인다[D1]. `solvent1=CO`는 단일 구조 토큰이며, 검증된 구조 해석은 메탄올(methanol, CH₄O, PubChem CID 887)이다[D12]. 이 슬롯은 화학적 역할을 해석할 수는 있지만, 모델이 출력한 값 자체가 실험 조건을 검증했다는 뜻은 아니다. 다만 `[Pd]`는 단일 Pd 원소 토큰이며 실제 촉매 제형·담지체·산화상태·실물 형태를 확인해 주지 않는다.  이 슬롯들은 화학적 역할을 해석할 수는 있지만, 모델이 출력한 값 자체가 실험 조건을 검증했다는 뜻은 아니다.

또한 이 단계의 temperature, time, yield_percent는 모두 null이며, temperature_status는 `not_provided_by_checkpoint`로 기록되어 있다[D1]. 즉 온도·시간·당량·압력은 이번 조건 체크포인트에서 제공되지 않았다. 따라서 각 조건 슬롯의 수치적 운영 조건은 `NOT SUPPLIED`이다.

**수율 예측.** rxn_yields는 이 반응 SMILES에 대해 raw_value 0.46616947650909424, 수율 82.95371431744555%를 반환했다[D1]. 출력 척도는 standardized_fraction이며, 상태는 `predicted_not_validated`이다. 입력 토큰 수는 46, 최대 입력 토큰은 300, 입력 절단은 false이며, conditions_in_input은 false이다[D1]. 즉 이 수율 예측은 반응 구조만 입력했고 조건 슬롯을 넣지 않았으며, 적용 가능성(applicability)도 평가되지 않았다. 따라서 이 값은 특정 실험 조건에서의 실험 수율이 아니라, 반응 SMILES에 대한 모델 예측값이다.[6]

### 3.2 route-02: 에틸 4-아세트아미도벤조에이트 → 벤조카인

**구조 변화.** 이 단계는 N-아세틸기가 제거되어 아미노기가 드러나고, 에틸 에스터는 유지되는 변환이다[D1]. 반응 SMILES는 `CCOC(=O)c1ccc(NC(C)=O)cc1 >> CCOC(=O)c1ccc(N)cc1`이다[D1].

![route-02/step-01: 에틸 4-아세트아미도벤조에이트에서 벤조카인으로; N-아세틸기가 제거되어 아미노기가 드러나며 에틸 에스터는 유지됨](assets/route-02-step-01.png)

**템플릿·분류 정보.** 템플릿 해시는 `8063032398e59c77d82569a4231c9d8f1dc9cd333085943b3f9ae7b5eafd5071`, 분류는 “0.0 Unrecognized”, 라이브러리 출현 횟수는 1668, 정책 확률은 0.0118, 정책 이름은 uspto, 템플릿 코드는 21399이다[D1]. 이 템플릿은 아미노기 관련 절단 방향을 기술하며, route-01과 마찬가지로 생략된 작용제가 재구성되지 않았다는 단서가 붙어 있다[D1].

**조건 후보.** Parrot은 이 반응에 대해서도 15개 후보를 반환했다[D1]. 상위 3개 후보의 주요 슬롯은 다음과 같다.

- rank 1: catalyst1 `""`, solvent1 `CCO`, solvent2 `""`, reagent1 `Cl`, reagent2 `""`, sequence_score −1.3240
- rank 2: catalyst1 `""`, solvent1 `Cl`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −2.6605
- rank 3: catalyst1 `""`, solvent1 `CCO`, solvent2 `""`, reagent1 `[Na+].[OH-]`, reagent2 `""`, sequence_score −3.2929

이 단계의 상위 후보들은 catalyst1이 비어 있는 경우가 많고, solvent1과 reagent1에 염소 계열, 에탄올 계열, 염기 계열 토큰이 섞여 나타난다[D1]. slot이 빈 값인 경우는 “모델 출력 미제공”으로 읽으며, 실험에서 해당 성분을 사용하지 않았다는 뜻이 아니다.

이 단계 역시 temperature, time, yield_percent는 null이고 temperature_status는 `not_provided_by_checkpoint`이다[D1]. 따라서 운영 온도·시간·당량·압력은 `NOT SUPPLIED`이다.

**수율 예측.** rxn_yields는 이 반응 SMILES에 대해 raw_value 0.21513395011425018, 수율 77.69549187778327%를 반환했다[D1]. 출력 척도는 standardized_fraction, 상태는 `predicted_not_validated`, 입력 토큰 수는 47, conditions_in_input은 false이다[D1]. 이 값 역시 반응 구조만 입력한 예측이며, 특정 실험 조건에서의 실험 수율이 아니다.[6]

### 3.3 route-05: 아세트산 → 에탄올 → 벤조카인

route-05는 2단계 경로이다. 첫째 단계는 아세트산에서 에탄올로의 변환이고, 둘째 단계는 4-아미노벤조산과 에탄올로부터 벤조카인을 생성하는 변환이다. 다만 첫째 단계는 검색 모델의 경로 간선으로 제시되었으며, 실제 순차 합성으로 검증되지는 않았다[D1].

#### 3.3.1 route-05/step-01: 아세트산 → 에탄올

**구조 변화.** 이 단계는 카복실산(–COOH)이 알코올(–CH₂OH)로 표현되는 변환이며, 반응 SMILES는 `CC(=O)O >> CCO`이다[D1]. 이 변환은 route-05의 경로 간선으로서 등장하지만, 실제 순차 합성에서 이 단계가 독립적으로 검증되었다는 증거는 이 자료에 없다[D1].

![route-05/step-01: 아세트산에서 에탄올로; 검색 모델의 경로 간선이며 실제 순차 합성으로 검증되지 않음](assets/route-05-step-01.png)

**템플릿·분류 정보.** 템플릿 해시는 `c42f96a0658c03bc12dc20efce06e66daaeccc675d73631eea24ea610a7227b8`, 분류는 “0.0 Unrecognized”, 라이브러리 출현 횟수는 3921, 정책 확률은 0.0915, 정책 이름은 uspto, 템플릿 코드는 32658이다[D1].

**조건 후보.** Parrot은 이 반응에 대해 15개 후보를 반환했다[D1]. 상위 3개 후보의 주요 슬롯은 다음과 같다.

- rank 1: catalyst1 `""`, solvent1 `C1CCOC1`, solvent2 `""`, reagent1 `[Al+3].[H-].[H-].[H-].[H-].[Li+]`, reagent2 `""`, sequence_score −1.8565
- rank 2: catalyst1 `""`, solvent1 `C1CCOC1`, solvent2 `""`, reagent1 `O`, reagent2 `[Al+3].[H-].[H-].[H-].[H-].[Li+]`, sequence_score −2.7974
- rank 3: catalyst1 `""`, solvent1 `C1CCOC1`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −2.9943

이 단계의 상위 후보에는 용매로 THF 계열 토큰(`C1CCOC1`)이 자주 등장하고, 시약 슬롯에 리튬 알루미늄 수소화물 계열로 읽힐 수 있는 분리된 이온 표현(`[Al+3].[H-].[H-].[H-].[H-].[Li+]`)이 나타난다[D1]. 다만 이 표현은 정의된 순수 중성 유기 화합물로서의 물질이라기보다 분리된 이온 표현이며, 실제 시약 제형·당량·용매 조성·작업 조건을 확인해 주지 않는다. 이 단계도 temperature, time, yield_percent는 null이고 temperature_status는 `not_provided_by_checkpoint`이다[D1]. 따라서 운영 조건은 `NOT SUPPLIED`이다.

**수율 예측.** rxn_yields는 이 반응 SMILES에 대해 raw_value 0.2100452482700348, 수율 77.58890327412914%를 반환했다[D1]. 출력 척도는 standardized_fraction, 상태는 `predicted_not_validated`, 입력 토큰 수는 13, conditions_in_input은 false이다[D1].[6]

#### 3.3.2 route-05/step-02: 4-아미노벤조산 + 에탄올 → 벤조카인

**구조 변화.** 이 단계는 4-아미노벤조산의 카복실기가 에틸 에스터로 변환되고 아미노기는 유지되는 반응이다[D1]. 반응 SMILES는 `CCO.Nc1ccc(C(=O)O)cc1 >> CCOC(=O)c1ccc(N)cc1`이다[D1]. 즉 생성물은 벤조카인이며, 반응물 쪽에는 에탄올과 4-아미노벤조산이 함께 표기되어 있다.

![route-05/step-02: 4-아미노벤조산과 에탄올에서 벤조카인으로; 카복실산이 에틸 에스터로 표현되고 아미노기는 유지됨](assets/route-05-step-02.png)

**템플릿·분류 정보.** 템플릿 해시는 `bf6bd9047791f3252d0082f87523bda9bf230f930fe417ac7de9fa8c502cbf89`, 분류는 “0.0 Unrecognized”, 라이브러리 출현 횟수는 6214, 정책 확률은 0.1681, 정책 이름은 uspto, 템플릿 코드는 31869이다[D1]. 이 템플릿은 에스터화 방향의 절단 형태를 기술하며, 생략된 작용제가 재구성되지 않았다는 단서가 붙어 있다[D1].

**조건 후보.** Parrot은 이 반응에 대해 15개 후보를 반환했다[D1]. 상위 3개 후보의 주요 슬롯은 다음과 같다.

- rank 1: catalyst1 `""`, solvent1 `CCO`, solvent2 `""`, reagent1 `CCOCC`, reagent2 `FB(F)F`, sequence_score −2.1755
- rank 2: catalyst1 `""`, solvent1 `CCO`, solvent2 `""`, reagent1 `CC(=O)Cl`, reagent2 `""`, sequence_score −2.3472
- rank 3: catalyst1 `""`, solvent1 `O=S(=O)(O)O`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −2.6159

route-05/step-02의 반응 `CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1`에 대해 Parrot이 제시한 원시 후보는 총 15개이며 [D1], 이어지는 설명 문단은 그중 rank 1, rank 2, rank 3만을 각각 별도의 슬롯 구성으로 다룬다. rank 1은 catalyst1=``, solvent1=`CCO`, solvent2=``, reagent1=`CCOCC`, reagent2=`FB(F)F`이고, rank 2는 catalyst1=``, solvent1=`CCO`, solvent2=``, reagent1=`CC(=O)Cl`, reagent2=``이며, rank 3은 catalyst1=``, solvent1=`O=S(=O)(O)O`, solvent2=``, reagent1=``, reagent2=``이다 [D1]. 구조 토큰의 물질명 대응은 다음과 같이 확인된다 [D12]. `CCO`는 에탄올(ethanol, C2H6O; PubChem CID 702)이고, `CCOCC`는 다이에틸 에터(diethyl ether/ethoxyethane, C4H10O; PubChem CID 3283)이며, 이는 에틸 아세테이트 구조가 아니다. 또한 route-05/step-02의 15개 후보 슬롯 어디에도 에틸 아세테이트 구조 토큰 `CCOC(=O)C` 또는 `CCOC(C)=O`는 존재하지 않는다. `FB(F)F`는 삼불화붕소(boron trifluoride, BF3; PubChem CID 6356)이고, `CC(=O)Cl`은 아세틸 클로라이드(acetyl chloride; PubChem CID 6367)이며, `O=S(=O)(O)O`는 이 근거 묶음에서 이름 확인 자료가 없으므로 원시 토큰으로만 남긴다. 모델이 예측한 슬롯은 실험에서 실제 사용된 시약·용매·촉매 역할을 입증하는 값이 아니므로, 구조 정체성과 실제 실험 역할은 서로 다른 개념으로 다루어야 하며 실험에서의 사용 여부는 확인되지 않았다.

`FB(F)F`는 삼불화붕소(boron trifluoride, BF₃)로 읽힐 수 있으며, MPBPWIN의 유기화합물 범위와는 별도로 취급해야 한다[D12][12][D6].
**수율 예측.** rxn_yields는 이 반응 SMILES에 대해 raw_value 0.31552639603614807, 수율 79.79832496878097%를 반환했다[D1]. 출력 척도는 standardized_fraction, 상태는 `predicted_not_validated`, 입력 토큰 수는 43, conditions_in_input은 false이다[D1].[6]

### 3.3.3 강의 근거와 AI 예측의 비교: route-05/step-02

이 절은 강의 자료의 벤조카인 역합성 예시와 이번 프로젝트의 AI 예측 결과를 나란히 놓고, 두 자료가 어디까지 겹치고 어디서 분리되는지 정리한다. 두 자료 모두 4-아미노벤조산과 에탄올을 출발점으로 벤조카인(에틸 4-아미노벤조산 에스터)을 얻는다는 점에서 반응의 골격은 같다[17, PDF pp. 80–81][D1]. 다만 강의는 교육용 역합성·메커니즘 설명이고, AI 예측은 구조 기반 템플릿·조건 후보·수율 예측이므로, 같은 생성물을 향한다는 사실 이상으로 조건을 동일시할 수 없다.

강의 자료 80–81쪽은 벤조카인의 에틸 에스터 결합을 끊어 4-아미노벤조산과 에탄올을 전구체로 제시하고, 정방향 변환으로 황산 촉매 피셔 에스터화를 예시로 든다[17, PDF pp. 80–81]. 83–84쪽은 과제에서 단계별 새 결합과 작용기 변화, 전자쌍의 출발·도착, 형식전하, 시약·촉매·용매의 역할을 설명하도록 요구한다[17, PDF pp. 83–84]. 90–95쪽은 피셔 에스터화의 일반적인 전자 흐름을 제시하는데, 카보닐 산소의 양성자화, 알코올 산소 비공유전자쌍이 카보닐 탄소로 이동해 새 C–O 결합을 만들고 카보닐 π 전자가 산소로 이동하며, 이후 양성자 이동, 물 이탈과 C=O 재형성, 촉매 재생 순서로 가르친다[17, PDF pp. 90–95]. 여기서 강의 그림은 메탄올/아세트산 계열의 일반 예시이며, 이 프로젝트의 route-05/step-02에 대한 측정 메커니즘이나 조건 증명으로 쓰지 않는다[D1].

Parrot의 route-05/step-02 rank-1 후보는 catalyst1이 비어 있고, solvent1=`CCO`, solvent2가 비어 있으며, reagent1=`CCOCC`, reagent2=`FB(F)F`이다[D1]. 이 슬롯을 그대로 두면 강의의 황산 촉매 피셔 에스터화와는 촉매·시약 구성이 다르다[17, PDF pp. 80–81]. 화학적으로 `CCO`는 에탄올, `CCOCC`는 디에틸 에터 계열 토큰, `FB(F)F`는 BF₃ 계열 토큰으로 읽을 수 있으나, 이는 해석이며 Parrot의 슬롯 분류가 아니다. 따라서 이 해석을 강의 조건과 합쳐 하나의 조건으로 만들지 않는다. 온도·시간·당량·압력은 제공되지 않았고, 이 단계의 운영 조건은 `NOT SUPPLIED`이다[D1].

rxn_yields는 이 반응 SMILES에 대해 79.79832496878097%를 반환했으며, 표시는 79.80%로 하되 상태는 `predicted_not_validated`이다[6][D1]. 이 값은 구조만 입력한 단계 예측이며, Parrot 조건이나 강의 조건에서의 실험 수율이 아니다[17, PDF pp. 80–81].

| 구분 | 강의 근거(과정 자료) | AI 예측(route-05/step-02) | 비교의 한계 |
|---|---|---|---|
| 반응 골격 | 4-아미노벤조산 + 에탄올 → 벤조카인(에틸 에스터) 역합성·정방향 예시[17] | 동일 반응 SMILES `CCO.Nc1ccc(C(=O)O)cc1 >> CCOC(=O)c1ccc(N)cc1`[D1] | 생성물 골격은 같으나 조건·메커니즘 증명은 별개 |
| 조건 | 황산 촉매 피셔 에스터화를 교육 예시로 제시[17, PDF pp. 80–81] | Parrot rank-1: catalyst1 `""`, solvent1 `CCO`, solvent2 `""`, reagent1 `CCOCC`, reagent2 `FB(F)F`[D1] | 모델 슬롯을 강의 조건으로 대체하거나 합치지 않음; `CCO`/`CCOCC`/`FB(F)F`는 화학 해석일 뿐 슬롯 분류가 아님 |
| 메커니즘 설명 | 90–95쪽 일반 피셔 에스터화 전자 흐름(메탄올/아세트산 계열 예시)[17, PDF pp. 90–95] | 이 프로젝트 내에서 측정된 메커니즘·장벽·속도 자료는 없음 | 강의 그림은 일반 교육 예시이며, 이 반응의 실험적 메커니즘 증명이 아님 |
| 수율 | 강의에 이 반응의 실험 수율 제시 없음[17, PDF pp. 80–81] | rxn_yields 79.80%, 상태 `predicted_not_validated`, conditions_in_input false[6][D1] | 구조만 입력한 예측값이며 조건별 실험 수율이 아님 |

요약하면, 강의와 AI 예측은 같은 벤조카인 골격을 공유하지만, 강의의 황산 촉매 피셔 에스터화 예시와 Parrot rank-1의 원래 슬롯은 서로 다른 기술이며, 79.80%는 구조 기반 예측 수율에 그친다. 따라서 이 비교는 두 자료의 범위와 한계를 구분하는 데 쓰이고, 어느 한쪽의 조건이나 메커니즘을 다른 쪽으로 검증한 것으로 읽지 않는다[6][17, PDF pp. 90–95][D1].

### 3.4 단계별 조건·수율 값의 표기 원칙

| route_id / step_id | Reaction SMILES (reactants >> product) | Parrot rank 1 (original slots) | Temperature / time / equivalents / pressure | Yield-BERT predicted yield (%) / status |
|---|---|---|---|---|
| route-01 / step-01 [D1] | `CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1` | catalyst1=`[Pd]`; solvent1=`CCO`; solvent2=`""`; reagent1=`""`; reagent2=`""` | temperature=미제공; time=미제공; equivalents=출력 필드 없음; pressure=출력 필드 없음 | 82.95% / predicted_not_validated (conditions_in_input=False) |
| route-02 / step-01 [D1] | `CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1` | catalyst1=`""`; solvent1=`CCO`; solvent2=`""`; reagent1=`Cl`; reagent2=`""` | temperature=미제공; time=미제공; equivalents=출력 필드 없음; pressure=출력 필드 없음 | 77.70% / predicted_not_validated (conditions_in_input=False) |
| route-05 / step-01 [D1] | `CC(=O)O>>CCO` | catalyst1=`""`; solvent1=`C1CCOC1`; solvent2=`""`; reagent1=`[Al+3].[H-].[H-].[H-].[H-].[Li+]`; reagent2=`""` | temperature=미제공; time=미제공; equivalents=출력 필드 없음; pressure=출력 필드 없음 | 77.59% / predicted_not_validated (conditions_in_input=False) |
| route-05 / step-02 [D1] | `CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1` | catalyst1=`""`; solvent1=`CCO`; solvent2=`""`; reagent1=`CCOCC`; reagent2=`FB(F)F` | temperature=미제공; time=미제공; equivalents=출력 필드 없음; pressure=출력 필드 없음 | 79.80% / predicted_not_validated (conditions_in_input=False) |

또한 단계 예측 수율을 곱해 전체 경로 수율을 계산하지 않는다. 분기 구조와 독립적으로 예측된 단계를 단순 곱으로 합치는 것은 이번 증거에서 지원되지 않는다[D1].[6]

## 4. 모델별 입력, 출력, 확인 범위, 실패와 한계

### 4.1 AiZynthFinder: 경로 탐색

AiZynthFinder는 역합성 경로 탐색에 사용되었다[2][D1]. 이번 실행에서 routes는 success로 기록되어 있으며, 12개 경로와 20개 단계가 생성되었다[16]. 다만 이는 출력 무결성 및 조인 검증에 대한 결과이며, 각 경로가 실제 실험적으로 실현 가능하다는 증명은 아니다. 검색은 대상 물질을 재고에서 제외한 상태로 수행되었고, 작용제나 부산물이 생략될 수 있다[D4].

템플릿 기반 절단 정보는 각 단계의 metadata에 기록되어 있다[D1]. 예를 들어 route-01/step-01의 템플릿은 아미노기 관련 형태를 기술하며, route-02/step-01과 route-05/step-02도 각각 다른 템플릿 코드를 가진다. 그러나 분류가 “0.0 Unrecognized”로 기록된 점은, 이 템플릿이 특정 명명된 반응 유형으로 즉시 분류되지 않았음을 보여 준다[D1]. 이 점은 템플릿이 틀렸다는 뜻이 아니라, 이번 출력에서 분류 정보가 제한적이라는 뜻이다.

### 4.2 Parrot: 조건 추천

Parrot은 반응 조건 후보 추천에 사용되었다[5][D1]. 이번 실행에서 conditions는 success로 기록되어 있으며, 선택된 반응들에 대해 각각 15개 후보가 반환되었다[D1]. Parrot 출력은 catalyst1, solvent1, solvent2, reagent1, reagent2 필드로 구성되며, 이 보고서는 그 필드를 그대로 사용한다. 후보를 병합하거나 서로 다른 rank의 슬롯을 섞어 하나의 조건으로 만들지 않는다.

Parrot의 sequence_score는 후보 순위 평가에 사용되지만, 반응 성공률이나 실험 수율을 직접 뜻하지는 않는다[D1]. 또한 Parrot 조건은 수율 모델의 입력이 아니다[D1]. 즉 조건 추천과 수율 예측은 서로 다른 모델이며, 조건 슬롯이 수율 예측에 반영되었다는 증거는 없다.

이번 조건 체크포인트는 temperature, time, yield_percent를 제공하지 않았다[D1]. temperature_status는 `not_provided_by_checkpoint`로 기록되어 있다. 따라서 온도·시간·당량·압력은 `NOT SUPPLIED`이며, 이 누락은 조건 추천 모델이 해당 값을 출력하지 않았다는 뜻이다. 실험에서 해당 성분을 사용하지 않았다는 뜻이 아니다.

### 4.3 rxn_yields: 수율 예측

rxn_yields[6]는 반응 SMILES 기반 수율 예측에 사용되었다[D1]. 이번 실행에서 yields는 success로 기록되어 있으며, 선택된 단계들에 대해 각각 예측값이 반환되었다[D1]. 예측값은 standardized_fraction 척도에서 recovered된 통계량으로 백분율로 변환되었다[D1].

정규화[8][9]에는 훈련 데이터의 평균 0.7318926847478698, 표준편차 0.20946128682168402가 사용되었고, 표준편차는 ddof=1로 계산되었다[D1]. 변환식은 `yield_percent = 100 * (raw_z * training_yield_std + training_yield_mean)`이다[D1]. 이 통계량은 USPTO 그램 규모 무작위 분할(train rows)에서 recovered된 것이며, 전역 데이터셋 대체 통계량이 아니다[D1]. 또한 정규화 계산이 정확하다는 것이 모델 정확도를 검증한다는 뜻은 아니다[D4].

예측 수율은 모두 `predicted_not_validated` 상태이며, applicability는 `not_assessed`이다[D1]. 즉 이 값들은 실험적으로 검증되지 않았고, 대상 물질 특이적 정확도나 도메인 포함 여부도 평가되지 않았다. 또한 입력에는 조건 슬롯이 포함되지 않았다(conditions_in_input=false)[D1]. 따라서 이 수율은 특정 실험 조건에서의 실험 수율이 아니다.

### 4.4 모델 간 관계 정리

- AiZynthFinder는 경로 구조를 제공한다.
- Parrot은 각 반응의 조건 후보를 제공한다.
- rxn_yields는 반응 SMILES에 대한 수율 예측을 제공한다.[6]
- Parrot 조건은 수율 예측의 입력이 아니다.
- 온도·시간·당량·압력은 조건 체크포인트에서 제공되지 않았다.
- 예측 수율은 실험 수율이 아니며, 적용 가능성도 평가되지 않았다.

AiZynthFinder는 경로 구조를 제공하고, Parrot은 각 반응의 조건 후보를 제공하며, rxn_yields는 반응 SMILES에 대한 수율 예측을 제공하지만, Parrot 조건은 수율 예측의 입력이 아니며 온도·시간·당량·압력은 조건 체크포인트에서 제공되지 않았고, 예측 수율은 실험 수율이 아니며 적용 가능성도 평가되지 않았다 [D1][6].

## 5. 추가 분석: MOPAC, EPI Suite, Discovery Studio Visualizer, 하네스 비교

이 절에서는 실행된 추가 분석을 정리한다. 각 분석은 실제 수행된 범위까지만 서술하고, 수행되지 않은 내용을 수행한 것처럼 쓰지 않는다. 또한 고립 분자 계산, 순수 물질 물성 추정, 단일 분자 화면 관찰은 반응 장벽·속도·수율·성공의 증거가 아니라는 한계를 함께 둔다.

### 5.1 MOPAC PM7 계산

MOPAC 23.2.5로 PM7[10] 고립 분자 기하 최적화가 수행되었다[D5]. 이번 작업에서는 다섯 중성 종에 대해 각각 5개의 RDKit ETKDGv3 conformer를 MMFF94s로 먼저 최소화한 뒤, 각각을 MOPAC으로 독립 최적화했다[D5]. 입력은 `CHARGE=0 MS=0`으로 설정되어 중성 단일항 상태를 지정했고, MOPAC 출력은 폐쇄껍질 RHF, SCF 완료, 정상 종료, 최종 기울기 노름이 요청된 `GNORM=0.5[11] kcal mol⁻¹ Å⁻¹` 미만임을 확인했다[D5]. 총 25개 작업 중 25개가 수렴했다[D5].

최적화된 구조 중 저장된 것은 각 분자식·전하·스핀에 대해 다섯 시작 배좌 중 PM7 생성열이 가장 낮은 수렴 기하이다[D5]. 이는 best-of-five 탐색이며, 전역 최소점이나 진동수 검증 최소점이라고 단정하지 않는다. 모든 계산은 기체상이며, 용매·촉매·수소·반대이온·반응 파트너·전이상태는 포함되지 않았다[D5].[10]

계산된 생성열은 종별로 기록되었다[D5]. 예를 들어 에틸 4-니트로벤조에이트는 −72.22692 kcal/mol, 벤조카인은 −73.05519 kcal/mol, 4-아미노벤조산은 −70.47009 kcal/mol, 에탄올은 −57.85665 kcal/mol, 아세트산은 −102.19677 kcal/mol로 기록되어 있다[D5]. 다만 이 값들은 서로 다른 분자식 간 직접 비교로 반응성·안정성을 순위화하는 근거가 아니다. 조성·전하가 다른 분자의 총에너지를 직접 비교해 반응성·안정성을 순위화하지 않는다는 원칙이 적용된다.

대표 결합 거리와 전하도 계산되었다[D5]. 예를 들어 에틸 4-니트로벤조에이트의 에스터 C=O는 1.2050 Å, 에스터 C–O는 1.3528 Å, 아릴 C–니트로 N은 1.4603 Å이며, 두 N–O 거리는 1.2198 Å로 같다[D5]. 벤조카인의 아릴 C–NH₂ N은 1.3772 Å, 에스터 C=O는 1.2080 Å, 에스터 C–O는 1.3613 Å이다[D5]. 4-아미노벤조산의 아릴 C–NH₂ N은 1.3760 Å, 카복실 C=O는 1.2071 Å, 카복실 C–O는 1.3654 Å이다[D5]. 에탄올의 C–O는 1.4142 Å, 아세트산의 C=O는 1.2021 Å, C–O는 1.3612 Å이다[D5].

이 기하와 전하 분포는 계산된 고립 분자의 특성을 기술할 뿐, 반응물 접근성, 반응 경로, 활성화 장벽, 실험 조건, 수율, 합성 성공을 입증하지 않는다[D5]. 특히 이 작업은 Pd 촉매나 route-01 상위 Parrot 조건 슬롯에서 누락된 환원 조건을 모델링하지 않았다[D5].[D1]

### 5.2 EPI Suite (MPBPWIN 및 EPI Web)

EPA의 EPI Suite는 유기화학물질의 녹는점·끓는점·증기압 등을 추정(screening-level)하는 도구[12]로 설명된다[D6]. 이번 작업에서는 다운로드 가능한 v4.11의 실행 어려움이 안내되어 EPI Suite Web[13] 베타를 사용했고, HTTP 200 응답은 받았으나 API 건강 상태는 `degraded`, `requestHandling.healthy=false`로 기록되었다[D6]. 따라서 결과는 서비스 제한 하에서 수신된 것으로 다룬다. 로컬 EPI Suite 설치는 수행하지 않았다[D6].

MPBPWIN v1.44 모델 추정치와 EPI Unified 데이터베이스 기록은 구분해야 한다[D6]. `estimatedValue`는 모델 추정치이고, `experimentalValues`/EpiUnified 증거는 데이터베이스 기록이며, `selectedValue`가 항상 측정값을 뜻하는 것도 아니다. 이번 결과에서 모델 추정치는 7개 물질에 대해 모두 `ESTIMATED`로 표시되었다[D6].[12]

주요 추정값과 데이터베이스 기록은 다음과 같이 정리된다[D6].

- 에틸 4-니트로벤조에이트: MPBPWIN MP 80.66 °C, BP 297.25 °C. EPI Unified 기록은 반환되지 않았다.[12][D6]
- 벤조카인: MPBPWIN MP 66.17 °C, BP 279.90 °C. EPI Unified 기록은 반환되지 않았다.[12][D6]
- 4-아미노벤조산: MPBPWIN MP 94.08 °C, BP 307.70 °C. EPI Unified MP 기록은 188.5 °C이며 분류는 `derived_or_analogue_database_entry_not_direct_measurement`이다.[12][D6]
- 에탄올: MPBPWIN MP −87.84 °C, BP 65.11 °C. EPI Unified MP는 −114.1 °C, BP는 78.2 °C이며 분류는 각각 `derived_or_analogue_database_entry_not_direct_measurement` 또는 `epi_database_evidence_provenance_insufficient_to_claim_direct_experiment`이다.[12][D6]
- 아세트산: MPBPWIN MP −21.26 °C, BP 122.30 °C. EPI Unified MP는 16.635 °C, BP는 117.9 °C이며 분류는 `literature_cited_epi_evidence_not_independently_verified_as_measurement` 또는 `epi_database_evidence_provenance_insufficient_to_claim_direct_experiment`이다.[12][D6]

에탄올, 아세트산, THF, 다이ethyl 에터에는 정확한 구조 일치 기록이 있었지만, 벤조카인과 에틸 4-니트로벤조에이트에는 EPI 검색 일치가 없어 보고된 값이 모델뿐이었다[D6]. 또한 일부 녹는점 기록은 기울기 유사(slope analogy)나 증기압/물 용해도 데이터 기반 계산 등으로 기술되어 직접 측정이 아니다[D6]. 아세트산 MP 기록은 1992 저자 문자열이 있으나 원문 논문·방법이 API에 포함되지 않아 주의가 필요하다[D6].

별도 교차 확인으로 호주 정부 국가 오염물질 목록은 아세트산 MP 16.7 °C, BP 118 °C를 제시하며, 이는 EpiUnified 기록 16.635 °C, 117.9 °C와 가깝다[D6]. 그러나 이 출처는 MPBPWIN 예측값을 검증하지 않는다. 실제로 MPBPWIN의 아세트산 추정값은 MP −21.26 °C, BP 122.30 °C로 다르다[D6].[12][14]

중요한 한계는, 선택된 Parrot 조건 예측이 반응 온도·압력·혼합 조성·양을 지정하지 않았고, EPI Web API는 순수 물질 BP/MP 추정값과 데이터베이스 기록만 반환했으며 혼합 상평형은 반환하지 않았다는 점이다[D6]. 따라서 순수 물질의 MP나 BP만으로 반응 용액에서 석출·용융·기화·반응 여부를 확정하지 않는다. 실제 운영 온도·압력, 용매·시약 당량·농도, 수분 함량, 화학 형태·염·수화 상태, 용해도나 혼합 거동 자료가 없으면 상태 판단을 유보한다[D6].

또한 `[Pd]`는 원소 원자 토큰이라 정의된 촉매 물질이 아니고, `[Al+3].[H-]...[Li+]`는 분리된 이온 표현이라 정의된 순수 중성 유기 화합물이 아니며, `FB(F)F`는 무기 BF₃라 MPBPWIN의 유기화합물 범위와 다르다[D6]. 이 세 입력은 제출되지 않았고, 값을 만들어 채우지 않았다[D6].[12]

### 5.3 Discovery Studio Visualizer 관찰

Discovery Studio Visualizer 2025 Client 25.1.0에서 실제 화면 관찰과 측정이 일부 수행되었다[D7]. 이번 증거에서 실제 측정이 이루어진 범위는 에틸 4-니트로벤조에이트의 PM7 배좌 1과 배좌 2에 대한 분자 내부 거리·각도뿐이다[D7].[10][D5]

실제 측정값은 다음과 같다[D7].

- 배좌 1: N10–H21 거리 2.684 Å, C8–C9–N10 각도 119.102°
- 배좌 2: N10–H21 거리 2.682 Å, C8–C9–N10 각도 119.062°

이 값들은 Visualizer의 Measure 도구와 DistanceMonitor/AngleMonitor 표에서 읽은 실제 측정값이다[D7]. 두 배좌에서 nitro N10과 같은 분자 내 ortho H21의 거리는 거의 같고, C8–C9–N10 국소 각도도 유사하다[D7]. 따라서 현재 Visualizer 기록은 선택된 두 PM7 최적화 기하에서 해당 nitro/아릴 주변의 국소 내부 배치가 서로 유사하다는 것까지만 보여 준다. 각도는 아릴 C8–C9 결합과 nitro N10이 이루는 분자 내부 각이며, 반응 공격각이 아니다[D7].[10][D5]

이 거리·각도는 외부 반응물이 분자에 접근할 공간, 결합 형성 가능성, 입체장애 장벽, 반응속도, 전환율, 수율을 측정하지 않는다[D7]. 두 배좌 결과만으로 전체 배좌 집단이나 용액 상태를 일반화하지 않는다. route-05의 PABA/ethanol 및 route-01의 나머지 배좌는 실제 측정이 없어 해석하지 않는다[D7].[D1]

실제 화면 관찰에는 에틸 4-니트로벤조에이트 배좌 1의 여러 방향 표시, 배좌 2의 단일 레코드 표시, 4-아미노벤조산 PM7 배좌 4의 카복실기 원자 C6/O7/O8 화면, 강체 회전한 표시 사본, 고립 에탄올 PM7 배좌 2 화면이 포함된다[D7]. 다만 강체 회전한 화면은 새 배좌가 아니라 표시 방향의 사본이며, 고립 에탄올 화면은 4-아미노벤조산과 함께 배치하지 않았다[D7]. 따라서 이 화면들은 정성적 단일 분자 관찰 이상으로 반응 복합체나 접근 궤적을 입증하지 않는다.[10][D5]

완료된 범위는 배좌 1·2의 거리·각도 4개 측정과 해당 Monitor 표 캡처, 원본 SDF 해시가 세션 전후 일치함을 기록한 것이다[D7]. 미완료 범위는 배좌 3–5와 route-05의 모든 측정이다[D7]. 배좌 전환 후 화면 재렌더링·선택 대상 연결이 간헐적으로 모호해졌고, 재열기 이후 기본 배좌가 1로 돌아오는 사례가 있어 잘못된 배좌에 수치를 연결할 위험이 있었기 때문에 같은 조작을 반복하지 않았다[D7]. 별도 코드·도구로 계산한 값은 Visualizer 측정값에 섞지 않았다[D7].[D1]


![Discovery Studio Visualizer 실제 화면: 같은 배좌, 분자 내부 C8–C9–N10 각도 119.102°](assets/visualizer-route01-conf1-angle.png)


![Discovery Studio Visualizer 실제 화면: 에틸 4-니트로벤조에이트, PM7 배좌 1, 분자 내부 N10–H21 거리 2.684 Å](assets/visualizer-route01-conf1-distance.png)


![Discovery Studio Visualizer 실제 화면: 고립 에탄올 PM7 배좌 2; 4-아미노벤조산과 함께 배치하지 않음](assets/visualizer-route05-ethanol-conf2.png)


![Discovery Studio Visualizer 실제 화면: 4-아미노벤조산, PM7 배좌 4, 고립 분자; 카복실기 원자 C6/O7/O8](assets/visualizer-route05-paba-conf4.png)


![4-아미노벤조산 PM7 배좌 4의 다른 방향 화면; 강체 회전한 표시 사본이며 새 배좌가 아님](assets/visualizer-route05-paba-edge.png)

### 5.4 하네스 비교

OpenCode와 Pi Coding Agent에 대해 각각 1회씩 성공 응답(HTTP 200)을 받은 사례 비교가 수행되었다[D8]. 두 하네스는 같은 모델 스냅샷(solar-pro4-260806), temperature 0, reasoning `none`, max_tokens 10000, n=1, 도구 비활성화 조건에서 실행되었다[D8]. 이는 사례 비교이며, 하네스 일반 성능의 우열을 입증하지 않는다[D8].

OpenCode 초안은 타깃, 선정 경로 3개, 경로 점수·수율, MOPAC 작업 수렴, EPI 상태, Visualizer 측정 범위를 대체로 제공 근거와 맞췄으나, EPI Suite의 구체적 MP/BP 추정값과 MOPAC 개별 에너지·결합 길이/전하 값이 없고 출처 URL도 없었다[D8]. Pi 초안은 반응 SMILES, 단계별 조건·수율, 점수와 추가 분석을 더 구체적으로 옮겼지만, 추가 분석 상태를 앞뒤 다르게 서술하는 내부 모순이 있었다[D8]. 또한 Pi 초안의 Visualizer 관련 표현은 실제 측정한 분자 내부 거리·각만으로 외부 반응물 접근성을 논할 수 있는 것처럼 읽힐 수 있어 범위를 좁혀야 한다[D8].[10][D5][12][D6][D7]

두 초안 모두 최종 보고서가 아니며, 그림·구조 이미지·실제 URL 연결 참고문헌·페이지 검증을 제공하지 않는다[D8]. 따라서 어느 초안도 제출용으로 확정할 수 없다. 이 비교는 하네스 사례 평가로만 다루고, 최종 보고서의 문체·정확성을 일반화하는 근거로 쓰지 않는다[D8].

## 6. 문헌 대조와 근거의 분리

### 6.1 route-01의 직접 실험 문헌

route-01의 변환, 즉 에틸 4-니트로벤조에이트에서 에틸 에스터를 유지한 벤조카인(에틸 4-아미노벤조에이트)으로의 방향족 니트로기 환원은 실제로 수행된 반응이다[D9][D1]. 이 점은 AI가 조건을 완성했다는 뜻이 아니라, 변환 그래프 자체가 직접 실험 문헌과 일치한다는 뜻이다[D9][D1].

직접 확인된 문헌 사례는 두 가지이다[D9][D1].

- Adams & Cohen, *Organic Syntheses[18]* **8**, 66 (1928): PtO₂ 촉매, 수소 기체(수소 3분자 당량 흡수까지), 95% alcohol(에탄올) 용매에서 에틸 4-니트로벤조에이트를 에틸 4-아미노벤조에이트로 환원하였다[D9][D1]. 수율은 15–16.5 g, 이론량의 91–100%로 보고되었고, 생성물 mp는 89–90 °C이다[D9][D1]. 이 수율은 여과·에탄올 증류 후 에터 재결정한 생성물의 질량 수율이며, 분리/재결정 후 수율로 읽힌다[D9][D1]. 온도·압력은 문헌에 수치로 기재되지 않았다[D9][D1].
- US 3,037,046[19] Example IV: Rh–alumina oxide 촉매(Rh 5 wt%), 벤젠 용매, 약 60 °C, 30 psig에서 수소화를 수행하였다[D9][D1]. 수율은 약 100% of theory로 보고되었고, 생성물 mp는 86–87 °C, 순도는 99.9%로 제시되었다[D9][D1]. 다만 Example IV 자체의 수율 측정법은 별도로 정의되지 않았고, Example I의 84.2%는 p-nitrobenzoic acid부터 에스터화와 환원을 포함하는 공정 값이므로 동일한 1단계 변환의 수율로 섞어 쓰지 않았다[D9][D1].

이 문헌 정보는 모델 입력·점수에 반영된 것처럼 쓰지 않는다. 문헌 검색은 예측 이후에 이루어졌고, 모델 입력이나 점수에 영향을 주지 않았다. 따라서 문헌 조건은 모델 출력과 분리해 후속 검토 후보로 표시한다.

### 6.2 Parrot 조건과의 대조

Parrot rank 1과 rank 4는 모두 route-01/step-01의 동일 반응 SMILES에 연결되어 있다[D9][D1]. rank 1은 catalyst1 `[Pd]`, solvent1 `CCO`, reagent1·reagent2가 비어 있고, rank 4는 catalyst1 `[Pd]`, solvent1 `CCO`, reagent1 `[H][H]`이다[D9][D1]. 두 후보 모두 온도·시간·압력을 제공하지 않는다[D9][D1].

문헌과 비교하면, rank 1과 rank 4의 `[Pd]`는 Org. Synth.의 PtO₂나 특허 Example IV의 Rh/Al₂O₃와 다르다[D9][D1]. `CCO`는 에탄올 구조 토큰이므로 Org. Synth.의 95% alcohol과 용매 계열은 맞지만 물 함량은 표현되지 않으며, 특허 Example IV의 벤젠과는 다르다[D9][D1]. rank 4의 `[H][H]`는 수소 분자 토큰으로 수소원 존재는 문헌과 일치하지만, 3당량 흡수량이나 수소압은 없다[D9][D1]. rank 1은 H₂ 슬롯이 누락된다[D9][D1]. 따라서 두 후보 모두 문헌 조건을 그대로 재현했다고 말할 수 없다. [19][D9]

### 6.3 Yield-BERT 예측과의 대조

route-01/step-01의 Yield-BERT[6] 예측은 82.95371431744555%이며, 상태는 `predicted_not_validated`, conditions_in_input은 false, applicability는 not_assessed이다[D9][D1]. 이 값은 반응 구조만 입력했고, Org. Synth.의 PtO₂/에탄올/H₂ 또는 특허 Example IV의 Rh/Al₂O₃/벤젠/H₂ 조건을 반영한 수율 예측이 아니다[D9][D1]. [19][D9]

동일한 기질·생성물 변환이라는 점에서 수치의 기술적 병치는 가능하다[D9][D1]. Org. Synth.의 분리 수율 91–100% 범위와 비교하면 예측은 약 8.05–17.05 퍼센트포인트 낮고, 특허 Example IV의 “approximately 100% of theory”와 비교하면 명목상 약 17.05 퍼센트포인트 낮다[D9][D1]. 그러나 이 예의 수율 측정법이 명시적으로 정의되지 않았으므로 확정적인 동일 기준 비교로 해석하지 않는다[D9][D1]. 두 차이는 조건을 맞춘 성능 오차나 실험 예측 잔차가 아니다[D9][D1]. [18][D9][6]

학습 데이터에 해당 Organic Syntheses 절차나 특허 반응이 포함됐는지, 중복 제거·문헌 중복 여부가 어떤지 확인할 수 있는 기록은 이번 자료에 없다[D9][D1]. 따라서 학습 데이터 중복 여부는 미확인이며, 있다고도 없다고도 결론내리지 않는다[D9][D1]. 한 반응 예로 Yield-BERT의 전체 정확도, 조건별 수율, 또는 실제 합성 성공을 입증할 수 없다[D9][D1].[6]

## 7. 조건부 경로 검토 결론과 실험 전 확인 사항

### 확인된 결과

- 벤조카인은 중성 유리 염기 형태의 C₉H₁₁NO₂ 화합물이며, PubChem CID 2337로 식별된다[1].
- AiZynthFinder 탐색은 route-01, route-02, route-05를 포함한 12개 경로를 생성했고, 각 모델의 출력은 정상 생성·정규화되었다[D1].
- route-01의 변환은 방향족 니트로기 환원으로, 직접 실험 문헌과 일치하는 변환 그래프이다[D9][D1].
- route-02는 N-아세틸기 제거를 통한 아미노기 노출 변환이며, route-05는 2단계 경로로 아세트산→에탄올 간선과 4-아미노벤조산+에탄올→벤조카인 단계를 포함한다[D1].
- MOPAC PM7 계산은 25/25 수렴했고, EPI Web 응답은 수신되었으며, Visualizer는 일부 실제 측정과 화면을 제공했다[D5].[10][D7]

### 우선 검토 경로와 근거

- Parrot 조건 후보는 실험 조건을 검증하지 않는다. 특히 route-01 상위 후보는 Pd 토큰과 에탄올 계열 용매를 제시하지만, 실제 촉매 제형·환원제·수소압·온도·시간·당량을 확인해 주지 않는다[D1].
- route-01 상위 후보의 `solvent1=CO`는 메탄올(CH₄O)로 검증되며[D12], `CCO`는 에탄올 구조 토큰이다. 이 슬롯들은 화학적 역할을 해석할 수는 있지만, 모델이 출력한 값 자체가 실험 조건을 검증했다는 뜻은 아니다[D1].
- route-05/step-02 상위 후보의 `CCOCC`는 디에틸 에터(C₄H₁₀O)로, `FB(F)F`는 삼불화붕소(BF₃)로 검증된다[D12]. 이 슬롯들은 화학적 역할을 해석할 수는 있지만, 모델이 출력한 값 자체가 실험 조건을 검증했다는 뜻은 아니다[D1].
- Yield-BERT 수율은 실험 수율이 아니며, 조건 입력이 없었고 적용 가능성도 평가되지 않았다[D1].[6]
- MOPAC은 고립 분자 기하·생성열·전하·쌍극자만을 제공하며, 반응 장벽·속도·수율·성공의 증거가 아니다[D5].[10]
- EPI Suite 추정값과 데이터베이스 기록은 혼합 상평형을 제공하지 않으며, 순수 물질 MP/BP만으로 반응 용액 상태를 확정하지 않는다[D6].[12]
- Visualizer는 일부 분자 내부 거리·각도와 정성적 단일 분자 화면만 제공하며, 반응물 접근·공격각·입체장애 장벽·반응 성공·수율을 측정하지 않는다[D7].
- route-05의 첫째 단계는 검색 모델의 경로 간선이며, 실제 순차 합성으로 검증되지 않았다[D1].

### 추가 확인 사항

- route-01을 실험한다면, Parrot rank 1의 H₂ 누락과 rank 4의 수소 토큰 존재를 별도로 검토하고, 실제 촉매 제형(Pd의 담지체·산화상태·실물 형태), 용매 조성(95% alcohol의 물 함량 등), 수소압·당량·온도·시간·작업업을 문헌 또는 별도 실험 설계로 확정해야 한다[D9][D1].
- route-02와 route-05/step-02는 에스터화·탈보호 계열 변환으로 읽을 수 있으나, 이번 조건 예측은 온도·시간·당량·압력을 제공하지 않으므로 운영 조건을 별도로 설계해야 한다[D1].
- route-05/step-01은 경로 간선일 뿐 실제 순차 합성 검증이 없으므로, 이 단계를 실제 합성에 포함하려면 독립적 검증이 필요하다[D1].
- 수율 예측은 반응 구조만 입력한 값이므로, 실험 계획에서는 조건별 수율·부산물·분리 수율·순도 기준을 별도로 설정해야 한다[D1].
- EPI Suite 값은 스크리닝 추정이므로, 실제 운영 상거동을 판단하려면 혼합 조성·농도·용매·온도·압력·용해도·염/수화 상태 등의 자료가 필요하다[D6].[12]
- Visualizer 관찰은 분자 내부 배치의 유사성까지만 지지하므로, 반응 접근성·입체장애·반응성 판단에는 추가 모델링 또는 실험이 필요하다[D7].
## 8. 재현 방법과 출처

### 8.1 실행 재현 개요

이번 실행은 AiZynthFinder 경로 탐색, Parrot 조건 추천, rxn_yields 수율 예측으로 구성되었다[16][D10]. 재현 관련 기록에서 routes와 yields는 이전 실행(benzocaine-live-20261031-03)의 결과를 바이트 단위로 재사용했고, 조건 추론은 이번 실행(benzocaine-live-20261031-04)에서 수행되었다[16]. 즉 이번 실행에서 세 모델 추론이 모두 새로 수행된 것은 아니다[16].[6]

재사용된 routes.json과 yields-rxn_yields.json의 해시는 각각 `a5256cab...`와 `18fd9a6f...`로 기록되어 있고, conditions-parrot.json의 해시는 `c1ec5ed4...`로 기록되어 있다[16][D10]. figures/manifest.json의 해시는 `222a4856...`이다[16][D10]. 입력 input.json의 해시는 `71ee5a5a...`이다[16][D10].[6]

### 8.2 재현 시 주의할 점

AiZynthFinder와 Parrot/rxn_yields의 Python 환경, 저장소, 체크포인트는 보존된 경로 아래 구성되어 있으며, 다른 기계에서 재현하려면 configs/runtime.json과 해당 자산을 맞춰야 한다[16]. 또한 routes와 yields는 이전 실행에서 복사된 것이므로, 이번 실행에서 세 모델 추론이 모두 새로 이루어졌다고 주장하지 않는다[16].[6]

재실행 검증 기록에서는 모델·USPTO 반응 템플릿 아카이브·재고 해시가 일치하고, routes 예측도 일치하며, Parrot 조건과 Yield-BERT 출력도 대표 실행과 일치하는 것으로 기록되어 있다[16][D10]. 다만 구성 JSON의 바이트 해시는 서로 다르고, 경로 구분자 정규화 후 구성 객체가 동일해지는 것으로 기록되어 있다[16][D10]. 이 바이트 차이의 원인은 unresolved로 남아 있다[16][D10]. 이 점은 동일 자산·동일 예측이라는 주장과 구성 파일 바이트 차이라는 관찰을 구분해 남겨 둔다.[6]

### 8.3 출처 목록

아래 출처는 보고서 본문에서 사용한 근거와 방법을 뒷받침한다. 외부 출처는 방법과 모델·데이터셋·문헌을, 프로젝트 출처는 이번 실행의 값·상태·해석을 뒷받침한다. 인용 번호는 이 보고서의 citation-source-map을 따른다.

1. Benzocaine identity, formula, structure identifier. PubChem CID 2337. https://pubchem.ncbi.nlm.nih.gov/compound/2337
2. AiZynthFinder retrospective route-planning method. [D1] https://github.com/MolecularAI/aizynthfinder
3. SynthEx project identity and release-status statements only. https://github.com/schwallergroup/synthex
4. ASKCOS v2 context recommender identity and service guidance. https://gitlab.com/mlpds_mit/askcosv2/context_recommender
5. Parrot reaction-condition prediction method and output fields. https://github.com/wangxr0526/Parrot
6. rxn_yields reaction-SMILES yield-prediction model. [6] https://github.com/rxn4chemistry/rxn_yields
7. DRFP reaction fingerprint library identity. https://github.com/reymond-group/drfp
8. rxn_yields normalization implementation and training-statistic procedure. [6] https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/training_scripts/launch_uspto_training.py
9. USPTO reaction-yield dataset source. https://ibm.ent.box.com/v/uspto-yields-data
10. MOPAC PM7 method documentation. [10][D5] https://openmopac.net/Manual/pm7.html
11. MOPAC geometry gradient/GNORM criterion documentation. [10][D5][11] https://openmopac.net/Manual/precision.html
12. EPA EPI Suite scope, MPBPWIN estimations, screening-level caveat, current v4.11 notice. [12][D6] https://www.epa.gov/tsca-screening-tools/epi-suitetm-estimation-program-interface
13. EPI Suite Web beta application endpoint only. [12][D6] https://episuite.dev/EpiWebSuite/#/
14. Australian government acetic-acid MP/BP reference values. [14] https://www.dcceew.gov.au/environment/protection/npi/substances/acetic-acid-ethanoic-acid
15. rxn_yields USPTO dataset exploration notebook. [6] https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/nbs/02_uspto_data_exploration.ipynb
16. Project execution manifests, commands, version and reuse records. evidence-run/manifest.json; evidence-run/reproducibility-manifest.json
17. Course-only claims summarized from the specified original lecture pages; original PDF excluded from redistribution. evidence-run/course-evidence-summary.md; evidence-run/course-material-acquisition.md. User obtains the course file from the course LMS.
18. Direct ethyl p-nitrobenzoate to benzocaine experiment, procedure, and reported isolated yield. https://doi.org/10.15227/orgsyn.008.0066
19. Direct hydrogenation experiment, patent Example IV conditions and reported yield. [19][D9] https://patents.google.com/patent/US3037046A/en

### 8.4 프로젝트 증거 파일

- D1: Route, condition and yield report-evidence output. evidence-run/report-evidence.json
- D2: Current status of additional analyses. evidence-run/additional-analysis-status-current.json
- D3: Resolved evidence conflicts and stale-state corrections. evidence-run/evidence-conflict-resolution.md
- D4: Validation notes and applicability/unsupported-status checks. evidence-run/validation_notes.json
- D5: Actual MOPAC inputs, convergence and computed values. evidence-run/mopac-results-interpretation.md[10][D5]
- D6: Actual EPI Web responses, values and provenance classifications. evidence-run/epi-analysis.md
- D7: Actual Visualizer observations, screenshots and measurements. evidence-run/visualizer-measurement-interpretation.md; evidence-run/visualizer-observation-index.csv; evidence-run/visualizer-measurements.csv[D7]
- D8: Actual OpenCode/Pi requests, responses and case comparison. evidence-run/harness-trial-02-comparison-evaluation.md; evidence-run/harness-trial-02-status.json; evidence-run/harness-trial-02-budget.json; evidence-run/reproducibility-manifest.json
- D9: Primary literature comparison, source identity/hash and acquisition guidance, and exact Parrot/Yield-BERT source data. evidence-run/literature-validation/route-01-primary-comparison-20261114/ 아래의 literature-comparison.md, comparison.json, validation.json, source-integrity.json, source-acquisition.md 및 evidence/routes.raw.json, conditions-parrot.raw.json, yields-rxn_yields.raw.json[6][D1]
- D10: Existing-PC rerun and corrected asset/configuration comparison; corrected validation은 보존된 원본 상충 기록과 구별된다. evidence-run/rerun/benzocaine-live-repro-20261105-01/ 아래의 reproduction-validation-corrected.json, reproduction-validation-original-conflicting.json, verification.json, manifest.json

- [D11] User-provided target selection provenance. evidence-run/report-context.json
- D12: Verified Parrot structure-token to chemical identity mapping. evidence-run/token-identity-evidence.json; evidence-run/chemical-token-audit.csv

## 부록: 미해결 사항과 기록 보존 원칙

- route-01의 Parrot 상위 조건은 문헌의 PtO₂나 Rh/Al₂O₃를 정확히 제시하지 않고, H₂ 슬롯도 후보마다 다르다. 문헌 조건은 모델 출력과 분리해 후속 검토 후보로 남겨 둔다[D9][D1].
- Yield-BERT 예측과 문헌 수율의 차이는 조건 일치 성능 오차로 해석하지 않는다. 학습 데이터 중복 여부도 미확인이다[D9][D1].[6]
- MOPAC은 고립 분자만 다루므로 반응 장벽·속도·수율·성공의 증거가 아니다[D5].[10]
- EPI Suite는 서비스 저하 상태에서 수신되었고, 혼합 상평형 정보는 제공하지 않는다[D6].[12]
- Visualizer는 일부 분자 내부 거리·각도와 정성적 단일 분자 화면만 제공하며, 반응물 접근·공격각·입체장애·반응 성공·수율을 측정하지 않는다[D7].
- route-05/step-01은 경로 간선이며 실제 순차 합성 검증이 없다[D1].
- 과거 준비-phase 상태 파일에는 추가 분석이 not_implemented로 남아 있었으나, 현재 증거는 MOPAC 25/25 수렴, 실제 EPI 응답, Visualizer 두 배좌 측정을 기록한다[D3]. 이 상충은 과거 기록을 지우지 않고, 현재 증거만 현재 사실로 사용한다[D3].[10][D5][D7]
- 구성 파일 바이트 해시 차이의 원인은 unresolved이며, 경로 구분자 정규화 후 구성 객체가 동일하다는 관찰과 함께 남겨 둔다[16][D10].

이 보고서는 제공된 증거와 스킬 규칙에 따라 작성했으며, 수행되지 않은 계산·GUI 관찰·모델 실행·실험 조건을 수행하지 않은 것으로 서술하지 않았다. 통합 조건·수율 표와 실제 그림 삽입은 문서 렌더러가 검증된 로컬 파일로 수행한다.
