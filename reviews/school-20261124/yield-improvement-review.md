# 수율 보완 검토

작성일: 2026-11-24  
범위: 문헌 비교, 공개 수율 모델/체크포인트 조사, 추가 실행 준비  
제외: 새 모델 추론·계산·설치·보고서 수정

기존 수율 적용성 검토와 Parrot 조건 검토는 수정하지 않았다. 이 문서는 그 결과를 입력으로 사용한다.

## 출처 계층

- **사용자 전달 정보:** 수율 생성 run, 대표 네 값, 당시 전체 설정·의존성 일부 미확인이라는 사실.
- **저장소 직접 확인:** `reports/benzocaine-final/evidence-run/latest-route-reproduction/yields-rxn_yields.json`의 반응 SMILES, raw value, 역정규화 값; `configs/yield-normalization.json`의 checkpoint/domain/정규화; `reproducibility-manifest.json`의 run 03 재사용 기록.
- **공식/1차 문헌:** Organic Syntheses의 benzocaine 절차, McMaster 실험 절차, `rxn_yields` 공식 코드·논문.
- **해석:** 문헌과 예측값의 비교 및 추가 실행안. 문헌값을 프로젝트 실험값이나 모델 정확도로 바꾸지 않았다.

## 단계별 비교

| 반응 | 기존 예측값 | 문헌 수율·조건·출처 | 적용·검증 근거 | 남은 한계 | 다음 조치 |
|---|---:|---|---|---|---|
| `route-01/step-01`: ethyl 4-nitrobenzoate → ethyl 4-aminobenzoate; `CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1` | **82.95%**; raw `0.46616948`; gram USPTO checkpoint 역정규화 | Organic Syntheses 1928, `ETHYL p-AMINOBENZOATE`: 19.5 g substrate, 150 cc 95% alcohol, 0.2 g PtO₂, H₂ 3 equivalents, 약 7분, ether recrystallization 후 **91–100% theoretical**. [Org. Synth. DOI 10.15227/orgsyn.008.0066](https://www.orgsyn.org/demo.aspx?prep=CV1P0240) | 변환과 생성물 정체성이 정확히 대응한다. 문헌은 실제 isolated/recrystallized product의 theoretical 대비 수율로, 모델값보다 조건이 완전하다. 별도의 특허 공정도 Pd/탄소·H₂ 기반에서 84.9%를 보고하지만 조건이 다르다. | PtO₂/H₂ 문헌과 모델 입력은 다르고, 모델 후보/실행에는 조건·분압·시간이 없다. 한 문헌 사례로 모델 정확도를 검증할 수 없다. | 추가 실행 전, 동일 reaction SMILES와 공식 checkpoint 재사용 가능 여부를 확인하고, 문헌 조건을 별도 baseline으로 기록한다. 새 추론은 승인 후에만 실행. |
| `route-02/step-01`: ethyl 4-acetamidobenzoate → ethyl 4-aminobenzoate; `CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1` | **77.70%**; raw `0.21513395` | 이번에 확보한 공식/1차 출처에서 이 **정확한 ethyl ester deacetylation**의 isolated yield와 완전 조건을 찾지 못했다. 검색된 생화학 논문은 p-acetamidobenzoic acid의 enzymic deacetylation을 다루지만 합성 단계의 비교 수율로 사용할 수 없다. | 반응 변환 자체는 명확하고 예측값은 원래 반응에 연결된다. 그러나 문헌값이 없어 수치 비교·오차 계산을 하지 않았다. | substrate form(ethyl ester), 산/염기/물, 온도·시간·workup, isolated yield가 미확인이다. p-acetamidobenzoic acid 문헌을 ester substrate에 전이할 수 없다. | 정확한 substrate와 deacetylation 조건을 포함한 primary procedure를 추가 검색한다. 후보가 없으면 실험 조건 없이는 문헌 비교를 종료한다고 기록한다. |
| `route-05/step-01`: `CC(=O)O>>CCO` (저장소에 기록된 acetic acid → ethanol) | **77.59%**; raw `0.21004525` | 이 변환과 동일한 benzocaine 합성 단계의 신뢰할 수 있는 isolated-yield 문헌을 확인하지 못했다. 벤조카인 경로 문헌은 ethanol을 PABA esterification의 reactant/solvent로 사용하며 acetic acid→ethanol을 보고하지 않는다. | 원래 반응 SMILES와 예측값의 연결은 유지한다. 그러나 이 숫자를 benzocaine route step 수율이나 ethanol 생성 수율로 해석할 문헌 근거가 없다. | route/template join 자체의 의도, 실제 starting material/product, omitted reagents, 수율 정의가 미확인이다. | 원본 route 생성 기록과 template mapping을 먼저 확인한다. 변환이 의도된 실험 단계가 아니면 문헌 수율 비교나 새 수율 추론 대상에서 제외한다. |
| `route-05/step-02`: PABA + ethanol → benzocaine; `CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1` | **79.80%**; raw `0.31552640` | McMaster Chem 2OB3 2004 procedure: PABA + 약 6 mL 95% ethanol + 0.5 mL concentrated H₂SO₄, reflux 60 min; 문서상 실험 절차는 확인되지만 이 검색 결과에는 대표 isolated %가 제시되지 않는다. 다른 공개 실험 자료는 PABA/ethanol/H₂SO₄ reflux 후 theoretical 대비 practical yield를 계산하도록 하지만 실험별 값이다. [McMaster manual](https://www.chemistry.mcmaster.ca/~chem2ob3/2004labmanual/2004_exp4.pdf) | 변환, reactants, product가 정확히 대응한다. 문헌은 실제 esterification 조건을 제공하므로 모델 후보와 별도 benchmark로 쓸 수 있다. 문헌 조건과 Parrot 출력의 일부 성분 겹침은 후보 검증이 아니다. | 문헌 수율의 정의·실험자·workup·purity가 자료마다 다르고, 현재 모델 입력에는 H₂SO₄ 농도·reflux·water removal·당량이 없다. | 정확한 primary procedure에서 numeric isolated yield가 있는 사례를 추가 확보한다. 그 뒤 문헌 조건과 모델 입력 차이를 표준 템플릿으로 비교한다. |

## 문헌 수율의 해석 규칙

Organic Syntheses의 91–100%는 재결정 후 theoretical amount 대비 isolated product 수율이다. McMaster 자료는 조건과 workup을 제공하지만 해당 PDF에서 대표 수율이 확인되지 않으므로 “문헌 수율 없음/조건만 확보”로 기록한다. 서로 다른 substrate, catalyst, purification, yield definition을 하나의 benchmark로 평균내지 않았다. 문헌 한 사례와 예측값의 차이를 모델 전체 MAE나 calibration으로 해석하지 않았다.

## 추가 공개 모델·체크포인트 조사

### 현재 checkpoint의 재사용

가장 낮은 비용의 대안은 기존 `rxn_yields` checkpoint와 이미 기록된 reaction SMILES를 그대로 재사용하는 것이다. 저장소의 `model-assets.lock.json`과 `yield-normalization.json`이 가중치 hash, source commit, gram random domain, normalization statistics를 기록하므로, 새 추론을 하더라도 입력·checkpoint·역정규화를 고정할 수 있다. 다만 재실행은 정확도 검증이 아니라 실행 재현/민감도 확인이다.

### 조사한 대안

1. **YieldBERT/YieldBERT-DA (`rxn_yields`)**: 공식 README와 논문은 reaction SMILES 기반 yield regression, random/time split, MAE/RMSE/R² 및 augmentation uncertainty를 설명한다. 공개 checkpoint가 있어도 이번 네 단계의 target-domain accuracy를 자동 보장하지 않는다. 기존 checkpoint와 다른 augmentation/ensemble을 실행하려면 해당 모델 파일·tokenizer·환경·normalization과 추가 inference 비용이 필요하다.
2. **Buchwald–Hartwig 전용 공개 benchmark**: `rxn_yields` 자료와 관련 논문에는 Buchwald–Hartwig와 Suzuki–Miyaura benchmark가 있으나, 현재 네 단계 중 route-01은 nitro reduction, route-02 deacetylation, route-05 esterification/불명확 변환이다. 전용 B–H checkpoint를 네 단계에 적용하는 것은 반응 유형 불일치이므로 대안으로 채택하지 않는다.
3. **ReaMVP, YieldFCP, graph yield models**: 공개 코드/논문은 다른 pretraining, feature, split 또는 benchmark를 사용한다. 모델명만으로 이 프로젝트의 네 반응에 적합하다고 판단할 수 없고, 현재 보관 checkpoint·환경·정규화와 호환되는 verified artifact를 확인하지 못했다. 따라서 설치·다운로드·실행 후보로 승격하지 않았다.

## 승인 후 실행 가능한 계획

| 우선순위 | 실행 | 필요한 자료 | 자원/비용 | 평가 |
|---|---|---|---|---|
| 1 | 기존 checkpoint로 네 reaction SMILES 재추론 및 byte/hash 비교 | 기존 checkpoint, tokenizer, Python 3.8.20, torch/transformers/rxnfp 버전 | 기존 환경 재사용; 새 다운로드 없음 | 기존 raw 값과 exact match, normalization 재계산; 정확도 검증 아님 |
| 2 | 동일 checkpoint의 SMILES randomization/augmentation 민감도 평가 | 공식 YieldBERT-DA 코드와 augmentation 설정, 동일 checkpoint 또는 compatible weights | CPU/GPU 시간은 사전 확인 필요; 새 모델 파일이 없으면 실행 불가 | 예측 분산/범위만 보고; 신뢰구간으로 과장하지 않음 |
| 3 | 문헌 조건을 reaction SMILES에 섞지 않고 별도 metadata 표로 비교 | 각 단계의 primary procedure, isolated yield 정의, 조건·workup | 조사 작업; 계산 불필요 | 단계별 조건 차이와 yield definition 차이 감사 |
| 4 | route-02/route-05-step01의 원본 route/template 검증 | source route JSON, template provenance, 실제 실험 계획 | 로컬 파일 확인 | 변환 자체가 유효한 비교 대상인지 판정 |

현재는 사용자 승인 전이므로 새 추론·계산·설치를 수행하지 않았다. 특히 문헌값이 없는 route-02와 route-05/step-01에 임의 수율이나 신뢰구간을 만들지 않았다.

## 현재 결론

- route-01은 동일 변환에 대한 1차 문헌 수율과 조건이 있어 가장 강한 외부 비교 근거를 확보했다. 그러나 catalyst와 조건이 달라 모델 정확도 검증은 아니다.
- route-05/step-02는 동일 변환의 실험 조건 문헌은 있으나, 현재 확보 자료에서 대표 numeric isolated yield가 부족하다.
- route-02는 정확한 substrate/변환의 comparable synthetic yield가 부족하다.
- route-05/step-01은 반응식의 route 의미부터 확인해야 하며, 수율 비교 대상이라고 확정할 수 없다.
- 공개 대안 모델은 조사했지만, 현재 네 단계에 대해 기존 checkpoint보다 검증된 우위를 보이는 실행 가능한 모델/체크포인트는 확인하지 못했다.

