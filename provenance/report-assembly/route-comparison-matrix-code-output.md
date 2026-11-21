# 경로 비교 매트릭스 (검증 원자료의 코드 조인)

경로 개요와 조건 후보의 상세 슬롯을 분리했다. 아래 후보 표는 각 Parrot 후보를 별도 행으로 보존하며, route-01 rank 1과 rank 4도 합치지 않는다. 문헌은 반응 변환의 선례이지 개별 Parrot 후보를 검증한 결과가 아니다. 수율은 반응 구조만 입력한 단계별 모델 예측값이며 조건별 실험 수율이 아니다.

## 경로 요약

| 경로·단계 (전체 단계 수) | 기존 보고서의 변환 표기 | 문헌·강의 근거 및 확인 사항 |
|---|---|---|
| route-01 / step-01 (1단계) | 3.1 route-01: 에틸 4-니트로벤조에이트 → 벤조카인 | [D9][D1] 동일 변환의 직접 문헌 사례. Org. Synth. 분리·재결정 후 질량 수율 91–100%; 특허 약 100% 이론량(측정법 별도 정의 없음). 세부 조건은 §6.1.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |
| route-02 / step-01 (1단계) | 3.2 route-02: 에틸 4-아세트아미도벤조에이트 → 벤조카인 | [D1] 이 증거 묶음에는 동일 단계의 문헌·강의 사례가 매핑되지 않음.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |
| route-05 / step-01 (2단계) | 3.3.1 route-05/step-01: 아세트산 → 에탄올 | [D1] 이 증거 묶음에는 동일 단계의 문헌·강의 사례가 매핑되지 않음.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |
| route-05 / step-02 (2단계) | 3.3.2 route-05/step-02: 4-아미노벤조산 + 에탄올 → 벤조카인 | [17, PDF pp. 80–81][D1] 벤조카인 교육 예시; [17, PDF pp. 90–95] 일반 메커니즘 교육자료. 실험 수율 근거 아님.<br>Parrot 온도·시간 미제공; 출력에 당량·압력 필드 없음; 수율 모델 입력에 조건 없음. |

## Parrot 후보·단계별 예측 수율

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

## 입력·검증 자료

- `report-evidence.json`: selected routes, route/step reaction mapping, step counts, normalized yield and candidates.
- `latest-route-reproduction/conditions-parrot.raw.json`: original Parrot slots, rank, score, reaction and route/step links.
- `latest-route-reproduction/yields-rxn_yields.raw.json`: raw/normalized yield record, status and conditions-input flag.
- `literature-validation/route-01-primary-comparison-20261114/comparison.json`: route-01 direct literature comparison only.
- `course-evidence-summary.md`: course page summary; educational evidence is not experimental validation.

미제공 온도·시간은 Parrot 출력 기준이다. 당량·압력 미기재는 이 결과 묶음의 Parrot 원시 출력에 해당 필드가 없다는 뜻이다. 표의 route-01 문헌은 route-01과 동일 반응 SMILES에 매핑된 사례만 표시한다. route-05의 강의 비교는 교육 예시로 표시하며 실험 문헌으로 취급하지 않는다.
