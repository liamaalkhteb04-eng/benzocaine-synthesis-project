# 수율·EPI 통합 보완 요약

작성일: 2026-11-24  
범위: 기존 자료의 읽기 전용 통합. 새 추론·계산·설치 없음.

기존 검토 폴더와 보고서·스킬·원시 결과는 수정하지 않았다. 수율 재실행, augmentation, 대안 모델 설치, Visualizer, MOPAC은 수행하지 않았다.

## 1. 수율 검토 마무리

`route-05/step-01`은 기존 원시 경로 기록에서 최종 benzocaine의 retrosynthetic tree가 `CCO`를 step-02 precursor로 만들기 위해 `CC(=O)O` terminal까지 연결한 **에탄올 공급 가지**임을 확인했다.

- 근거: `reports/benzocaine-final/evidence-run/latest-route-reproduction/routes-selected-raw.json`, `route-05`
- root: benzocaine; 최종 disconnection의 child: `CCO`; 그 child의 reaction edge: `CCO>>CC(=O)O`; terminal `CC(=O)O`: `in_stock: true`
- tree reaction은 retrosynthetic 방향이고, yield evidence는 forward query `CC(=O)O>>CCO`로 materialized되어 있다.
- 따라서 route graph상 step-02에 공급되는 순차 branch인 것은 확인되지만, acetic acid→ethanol의 실험 합성 제안·조건·수율이 확인된 것은 아니다.
- template `32658`은 `classification: 0.0 Unrecognized`이고 omitted agents가 복원되지 않았다.

결론: 77.59%는 실제 ethanol 공급 수율이나 benzocaine 전체 수율이 아니라, route edge를 forward 형식으로 조회한 `predicted_not_validated` 값이다. 이 단계는 문헌 수율 비교 대상에서 제외한다.

## 2. 네 수율의 보고서 사용 범위

| 반응 | 기존 예측값 | 문헌 근거 | 적용 한계 | 보고서에서 제시 가능한 의미 |
|---|---:|---|---|---|
| route-01/step-01: ethyl 4-nitrobenzoate → ethyl 4-aminobenzoate | 82.95% | Organic Syntheses: PtO₂/95% alcohol/H₂, 약 7분, 재결정 후 91–100% theoretical. https://www.orgsyn.org/demo.aspx?prep=CV1P0240 | catalyst·조건·workup이 다르고 문헌 한 사례는 모델 정확도 검증이 아님 | 해당 reaction SMILES에 대한 USPTO gram-scale checkpoint 예측값; 문헌값은 별도 조건 비교 |
| route-02/step-01: ethyl 4-acetamidobenzoate → ethyl 4-aminobenzoate | 77.70% | 정확히 대응하는 comparable synthetic isolated yield와 완전 조건을 확보하지 못함 | substrate·deacetylation 조건·workup·수율 정의 미확인 | 모델의 reaction-SMILES 예측값이며, 직접 문헌 검증 없음 |
| route-05/step-01: acetic acid → ethanol query | 77.59% | 동일한 유효 benzocaine route 단계의 문헌 수율 없음 | route branch provenance는 확인했지만 chemical step validity와 omitted agents 미확인 | ethanol 공급 branch에 대한 forward yield query의 예측값; 실제 단계/전체 수율 아님 |
| route-05/step-02: PABA + ethanol → benzocaine | 79.80% | McMaster procedure: PABA+95% ethanol+농축 H₂SO₄, reflux 60분; 현재 자료에서 대표 numeric isolated yield는 확인되지 않음. https://www.chemistry.mcmaster.ca/~chem2ob3/2004labmanual/2004_exp4.pdf | 모델 입력에는 산 농도·reflux·당량·water removal이 없음 | 해당 reaction SMILES의 예측값; 문헌 조건은 별도 비교 근거 |

공통: 네 값은 실제 실험 수율, route overall yield, 모델 정확도, 신뢰구간이 아니다. Parrot 조건은 yield 모델 입력이 아니며 `predicted_not_validated`/`applicability: not_assessed` 상태다.

## 3. 기존 EPI 결과

단위는 모두 °C이다. `MPBPWIN estimate`는 모델 추정값이며, `EPI Unified` 값은 database/evidence 값으로 별도 표기한다. EPI Unified 값도 직접 실험값으로 확정하지 않았다.

| 물질 | MP 모델 | MP EPI/DB | BP 모델 | BP EPI/DB | 확인한 결과 |
|---|---:|---:|---:|---:|---|
| ethyl 4-nitrobenzoate | 80.66 | 없음 | 297.25 | 없음 | EPI 모델값만 확인; exact EPI Unified record 없음 |
| benzocaine | 66.17 | 없음 | 279.90 | 없음 | EPI 모델값만 확인; exact EPI Unified record 없음 |
| 4-aminobenzoic acid | 94.08 | 188.5 | 307.70 | 없음 | MP DB 값은 derived/analogue entry로 분류됨 |
| ethanol | -87.84 | -114.1 | 65.11 | 78.2 | MP derived/analogue; BP provenance 불충분 |
| acetic acid | -21.26 | 16.635 | 122.30 | 117.9 | MP literature-cited but independently unverified; BP provenance 불충분 |
| tetrahydrofuran | -84.89 | -108.44 | 69.36 | 65.0 | MP derived/analogue; BP provenance 불충분 |
| diethyl ether | -101.15 | -116.3 | 47.02 | 34.6 | MP derived/analogue; BP provenance 불충분 |

추가 확인된 acetic acid 외부 cross-check는 Australian Government NPI의 MP 16.7°C, BP 118°C이며 EPI DB 값과 가깝다. 이는 MPBPWIN 모델값을 검증하지 않는다.

## 4. EPI 판단 표

| 항목 | 확인한 결과 | 판단 가능한 내용 | 판단이 어려운 이유 | 필요한 추가 정보 |
|---|---|---|---|---|
| 순물질 MP/BP | 위 표의 모델 추정값과 EPI/DB 값 분리 확인 | screening-level pure-compound property 비교 가능 | DB provenance가 직접 실험·방법·압력을 일관되게 제공하지 않음 | 원 논문/실험 method, purity, pressure |
| benzocaine/ethyl 4-nitrobenzoate | 모델값만 있고 EPI Unified exact record 없음 | 모델 산출값의 존재만 보고 가능 | measured/DB benchmark 부재 | 신뢰 가능한 measured property source |
| ethanol/acetic acid/THF/ether | 모델·DB 값 모두 존재 | 대략적인 순물질 물성 범위와 source 차이 표시 가능 | DB 값 중 derived/analogue 또는 provenance 부족 분류 | 직접 실험 출처와 pressure |
| Parrot 후보와 물성 연결 | 슬롯 구조 토큰과 EPI 입력은 별도 기록 | 특정 순물질의 MP/BP를 별도 참고값으로 제시 가능 | EPI가 Parrot의 역할·농도·당량을 검증하지 않음 | 실제 물질 identity/role mapping |
| 반응 온도·압력 비교 | 이번 자료에는 Parrot temperature/time/pressure 없음 | Organic Syntheses route-01의 H₂/ethanol/PtO₂ 조건, McMaster route-05 step-02의 reflux/acid 조건을 문헌 조건으로 별도 제시 가능 | 문헌 조건은 모델 출력이 아니며 mixture phase behavior를 주지 않음 | 실제 reaction temperature, pressure, concentration, atmosphere |
| 석출·기화·반응성 | 순물질 물성으로 단정하지 않음 | 추가 mixture analysis가 필요하다는 결론만 가능 | 용액 조성·물 함량·염/화학형태·압력·공정이 없음 | solubility, VLE/SLE, equivalents, salts, water content |

## 5. 현재까지의 가장 타당한 다음 단계

수율은 추가 추론 없이 현재 상태에서 보고서용 의미와 한계를 정리할 수 있다. route-05/step-01은 수율 비교에서 제외하고, 필요하면 원본 route generator의 edge-direction/materialization 로그를 읽기 전용으로 더 확인한다.

EPI는 기존 자료로 물질별 MP/BP와 provenance 구분을 완료했다. 핵심 미해결은 반응 혼합물의 phase behavior이며, 이는 새 계산·추가 데이터가 필요한 별도 분석이다. 현재 범위에서는 실행하지 않는다.

