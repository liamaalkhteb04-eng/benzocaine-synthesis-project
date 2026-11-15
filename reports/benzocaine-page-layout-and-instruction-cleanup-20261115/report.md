# 벤조카인(Benzocaine) 합성 경로 예측 및 추가 분석 보고서

## 1. 표적 물질과 선정 근거

벤조카인(Benzocaine, C₉H₁₁NO₂)은 파라-아미노벤조산 에틸 에스터(para-aminobenzoic acid ethyl ester)로, 국소 마취제로 널리 알려진 분자이다. 본 보고서의 표적 구조는 중성 유리 염기(neutral free base) 형태이며, SMILES는 `CCOC(=O)c1ccc(N)cc1`이다. 구조상 두 작용기가 합성 경로 비교의 핵심 질문을 만든다. 하나는 방향족 고리의 파라 위치에 있는 아미노기(–NH₂)이고, 다른 하나는 카복실산이 에틸 에스터(–COOEt)로 표현된 부분이다. 이 두 작용기는 역합성 분석(retrosynthetic analysis)에서 서로 다른 전구체(precursor) 분해 전략을 낳는다. 예를 들어 아미노기를 니트로기(–NO₂)에서 환원하는 경로, 보호된 아미드에서 탈보호하는 경로, 또는 에스터화 단계에서 아미노산을 직접 사용하는 경로가 각각 다른 구조 변화를 제안한다[1][D1].

이 보고서는 벤조카인을 최종 과정 표적으로 삼아 실제 합성 예측과 증거 기반 추가 분석을 수행한다. 표적 선정은 과정 과제에서 주어진 목표 분자를 다루는 데 목적이 있으며, 이 사실만으로 화학적 우수성을 주장하지 않는다. 아래에서는 예측된 경로에서 작용기가 어떻게 바뀌는지, 조건·수율 모델의 신뢰 범위가 어디까지인지, 그리고 어떤 경로를 어떤 이유로 먼저 검토할 수 있는지를 증거 중심으로 정리한다.

![벤조카인(C9H11NO2) 구조: 파라 아미노기와 에틸 에스터](assets/target.png)

## 2. 탐색 범위와 경로 선정

### 2.1 경로 선정 및 비교

이번 탐색에서는 총 12개 경로가 해결(solved) 상태로 확인되었고, 이 중 4개 경로는 1단계, 8개 경로는 2단계로 구성된다. 검토 대상은 검색 점수 기준으로 앞선 1단계 경로 두 개와, 단계 수와 중간체 준비를 비교하기 위한 2단계 경로 한 개를 선별한 것이다. 이 선별은 검색 순서와 다양성을 반영한 것이며, 실험 가능성이나 최적 경로 판정을 뜻하지 않는다. [2][D1]

아래 표는 세 경로의 단계 수, 전구체 수와 모델 stock 플래그, 각 단계의 예측 수율, 그리고 조건 출력의 차이를 실제 결과 그대로 정리한 것이다. route-01과 route-02는 각각 1단계, route-05는 2단계이다. route-05의 수율은 step-01 77.5889033%, step-02 79.7983250%로 개별 기재하며, 단계별 예측값을 곱하거나 합산하여 전체 수율을 계산하지 않는다. 모든 수율 예측값은 반응 SMILES만 입력하여 얻은 Yield-BERT의 단계별 예측이며, 온도·시간·당량·조건 수율이 함께 입력된 실험 수율이 아니다. 적용 범위(applicability)는 `not_assessed`로 기록되어 있다. [6][8][D1][D4]

| 경로 | 단계 수 | 전구체 수 / stock 플래그 | 단계 반응(축약) | 단계별 예측 수율 | Parrot 조건(상위 후보) | 누락 조건 |
|---|---|---|---|---|---|---|
| route-01 | 1 | 1 / 1 | ethyl 4-nitrobenzoate → benzocaine | 82.95% (predicted_not_validated) | rank 1: catalyst1 `[Pd]`, solvent1 `CCO`, solvent2 빈 값, reagent1 빈 값, reagent2 빈 값; rank 4: catalyst1 `[Pd]`, solvent1 `CCO`, reagent1 `[H][H]` | 온도, 시간, 당량, 압력/분위기, 조건 수율 |
| route-02 | 1 | 1 / 1 | ethyl 4-acetamidobenzoate → benzocaine | 77.70% (predicted_not_validated) | rank 1: catalyst1 빈 값, solvent1 `CCO`, solvent2 빈 값, reagent1 `Cl`, reagent2 빈 값 | 온도, 시간, 당량, 압력/분위기, 조건 수율 |
| route-05 | 2 | 2 / 2 | step-01: acetic acid → ethanol; step-02: ethanol + 4-aminobenzoic acid → benzocaine | step-01 77.59%, step-02 79.80% (각각 predicted_not_validated) | step-01 rank 1: catalyst1 빈 값, solvent1 `C1CCOC1`, reagent1 `[Al+3].[H-].[H-].[H-].[H-].[Li+]`; step-02 rank 1: catalyst1 빈 값, solvent1 `CCO`, solvent2 빈 값, reagent1 `CCOCC`, reagent2 `FB(F)F` | 온도, 시간, 당량, 압력/분위기, 조건 수율 |

Parrot 조건 필드는 모델 데이터셋 슬롯 이름(`catalyst1`, `solvent1`, `solvent2`, `reagent1`, `reagent2`)과 반환값을 그대로 보존하였다. 이 값들은 후보 조합이며, 각 토큰이 실험에서 어떤 화학적 역할을 하는지는 이 출력만으로 검증되지 않는다. 예를 들어 route-05/step-02 rank 1의 `reagent1=CCOCC`, `reagent2=FB(F)F`는 모델 슬롯 값이며, 이를 용매나 시약 역할로 옮겨 해석하지 않는다. `CCO`는 에탄올에 대응하는 토큰이고, `CCOCC`와 `FB(F)F`는 각각 디에틸 에터 및 BF3에 대응하는 구조 토큰으로 읽을 수 있으나, 실제 실험 역할은 별도로 확인해야 한다. 후보 점수는 확률이나 실험 성공률이 아니다. [5][D1]

route-01의 rank 1과 rank 4는 서로 다른 후보 조합이다. rank 1은 catalyst1 `[Pd]`, solvent1 `CCO`이며 reagent 슬롯이 비어 있고, rank 4는 catalyst1 `[Pd]`, solvent1 `CCO`에 reagent1 `[H][H]`가 있다. route-02의 `Cl`은 모호한 모델 토큰으로, 이를 HCl로 재해석하지 않고 그대로 보고한다. route-05는 2단계 경로이며, step-01은 아세트산에서 에탄올로의 분해적 전구체 변환에 해당하는 모델 경로 가장자리(edge)이다. 이 가장자리는 실제 준비 과정이나 검증된 반응 순서로 확인된 것이 아니다. [2][5][D1][D4]

모델 stock 플래그는 경로 탐색기의 재고 데이터베이스 상태를 반영할 뿐, 현재 구매 가능성·가격·실험 난이도를 뜻하지 않는다. 가격과 실험 난이도는 이 보고서에서 다루지 않는다. [2][D1]

이 비교에서 route-01을 먼저 문헌과 시약 정보를 확인할 후보로 제안하는 근거는, 해당 변환(에틸 4-니트로벤조에이트 → 에틸 4-아미노벤조에이트, 벤조카인)이 검토된 변환 중 직접적인 1차 문헌 선례가 있는 경로이기 때문이다. 관련 문헌으로는 Organic Syntheses Procedure 1 [18]과 US Patent 3,037,046 Example IV [19]가 있으며, 문헌 비교와 원문 확보 안내는 [D9]에 제시되어 있다. 이 문헌 검토는 AI 추론 이후에 수행되었으며, 어떤 모델 입력에도 포함되지 않았고 경로 순위, Parrot 출력, Yield-BERT 예측에는 영향을 주지 않았다. route-02는 대체 단일 단계 경로로, route-05는 단계 수와 중간체 준비를 비교하기 위한 비교군으로 유지한다. 이 우선순위는 예측 수율만으로 정한 것이 아니며, 최적 경로나 실험 권고가 아니다. 판단을 바꿀 수 있는 근거로는 실제 문헌에 보고된 반응 조건, 시약 정체성, 촉매/환원제 정보, 용매·농도·염·수분 상태, 그리고 적용 범위가 확인된 수율 데이터가 있으며, 이에 대한 상세 조건·수율·모델 후보 표는 3.1.1절에 제시되어 있으므로 해당 소절을 참조한다. [18][19][D9][D1]

## 3. 대표 경로의 단계별 구조 변화와 조건·수율

### 3.1 route-01 / step-01

route-01은 단일 단계로 벤조카인을 생성한다. 원시 반응 SMILES는 `CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1`이다. 출발물질은 에틸 4-니트로벤조에이트(ethyl 4-nitrobenzoate)이고 생성물은 벤조카인이다. 이 단계에서 방향족 니트로기(–NO₂)가 아미노기(–NH₂)로 바뀌고, 에틸 에스터는 유지된다. 템플릿 기반 역합성 간선은 아미노기 쪽에서 니트로기를 분리하는 형태로 기록되며, 생략된 시약은 재구성되지 않았다[2][D1].

![route-01/step-01: 에틸 4-니트로벤조에이트에서 벤조카인으로; 방향족 니트로기(–NO₂)가 아미노기(–NH₂)로 바뀌고 에틸 에스터는 유지됨](assets/route-01-step-01.png)

**작용기와 전자 이동.** route-01/step-01의 원시 반응 SMILES `CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1`는 에틸 4-니트로벤조에이트에서 벤조카인으로의 단일 단계 변화를 나타내며, 방향족 니트로기가 아미노기로 바뀌고 에틸 에스터는 유지된다. 출발물질의 니트로기는 SMILES에서 `[N+](=O)[O-]`로 표현되어 형식전하 분리를 드러내고, 생성물의 아미노기는 중성 `N`으로 표기된다. Parrot 최상위 후보는 촉매 토큰 `[Pd]`와 용매 `CCO`(에탄올)를 제시하지만 시약 슬롯이 비어 있고 수소원·환원제·온도·시간·당량이 공급되지 않으므로, 첨가된 수소의 출처나 완전한 환원 화살표 순서를 이 출력에서 재구성하지 않는다. 이 단계의 전자쌍 이동과 시약 역할은 구조 변화만 확인된 상태이며, 구체적인 화살표 경로는 일반 가능한 해석으로만 언급할 수 있고 AI 반환 메커니즘으로 서술하지 않는다[2][5][D1][D4].

Parrot 조건 모델의 최상위 후보는 촉매 토큰 `[Pd]`, 용매 `CCO`(에탄올), 시약 슬롯 비어 있음, 서열 점수(sequence score) −1.700762152671814이다. 이 후보에는 환원제, 수소원, 온도, 시간, 당량이 없다. 낮은 순위의 수소 토큰이나 다른 후보를 최상위 조건으로 옮겨 해석하지 않으며, 이 출력만으로 반응 메커니즘을 추론하지 않는다. 온도, 시간, 조건 수율은 모두 미제공이다[5][D1][D4].

수율 모델(rxn_yields)의 예측값은 이 반응 SMILES만 입력으로 사용했으며, 조건 정보는 입력에 포함되지 않았다. 예측 수율은 82.95%이며, 상태(status)는 `predicted_not_validated`이다. 이는 실험적 검증 수율이 아니며, 조건별 실험 수율도 아니다. 정규화 복원에는 훈련 통계가 사용되었고, 표적 분자에 대한 적용 범위(applicability)는 평가되지 않았다[6][8][D1][D4].

### 3.1.1 route-01 direct experimental literature and AI-condition comparison

기준 반응은 `CCOC(=O)c1ccc([N+](=O)[O-])cc1 >> CCOC(=O)c1ccc(N)cc1`이며, 이번 절은 기존 AI 원시 결과를 실제 1차 문헌의 출발물질·생성물 반응과 대조한 조사 기록이다. [D9]

| Source / candidate | Catalyst / raw slots | Hydrogen or reductant | Solvent / work-up | Temperature / time / pressure | Yield / definition |
|---|---|---|---|---|---|
| Organic Syntheses, Procedure 1 [18][D9] | PtO2 0.2 g | H2 uptake 3 molecular equivalents | 95% alcohol 150 cc; filter catalyst, distil alcohol, recrystallize with ca. 40 cc ether | temperature and pressure unreported; H2 uptake ca. 7 min | 15-16.5 g, 91-100% theory; isolated after recrystallization; conversion/analytical yield not separately reported |
| US 3,037,046, Example IV [19][D9] | Rh-alumina 1.89 g (Rh 5 wt%) | H2 hydrogenation; equivalents unreported | benzene, volume unreported | ca. 60 deg C; time unreported; 30 psig | ca. 100% theory; yield method unclear; mp 86-87 deg C; purity 99.9% |
| Parrot route-01/step-01 rank 1 [5][D1] | catalyst1 `[Pd]` | reagent1 empty; reagent2 empty | solvent1 `CCO`; solvent2 empty | temperature/time/yield null; no pressure field | no experimental yield; sequence_score -1.700762152671814 |
| Parrot route-01/step-01 rank 4 [5][D1] | catalyst1 `[Pd]` | reagent1 `[H][H]`; reagent2 empty | solvent1 `CCO`; solvent2 empty | temperature/time/yield null; no pressure field | no experimental yield; sequence_score -2.878655195236206 |

이 슬롯을 화학적으로 읽을 때 `[Pd]`는 단일 Pd 원소 토큰이고, `CCO`는 에탄올 구조 토큰이며, `[H][H]`는 수소 분자 토큰이다. 그러나 `[Pd]`는 촉매의 담지체·산화상태·실물 형태를 확정하지 않으며, `CCO`는 95% alcohol의 물 함량이나 용매 조성을 지정하지 않는다. rank 1은 수소원 슬롯이 비어 있고, rank 4는 수소 토큰을 포함하지만 어느 문헌 사례와도 촉매·용매 조합이 일치하지 않는다. 따라서 모델 슬롯과 화학적 해석은 구분해서 읽어야 하며, 이 출력만으로 문헌 조건과의 일치를 주장할 수 없다. [5][D1][18][19][D9]

점수(sequence_score)는 Parrot의 순위 지표이며 반응 확률이나 실험 성공률이 아니다. rank 1과 rank 4는 서로 다른 후보 조합이므로, 한 후보의 수소 토큰을 다른 후보의 조건처럼 합쳐서 해석하지 않는다. [5][D1]

Yield-BERT가 route-01/step-01 반응 SMILES만으로 예측한 값은 82.95371431744555%이며, 상태는 `predicted_not_validated`, `conditions_in_input=false`, `applicability=not_assessed`로 기록되어 있다. 이는 반응 구조만 입력한 예측이며, Organic Syntheses의 PtO₂/95% alcohol/H₂ 조건이나 특허의 Rh–alumina/benzene/30 psig 조건을 반영한 조건화 예측이 아니다. [6][D1][D4] [18][19][D9]

동일한 기질·생성물 변환이라는 점에서 수치의 기술적 병치는 가능하다. Organic Syntheses의 분리 수율 91–100% 범위와 비교하면 예측은 문헌 구간보다 약 8.05–17.05 퍼센트포인트 낮다(82.95371431744555 − 91, 82.95371431744555 − 100). 특허 Example IV의 “approximately 100% of theory”와 비교하면 명목상 약 17.05 퍼센트포인트 낮지만, 이 예의 수율 측정법이 명시적으로 정의되지 않았으므로 확정적인 같은 기준 비교로 해석하지 않는다. 이 차이는 조건을 맞춘 성능 오차나 실험 예측 잔차가 아니다. [18][19][D9][6][D1]

학습 데이터에 해당 Organic Syntheses 절차나 특허 반응이 포함됐는지, 중복 제거 또는 문헌 중복 여부가 어떤지 확인할 수 있는 기록은 이번 자료에 없다. 따라서 학습 데이터 중복 여부는 미확인이며, 있다고도 없다고도 결론내리지 않는다. 한 반응 예로 Yield-BERT의 전체 정확도, 조건별 수율, 또는 실험 합성 성공을 입증할 수 없다. [6][D1][D4] [18][19][D9]

### 3.2 route-02 / step-01

route-02도 단일 단계로 벤조카인을 생성한다. 원시 반응 SMILES는 `CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1`이다. 출발물질은 에틸 4-아세트아미도벤조에이트(ethyl 4-acetamido benzoate)이고 생성물은 벤조카인이다. 이 단계에서는 N-아세틸기가 제거되어 아미노기가 드러나며, 에틸 에스터는 유지된다. 템플릿 기반 간선은 아미드 쪽 결합을 분해하는 형태로 기록되며, 생략된 시약은 재구성되지 않았다[2][D1].

![route-02/step-01: 에틸 4-아세트아미도벤조에이트에서 벤조카인으로; N-아세틸기가 제거되어 아미노기가 드러나며 에틸 에스터는 유지됨](assets/route-02-step-01.png)

**작용기와 전자 이동.** route-02/step-01의 원시 반응 SMILES `CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1`는 에틸 4-아세트아미도벤조에이트에서 벤조카인으로의 단일 단계 변화를 나타내며, N-아세틸기가 제거되어 아미노기가 드러나고 에틸 에스터는 유지된다. 이 간선은 템플릿 기반 역합성 분해로 기록되었고 생략된 시약은 재구성되지 않았으므로, 실제 탈보호 시약과 부산물의 정체는 이 출력에서 확정되지 않는다. Parrot 최상위 후보는 용매 `CCO`(에탄올)와 시약 토큰 `Cl`을 제시하지만 촉매 슬롯이 비어 있고 온도·시간·당량도 공급되지 않으며, `Cl`을 HCl로 재해석하거나 특정 산 시약으로 단정하지 않는다. 이 출력만으로는 전자 화살표의 출발점·도착점과 시약·촉매·용매의 역할을 resolved된 형태로 제시할 수 없으므로, 구조 순변화만 기술하고 전자 이동의 구체 경로는 일반 가능한 해석으로도 확정하지 않는다[2][5][D1][D4].

Parrot 최상위 후보는 촉매 슬롯 비어 있음, 용매 `CCO`(에탄올), 시약 토큰 `Cl`, 서열 점수 −1.3239554166793823이다. `Cl`을 HCl로 재해석하지 않으며, 이 토큰을 특정 산 시약으로 단정하지 않는다. 온도, 시간, 당량, 조건 수율은 모두 미제공이다[5][D1][D4].

수율 모델의 예측값은 이 반응 SMILES만 입력으로 사용했으며, 예측 수율은 77.70%이다. 상태는 `predicted_not_validated`이고, 조건 정보는 입력에 포함되지 않았다. 적용 범위와 표적 정확도는 평가되지 않았다[6][8][D1][D4].

### 3.3 route-05 / step-01

route-05는 2단계 경로이다. step-01의 원시 반응 SMILES는 `CC(=O)O>>CCO`이다. 이 간선은 아세트산(acetic acid)에서 에탄올(ethanol)로 가는 검색 모델의 경로 간선이며, 실제 순차 합성으로 검증되지 않았다. 즉 이 단계는 역합성 탐색에서 생성된 모델 간선일 뿐, 실험적 정방향 반응 순서로 확인된 경로가 아니다[2][D1].

![route-05/step-01: 아세트산에서 에탄올로; 검색 모델의 경로 간선이며 실제 순차 합성으로 검증되지 않음](assets/route-05-step-01.png)

**작용기와 전자 이동.** route-05/step-01의 원시 반응 SMILES `CC(=O)O>>CCO`는 아세트산에서 에탄올로 가는 검색 모델의 경로 간선이며, 실제 순차 합성으로 검증된 정방향 반응 순서가 아니다. route-05/step-01의 `CC(=O)O>>CCO` 변환은 역합성 탐색 그래프의 연결로 확인되었으며, 검증된 정방향 실험 반응 순서로 해석되지 않는다 [2][D1]. Parrot 최상위 후보는 용매 `C1CCOC1`(테트라하이드로퓨란)과 시약 토큰 `[Al+3].[H-].[H-].[H-].[H-].[Li+]`를 제시하지만 촉매 슬롯이 비어 있고 온도·시간·당량·조건 수율이 모두 미제공이므로, 전체 경로·당량·온도·시간을 이 출력에서 채우지 않는다. 해당 후보 조합에 기대어 하이드라이드가 카보닐 탄소로 향하고 C=O 파이 전자가 산소로 이동하는 화살표를 일반적인 plausible 해석으로만 조건부로 언급할 수 있으며, 이는 AI 예측 메커니즘이 아니고 검증된 반응 경로도 아니다[2][5][D1][D4].

Parrot 최상위 후보는 촉매 슬롯 비어 있음, 용매 `C1CCOC1`(테트라하이드로퓨란), 시약 `[Al+3].[H-].[H-].[H-].[H-].[Li+]`(리튬 알루미늄 수소화물 관련 이온 표현), 서열 점수 −1.8564977645874023이다. 온도, 시간, 당량, 조건 수율은 미제공이다. 이 간선은 모델 탐색 결과로 제공되며, 실험적 합성 순서로 확정된 것이 아니다[5][D1][D4].

수율 모델의 예측값은 이 반응 SMILES만 입력으로 사용했고, 예측 수율은 77.59%이다. 상태는 `predicted_not_validated`이며, 조건 정보는 입력에 포함되지 않았다[6][8][D1][D4].

### 3.4 route-05 / step-02

route-05의 step-02 원시 반응 SMILES는 `CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1`이다. 출발물질은 에탄올과 4-아미노벤조산(4-aminobenzoic acid)이고 생성물은 벤조카인이다. 이 단계에서는 카복실산이 에틸 에스터로 표현되고, 아미노기는 유지된다. 템플릿 기반 간선은 에스터화 형태로 기록되며, 생략된 시약은 재구성되지 않았다[2][D1].

![route-05/step-02: 4-아미노벤조산과 에탄올에서 벤조카인으로; 카복실산이 에틸 에스터로 표현되고 아미노기는 유지됨](assets/route-05-step-02.png)

**작용기와 전자 이동.** route-05/step-02의 반응 SMILES는 `CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1`이며, 구조 변화는 카복실산(4-aminobenzoic acid의 -COOH)이 에틸 에스터(ethyl ester, -COOC2H5)로 바뀌는 것이다. 아릴 아미노기(-NH2)는 유지된다. 이 단계는 모델 경로에서 ethanol과 4-aminobenzoic acid를 반응물로 둔 에스터화 가장자리로 제시되며, 실제 실험에서 확인된 정방향 반응으로 단정하지 않는다. [D1]

강의 비교 관점에서 이 변환은 Fischer 에스터화의 교육적 예시로 설명할 수 있다. 일반적인 강의 메커니즘은 다음과 같은 순서로 기술한다. 먼저 산 촉매가 카보닐 산소를 양성자화하여 카보닐 탄소의 전자 결핍을 키운다. 이어 에탄올의 산소 비공유 전자쌍이 아실 탄소를 공격하고, C–O 결합이 형성되며 C=O 파이 전자가 산소로 이동한다. 이후 양성자 이동과 물 분자의 이탈이 일어나고, 카보닐이 복원되며 촉매가 재생된다. 이 설명은 교육적 비교용이며, Parrot이 출력한 모델 슬롯과 동일한 화학적 역할을 주장하는 것이 아니다. 모델 출력의 조건 슬롯은 별도로 보존하여 해석한다. [17, PDF pp. 90–95][5][D1].

#### 강의 예시와 AI 예측 비교

| 항목 | 강의 예시 | AI 예측 및 조건 후보 |
|---|---|---|
| 기질/생성물 | 4-aminobenzoic acid + ethanol → benzocaine (강의 예시) | ethanol + 4-aminobenzoic acid → benzocaine (반응 SMILES 기준) |
| 촉매/시약/용매 | H2SO4 촉매 (강의 예시) | catalyst1: (빈 슬롯); solvent1: `CCO`; solvent2: (빈 슬롯); reagent1: `CCOCC`; reagent2: `FB(F)F` (모델 슬롯; 실험 역할 미검증) [5][D1] |
| 전자 흐름 출발점 | 카르보닐 O 양성자화에서 시작 (강의 메커니즘) | Parrot은 화살표 메커니즘을 반환하지 않음 |
| 예측 수율 | 값 제공되지 않음 | 79.80% (predicted_not_validated; 반응 SMILES만 입력, conditions_in_input=false, applicability 미평가) |

route-05/step-02의 Parrot 상위 후보(rank 1)는 원시 JSON 기준으로 catalyst1이 빈 값, solvent1이 `CCO`, solvent2가 빈 값, reagent1이 `CCOCC`, reagent2가 `FB(F)F`이다. 따라서 이 단계의 조건 표기는 solvent2에 `CCOCC`가 있는 형태가 아니라, `reagent1=CCOCC`, `reagent2=FB(F)F`, `solvent2` 빈 값으로 읽어야 한다. 이 토큰들은 모델 데이터셋 슬롯 값이며, `CCO`는 에탄올에 대응하는 토큰, `CCOCC`와 `FB(F)F`는 각각 디에틸 에터 및 BF3에 대응하는 구조 토큰으로 볼 수 있으나, 실험에서의 검증된 역할로 옮겨 쓰지 않는다. 이 단계의 모델 예측 수율은 79.7983250%이며, 상태는 predicted_not_validated이고, 온도·시간·당량·조건 수율은 공급되지 않았다. 조건 후보 점수와 수율 예측은 확률이나 실험 성공률이 아니다. 이 정보는 프로젝트 조건 증거 [D1]와 방법 [5]에 근거한다. [6][D4]

수율 모델의 예측값은 이 반응 SMILES만 입력으로 사용했고, 예측 수율은 79.80%이다. 상태는 `predicted_not_validated`이며, 조건 정보는 입력에 포함되지 않았다. 적용 범위와 표적 정확도는 평가되지 않았다[6][8][D1][D4].

## 4. 통합 조건·수율 표

아래 표는 선정된 route-01, route-02, route-05의 각 단계를 route_id, step_id, 반응 SMILES 기준으로 연결한 단일 통합 표이다[D1]. Parrot 후보 점수와 서열 점수는 수율·확률·실험 성공률이 아니다[5][D1][D4]. 온도, 시간, 당량, 조건 수율은 조건 모델이 제공하지 않았으므로 `NOT SUPPLIED`로 표기한다[5][D1][D4]. 수율 모델 예측값은 실험값이 아니며, 조건별 실험 수율도 아니다[6][D1][D4]. 전체 수율은 독립적으로 예측된 단계값을 곱해 검증된 전체 수율로 만들지 않는다[6][D1][D4].

| route / step | 전구체 → 생성물 | 작용기 변화 | Parrot 최상위 후보(촉매/용매/시약)와 서열 점수 | 온도 / 시간 / 당량 / 조건 수율 | rxn_yields 예측 수율(%) 및 검증 상태 |
|---|---|---|---|---|---|
| route-01 / step-01 | 에틸 4-니트로벤조에이트 → 벤조카인 | 방향족 –NO₂ → –NH₂; 에틸 에스터 유지 | `[Pd]` / 에탄올 / (비어 있음), −1.700762 | NOT SUPPLIED / NOT SUPPLIED / NOT SUPPLIED / NOT SUPPLIED | 82.95%, predicted_not_validated; 조건 미입력, 적용 범위 미평가 |
| route-02 / step-01 | 에틸 4-아세트아미도벤조에이트 → 벤조카인 | N-아세틸기 제거 → –NH₂ 노출; 에틸 에스터 유지 | (비어 있음) / 에탄올 / `Cl`, −1.323955 | NOT SUPPLIED / NOT SUPPLIED / NOT SUPPLIED / NOT SUPPLIED | 77.70%, predicted_not_validated; 조건 미입력, 적용 범위 미평가 |
| route-05 / step-01 | 아세트산 → 에탄올 | 모델 간선; 실험 순서 미검증 | (비어 있음) / 테트라하이드로퓨란 / `[Al+3].[H-].[H-].[H-].[H-].[Li+]`, −1.856498 | NOT SUPPLIED / NOT SUPPLIED / NOT SUPPLIED / NOT SUPPLIED | 77.59%, predicted_not_validated; 조건 미입력, 적용 범위 미평가 |
| route-05 / step-02 | 에탄올 + 4-아미노벤조산 → 벤조카인 | 카복실산 → 에틸 에스터; –NH₂ 유지 | Parrot rank-1 raw fields: catalyst1 (empty); solvent1 `CCO`; solvent2 (empty); reagent1 `CCOCC`; reagent2 `FB(F)F`; sequence_score -2.175484 [5][D1] | NOT SUPPLIED / NOT SUPPLIED / NOT SUPPLIED / NOT SUPPLIED | 79.80%, predicted_not_validated; 조건 미입력, 적용 범위 미평가 [6][8][D1][D4] |

## 5. 각 모델의 입력, 출력, 검증, 실패, 한계

### 5.1 경로 탐색(AiZynthFinder)

AiZynthFinder는 표적 구조를 입력받아 템플릿/정책 기반 역합성 탐색을 수행한다. 이번 실행에서는 해결 표시된 경로 12개와 총 20개 단계가 출력되었다. 각 경로는 route_id, 단계 수, 상태 점수, 반응 수, 전구체 수, 재고 내 전구체 수로 기록된다. route-01과 route-02는 1단계, route-05는 2단계이다[2][D1].

경로 탐색 결과는 템플릿 해시, 분류(classification), 라이브러리 출현 횟수, 정책 확률, 정책 이름, 템플릿 코드, 템플릿 식, 매핑된 반응 SMILES를 포함한다. 예를 들어 route-01/step-01의 정책 이름은 `uspto`, 정책 확률은 0.42239999771118164, 정책 확률 순위는 0이다. route-02/step-01의 정책 확률은 0.011800000444054604, 순위는 5이다. route-05/step-01의 정책 확률은 0.09149999916553497, 순위는 0이다. route-05/step-02의 정책 확률은 0.1680999994277954, 순위는 2이다[2][D1].

경로 탐색의 주의사항은 템플릿 기반 분해이며 생략된 시약이 재구성되지 않았다는 점이다. 또한 재고 플래그와 템플릿 점수는 실용적 실행 가능성을 증명하지 않는다. 탐색은 표적을 재고에서 제외하며, 부산물·보호기·선택성 문제가 생략될 수 있다[2][D1][D4].

### 5.2 조건 모델(Parrot)

Parrot은 반응 SMILES를 입력받아 촉매·용매·시약 슬롯의 후보 조합을 출력한다. 이번 실행에서는 각 단계마다 상위 15개 후보가 기록되었다. 각 후보는 rank, catalyst1, solvent1, solvent2, reagent1, reagent2, sequence_score를 가진다. 예를 들어 route-01/step-01의 최상위 후보는 `[Pd]`, `CCO`, 비어 있음, 비어 있음, −1.700762152671814이다. route-02/step-01의 최상위 후보는 비어 있음, `CCO`, `Cl`, 비어 있음, −1.3239554166793823이다. route-05/step-01의 최상위 후보는 비어 있음, `C1CCOC1`, `[Al+3].[H-].[H-].[H-].[H-].[Li+]`, 비어 있음, −1.8564977645874023이다. route-05/step-02의 rank-1 후보는 catalyst1 빈 값, solvent1 `CCO`, solvent2 빈 값, reagent1 `CCOCC`, reagent2 `FB(F)F`, sequence_score -2.1754837036132812이다[5][D1].

Parrot 출력은 촉매·용매·시약 슬롯만 제공하며, 온도·시간·당량은 출력되지 않았다. 조건 모델의 온도 필드는 null이고, 온도 상태는 `not_provided_by_checkpoint`이다. 시간 필드와 수율_percent 필드도 null이다. 따라서 각 단계의 온도, 시간, 당량, 조건 수율은 `NOT SUPPLIED`로 남긴다. Parrot 후보 점수는 확률이나 수율이 아니다[5][D1][D4].

Parrot 조건 출력은 rxn_yields 수율 모델의 입력으로 제공되지 않았다. 즉 조건 후보와 수율 예측은 서로 다른 모델 출력이며, 조건 기반 실험 수율로 연결되지 않는다[5][6][D1][D4].

### 5.3 수율 모델(rxn_yields)

rxn_yields는 반응 SMILES를 입력받아 수율 예측을 출력한다. 이번 실행에서는 각 단계의 반응 SMILES만 입력으로 사용했고, 조건 정보는 입력에 포함되지 않았다. 각 단계의 입력 토큰 수는 46, 47, 13, 43개이며, 최대 입력 토큰 300 이내에서 잘림 없이 처리되었다. 수율 모델은 표준화된 분수(standardized_fraction) 척도로 원시값을 출력하고, 훈련 통계로 백분율로 복원했다[6][8][D1][D4].

예측 수율은 route-01/step-01 82.95%, route-02/step-01 77.70%, route-05/step-01 77.59%, route-05/step-02 79.80%이다. 모든 예측의 상태는 `predicted_not_validated`이고, 물리적 범위 내에 있다. 적용 범위(applicability)는 `not_assessed`이다. 즉 이 예측값은 실험적 검증 수율이 아니며, 조건별 실험 수율도 아니다. 표적 분자에 대한 정확도나 도메인 포함 여부도 평가되지 않았다[6][8][D1][D4].

정규화 복원에는 훈련 데이터의 평균과 표준편차가 사용되었다[6][8][D1][D4]. 훈련 수율 평균은 0.7318926847478698, 표준편차는 0.20946128682168402이며, 자유도 1의 표본 표준편차가 사용되었다[8][D1][D4]. 복원식은 `yield_percent = 100 * (raw_z * training_yield_std + training_yield_mean)`이다[6][8][D1]. 이 통계는 저자들이 제공한 전처리와 pandas 표본 표준편차로 복원한 것이며, 전역 데이터셋 대체 통계가 아니다[8][15][D1]. 훈련 도메인은 USPTO 그램 규모 무작위 분할(random split)이며, 표적 특이적 적용 범위는 평가되지 않았다[9][15][D1][D4].

### 5.4 DRFP 및 기타 모델

DRFP는 지문(fingerprint) 관련 도구로 인용된다[7]. ASKCOS v2와 SynthEx는 공식 저장소 수준에서 언급된다[4][3]. 이번 실행에서 실제로 사용한 핵심 예측 모델은 AiZynthFinder, Parrot, rxn_yields이며, 사용하지 않은 모델을 실행한 것처럼 쓰지 않는다. 본 프로젝트에서 경로, 반응 조건, 수율 예측은 AiZynthFinder, Parrot, rxn_yields를 통해 수행되었고, ASKCOS v2와 SynthEx는 저장소 수준에서 식별되었으며, DRFP는 지문 도구로 기술되었다 [2][5][6][7][D1][D2].

## 6. 추가 분석

### 6.1 MOPAC PM7 계산

MOPAC 23.2.5는 PM7 고립 분자 기하 최적화를 수행했다[10][D5]. 중성 5종 분자에 대해 각각 RDKit ETKDGv3 배좌 5개를 MMFF94s로 먼저 최소화한 뒤, MOPAC으로 독립 최적화했다[D5]. 입력은 `CHARGE=0 MS=0`으로 명시했으며, 지정된 상태는 중성 단일항이다[D5]. MOPAC 출력은 폐쇄껍질 RHF, SCF 완료, 정상 작업 종료, 최종 기울기 노름이 요청된 `GNORM=0.5 kcal mol⁻¹ Å⁻¹` 미만인 것을 25/25 작업에서 확인했다[D5][11].

저장된 구조는 분자식과 전하가 같은 다섯 시작 배좌 중 PM7 생성열이 가장 낮은 수렴 기하이다[D5][10]. 이는 5개 시작 중 최선 탐색이지, 증명된 전역 최소점이나 진동수 확인 최소점이 아니다[D5]. 모든 작업은 기체상이며, 용매·촉매·수소·반대이온·반응 파트너·전이상태는 포함되지 않았다[D5]. 계산된 생성열은 분자별로 출력 기록으로만 나열하며, 서로 다른 분자식과 조성의 총에너지를 비교해 안정성이나 반응성 순위를 매기지 않는다[D5][10].

에틸 4-니트로벤조에이트 선택 배좌에서 ester C=O 1.2050 Å, ester C–O 1.3528 Å, aryl C–nitro N 1.4603 Å, 두 N–O 거리는 1.2198 Å와 1.2198 Å이다. 선택된 배좌의 N 부분전하는 +0.6117 e, 두 O 부분전하는 −0.3904 e와 −0.3888 e이다. 벤조카인 선택 배좌에서 aryl C–NH₂ N 1.3772 Å, ester C=O 1.2080 Å, ester C–O 1.3613 Å이며, 아미노 N 부분전하는 −0.6321 e, 카보닐과 알콕시 O 부분전하는 −0.4421 e와 −0.5283 e이다. 4-아미노벤조산 선택 배좌에서 aryl C–NH₂ N 1.3760 Å, carboxyl C=O 1.2071 Å, carboxyl C–O 1.3654 Å이며, 아미노 N 부분전하는 −0.6274 e, carboxyl O 부분전하는 −0.5262 e와 −0.5700 e이다. 에탄올은 C–O 1.4142 Å, O 부분전하 −0.5507 e이다. 아세트산은 C=O 1.2021 Å, C–O 1.3612 Å, O 부분전하 −0.5065 e와 −0.5675 e이다[D5][10].

부분전하는 MOPAC의 인구 기반 순 원자 전하이며, 직접 관측 가능한 원자 성질이 아니다. 서로 조성이 다른 분자의 총에너지로 안정성 순위를 만들지 않으며, 이 계산은 반응 장벽·속도·수율을 증명하지 않는다. 특히 이 작업은 route-01의 높은 순위 Parrot 조건 슬롯에 나타나는 Pd 촉매나 누락된 환원 조건을 모델링하지 않는다[D5][10][11][5][D1].

### 6.2 EPI Suite MPBPWIN

EPA의 EPI Suite는 다운로드 가능한 v4.11의 기술적 실행 어려움을 안내하며, EPI Suite Web 베타를 사용하도록 지시한다[12][13]. 이번 실행에서는 EPI Web 엔드포인트를 사용했고, SMILES 전용 추정 배치와 CAS 확인 데이터 쿼리 모두 HTTP 200을 받았다[13][D6]. 다만 API 상태 문서는 `degraded`와 `requestHandling.healthy=false`를 보고했으므로, 이 서비스 제한을 함께 기록한다[D6]. 로컬 EPI Suite 설치는 수행하지 않았다[D6].

MPBPWIN은 유기 화학물질의 녹는점, 끓는점, 증기압을 여러 기법의 조합으로 추정하는 모델로 설명된다. EPA는 EPI Suite를 스크리닝 수준으로 설명하며, 추정값은 적합한 측정값을 대체해서는 안 된다. 아래에서는 MPBPWIN 모델 추정값과 EPI Unified 데이터베이스 레코드를 구분한다. 모든 온도는 °C이다[12][D6].

에틸 4-니트로벤조에이트는 MPBPWIN MP 추정 80.66 °C, BP 추정 297.25 °C이며, EPI Unified 레코드는 반환되지 않았다. 벤조카인은 MPBPWIN MP 추정 66.17 °C, BP 추정 279.90 °C이며, EPI Unified 레코드는 반환되지 않았다. 4-아미노벤조산은 MPBPWIN MP 추정 94.08 °C, BP 추정 307.70 °C이며, EPI Unified MP 레코드로 188.5 °C가 반환되었고 분류는 `derived_or_analogue_database_entry_not_direct_measurement`이다. 에탄올은 MPBPWIN MP 추정 −87.84 °C, BP 추정 65.11 °C이며, EPI Unified MP −114.1 °C, BP 78.2 °C가 반환되었고 분류는 각각 `derived_or_analogue_database_entry_not_direct_measurement` 및 `epi_database_evidence_provenance_insufficient_to_claim_direct_experiment`이다. 아세트산은 MPBPWIN MP 추정 −21.26 °C, BP 추정 122.30 °C이며, EPI Unified MP 16.635 °C, BP 117.9 °C가 반환되었고 분류는 각각 `literature_cited_epi_evidence_not_independently_verified_as_measurement` 및 `epi_database_evidence_provenance_insufficient_to_claim_direct_experiment`이다[12][13][D6].

제출된 7개 구조는 중성 유기 화합물이며 순 형식 전하가 0이다. 세 입력은 제출되지 않았다. `[Pd]`는 원소 원자 토큰이며 정의된 촉매 물질이 아니고, `[Al+3].[H-]...[Li+]`는 분리된 이온성 LiAlH₄ 표현이며 정의된 순수 중성 유기 화합물이 아니며, `FB(F)F`는 무기 BF₃이며 MPBPWIN의 명시된 범위 내 유기 화학물질이 아니다. 이 항목들에 대해 값을 조작하지 않았다[12][D6].

EPI Unified 필드는 균일하게 실험실 측정값이 아니다. 네 개의 녹는점 레코드는 명시적으로 기울기 유사성(slope analogy) 또는 VP/물 용해도 데이터 기반 계산이라고 기술되며, 이는 직접 관측이 아니라 파생/유사체 항목이다. 아세트산 MP 레코드는 1992 저자 문자열을 가지지만 API에서 기초 논문이나 방법을 제공하지 않으므로 저자 메타데이터에 주의가 필요하다. 다른 끓는점 레코드는 EpiUnified 증거로 태그되지만 저자·연도·압력을 반환하지 않으므로, 이 응답만으로는 측정 출처를 독립적으로 확인할 수 없다. `experimentalValues` 필드 이름만으로 모든 항목을 실험이라고 부를 수 없다[12][13][D6].

호주 정부 국가 오염물질 인벤토리는 아세트산 MP 16.7 °C, BP 118 °C를 제시하며, 이는 EpiUnified 데이터베이스 항목 16.635 °C 및 117.9 °C와 가깝다[14][D6]. 이 출처는 MPBPWIN 예측을 검증하지 않으며, 아세트산의 MPBPWIN 추정은 −21.26 °C와 122.30 °C였다[12][D6].

순물질의 녹는점·끓는점만으로 반응 혼합물의 석출·기화·반응 상태를 확정하지 않는다[12][13][D6]. 선택된 Parrot 조건 예측은 반응 온도·압력·혼합물 조성/량을 지정하지 않는다[5][D1]. Web API는 순수 화합물 BP/MP 추정값과 데이터베이스 레코드를 반환했으며, 혼합물 상평형을 반환하지 않았다[13][D6]. 운전 상(phase)을 평가하려면 실제 온도·압력, 용매·시약 당량·농도, 수분 함량, 화학형·염/수화 상태, 대기 조건, 혼합물 증기-액체/고체-액체 거동 또는 용해도 자료가 필요하다[12][13]. 순수 화합물 MP나 BP는 반응 feasibility나 수율의 증거가 아니다[12][13][D6].

### 6.3 Discovery Studio Visualizer 관찰

BIOVIA Discovery Studio Visualizer 2025 Client 25.1.0에서 실제 관찰한 것은 4종 5개 배좌이다. 에틸 4-니트로벤조에이트 배좌 1·2, 벤조카인 배좌 1, 4-아미노벤조산 배좌 4, 에탄올 배좌 2가 이에 해당한다. 에틸 4-니트로벤조에이트 배좌 1은 N10–H21 거리 2.684 Å, C8–C9–N10 각도 119.102°가 직접 측정되었다. 배좌 2는 N10–H21 거리 2.682 Å, C8–C9–N10 각도 119.062°가 측정되었다. 이 두 측정은 Visualizer Measure 도구의 DistanceMonitor/AngleMonitor 표에서 얻은 이전 실제 측정값이다[D7].

![Discovery Studio Visualizer 실제 화면: 에틸 4-니트로벤조에이트, PM7 배좌 1, 분자 내부 N10–H21 거리 2.684 Å](assets/visualizer-route01-conf1-distance.png)

![Discovery Studio Visualizer 실제 화면: 같은 배좌, 분자 내부 C8–C9–N10 각도 119.102°](assets/visualizer-route01-conf1-angle.png)

4-아미노벤조산 배좌 4는 카복실기 원자 C6/O7/O8이 표시된 고립 분자 화면으로 관찰되었다. 에탄올 배좌 2는 고립 에탄올 화면으로 관찰되었으며, 4-아미노벤조산과 함께 배치하지 않았다. 4-아미노벤조산 배좌 4의 다른 방향 화면은 강체 회전한 표시 사본이며 새 배좌가 아니다. 이 화면들은 고립 분자 내부의 정성적 노출/가림 관찰로만 설명한다[D7].

![Discovery Studio Visualizer 실제 화면: 4-아미노벤조산, PM7 배좌 4, 고립 분자; 카복실기 원자 C6/O7/O8](assets/visualizer-route05-paba-conf4.png)

![4-아미노벤조산 PM7 배좌 4의 다른 방향 화면; 강체 회전한 표시 사본이며 새 배좌가 아님](assets/visualizer-route05-paba-edge.png)

![Discovery Studio Visualizer 실제 화면: 고립 에탄올 PM7 배좌 2; 4-아미노벤조산과 함께 배치하지 않음](assets/visualizer-route05-ethanol-conf2.png)

Visualizer 관찰의 범위는 고립 분자 구조에만 해당한다. 서로 다른 반응물 사이의 접근 거리나 공격각은 측정하지 않았다. 반응물 쌍을 함께 배치하지 않았으므로 반응물 접근을 측정했다고 쓰지 않는다. 여러 방향 화면은 단일 분자의 투영에서 본 정성적 노출/가림으로만 설명한다. 구조 정렬·고정 회전 복사본은 새 배좌가 아니다. Visualizer 정적 구조로 활성화 장벽, 반응 속도, 합성 성공이나 수율을 확정하지 않는다[D7].

### 6.4 하네스 비교

OpenCode와 Pi Coding Agent는 같은 skill, 입력 자료, Solar Pro 4 snapshot, temperature 0, reasoning `none`, `max_tokens=10000`, 도구 비활성화 설정으로 각각 1회 성공한 사례이다. OpenCode 실행 ID는 `opencode-trial-02`, Pi 실행 ID는 `pi-trial-02`이며, 둘 다 HTTP 200으로 완료되었다. 실제 요청 페이로드는 시스템/사용자 메시지 래퍼가 바이트 단위로 같지 않았다. OpenCode는 시스템 메시지 1,348 B, 사용자 메시지 199,764 B를 보냈고, Pi는 각각 585 B, 199,832 B를 보냈다. 사용자 메시지의 일부 차이는 첨부 파일 래퍼에서 왔고, 시스템 프롬프트 래퍼도 달랐다. 따라서 동일한 자료와 설정을 유지했지만, 하네스 자체의 system framing은 비교 변수로 남는다[D8].

내용 비교에서 OpenCode 초안은 타깃, 선정 경로 3개, 경로 점수·수율, MOPAC 작업 수렴, EPI 상태, Visualizer 측정 범위를 제공 근거와 대체로 맞췄지만, EPI Suite의 구체적 MP/BP 추정값과 MOPAC 개별 에너지·결합 길이/전하 값이 없고 출처 URL도 없다. 또한 하네스 비교를 “도구 실행 미승인/미구현”이라고 적었는데, 이는 입력 번들의 오래된 상태에 따른 것이다. Pi 초안은 반응 SMILES, 단계별 조건·수율, 점수와 추가 분석을 더 구체적으로 옮겼고 주요 수치도 근거와 맞지만, 추가 분석 상태를 앞뒤 다르게 서술했다. 2절에서 MOPAC·EPI·Visualizer가 준비/미실행이라고 쓴 뒤 5절에서 실제 계산·조회·측정 결과를 자세히 기술한다. 또한 “Visualizer 관찰을 접근성·차폐 논의에 쓸 수 있다”는 문구는 실제로 측정한 분자 내부 거리·각만으로 외부 반응물 접근성을 논할 수 있는 것처럼 읽힐 수 있어 범위를 좁혀야 한다[D8][D3][D5][D6][D7][D5][D6][D7].

이 두 실행은 각 하네스를 한 번씩 실행한 사례 비교이며, 하네스 일반 성능의 우열을 입증하지 않는다. 사실 일치, 근거 인용, 필수 내용, 읽기 쉬움, 누락과 과장을 중심으로 비교했고, 토큰·시간·비용은 보조 지표이다. 사례 1회씩은 일반 성능 우위를 증명하지 않는다[D8].

## 7. 종합 결론 및 실험 전 확인 목록

### 7.1 조건부 경로 우선순위

현재 근거에서는 route-01을 먼저 문헌과 시약 정보를 확인할 후보로, route-02를 단일 단계 대체 경로로, route-05를 단계 수와 중간체 준비를 비교하기 위한 비교 경로로 본다. [2][5][6][8][D1][D4] 이 우선순위는 구조 변환의 단계 수와 조건 후보 출력의 비교 용이성에 근거한 것이며, 단계별 예측 수율만으로 선택한 것이 아니다. route-01은 한 단계에서 방향족 니트로기가 아미노기로 바뀌고 에틸 에스터가 유지되는 구조 변화가 분명하며, 단일-stage 비교로 조건 후보를 살펴보기 쉽다. route-02는 다른 단일 단계 경로로서, `Cl` 토큰의 정체와 반응 맥락을 별도로 확인해야 한다. route-05는 2단계 경로이며, step-01은 아세트산에서 에탄올로의 모델 경로 가장자리이므로 실제 준비·검증 여부와 별개로 단계 수와 전구체 준비를 비교하는 용도로만 유지한다.

이 우선순위는 최적 경로나 실험 권고가 아니다. route-01의 구조 변환 자체는 Organic Syntheses Procedure 1과 US Patent 3,037,046 Example IV에서 직접 수행된 반응으로 확인되므로, “구조적으로 가능성이 확인되지 않은 가상 변환”이 아니라 실제 문헌과 일치하는 변환이다. 다만 이 문헌 일치는 AI가 조건을 완성했다는 뜻이 아니며, Parrot rank 1의 수소원 누락, rank 4의 수소 토큰 포함과 순위 차이, 그리고 두 후보 모두 온도·시간·압력 부재는 모델 출력과 문헌 조건을 분리해 읽어야 함을 보여준다. [18][19][D9] 판단을 바꿀 수 있는 근거로는 실제 문헌의 반응 조건, 시약·촉매·환원제의 정체성, 용매·농도·염·수분 상태, 압력/분위기 조건, 그리고 적용 범위가 확인된 수율 데이터가 있다. 예측 수율은 반응 구조만 입력한 Yield-BERT의 단계별 값이며, 실험 수율이 아니다. [6][D1][D4] [5]

추가 분석은 각각 제한된 범위로만 해석한다. MOPAC PM7 계산은 기체상 고립 분자의 기하 최적화(25/25 수렴)이며 반응 energetics가 아니다. [D5] EPI Suite는 순물질의 녹는점·끓는점 추정 및 참고 레코드를 제공하지만, 반응 혼합물의 석출·기화·반응 상태를 확정하지 않는다. [D6] Discovery Studio Visualizer는 실제 내부 측정 거리·각도와 단일 분자의 정성적 노출/가림만 기록했으며, 서로 다른 반응물 사이의 접근 거리나 공격각은 측정하지 않았다. [D7] OpenCode와 Pi는 각각 한 번씩 초안을 생성한 사례 비교이며, 일반 성능의 우열 증거가 아니다. [D8] [10]

동일 표적(benzocaine, SMILES `CCOC(=O)c1ccc(N)cc1`, 분자식 C₉H₁₁NO₂)에 대한 로컬 종단간 재실행(run ID `benzocaine-live-repro-20261105-01`)에서는 경로 탐색, Parrot 조건, rxn_yields 수율의 세 단계가 모두 성공했고, 경로 12개, 조건 예측 14건, 수율 단계 20건이 기록되었다. 경로/단계 매핑은 20/20 조건 매핑으로 통과했으며, route/reaction/candidate/yield 출력은 이전 실행과 동일했다. 다만 검색 시간은 이전 8.43 s에서 이번 15.46 s로 달라졌고, 그 원인은 분리되지 않아 런타임 부하·캐시 변동 가능성으로만 잠정 해석한다. 이 재실행은 새로운 분자나 새로운 PC를 테스트하지 않았으며, 동일 PC에서의 benzocaine 재실행이 다른 분자나 다른 환경으로의 이식성을 입증하지는 않는다. [D10] [5][6][D1]

실험 전 확인해야 할 사항으로는 문헌 조건의 온도·시간·압력·수소 소비 당량, 촉매 제형·담지체·산화상태, 용매 조성(특히 95% alcohol의 물 함량), 염·수분·농도 조건, 그리고 수율 정의(분리 수율인지 분석 수율인지, 전환율인지)가 있다. 이 보고서는 가격과 실험 난이도를 다루지 않으며, 조건 후보 점수나 예측 수율을 실험 성공률이나 검증된 전체 경로 수율로 해석하지 않는다. [2][5][6][8][D1][D4][D10]

### 7.2 추가 분석의 기여와 한계

MOPAC 23.2.5 PM7 계산은 25/25개의 고립 중성 단일항 분자가 수렴한 결과를 제공한다. 이 계산은 용매, 촉매, 반응 상대, 전이상태를 포함하지 않으므로, 반응 중심 구조에 대한 계산상 기하·부분전하·결합거리 정보를 제공할 수는 있지만, 반응성 기작, 활성화 장벽, 반응 속도, 반응 성공, 수율을 말하지는 못한다. 예를 들어 ethyl 4-nitrobenzoate의 선택된 니트로 N–O 거리는 각각 1.2198 Å, 니트로 N 부분전하는 +0.6117이며, benzocaine의 아릴 C–N 거리는 1.3772 Å, 아미노 N 부분전하는 -0.6321로 계산되었다. 이 값들은 고립 분자의 계산상 구조·인구(population) 값이며, 서로 다른 분자식·조성의 총에너지를 비교해 안정성이나 반응성 순위를 매기는 데 쓰지 않는다. 진동수 분석이 없으면 최적화 구조가 진정한 국소 최소점이라고 단정하지 않는다. 이 내용은 [D5]와 방법 [10][11]에 근거한다.

EPI Suite Web/MPBPWIN 추정은 순물질에 대한 모델 추정값과 데이터베이스/문헌 레코드를 구분해야 한다. benzocaine의 추정 녹는점은 66.17 °C, 끓는점은 279.90 °C이며, benzocaine에 대한 EPI Unified 정확 구조 레코드는 없다. 4-aminobenzoic acid는 추정 MP 94.08 °C, BP 307.70 °C, ethanol은 추정 MP -87.84 °C, BP 65.11 °C로 제시된다. 한편 ethanol의 데이터베이스 BP 78.2 °C는 출처가 충분하지 않아 직접 실험값으로 부르지 않는다. 서비스 상태가 저하(degraded)되었던 점도 함께 기록한다. 순물질의 녹는점·끓는점만으로 반응 혼합물의 용해, 석출, 기화, 반응 상태를 확정하지 않는다. 이 내용은 [D6]과 방법 [12][13]에 근거한다.

Discovery Studio Visualizer 25.1.0에서는 4종 5개 배좌를 관찰하였다. 관찰 대상은 ethyl 4-nitrobenzoate 배좌 1·2, benzocaine 1, PABA 4, ethanol 2이다. 실제 분자내 측정은 ethyl 4-nitrobenzoate에만 수행되었으며, N10–H21 거리는 2.684 Å과 2.682 Å, C8–C9–N10 각도는 119.102°와 119.062°로 기록되었다. 여러 방향 화면은 단일 분자의 투영에서 본 정성적 노출/가림 관찰에만 사용한다. 서로 다른 반응물 사이의 접근 거리나 공격각은 측정하지 않았다. Visualizer의 정적 구조로 활성화 장벽, 반응 속도, 합성 성공, 수율을 확정하지 않는다. 이 내용은 [D7]에 근거한다.

여러 분석을 함께 제시하더라도, 각각은 자신의 증거 범위 안에서만 기여한다. MOPAC은 고립 분자 기하·부분전하·결합거리의 계산상 값을, EPI Suite는 순물질 물성의 추정값과 데이터베이스 레코드를, Visualizer는 단일 분자의 정성적 관찰과 제한된 분자내 측정을 제공한다. 이 결과들을 연결해도 반응 성공이나 전체 수율이 검증된 것은 아니다[D5][D6][D7].

### 7.3 경로별·단계별 실험 전 확인 목록

아래 항목은 현재 출력에서 확인되지 않은 정보를 미제공 상태로 남겨 둔 체크리스트이다. 값을 임의로 채우지 않는다.

- route-01/step-01: 환원제 또는 수소 공급원(hydrogen source)이 모델 슬롯에서 비어 있거나 rank 4의 `[H][H]`처럼 모호하게 제시된다. 촉매 identity는 `[Pd]`로 제시되지만, 실제 촉매 종류·담체·부하량·사용 형태는 확인되지 않았다. 온도·시간·당량·압력/분위기, 조건 수율은 미제공이다. 반응물 용해·농도·염/수화 상태·수분, work-up·생성물 분리·결정화 자료도 미제공이다. [D1]
- route-02/step-01: reagent1의 `Cl`은 모호한 모델 토큰이며, HCl이나 다른 염소 종으로 재해석하지 않는다. 촉매 슬롯은 비어 있고, 용매는 `CCO`로 제시된다. 온도·시간·당량·압력/분위기, 조건 수율은 미제공이다. 반응물·생성물의 용해·농도·염/수화 상태·수분, work-up·분리·결정화 자료도 미제공이다.
- route-05/step-01: 아세트산에서 에탄올로의 변환은 모델 경로 가장자리이며, 실제 준비·검증 여부가 확인되지 않았다. 촉매 슬롯은 비어 있고, solvent1은 `C1CCOC1`, reagent1은 `[Al+3].[H-].[H-].[H-].[H-].[Li+]`로 제시된다. 이 시약 토큰의 실험 역할도 검증되지 않았다. 온도·시간·당량·압력/분위기, 조건 수율은 미제공이다.
- route-05/step-02: solvent1 `CCO`, solvent2 빈 값, reagent1 `CCOCC`, reagent2 `FB(F)F`가 모델 슬롯으로 제시된다. 온도·시간·당량·압력/분위기, 조건 수율은 미제공이다. 반응물·생성물의 용해·농도·염/수화 상태·수분, work-up·분리·결정화 자료도 미제공이다.
- 공통: 세 경로 모두 온도·시간·당량·압력/분위기·조건 수율이 공급되지 않았다. 모든 수율 예측값은 반응 구조만 입력한 Yield-BERT의 단계별 예측이며, 적용 범위는 `not_assessed`이다. 단계별 예측값을 곱하거나 합산해 전체 수율로 쓰지 않는다.

## 8. 재현 방법

이 보고서의 예측 결과는 benzocaine-live-20261031-04 실행에서 생성되었다. 경로 탐색 결과는 이전 실행(benzocaine-live-20261031-03)의 결과를 재사용했고, 조건 추론은 이번 실행에서 수행되었다. 수율 예측도 이전 실행 결과를 재사용했다. 따라서 이번 실행에서 세 번의 신선한 추론을 모두 새로 수행했다고 주장하지 않는다. benzocaine-live-20261031-03은 원래의 성공적인 AiZynthFinder 경로 실행이며, benzocaine-live-20261031-04는 대표 결과 묶음으로, 그 routes.json은 -03과 바이트 동일(SHA-256 a5256cab92771f695bff3b594e7a29ff0193f343923a51090e9df6da7dab6e63)하다. 성공적인 Parrot 조건과 Yield-BERT 예측은 -04에 담겨 있으며, -03의 Parrot 조건 파일은 실패하여 성공적인 조건 참조가 아니다. benzocaine-live-repro-20261105-01은 동일 PC에서 제출 코드를 사용한 전체 재실행으로, 경로는 -03과, Parrot 조건 및 Yield-BERT 출력은 -04와 비교한다. 경로 실행 간 자산 해시는 일치한다: ONNX 모델 uspto_model.onnx SHA-256 bd0a3cb74cd7068de474c8fb789a00a66bc42c75636d66510ccac585ebe928f8, 압축 반응-템플릿 아카이브 uspto_templates.csv.gz SHA-256 a4f1945e90cfa195538320833d68aed38f14e2fcc2f8afb5d958bc920edcafbe, ZINC 출처 SHA-256 99d39a6f807c3e815487500bafc2b4a9dc66a31af189e3b1776874fb0d4a188d, 그리고 26개 파생 stock 버킷 크기/해시 항목 전체. 반면 구체화된 구성 JSON 바이트 해시는 서로 다르다(-03 ef98c6f2fa1540fb59b41837afc33b550d7c5800fa16e71e50ebc3ec7edfc6bd, -05 9cf3ea6f9da7d0e1c5bfd942c74fa551a87eb70ea36bc7b48662a9e4d31d2563). 기록된 구성 객체는 경로 구분자 정규화 후 일치하며, 역사적 임시 JSON은 보존되지 않아 정확한 바이트 수준 원인은 unresolved이다. 역사적 구성-템플릿 해시는 기록되지 않아 비교할 수 없다. 원본 reproduction-validation.json에는 원시 자산과 모순되는 두 개의 거짓 해시 플래그가 있으며, 원본을 보존한 채 원시 증거에서 별도로 재계산한 corrected validation이 통과되었다. 예측 동일성과 자산 해시 동일성은 구분하여 유지한다. 재실행은 동일 PC의 동일 분자에만 해당하며, 다른 분자나 다른 PC는 시험하지 않았다. [D10]

구조 그림은 `draw_structures.py`로 생성했고, 경로 그림은 `draw_routes.py`로 생성했다[D1]. 조건 추론은 `predict_conditions.py --model parrot`로 수행했다[D1]. 증거 번들은 `build_evidence.py`로 조립했다[5][D1]. 각 명령은 재현성 매니페스트에 기록되어 있다[16].

이번 실행에서 재사용한 과거의 모델 환경과 체크포인트는 읽기 전용으로 활용되었으며, 다른 컴퓨터에서 재현하려면 문서화된 휴대용 런타임 구성에 따라 별도로 준비해야 한다[16].

MOPAC은 23.2.5 버전을 사용했고, 실행 종류는 PM7 기체상 고립 분자 기하 최적화이다[10][16][D5]. EPI Suite는 EPI Suite Web 베타 원격 엔드포인트를 사용했고, 로컬 설치는 수행하지 않았다[13][16][D6]. Discovery Studio Visualizer는 25.1.0 버전을 사용했다[16][D7].

수율 모델의 정규화 복원은 rxn_yields 훈련 스크립트에서 사용한 체크포인트와 훈련 통계를 기준으로 수행되었으며, 적용 범위 평가 여부는 별도로 명시한다[6][8][D1][D4]. USPTO 데이터 탐색 노트북은 [15]이다. DRFP 저장소는 [7]이다.

문서 변환 검증과 새 물질 추론 검증은 구분한다. 이 보고서는 저장된 예측을 이용해 작성한 문서이며, 새 물질의 새 추론을 수행한 기록이 아니다[16].



## 9. 참고문헌 및 프로젝트 증거 파일

### 9.1 참고문헌

1. Benzocaine identity — https://pubchem.ncbi.nlm.nih.gov/compound/2337
2. aizynthfinder — https://github.com/MolecularAI/aizynthfinder
3. SynthEx official repository (source availability status) — https://github.com/schwallergroup/synthex
4. askcos — https://gitlab.com/mlpds_mit/askcosv2/context_recommender
5. parrot — https://github.com/wangxr0526/Parrot
6. rxn_yields — https://github.com/rxn4chemistry/rxn_yields
7. drfp — https://github.com/reymond-group/drfp
8. Yield normalization code — https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/training_scripts/launch_uspto_training.py
9. Training data — https://ibm.ent.box.com/v/uspto-yields-data
10. MOPAC PM7 manual — https://openmopac.net/Manual/pm7.html
11. MOPAC geometry convergence/GNORM — https://openmopac.net/Manual/precision.html
12. EPA EPI Suite and Web notice — https://www.epa.gov/tsca-screening-tools/epi-suitetm-estimation-program-interface
13. EPI Suite Web — https://episuite.dev/EpiWebSuite/#/
14. Australian Government acetic acid property cross-check — https://www.dcceew.gov.au/environment/protection/npi/substances/acetic-acid-ethanoic-acid
15. rxn_yields USPTO data exploration notebook — https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/nbs/02_uspto_data_exploration.ipynb


16. Benzocaine prediction and analysis execution records — `evidence-run/manifest.json`, `evidence-run/reproducibility-manifest.json`, and `results/benzocaine-live-20261031-04/manifest.json`.
17. 강의자료, 「02_반응과_전자이동_개선_v2」 — 수업 LMS에서 확보; PDF 80–81, 83–84, 90–95. 공개 패키지의 확보 안내: `evidence-run/course-material-acquisition.md`.
18. Adams & Cohen, "Ethyl p-Aminobenzoate [Benzocaine]," Organic Syntheses 8 (1928), 66 — DOI https://doi.org/10.15227/orgsyn.008.0066; Procedure 1, printed p. 66 / PDF p. 2.
19. US Patent 3,037,046, "Benzocaine Process," Example IV, printed p. 3 / scan PDF p. 2 — https://patents.google.com/patent/US3037046A/en

### 9.2 프로젝트 증거 파일
아래 증거 목록은 본 보고서에서 인용한 프로젝트 파일과 외부 자료를 정리한 것이다.

- [D1] `evidence-run/report-evidence.json`
- [D2] `evidence-run/additional-analysis-status-current.json`
- [D3] `evidence-run/evidence-conflict-resolution.md`
- [D4] `evidence-run/validation_notes.json`
- [D5] `evidence-run/mopac-results-interpretation.md`
- [D6] `evidence-run/epi-analysis.md`
- [D7] `evidence-run/visualizer-accessibility-observations.md`, `evidence-run/visualizer-observation-index.csv`, `evidence-run/visualizer-measurements.csv`
- [D8] `evidence-run/harness-trial-02-comparison-evaluation.md`, `evidence-run/harness-trial-02-status.json`, `evidence-run/harness-trial-02-budget.json`, `evidence-run/reproducibility-manifest.json`
- [D9] `evidence-run/literature-validation/route-01-primary-comparison-20261114/literature-comparison.md`, `comparison.json`, `validation.json`, `source-integrity.json`, `source-acquisition.md`; raw route/condition/yield comparison inputs are under `evidence/`
- [D10] `evidence-run/rerun/benzocaine-live-repro-20261105-01/reproduction-validation-corrected.json` (정정 검증본; SHA-256 `7087c15ddeabf85006934214fb148f3b3a6bbc173b69502b011a9b3517cef287`); `evidence-run/rerun/benzocaine-live-repro-20261105-01/reproduction-validation-original-conflicting.json` (상충 원본 보존; SHA-256 `63ab33c238fda07120f87ff9e4024195b12bb68cc689565539f83112dd7db7a8`); `evidence-run/rerun/benzocaine-live-repro-20261105-01/verification.json`; `evidence-run/rerun/benzocaine-live-repro-20261105-01/manifest.json`

## 부록: 현재 증거와 분석 상태 요약

현재 증거 번들은 2026-11-03에 조립되었으며, 경로·조건·수율 예측은 완료되었으나 실험적 검증은 수행되지 않았다. MOPAC은 25/25 PM7 고립 분자 최적화가 수렴했고, EPI Suite는 Web 응답이 수신되었으나 서비스 상태가 저하(degraded)로 기록되었다. Discovery Studio Visualizer는 실제 화면 관찰이 수행되었으나, 반응물 쌍 접근 거리·공격각 측정은 수행되지 않았다. 하네스 비교는 OpenCode와 Pi 각각 1회 성공 사례로 완료되었고, 일반 성능 순위는 지원되지 않는다. 최종 보고서는 이 증거를 바탕으로 Solar Pro 4가 작성했으며, 예측·관측·측정의 구분과 미해결 한계를 함께 기술했다[D2][D5][D6][D7][D8].

