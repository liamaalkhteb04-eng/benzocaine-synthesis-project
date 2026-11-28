# 처리 전 원문·기술 기록 보존

<a id="c03"></a>
## C03 route01 조건·수율 설명

**템플릿·분류 정보.** 이 단계의 템플릿 해시는 `664f7756f7526ad6c07e82dd3b3c15f7aabccbc99837dd22105068a2cfc385b5`이며, 분류는 “0.0 Unrecognized”로 기록되어 있다[D1]. 라이브러리 출현 횟수는 33350, 정책 확률은 0.4224, 정책 이름은 uspto, 템플릿 코드는 17064이다[D1]. 템플릿은 아미노기 관련 변환을 기술하는 형태이며, 이 보고서에서는 템플릿이 제시한 절단(disconnection) 방향을 그대로 읽되, 생략된 작용제가 재구성되지 않았다는 단서를 함께 둔다[D1].

**조건 후보.** Parrot은 이 반응에 대해 15개 후보를 반환했다[D1]. 상위 4개 후보의 주요 슬롯은 다음과 같다.

- rank 1: catalyst1 `[Pd]`, solvent1 `CCO`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −1.7008
- rank 2: catalyst1 `[Pd]`, solvent1 `CO`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −2.0482
- rank 3: catalyst1 `[Pd]`, solvent1 `CCOC(C)=O`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −2.7931
- rank 4: catalyst1 `[Pd]`, solvent1 `CCO`, solvent2 `""`, reagent1 `[H][H]`, reagent2 `""`, sequence_score −2.8787

상위 후보들은 catalyst1에 Pd 원자 토큰을, solvent1에 에탄올 계열 또는 메탄올 계열 토큰을 배치하는 경향을 보인다[D1]. `solvent1=CO`는 단일 구조 토큰이며, 검증된 구조 해석은 메탄올(methanol, CH₄O, PubChem CID 887)이다[D12]. 이 슬롯은 화학적 역할을 해석할 수는 있지만, 모델이 출력한 값 자체가 실험 조건을 검증했다는 뜻은 아니다. 다만 `[Pd]`는 단일 Pd 원소 토큰이며 실제 촉매 제형·담지체·산화상태·실물 형태를 확인해 주지 않는다. 또한 이 단계의 temperature, time, yield_percent는 모두 null이며, temperature_status는 `not_provided_by_checkpoint`로 기록되어 있다[D1]. 즉 온도·시간·당량·압력은 이번 조건 체크포인트에서 제공되지 않았다. 따라서 각 조건 슬롯의 수치적 운영 조건은 `NOT SUPPLIED`이다.

**수율 예측.** rxn_yields는 이 반응 SMILES에 대해 raw_value 0.46616947650909424, 수율 82.95371431744555%를 반환했다[D1]. 출력 척도는 standardized_fraction이며, 상태는 `predicted_not_validated`이다. 입력 토큰 수는 46, 최대 입력 토큰은 300, 입력 절단은 false이며, conditions_in_input은 false이다[D1]. 즉 이 수율 예측은 반응 구조만 입력했고 조건 슬롯을 넣지 않았으며, 적용 가능성(applicability)도 평가되지 않았다. 따라서 이 값은 특정 실험 조건에서의 실험 수율이 아니라, 반응 SMILES에 대한 모델 예측값이다[6].

<a id="c04"></a>
## C04 route02 경계·조각 결합

**구조 변화.** 이 단계는 N-아세틸기가 제거되어 아미노기가 드러나고, 에틸 에스터는 유지되는 변환이다[D1]. 반응 SMILES는 `CCOC(=O)c1ccc(NC(C)=O)cc1 >> CCOC(=O)c1ccc(N)cc1`이다[D1]. 저장된 매핑 반응 SMILES에서는 아세틸 탄소 쪽 연결(atom map 13–14, 13–15)이 끊어지고, 아미노 질소(atom map 10)의 수소 수가 1에서 2로 늘어나는 그래프 차이로 기록된다[D13]. 이 역시 저장된 구조·매핑의 차이이며, 실험적 원자 추적이나 단계별 메커니즘 증명이 아니다.

<a id="c05"></a>
## C05 route02 조건·선택성 한계

**템플릿·분류 정보.** 템플릿 해시는 `8063032398e59c77d82569a4231c9d8f1dc9cd333085943b3f9ae7b5eafd5071`, 분류는 “0.0 Unrecognized”, 라이브러리 출현 횟수는 1668, 정책 확률은 0.0118, 정책 이름은 uspto, 템플릿 코드는 21399이다[D1]. 이 템플릿은 아미노기 관련 절단 방향을 기술하며, route-01과 마찬가지로 생략된 작용제가 재구성되지 않았다는 단서가 붙어 있다[D1].

**조건 후보.** Parrot은 이 반응에 대해서도 15개 후보를 반환했다[D1]. 상위 3개 후보의 주요 슬롯은 다음과 같다.

- rank 1: catalyst1 `""`, solvent1 `CCO`, solvent2 `""`, reagent1 `Cl`, reagent2 `""`, sequence_score −1.3240
- rank 2: catalyst1 `""`, solvent1 `Cl`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −2.6605
- rank 3: catalyst1 `""`, solvent1 `CCO`, solvent2 `""`, reagent1 `[Na+].[OH-]`, reagent2 `""`, sequence_score −3.2929

이 단계의 상위 후보들은 catalyst1이 비어 있는 경우가 많고, solvent1과 reagent1에 염소 계열, 에탄올 계열, 염기 계열 토큰이 섞여 나타난다[D1]. slot이 빈 값인 경우는 “모델 출력 미제공”으로 읽으며, 실험에서 해당 성분을 사용하지 않았다는 뜻이 아니다.

이 단계 역시 temperature, time, yield_percent는 null이고 temperature_status는 `not_provided_by_checkpoint`이다[D1]. 따라서 운영 온도·시간·당량·압력은 `NOT SUPPLIED`이다.

**수율 예측.** rxn_yields는 이 반응 SMILES에 대해 raw_value 0.21513395011425018, 수율 77.69549187778327%를 반환했다[D1]. 출력 척도는 standardized_fraction, 상태는 `predicted_not_validated`, 입력 토큰 수는 47, conditions_in_input은 false이다[D1]. 이 값 역시 반응 구조만 입력한 예측이며, 특정 실험 조건에서의 실험 수율이 아니다[6].

<a id="c06"></a>
## C06 미검증 공급 질의의 조건·수율

**템플릿·분류 정보.** 템플릿 해시는 `c42f96a0658c03bc12dc20efce06e66daaeccc675d73631eea24ea610a7227b8`, 분류는 “0.0 Unrecognized”, 라이브러리 출현 횟수는 3921, 정책 확률은 0.0915, 정책 이름은 uspto, 템플릿 코드는 32658이다[D1].

**조건 후보.** Parrot은 이 반응에 대해 15개 후보를 반환했다[D1]. 상위 3개 후보의 주요 슬롯은 다음과 같다.

- rank 1: catalyst1 `""`, solvent1 `C1CCOC1`, solvent2 `""`, reagent1 `[Al+3].[H-].[H-].[H-].[H-].[Li+]`, reagent2 `""`, sequence_score −1.8565
- rank 2: catalyst1 `""`, solvent1 `C1CCOC1`, solvent2 `""`, reagent1 `O`, reagent2 `[Al+3].[H-].[H-].[H-].[H-].[Li+]`, sequence_score −2.7974
- rank 3: catalyst1 `""`, solvent1 `C1CCOC1`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −2.9943

이 단계의 상위 후보에는 용매로 THF 계열 토큰(`C1CCOC1`)이 자주 등장하고, 시약 슬롯에 리튬 알루미늄 수소화물 계열로 읽힐 수 있는 분리된 이온 표현(`[Al+3].[H-].[H-].[H-].[H-].[Li+]`)이 나타난다[D1]. 다만 이 표현은 정의된 순수 중성 유기 화합물로서의 물질이라기보다 분리된 이온 표현이며, 실제 시약 제형·당량·용매 조성·작업 조건을 확인해 주지 않는다. 이 단계도 temperature, time, yield_percent는 null이고 temperature_status는 `not_provided_by_checkpoint`이다[D1]. 따라서 운영 조건은 `NOT SUPPLIED`이다.

**수율 예측.** rxn_yields는 이 반응 SMILES에 대해 raw_value 0.2100452482700348, 수율 77.58890327412914%를 반환했다[D1]. 출력 척도는 standardized_fraction, 상태는 `predicted_not_validated`, 입력 토큰 수는 13, conditions_in_input은 false이다[D1][6]. 이 값은 모델이 forward SMILES `CC(=O)O>>CCO`에 대해 출력한 예측값이며, route-05의 실제 ethanol 공급 수율이나 benzocaine 합성 단계 수율로 비교할 수 없다[D14].

<a id="c07"></a>
## C07 에스터화 후보·McMaster 문헌

**템플릿·분류 정보.** 템플릿 해시는 `bf6bd9047791f3252d0082f87523bda9bf230f930fe417ac7de9fa8c502cbf89`, 분류는 “0.0 Unrecognized”, 라이브러리 출현 횟수는 6214, 정책 확률은 0.1681, 정책 이름은 uspto, 템플릿 코드는 31869이다[D1]. 이 템플릿은 에스터화 방향의 절단 형태를 기술하며, 생략된 작용제가 재구성되지 않았다는 단서가 붙어 있다[D1].

**조건 후보.** Parrot은 이 반응에 대해 15개 후보를 반환했다[D1]. 상위 3개 후보의 주요 슬롯은 다음과 같다.

- rank 1: catalyst1 `""`, solvent1 `CCO`, solvent2 `""`, reagent1 `CCOCC`, reagent2 `FB(F)F`, sequence_score −2.1755
- rank 2: catalyst1 `""`, solvent1 `CCO`, solvent2 `""`, reagent1 `CC(=O)Cl`, reagent2 `""`, sequence_score −2.3472
- rank 3: catalyst1 `""`, solvent1 `O=S(=O)(O)O`, solvent2 `""`, reagent1 `""`, reagent2 `""`, sequence_score −2.6159

route-05/step-02의 반응 `CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1`에 대해 Parrot이 제시한 원시 후보는 총 15개이며 [D1], 이어지는 설명 문단은 그중 rank 1, rank 2, rank 3만을 각각 별도의 슬롯 구성으로 다룬다. rank 1은 catalyst1=``, solvent1=`CCO`, solvent2=``, reagent1=`CCOCC`, reagent2=`FB(F)F`이고, rank 2는 catalyst1=``, solvent1=`CCO`, solvent2=``, reagent1=`CC(=O)Cl`, reagent2=``이며, rank 3은 catalyst1=``, solvent1=`O=S(=O)(O)O`, solvent2=``, reagent1=``, reagent2=``이다 [D1]. 구조 토큰의 물질명 대응은 다음과 같이 확인된다 [D12]. `CCO`는 에탄올(ethanol, C2H6O; PubChem CID 702)이고, `CCOCC`는 다이에틸 에터(diethyl ether/ethoxyethane, C4H10O; PubChem CID 3283)이며, 이는 에틸 아세테이트 구조가 아니다. 또한 route-05/step-02의 15개 후보 슬롯 어디에도 에틸 아세테이트 구조 토큰 `CCOC(=O)C` 또는 `CCOC(C)=O`는 존재하지 않는다. `FB(F)F`는 삼불화붕소(boron trifluoride, BF3; PubChem CID 6356)이고, `CC(=O)Cl`은 아세틸 클로라이드(acetyl chloride; PubChem CID 6367)이며, `O=S(=O)(O)O`는 이 근거 묶음에서 이름 확인 자료가 없으므로 원시 토큰으로만 남긴다. 모델이 예측한 슬롯은 실험에서 실제 사용된 시약·용매·촉매 역할을 입증하는 값이 아니므로, 구조 정체성과 실제 실험 역할은 서로 다른 개념으로 다루어야 하며 실험에서의 사용 여부는 확인되지 않았다.

`FB(F)F`는 삼불화붕소(boron trifluoride, BF₃)로 읽힐 수 있으며, MPBPWIN의 유기화합물 범위와는 별도로 취급해야 한다[D12][12][D6].

**수율 예측.** rxn_yields는 이 반응 SMILES에 대해 raw_value 0.31552639603614807, 수율 79.79832496878097%를 반환했다[D1]. 출력 척도는 standardized_fraction, 상태는 `predicted_not_validated`, 입력 토큰 수는 43, conditions_in_input은 false이다[D1][6].

<a id="c08"></a>
## C08 §4.3 모델 방법·공식 평가 누락

rxn_yields[6]는 반응 SMILES 기반 수율 예측에 사용되었다[D1]. 이번 실행에서 yields는 success로 기록되어 있으며, 선택된 단계들에 대해 각각 예측값이 반환되었다[D1]. 예측값은 standardized_fraction 척도에서 recovered된 통계량으로 백분율로 변환되었다[D1].

정규화[8][9]에는 훈련 데이터의 평균 0.7318926847478698, 표준편차 0.20946128682168402가 사용되었고, 표준편차는 ddof=1로 계산되었다[D1]. 변환식은 `yield_percent = 100 * (raw_z * training_yield_std + training_yield_mean)`이다[D1]. 이 통계량은 USPTO 그램 규모 무작위 분할(train rows)에서 recovered된 것이며, 전역 데이터셋 대체 통계량이 아니다[D1]. 또한 정규화 계산이 정확하다는 것이 모델 정확도를 검증한다는 뜻은 아니다[D4].

<a id="c09"></a>
## C09 하네스 입력 차이의 본문 반영

OpenCode와 Pi Coding Agent에 대해 각각 1회씩 성공 응답(HTTP 200)을 받은 사례 비교가 수행되었다[D8]. 두 하네스는 같은 모델 스냅샷(solar-pro4-260806), temperature 0, reasoning `none`, max_tokens 10000, n=1, 도구 비활성화 조건에서 실행되었다[D8]. 이는 사례 비교이며, 하네스 일반 성능의 우열을 입증하지 않는다[D8].

<a id="c10"></a>
## C10 문헌 수율 병치의 현재 검토 상태

route-01/step-01의 Yield-BERT[6] 예측은 82.95371431744555%이며, 상태는 `predicted_not_validated`, conditions_in_input은 false, applicability는 not_assessed이다[D9][D1]. 이 값은 반응 구조만 입력했고, Org. Synth.의 PtO₂/에탄올/H₂ 또는 특허 Example IV의 Rh/Al₂O₃/벤젠/H₂ 조건을 반영한 수율 예측이 아니다[D9][D1]. [19][D9]

동일한 기질·생성물 변환이라는 점에서 수치의 기술적 병치는 가능하다[D9][D1]. Org. Synth.의 분리 수율 91–100% 범위와 비교하면 예측은 약 8.05–17.05 퍼센트포인트 낮고, 특허 Example IV의 “approximately 100% of theory”와 비교하면 명목상 약 17.05 퍼센트포인트 낮다[D9][D1]. 그러나 이 예의 수율 측정법이 명시적으로 정의되지 않았으므로 확정적인 동일 기준 비교로 해석하지 않는다[D9][D1]. 두 차이는 조건을 맞춘 성능 오차나 실험 예측 잔차가 아니다[D9][D1]. [18][D9][6]

학습 데이터에 해당 Organic Syntheses 절차나 특허 반응이 포함됐는지, 중복 제거·문헌 중복 여부가 어떤지 확인할 수 있는 기록은 이번 자료에 없다[D9][D1]. 따라서 학습 데이터 중복 여부는 미확인이며, 있다고도 없다고도 결론내리지 않는다[D9][D1]. 한 반응 예로 Yield-BERT의 전체 정확도, 조건별 수율, 또는 실제 합성 성공을 입증할 수 없다[D9][D1][6].

<a id="c11"></a>
## C11 우선 검토 근거·낡은 적용성 결론

- Parrot 조건 후보는 실험 조건을 검증하지 않는다. 특히 route-01 상위 후보는 Pd 토큰과 에탄올 계열 용매를 제시하지만, 실제 촉매 제형·환원제·수소압·온도·시간·당량을 확인해 주지 않는다[D1].
- route-01 상위 후보의 `solvent1=CO`는 메탄올(CH₄O)로 검증되며[D12], `CCO`는 에탄올 구조 토큰이다. 이 슬롯들은 화학적 역할을 해석할 수는 있지만, 모델이 출력한 값 자체가 실험 조건을 검증했다는 뜻은 아니다[D1].
- route-05/step-02 상위 후보의 `CCOCC`는 디에틸 에터(C₄H₁₀O)로, `FB(F)F`는 삼불화붕소(BF₃)로 검증된다[D12]. 이 슬롯들은 화학적 역할을 해석할 수는 있지만, 모델이 출력한 값 자체가 실험 조건을 검증했다는 뜻은 아니다[D1].
- Yield-BERT 수율은 실험 수율이 아니며, 조건 입력이 없었고 적용 가능성도 평가되지 않았다[D1][6].
- MOPAC은 고립 분자 기하·생성열·전하·쌍극자만을 제공하며, 반응 장벽·속도·수율·성공의 증거가 아니다[D5][10].
- EPI Suite 추정값과 데이터베이스 기록은 혼합 상평형을 제공하지 않으며, 순수 물질 MP/BP만으로 반응 용액 상태를 확정하지 않는다[D6][12].
- Visualizer는 일부 분자 내부 거리·각도와 정성적 단일 분자 화면만 제공하며, 반응물 접근·공격각·입체장애 장벽·반응 성공·수율을 측정하지 않는다[D7].
- route-05의 첫째 단계는 검색 모델의 경로 간선이며, 실제 순차 합성으로 검증되지 않았다[D1].

<a id="c12"></a>
## C12 표4의 기존 적용성 설명·인용 반영

### 3.4 단계별 조건·수율 값의 표기 원칙

| route_id / step_id | Reaction SMILES (reactants >> product) | Parrot rank 1 (original slots) | Temperature / time / equivalents / pressure | Yield-BERT predicted yield (%) / status |
|---|---|---|---|---|
| route-01 / step-01 [D1] | `CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1` | catalyst1=`[Pd]`; solvent1=`CCO`; solvent2=`""`; reagent1=`""`; reagent2=`""` | temperature=미제공; time=미제공; equivalents=출력 필드 없음; pressure=출력 필드 없음 | 82.95% / predicted_not_validated (conditions_in_input=False) |
| route-02 / step-01 [D1] | `CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1` | catalyst1=`""`; solvent1=`CCO`; solvent2=`""`; reagent1=`Cl`; reagent2=`""` | temperature=미제공; time=미제공; equivalents=출력 필드 없음; pressure=출력 필드 없음 | 77.70% / predicted_not_validated (conditions_in_input=False) |
| route-05 / step-01 [D1] | `CC(=O)O>>CCO` | catalyst1=`""`; solvent1=`C1CCOC1`; solvent2=`""`; reagent1=`[Al+3].[H-].[H-].[H-].[H-].[Li+]`; reagent2=`""` | temperature=미제공; time=미제공; equivalents=출력 필드 없음; pressure=출력 필드 없음 | 77.59% / predicted_not_validated (conditions_in_input=False) |
| route-05 / step-02 [D1] | `CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1` | catalyst1=`""`; solvent1=`CCO`; solvent2=`""`; reagent1=`CCOCC`; reagent2=`FB(F)F` | temperature=미제공; time=미제공; equivalents=출력 필드 없음; pressure=출력 필드 없음 | 79.80% / predicted_not_validated (conditions_in_input=False) |

<a id="c13"></a>
## C13 그림9A/B와 두 배좌 측정 구별

이 값들은 Visualizer의 Measure 도구와 DistanceMonitor/AngleMonitor 표에서 읽은 실제 측정값이다[D7]. 두 배좌에서 nitro N10과 같은 분자 내 ortho H21의 거리는 거의 같고, C8–C9–N10 국소 각도도 유사하다[D7]. 따라서 현재 Visualizer 기록은 선택된 두 PM7 최적화 기하에서 해당 nitro/아릴 주변의 국소 내부 배치가 서로 유사하다는 것까지만 보여 준다. 각도는 아릴 C8–C9 결합과 nitro N10이 이루는 분자 내부 각이며, 반응 공격각이 아니다[D7][10][D5].

<a id="r01"></a>
## R01 표1의 문헌·절 참조 정리

#### 표 1. 대표 경로 요약

| 경로·단계 (전체 단계 수) | 기존 보고서의 변환 표기 | 문헌·강의 근거 및 확인 사항 |
|---|---|---|
| route-01 / step-01 (1단계) | 3.1 route-01: 에틸 4-니트로벤조에이트 → 벤조카인 | [D9][D1] 동일 변환의 직접 문헌 사례. Org. Synth. 분리·재결정 후 질량 수율 91–100%; 특허 약 100% 이론량(측정법 별도 정의 없음). 세부 조건은 §6.1.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |
| route-02 / step-01 (1단계) | 3.2 route-02: 에틸 4-아세트아미도벤조에이트 → 벤조카인 | [D1] 이 증거 묶음에는 동일 단계의 문헌·강의 사례가 매핑되지 않음.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |
| route-05 / step-01 (2단계) | 3.3.1 route-05/step-01: 아세트산 → 에탄올 | [D1] 이 증거 묶음에는 동일 단계의 문헌·강의 사례가 매핑되지 않음.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |
| route-05 / step-02 (2단계) | 3.3.2 route-05/step-02: 4-아미노벤조산 + 에탄올 → 벤조카인 | [17, PDF pp. 80–81][D1] 벤조카인 교육 예시; [17, PDF pp. 90–95] 일반 메커니즘 교육자료. 실험 수율 근거 아님.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |

<a id="r02"></a>
## R02 표2 코드형 표시·조건 후보

#### 표 2. Parrot 조건 후보·단계별 예측 수율

| 경로·단계 (경로 단계 수) | Parrot rank | sequence_score | Parrot 원래 슬롯 | Yield-BERT 예측값 / 상태 |
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

<a id="r03"></a>
## R03 강의 비교의 반복 정리

Parrot의 route-05/step-02 rank-1 후보는 catalyst1이 비어 있고, solvent1=`CCO`, solvent2가 비어 있으며, reagent1=`CCOCC`, reagent2=`FB(F)F`이다[D1]. 이 슬롯을 그대로 두면 강의의 황산 촉매 피셔 에스터화와는 촉매·시약 구성이 다르다[17, PDF pp. 80–81]. 화학적으로 `CCO`는 에탄올, `CCOCC`는 디에틸 에터 계열 토큰, `FB(F)F`는 BF₃ 계열 토큰으로 읽을 수 있으나, 이는 해석이며 Parrot의 슬롯 분류가 아니다. 따라서 이 해석을 강의 조건과 합쳐 하나의 조건으로 만들지 않는다. 온도·시간·당량·압력은 제공되지 않았고, 이 단계의 운영 조건은 `NOT SUPPLIED`이다[D1].

rxn_yields는 이 반응 SMILES에 대해 79.79832496878097%를 반환했으며, 표시는 79.80%로 하되 상태는 `predicted_not_validated`이다[6][D1]. 이 값은 구조만 입력한 단계 예측이며, Parrot 조건이나 강의 조건에서의 실험 수율이 아니다[17, PDF pp. 80–81].

#### 표 3. 강의 근거와 AI 예측의 비교: route-05/step-02

| 구분 | 강의 근거(과정 자료) | AI 예측(route-05/step-02) | 비교의 한계 |
|---|---|---|---|
| 반응 골격 | 4-아미노벤조산 + 에탄올 → 벤조카인(에틸 에스터) 역합성·정방향 예시[17] | 동일 반응 SMILES `CCO.Nc1ccc(C(=O)O)cc1 >> CCOC(=O)c1ccc(N)cc1`[D1] | 생성물 골격은 같으나 조건·메커니즘 증명은 별개 |
| 조건 | 황산 촉매 피셔 에스터화를 교육 예시로 제시[17, PDF pp. 80–81] | Parrot rank-1: catalyst1 `""`, solvent1 `CCO`, solvent2 `""`, reagent1 `CCOCC`, reagent2 `FB(F)F`[D1] | 모델 슬롯을 강의 조건으로 대체하거나 합치지 않음; `CCO`/`CCOCC`/`FB(F)F`는 화학 해석일 뿐 슬롯 분류가 아님 |
| 메커니즘 설명 | 90–95쪽 일반 피셔 에스터화 전자 흐름(메탄올/아세트산 계열 예시)[17, PDF pp. 90–95] | 이 프로젝트 내에서 측정된 메커니즘·장벽·속도 자료는 없음 | 강의 그림은 일반 교육 예시이며, 이 반응의 실험적 메커니즘 증명이 아님 |
| 수율 | 강의에 이 반응의 실험 수율 제시 없음[17, PDF pp. 80–81] | rxn_yields 79.80%, 상태 `predicted_not_validated`, conditions_in_input false[6][D1] | 구조만 입력한 예측값이며 조건별 실험 수율이 아님 |

요약하면, 강의와 AI 예측은 같은 벤조카인 골격을 공유하지만, 강의의 황산 촉매 피셔 에스터화 예시와 Parrot rank-1의 원래 슬롯은 서로 다른 기술이며, 79.80%는 구조 기반 예측 수율에 그친다. 따라서 이 비교는 두 자료의 범위와 한계를 구분하는 데 쓰이고, 어느 한쪽의 조건이나 메커니즘을 다른 쪽으로 검증한 것으로 읽지 않는다[6][17, PDF pp. 90–95][D1].

<a id="r04"></a>
## R04 모델 출력·상태 코드 한국어화

AiZynthFinder는 역합성 경로 탐색에 사용되었다[2][D1]. 이번 실행에서 routes는 success로 기록되어 있으며, 12개 경로와 20개 단계가 생성되었다[16]. 다만 이는 출력 무결성 및 조인 검증에 대한 결과이며, 각 경로가 실제 실험적으로 실현 가능하다는 증명은 아니다. 검색은 대상 물질을 재고에서 제외한 상태로 수행되었고, 작용제나 부산물이 생략될 수 있다[D4].

템플릿 기반 절단 정보는 각 단계의 metadata에 기록되어 있다[D1]. 예를 들어 route-01/step-01의 템플릿은 아미노기 관련 형태를 기술하며, route-02/step-01과 route-05/step-02도 각각 다른 템플릿 코드를 가진다. 그러나 분류가 “0.0 Unrecognized”로 기록된 점은, 이 템플릿이 특정 명명된 반응 유형으로 즉시 분류되지 않았음을 보여 준다[D1]. 이 점은 템플릿이 틀렸다는 뜻이 아니라, 이번 출력에서 분류 정보가 제한적이라는 뜻이다.

경로 식별자(route-01~route-12, step-01~step-02)와 템플릿 코드, “0.0 Unrecognized” 분류 값은 재현 표에서 관리한다. 본문은 실행 성공과 화학적 성공을 구분하며, 식별자 제거로 방법을 숨기지 않는다.

### 4.2 Parrot: 조건 추천

Parrot은 반응 조건 후보 추천에 사용되었다[5][D1]. 이번 실행에서 conditions는 success로 기록되어 있으며, 선택된 반응들에 대해 각각 15개 후보가 반환되었다[D1]. Parrot 출력은 catalyst1, solvent1, solvent2, reagent1, reagent2 필드로 구성되며, 이 보고서는 그 필드를 그대로 사용한다. 후보를 병합하거나 서로 다른 rank의 슬롯을 섞어 하나의 조건으로 만들지 않는다.

Parrot의 sequence_score는 후보 순위 평가에 사용되지만, 반응 성공률이나 실험 수율을 직접 뜻하지는 않는다[D1]. 또한 Parrot 조건은 수율 모델의 입력이 아니다[D1]. 즉 조건 추천과 수율 예측은 서로 다른 모델이며, 조건 슬롯이 수율 예측에 반영되었다는 증거는 없다.

이번 조건 체크포인트는 temperature, time, yield_percent를 제공하지 않았다[D1]. temperature_status는 `not_provided_by_checkpoint`로 기록되어 있다. 따라서 온도·시간·당량·압력은 `NOT SUPPLIED`이며, 이 누락은 조건 추천 모델이 해당 값을 출력하지 않았다는 뜻이다. 실험에서 해당 성분을 사용하지 않았다는 뜻이 아니다.

<a id="r05"></a>
## R05 MOPAC 방법·인용 경계

MOPAC 23.2.5로 PM7[10] 고립 분자 기하 최적화가 수행되었다[D5]. 이번 작업에서는 다섯 중성 종에 대해 각각 5개의 RDKit ETKDGv3 conformer를 MMFF94s로 먼저 최소화한 뒤, 각각을 MOPAC으로 독립 최적화했다[D5]. 입력은 `CHARGE=0 MS=0`으로 설정되어 중성 단일항 상태를 지정했고, MOPAC 출력은 폐쇄껍질 RHF, SCF 완료, 정상 종료, 최종 기울기 노름이 요청된 `GNORM=0.5[11] kcal mol⁻¹ Å⁻¹` 미만임을 확인했다[D5]. 총 25개 작업 중 25개가 수렴했다[D5].

최적화된 구조 중 저장된 것은 각 분자식·전하·스핀에 대해 다섯 시작 배좌 중 PM7 생성열이 가장 낮은 수렴 기하이다[D5]. 이는 best-of-five 탐색이며, 전역 최소점이나 진동수 검증 최소점이라고 단정하지 않는다. 모든 계산은 기체상이며, 용매·촉매·수소·반대이온·반응 파트너·전이상태는 포함되지 않았다[D5][10].

<a id="r06"></a>
## R06 EPI 코드·물성 반복 정리

EPA의 EPI Suite는 유기화학물질의 녹는점·끓는점·증기압 등을 추정(screening-level)하는 도구[12]로 설명된다[D6]. 이번 작업에서는 다운로드 가능한 v4.11의 실행 어려움이 안내되어 EPI Suite Web[13] 베타를 사용했고, HTTP 200 응답은 받았으나 API 건강 상태는 `degraded`, `requestHandling.healthy=false`로 기록되었다[D6]. 따라서 결과는 서비스 제한 하에서 수신된 것으로 다룬다. 로컬 EPI Suite 설치는 수행하지 않았다[D6].

MPBPWIN v1.44 모델 추정치와 EPI Unified 데이터베이스 기록은 구분해야 한다[D6]. `estimatedValue`는 모델 추정치이고, `experimentalValues`/EpiUnified 증거는 데이터베이스 기록이며, `selectedValue`가 항상 측정값을 뜻하는 것도 아니다. 이번 결과에서 모델 추정치는 7개 물질에 대해 모두 `ESTIMATED`로 표시되었다[D6][12].

주요 추정값과 데이터베이스 기록은 다음과 같이 정리된다[D6].

- 에틸 4-니트로벤조에이트: MPBPWIN MP 80.66 °C, BP 297.25 °C. EPI Unified 기록은 반환되지 않았다.[12][D6]
- 벤조카인: MPBPWIN MP 66.17 °C, BP 279.90 °C. EPI Unified 기록은 반환되지 않았다.[12][D6]
- 4-아미노벤조산: MPBPWIN MP 94.08 °C, BP 307.70 °C. EPI Unified MP 기록은 188.5 °C이며 분류는 `derived_or_analogue_database_entry_not_direct_measurement`이다.[12][D6]
- 에탄올: MPBPWIN MP −87.84 °C, BP 65.11 °C. EPI Unified MP는 −114.1 °C, BP는 78.2 °C이며 분류는 각각 `derived_or_analogue_database_entry_not_direct_measurement` 또는 `epi_database_evidence_provenance_insufficient_to_claim_direct_experiment`이다.[12][D6]
- 아세트산: MPBPWIN MP −21.26 °C, BP 122.30 °C. EPI Unified MP는 16.635 °C, BP는 117.9 °C이며 분류는 `literature_cited_epi_evidence_not_independently_verified_as_measurement` 또는 `epi_database_evidence_provenance_insufficient_to_claim_direct_experiment`이다.[12][D6]

에탄올, 아세트산, THF, 다이ethyl 에터에는 정확한 구조 일치 기록이 있었지만, 벤조카인과 에틸 4-니트로벤조에이트에는 EPI 검색 일치가 없어 보고된 값이 모델뿐이었다[D6]. 또한 일부 녹는점 기록은 기울기 유사(slope analogy)나 증기압/물 용해도 데이터 기반 계산 등으로 기술되어 직접 측정이 아니다[D6]. 아세트산 MP 기록은 1992 저자 문자열이 있으나 원문 논문·방법이 API에 포함되지 않아 주의가 필요하다[D6].

<a id="r07"></a>
## R07 Visualizer 관찰·출처·본문 참조

실제 화면 관찰에는 에틸 4-니트로벤조에이트 배좌 1의 여러 방향 표시, 배좌 2의 단일 레코드 표시, 4-아미노벤조산 PM7 배좌 4의 카복실기 원자 C6/O7/O8 화면, 강체 회전한 표시 사본, 고립 에탄올 PM7 배좌 2 화면이 포함된다[D7]. 다만 강체 회전한 화면은 새 배좌가 아니라 표시 방향의 사본이며, 고립 에탄올 화면은 4-아미노벤조산과 함께 배치하지 않았다[D7]. 따라서 이 화면들은 정성적 단일 분자 관찰 이상으로 반응 복합체나 접근 궤적을 입증하지 않는다[10][D5].

완료된 범위는 배좌 1·2의 거리·각도 4개 측정과 해당 Monitor 표 캡처, 원본 SDF 해시가 세션 전후 일치함을 기록한 것이다[D7]. 미완료 범위는 배좌 3–5와 route-05의 모든 측정이다[D7]. 배좌 전환 후 화면 재렌더링·선택 대상 연결이 간헐적으로 모호해졌고, 재열기 이후 기본 배좌가 1로 돌아오는 사례가 있어 잘못된 배좌에 수치를 연결할 위험이 있었기 때문에 같은 조작을 반복하지 않았다[D7]. 별도 코드·도구로 계산한 값은 Visualizer 측정값에 섞지 않았다[D7][D1].

<a id="r08"></a>
## R08 재현 이력·기술 기록 외부 연결

이번 실행은 AiZynthFinder 경로 탐색, Parrot 조건 추천, rxn_yields 수율 예측으로 구성되었다[16][D10]. 재현 관련 기록에서 routes와 yields는 이전 실행(benzocaine-live-20261031-03)의 결과를 바이트 단위로 재사용했고, 조건 추론은 이번 실행(benzocaine-live-20261031-04)에서 수행되었다[16]. 즉 이번 실행에서 세 모델 추론이 모두 새로 수행된 것은 아니다[16][6].

### 8.2 재현 시 주의할 점

AiZynthFinder와 Parrot/rxn_yields의 Python 환경, 저장소, 체크포인트는 보존된 경로 아래 구성되어 있으며, 다른 기계에서 재현하려면 configs/runtime.json과 해당 자산을 맞춰야 한다[16]. 또한 routes와 yields는 이전 실행에서 복사된 것이므로, 이번 실행에서 세 모델 추론이 모두 새로 이루어졌다고 주장하지 않는다[16][6].

재실행 검증 기록에서는 모델·USPTO 반응 템플릿 아카이브·재고 해시가 일치하고, routes 예측도 일치하며, Parrot 조건과 Yield-BERT 출력도 대표 실행과 일치하는 것으로 기록되어 있다[16][D10]. 다만 구성 JSON의 바이트 해시는 서로 다르고, 경로 구분자 정규화 후 구성 객체가 동일해지는 것으로 기록되어 있다[16][D10]. 이 바이트 차이의 원인은 unresolved로 남아 있다[16][D10]. 이 점은 동일 자산·동일 예측이라는 주장과 구성 파일 바이트 차이라는 관찰을 구분해 남겨 둔다[6].

<a id="r09"></a>
## R09 참고문헌·프로젝트 근거 표시

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
20. Prediction of chemical reaction yields using deep learning. https://doi.org/10.1088/2632-2153/abc81d
21. 배포 수율 체크포인트의 공식 평가 기록. https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/trained_models/uspto/uspto_gram_random_test_epochs_2_pretrained/checkpoint-19762-epoch-2/eval_results.txt
22. McMaster Chem2OB3 벤조카인 실험 절차. https://www.chemistry.mcmaster.ca/~chem2ob3/2004labmanual/2004_exp4.pdf

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
- D11: User-provided target selection provenance. evidence-run/report-context.json
- D12: Verified Parrot structure-token to chemical identity mapping. evidence-run/token-identity-evidence.json; evidence-run/chemical-token-audit.csv
- D13: 반응 매핑과 경계·조각 연결 대조. evidence-run/mapped-bond-differences.csv; evidence-run/step-structure-detail-20261125-01/
- D14: 공급 가지의 원시 경로와 단계 연결 검토. evidence-run/route05-step01-provenance-review.md
- D15: 집 PC 단일 분자 관찰 기록. evidence-run/home_visualizer/README.md; evidence-run/home_visualizer/capture_manifest.csv
- D16: 수율 모델 적용성 검토와 원시 실행 대조. evidence-run/yield-applicability/
- D18: 조건 후보의 구조·역할·불완전성 검토. evidence-run/parrot-condition-review.md
- D19: 학교 문헌 조건·수율 검토. evidence-run/yield-improvement-review.md

<a id="r10"></a>
## R10 부록의 한계·기록 구분

- route-01의 Parrot 상위 조건은 문헌의 PtO₂나 Rh/Al₂O₃를 정확히 제시하지 않고, H₂ 슬롯도 후보마다 다르다. 문헌 조건은 모델 출력과 분리해 후속 검토 후보로 남겨 둔다[D9][D1].
- Yield-BERT 예측과 문헌 수율의 차이는 조건 일치 성능 오차로 해석하지 않는다. 학습 데이터 중복 여부도 미확인이다[D9][D1][6].
- MOPAC은 고립 분자만 다루므로 반응 장벽·속도·수율·성공의 증거가 아니다[D5][10].
- EPI Suite는 서비스 저하 상태에서 수신되었고, 혼합 상평형 정보는 제공하지 않는다[D6][12].
- Visualizer는 일부 분자 내부 거리·각도와 정성적 단일 분자 화면만 제공하며, 반응물 접근·공격각·입체장애·반응 성공·수율을 측정하지 않는다[D7].
- route-05/step-01은 경로 간선이며 실제 순차 합성 검증이 없다[D1].
- 과거 준비-phase 상태 파일에는 추가 분석이 not_implemented로 남아 있었으나, 현재 증거는 MOPAC 25/25 수렴, 실제 EPI 응답, Visualizer 두 배좌 측정을 기록한다[D3]. 이 상충은 과거 기록을 지우지 않고, 현재 증거만 현재 사실로 사용한다[D3][10][D5][D7].
- 구성 파일 바이트 해시 차이의 원인은 unresolved이며, 경로 구분자 정규화 후 구성 객체가 동일하다는 관찰과 함께 남겨 둔다[16][D10].

이 보고서는 제공된 증거와 스킬 규칙에 따라 작성했으며, 수행되지 않은 계산·GUI 관찰·모델 실행·실험 조건을 수행하지 않은 것으로 서술하지 않았다. 통합 조건·수율 표와 실제 그림 삽입은 문서 렌더러가 검증된 로컬 파일로 수행한다.

<a id="r11"></a>
## R11 실행 개요의 상태 코드

이번 실행은 AiZynthFinder[2]로 역합성 경로를 찾고, Parrot[5]로 반응 조건 후보를 추천하며, rxn_yields[6]로 수율을 예측하는 세 단계로 진행되었다. 실행 요약에는 routes, conditions, yields가 모두 성공으로 기록되어 있다[D1]. 여기서 성공은 각 파이프라인의 출력 파일이 정상적으로 생성되고 정규화되었다는 의미이며, 예측값이 실험으로 확인되었다는 뜻은 아니다. 각 도구의 입력·출력·검증 범위는 뒤에서 따로 구분한다.

<a id="r12"></a>
## R12 route01 구조 설명·그림3 연결

**구조 변화.** 이 단계는 방향족 니트로기(–NO₂)가 아미노기(–NH₂)로 바뀌는 환원 변환이며, 에틸 에스터는 유지된다[D1]. 반응 SMILES는 `CCOC(=O)c1ccc([N+](=O)[O-])cc1 >> CCOC(=O)c1ccc(N)cc1`이다[D1]. 저장된 매핑 반응 SMILES에서는 니트로 질소(atom map 10)의 형식전하가 +1에서 0으로 바뀌고, 결합된 두 산소(atom map 13, 14)와의 연결이 끊어지는 그래프 차이로 기록된다[D13]. 이는 저장된 구조·매핑의 차이이며, 실험적 원자 추적이나 단계별 메커니즘 증명이 아니다.

