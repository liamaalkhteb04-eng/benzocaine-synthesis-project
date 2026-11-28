# Parrot 조건 후보 화학적 적합성 검토

기준: 저장소 커밋 `801ace04d7e9ca528584c41429712faa0c84f399`의 원시 결과. 수율 적용성 결론은 별도 폴더의 기존 문서를 보존하며 이 검토에서 변경하지 않는다.

## 판정 원칙

- `catalyst1`, `solvent1/2`, `reagent1/2` 슬롯과 rank/SMILES/score는 원시 출력 그대로 보존했다.
- SMILES에서 직접 읽을 수 있는 물질 정체성과, 그 물질을 촉매·용매·환원제·산 촉매 등으로 해석하는 실험 역할은 분리했다. 빈 슬롯은 “출력에 없음”일 뿐 “실험에서 사용하지 않음”의 증거가 아니다.
- 후보끼리 성분을 합쳐 새로운 조건을 만들지 않았다.
- 아래 문헌 비교는 모델 출력의 검증이 아니다. 문헌에 유사 변환이 있다는 사실은 후보 조건이 재현되었다는 뜻이 아니다.
- Parrot 출력에는 `temperature: null`, `time: null`, `use_temperature: false`가 기록되어 모든 후보에서 온도·시간·당량·압력·분위기가 확인되지 않는다.

## 원시 후보 연결

| 단계 | reaction SMILES | 원시 상위 후보 (rank: catalyst1; solvent1; solvent2; reagent1; reagent2; score) |
|---|---|---|
| route-01/step-01 | `CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1` | 1: `[Pd]`; `CCO`; 없음; 없음; 없음; -1.7008. 2: `[Pd]`; `CO`; 없음; 없음; 없음; -2.0482. 3: `[Pd]`; `CCOC(C)=O`; 없음; 없음; 없음; -2.7931. 문헌 비교용 4: `[Pd]`; `CCO`; 없음; `[H][H]`; 없음; -2.8787. |
| route-02/step-01 | `CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1` | 1: 없음; `CCO`; 없음; `Cl`; 없음; -1.3240. 2: 없음; `Cl`; 없음; 없음; 없음; -2.6605. 3: 없음; `CCO`; 없음; `[Na+].[OH-]`; 없음; -3.2929. |
| route-05/step-01 | `CC(=O)O>>CCO` | 1: 없음; `C1CCOC1`; 없음; `[Al+3].[H-].[H-].[H-].[H-].[Li+]`; 없음; -1.8565. 2: 없음; `C1CCOC1`; 없음; `O`; `[Al+3].[H-].[H-].[H-].[H-].[Li+]`; -2.7974. 3: 없음; `C1CCOC1`; 없음; 없음; 없음; -2.9943. |
| route-05/step-02 | `CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1` | 1: 없음; `CCO`; 없음; `CCOCC`; `FB(F)F`; -2.1755. 2: 없음; `CCO`; 없음; `CC(=O)Cl`; 없음; -2.3472. 3: 없음; `O=S(=O)(O)O`; 없음; 없음; 없음; -2.6159. |

원시 전체 파일: `reports/benzocaine-final/evidence-run/latest-route-reproduction/conditions-parrot.raw.json`.

## 단계·후보별 평가

| 단계/후보 | 확인된 내용 | 문제 또는 불확실성 | 판단 근거 | 추가 확인 사항 |
|---|---|---|---|---|
| route-01 r1 | `[Pd]`와 `CCO`가 슬롯에 있다. 구조 토큰 자체는 Pd 원자와 ethanol 구조로 읽을 수 있다. | nitro→amine에는 수소원/수소화제와 촉매 형태·지지체가 필요할 수 있는데 reagent 슬롯은 비어 있다. `[Pd]`가 실제 Pd/C인지 PdO₂인지, `CCO`가 용매인지 확인 불가. | Organic Syntheses의 ethyl p-nitrobenzoate→benzocaine 절차는 PtO₂, ethanol, H₂를 명시한다. 이는 r1을 검증하지 않는다. | checkpoint의 label mapping/출력 슬롯 의미, 실제 Pd 전구체·지지체·H₂ 공급·압력·온도·시간 확인. |
| route-01 r2 | `[Pd]`와 `CO`(methanol 구조)가 출력됨. | r1과 마찬가지로 명시적 수소원과 촉매 형태가 없다. methanol이 solvent인지 다른 역할인지 모델 슬롯만으로 확정 불가. | 문헌의 ethanol/PtO₂/H₂ 조건과 직접 일치하지 않는다. 유사 변환 문헌은 후보 검증이 아님. | 실제 실험 recipe와 catalyst identity 확인. |
| route-01 r3 | `[Pd]`와 `CCOC(C)=O`(ethyl acetate 구조)가 출력됨. | 수소원·촉매 형태·반응 조건이 없다. ethyl acetate의 실제 역할도 확정 불가. | 공식 원시 출력에는 슬롯만 있고 temperature/time이 없다. 문헌 nitro reduction의 필수 성분과 비교하면 누락 정보가 크다. | 동일 반응의 독립 문헌 조건 및 실제 실행 기록 대조. |
| route-01 r4 | r4에는 `[H][H]`가 reagent1로 명시되어 수소원 구조 토큰과 Pd/ethanol이 함께 출력된다. | `[Pd]`가 문헌의 PtO₂를 의미하지 않으며 지지체·압력·온도·시간·당량이 없다. 따라서 문헌과 더 가까운 구성일 뿐 검증된 조건은 아니다. | Organic Syntheses 1928, procedure 1은 ethyl p-nitrobenzoate, 95% alcohol, platinum oxide, H₂ 흡수 및 7분을 명시한다. 출력과 문헌은 촉매/세부 조건이 다르다. | Pd catalyst identity/support, H₂ pressure/uptake, time/temperature 확인. |
| route-02 r1 | `CCO`와 `Cl`이 각각 solvent1/reagent1 슬롯에 있다. SMILES `Cl`의 물질 정체성은 염소 원자 표기지만 실제 시약명·산성 매질·염화수소 공급원인지 확정할 수 없다. | N-acetyl deprotection에 필요한 산/염기·물·온도·시간이 명시되지 않는다. `Cl`의 역할을 HCl로 임의 해석하면 안 된다. | 출력에 산/가수분해 조건이 완전하게 표현되지 않았고 temperature/time이 없다. | 실제 reagent identity와 농도, 물/산/염기, deacetylation protocol 확인. |
| route-02 r2 | `Cl`이 solvent1에만 있고 나머지 슬롯은 비어 있다. | 용매로서의 염소 원자 표기는 실험 용매 정보를 제공하지 않는다. 필요한 deprotection chemistry를 판단할 수 없다. | 슬롯 위치는 역할을 암시할 뿐, 구조 토큰이 그 역할을 보증하지 않는다. | 원시 label mapping 및 실험 조건 확인. |
| route-02 r3 | `CCO`와 `[Na+].[OH-]`가 출력된다. 구조 토큰은 ethanol과 sodium hydroxide 이온쌍으로 읽을 수 있다. | 염기성 가수분해가 N-acetyl 제거에 적합한지, ester도 영향을 받지 않는지, 농도·온도·시간이 없어 판단 불가. | 출력은 모델 후보일 뿐 실제 실험 recipe가 아니다. 후보와 문헌 조건을 혼합하지 않는다. | 선택성·ester 안정성·실제 deacetylation 조건 확인. |
| route-05 r1 | `C1CCOC1`(tetrahydrofuran 구조)와 `[Al+3].[H-]4.[Li+]`(LiAlH₄ 구성에 해당하는 구조 토큰)이 있다. | LiAlH₄는 강한 환원성 물질이며 carboxylic acid→alcohol 변환과 방향성은 가능하지만, 물/산성 성분과의 비호환·첨가 순서·무수 조건·온도·quench가 전혀 없다. | 이 평가는 구조와 일반 반응성에서의 위험/정보 부족 판단이며, 출력이 실제 LiAlH₄ 시약 또는 실험 역할을 보증한다는 뜻이 아니다. | 실제 reagent identity, 무수 THF 여부, 당량, 저온 첨가, quench와 목표 변환의 실험 근거 확인. |
| route-05 r2 | r1의 THF와 LiAlH₄ 구성에 `O`(물 구조)가 reagent2로 추가되어 있다. | LiAlH₄와 물은 직접적으로 비호환 가능성이 높다. 그러나 `O`가 실제 물을 뜻하는지, quench/용매/오류인지 알 수 없다. 출력에 있음은 실험에 실제 사용했다는 뜻이 아니다. | 후보 하나의 성분을 다른 후보와 합치지 않고 r2 자체를 평가하면, reagent2의 구조 토큰과 강한 hydride의 공존은 확인 대상 충돌을 만든다. | `O`의 label mapping, 실제 물 첨가 시점, 무수 조건과 quench 기록 확인. |
| route-05 r3 | THF만 출력되고 catalyst/reagent 슬롯은 비어 있다. | acetic acid→ethanol에 필요한 환원 성분·조건이 출력에 없다. THF는 용매 구조로 읽을 수 있으나 역할은 확정 불가. | 출발/생성물 변환을 수행할 성분과 조건이 직접 확인되지 않는다. | route 생성 오류 여부, omitted reagent/condition 기록 확인. |
| route-05 r1–r3 공통 | 원시 입력은 `CC(=O)O>>CCO`이고 후보 순위가 보존된다. | 이 단계의 반응식 자체가 실제 benzocaine route의 ethanol 생성 단계를 대표하는지 별도 확인이 필요하다. | 공식 조건 후보의 존재는 route chemistry 검증이 아니다. | 원본 route/template와 의도된 실제 변환 확인. |
| route-05 r1–r3 step-02 | r1은 ethanol/diethyl ether/`FB(F)F`, r2는 ethanol/acetyl chloride, r3는 sulfuric acid만 출력된다. 구조 토큰은 각각 직접 읽되, 역할은 확정하지 않는다. | PABA+ethanol esterification에는 산 촉매와 물 제거/평형 관리가 중요할 수 있다. r1의 `FB(F)F`는 물질 정체성은 구조 토큰으로 보존하되 실험 역할·적합성은 공식 mapping 없이는 추정하지 않는다. r2의 acetyl chloride와 ethanol은 반응성/수분 민감성 검토가 필요하지만 세부 조건이 없다. r3는 산 촉매 후보처럼 보일 수 있어도 농도·당량·온도·시간이 없다. | McMaster 2004 primary teaching procedure는 PABA, 95% ethanol, concentrated H₂SO₄, reflux 60 min을 명시한다. 모델 후보 중 r3가 산 구조를 포함한다는 점은 유사성일 뿐, r3 검증이 아니다. | 실제 catalyst/reagent identity, acid concentration, water removal, reflux temperature/time, workup 확인. |

## 문헌과 모델 출력의 분리

- **route-01 문헌 비교:** Organic Syntheses의 `ETHYL p-AMINOBENZOATE` 절차는 ethyl p-nitrobenzoate를 95% alcohol, platinum oxide, hydrogen으로 환원하고 약 91–100% 수율을 보고한다. 이는 r4의 “Pd + ethanol + H₂”와 일부 구성만 유사하다. Pd와 PtO₂, 지지체, 압력/시간이 다르므로 r4가 문헌 조건으로 검증되었다고 쓰지 않는다.
- **route-05/step-02 문헌 비교:** McMaster Chem 2OB3 실험 절차는 PABA+95% ethanol+농축 sulfuric acid, reflux 60 min을 사용한다. 이는 모델 r3의 `O=S(=O)(O)O` 존재와 일부 구조적 유사성이 있지만, r3 출력에는 PABA/ethanol이 조건 슬롯으로 들어간 것이 아니고 농도·시간도 없다. 따라서 r3를 문헌 조건으로 인증하지 않는다.
- **route-02 및 route-05/step-01:** 이번 검토에서 직접 연결되는 1차 절차 근거를 확인하지 못했다. 출력 후보만으로 실제 deacetylation 또는 acetic acid→ethanol 실험이 성립한다고 결론내리지 않는다.

## 종합 결론

Parrot 후보는 반응 SMILES에 대해 슬롯·순위·구조 토큰을 출력했지만, 온도·시간·당량·압력과 실제 label-to-role mapping이 없으므로 실험 조건으로 바로 해석할 수 없다. route-01 r4와 route-05/step-02 r3는 문헌 조건과 일부 겹치는 성분이 있으나, 이는 후보의 부분적 화학적 plausibility를 검토할 근거일 뿐 검증이 아니다. route-05/step-01은 반응식 의미와 후보 성분/조건 모두 불명확해 가장 강한 보류가 필요하다.

## 출처

- 원시 Parrot 결과: `reports/benzocaine-final/evidence-run/latest-route-reproduction/conditions-parrot.raw.json`
- Parrot 공식 저장소: https://github.com/wangxr0526/Parrot
- route-01 1차 절차: https://www.orgsyn.org/demo.aspx?prep=CV1P0240
- route-05/step-02 1차 실험 절차: https://www.chemistry.mcmaster.ca/~chem2ob3/2004labmanual/2004_exp4.pdf
- benzocaine esterification procedure: https://cbspd.s3.ap-south-1.amazonaws.com/assets/documents/5Aj8t2SUyFnduxD6mdZJK2lkQ9GMzO1g.pdf

