# Route-01 문헌 대조: ethyl 4-nitrobenzoate → benzocaine

기준 반응: `CCOC(=O)c1ccc([N+](=O)[O-])cc1 >> CCOC(=O)c1ccc(N)cc1`.
이번 작업은 기존 AI 원시 결과를 실제 1차 문헌의 정확한 출발물질·생성물 반응과 대조한 조사 기록이다. 보고서/예측/원본 결과 파일은 수정하지 않았다.

## 원문에서 확인한 직접 실험

| 1차 출처 | 직접 반응·위치 | 촉매 | 환원제/수소원 | 용매 | 온도 | 시간 | 압력 | 수율·정의 |
|---|---|---|---|---|---|---|---|---|
| Adams & Cohen, *Organic Syntheses* **8**, 66 (1928), “Ethyl p-Aminobenzoate [Benzocaine]”; DOI [10.15227/orgsyn.008.0066](https://doi.org/10.15227/orgsyn.008.0066), [공식 절차 원문](https://www.orgsyn.org/demo.aspx?prep=CV1P0240), Procedure 1, PDF 인쇄면 66 / 책자 *Collective Volume 1* p.240 | 19.5 g (0.1 mol) ethyl p-nitrobenzoate → ethyl p-aminobenzoate | PtO₂ 0.2 g | 수소 기체; 3 molecular equivalents 흡수까지 수소화 | 95% alcohol (원문 표현; 에탄올) 150 cc. 생성물은 ether 약 40 cc.에서 재결정 | 문헌에 미기재 | 약 7분(수소 흡수 시간으로 서술) | 문헌에 미기재 | 15–16.5 g, 이론량의 91–100%. 여과·에탄올 증류 후 에터 재결정한 생성물의 질량 수율이므로 분리/재결정 후 수율. 전환율·분석 수율은 별도 보고 안 됨. 생성물 mp 89–90 °C. |
| US 3,037,046, “Benzocaine Process” (1962), [특허 원문 HTML](https://patents.google.com/patent/US3037046A/en), [원 특허 스캔 PDF](https://patentimages.storage.googleapis.com/15/4a/0a/ba6322b99ce131/US3037046.pdf), Example IV, 특허 인쇄면 3 (스캔 PDF 2쪽) | ethyl p-nitrobenzoate 18.9 g in benzene → ethyl p-aminobenzoate | 1.89 g Rh–alumina oxide catalyst (Rh 5 wt%) | 수소화(hydrogenation); 수소 기체가 쓰였으나 소비 당량은 미기재 | benzene (용량 미기재) | 약 60 °C | Example IV에 미기재. Example I 절차에 따라 처리하지만, Example IV의 개별 반응시간은 적지 않음. Example I의 종점은 압력 감소로 확인. | 30 psig | 약 100% of theory; product mp 86–87 °C, 순도 99.9%라고 보고. Example IV는 수율법을 별도 정의하지 않는다. Example I 방식의 냉각·석출·여과 work-up을 따르므로 분리 생성물 수율로 읽을 근거는 있으나, Example IV에서 분리 질량/수율 측정법은 별도 기재되지 않음. 분석 수율 또는 전환율로 표기되지 않음. |

Organic Syntheses Procedure는 출발물질의 산 제거·알코올 재결정을 Note 1에 지시한다. 원문은 수소 흡수량과 소요시간을 제시하지만 온도·압력을 수치로 주지 않는다. 특허 Example IV는 이 반응 자체의 조건(벤젠, Rh/Al₂O₃, 30 psig, 약 60 °C)을 제시한다. 특허 Example I의 84.2%는 p-nitrobenzoic acid부터 에스터화와 후속 환원을 포함하는 공정의 값이므로, 정확히 동일한 1단계 변환의 수율로 섞어 쓰지 않았다.

## AI 원시 결과와 슬롯별 비교

두 후보 모두 원시 파일 `evidence/conditions-parrot.raw.json`에서 동일한 반응 SMILES와 `route-01/step-01`에 연결되어 있다. 후보를 섞지 않고 별도 비교했다.

| 구분 | Parrot rank 1 | Parrot rank 4 | 문헌과의 대조 |
|---|---|---|---|
| 원시 후보 점수 | sequence_score −1.700762152671814 | sequence_score −2.878655195236206 | Parrot 순위 점수이며 반응 확률·실험 성공률은 아님 |
| catalyst1 | `[Pd]` | `[Pd]` | rank 1과 4 모두 Pd 원자 토큰. Org. Synth.의 PtO₂와 다르고, Pd 촉매의 담지체·산화상태·실물 형태도 출력에서 확인되지 않음. 특허 Example IV의 Rh/Al₂O₃와도 다름 |
| solvent1 / solvent2 | `CCO` / 빈 값 | `CCO` / 빈 값 | `CCO`는 에탄올 구조 토큰. Org. Synth.의 95% alcohol과 용매 계열은 맞지만 물 함량은 표현되지 않음. 특허 Example IV의 benzene과는 다름 |
| reagent1 / reagent2 | 빈 값 / 빈 값 | `[H][H]` / 빈 값 | rank 1은 H₂ 슬롯이 누락됨. rank 4는 `[H][H]`라는 수소 분자 토큰을 명시해 수소원 존재는 Org. Synth.·특허와 일치하지만, 3당량 흡수량이나 수소압은 없음 |
| 조건 필드 | temperature/time/yield 모두 null | temperature/time/yield 모두 null | 두 후보 모두 온도·시간·압력을 제공하지 않음. rank 4의 수소 토큰을 rank 1 조건에 합쳐 하나의 후보처럼 취급하지 않음 |

모델 슬롯은 Parrot 데이터의 `catalyst1`, `solvent1`, `solvent2`, `reagent1`, `reagent2` 필드 그대로다. 이를 화학적으로 읽을 때 `[Pd]`는 단일 Pd 원소 토큰, `CCO`는 에탄올 구조, `[H][H]`는 H₂ 구조 토큰이다. 이는 각각의 실제 촉매 제형, 실험 용매 조성, 환원 조건이 검증됐다는 뜻이 아니다. 모델 순위와 화학적 역할 해석도 별개다.

## Yield-BERT 82.95% 비교

`evidence/yields-rxn_yields.raw.json`에서 route-01/step-01의 정확한 반응 SMILES에 대응하는 Yield-BERT 예측은 82.95371431744555%이며 상태는 `predicted_not_validated`이다. 해당 결과는 반응 구조만 입력했고 `conditions_in_input=false`, `applicability=not_assessed`로 기록되어 있어, 위 문헌의 PtO₂/에탄올/H₂ 또는 Rh/Al₂O₃/벤젠/H₂ 조건을 반영한 수율 예측이 아니다.

동일한 기질·생성물 변환이라는 점에서 **수치의 기술적 병치는 가능**하다. Org. Synth.의 분리 수율 91–100% 범위와 산술적으로 비교하면 예측은 문헌 구간보다 약 8.05–17.05 퍼센트포인트 낮다(82.9537−91, 82.9537−100). 특허 Example IV의 “approximately 100% of theory”와 비교하면 명목상 약 17.05 퍼센트포인트 낮지만, 이 예의 수율 측정법이 명시적으로 정의되지 않았으므로 확정적인 같은 기준 비교로 해석하지 않는다. 두 차이는 조건을 맞춘 성능 오차나 실험 예측 잔차가 아니다.

학습 데이터에 해당 Organic Syntheses 절차나 특허 반응이 포함됐는지, 중복 제거 또는 문헌 중복 여부가 어떤지 확인할 수 있는 기록은 이번 자료에 없다. 따라서 학습 데이터 중복 여부는 **미확인**이며, 있다고도 없다고도 결론내리지 않는다. 한 반응 예로 Yield-BERT의 전체 정확도, 조건별 수율, 또는 우리 실험의 합성 성공을 입증할 수 없다.

## 근거가 지지하는 점과 남은 질문

**문헌이 지지하는 점:** ethyl 4-nitrobenzoate에서 에틸 에스터를 유지한 ethyl 4-aminobenzoate(benzocaine)로 가는 1단계 방향족 니트로기 환원은 실제로 수행된 반응이다. 따라서 route-01의 변환 그래프 자체는 직접적인 실험 문헌과 일치한다. 독립적인 두 직접 사례가 서로 다른 촉매/용매 조합으로 수소화와 생성물 분리를 보고한다.

**아직 확인되지 않은 점:** Parrot rank 1은 문헌의 PtO₂나 Rh/Al₂O₃를 정확히 제시하지 않고 환원제/수소원을 누락한다. rank 4만 수소 토큰을 제시하지만 촉매·용매가 어느 문헌 사례와도 동일하지 않고, 양 후보 모두 온도·시간·압력이 없다. Yield-BERT 82.95%는 이 문헌 조건에 조건화되지 않았고, 데이터 중복 여부도 모른다. 따라서 원시 모델값만으로 어떤 문헌 조건에서의 실험수율을 예측했다고 말할 수 없다.

**보고서 결론에 반영할 발견:** route-01은 “구조적으로 가능성이 확인되지 않은 가상 변환”이 아니라 직접 수행된 환원 반응이다. 다만 그 근거는 AI가 조건을 완성했다는 뜻이 아니다. Parrot rank 1의 H₂ 누락과 rank 4의 순위/슬롯 차이를 명시하고, 문헌 조건은 모델 출력과 분리해 후속 검토 후보로 표시하는 것이 타당하다. 이 조사 기록은 기존 보고서에 반영하지 않았다.

## 재현 파일

- `sources/orgsyn-1928-8-66.pdf`: Organic Syntheses 공식 절차 스캔. Procedure는 PDF 2쪽이며 인쇄 서지 1928, Vol. 8, p.66 / Collection Vol. 1, p.240.
- `sources/US3037046.pdf`: 특허 원문 스캔. Example IV는 PDF 스캔 2쪽, 인쇄면 3.
- `evidence/conditions-parrot.raw.json`: Parrot rank 1 및 rank 4의 원시 조건 출력.
- `evidence/routes.raw.json`: AiZynthFinder route-01 원시 경로.
- `evidence/yields-rxn_yields.raw.json`: route-01 수율 원시 예측.
- `comparison.json`: 위 슬롯·수율·해시의 기계 판독 기록.
- `source-integrity.json`: 저장 원문/원시 결과의 SHA-256.
