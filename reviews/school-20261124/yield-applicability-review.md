# 수율 모델 적용 가능성 평가 — 학교 PC 확인본

작성일: 2026-11-24  
기준 저장소 커밋: `801ace04d7e9ca528584c41429712faa0c84f399`

## 결론

이 검토에서 확인 가능한 결론은 **수율 예측 실행과 역정규화는 재현·추적되지만, 네 단계에 대한 모델 적용 가능성(정확도 또는 화학적 성공률)은 판정 불가**라는 것이다. 모델은 반응 SMILES만 입력받았고 Parrot 조건, 온도, 시간, 당량을 입력받지 않았다. 따라서 출력값은 해당 입력에 대한 모델 예측값이지 실험 수율이나 조건부 성공 확률이 아니다.

특히 `route-05/step-01`의 `CC(=O)O>>CCO`는 화학적으로 아세트산에서 에탄올로 가는 형태의 반응 SMILES이며, 일반적인 벤조카인 합성 단계의 실제 변환을 대표한다고 보기 어렵다. 이 단계의 77.59%를 실험 수율처럼 해석하거나 route 전체의 수율로 곱하면 안 된다.

## 증거 출처의 구분

### 집 PC에서 사용자에게 전달받은 사실

- 수율은 `benzocaine-live-20261031-03`에서 생성되었고 run 04와 최종 보고서가 재사용했다.
- 체크포인트는 `uspto_gram_random_test_epochs_2_pretrained/checkpoint-19762-epoch-2`이다.
- 보관 가중치 해시와 당시 실행 기록이 일치한다.
- 반응 SMILES를 입력했고 Parrot 조건은 별도로 전달하지 않았다.
- 원시 출력의 역정규화 결과가 대표 네 단계의 보고서 값 82.95%, 77.70%, 77.59%, 79.80%와 일치한다.
- 당시 전체 설정 파일과 의존성 버전 일부는 미확인이다.
- 이 작업 전에는 적용 가능성 자체를 판정하지 않았다.

### 학교 PC에서 저장소로 직접 확인한 사실

- 커밋 `801ace04…`로 체크아웃되었다.
- `configs/model-assets.lock.json`은 `rxn_yields`의 source commit을 `d9e6b87ce1b881978490d68bfc00021e3b48127a`, 가중치 SHA-256을 `2931dab333037a120ec4ec4de9ea91a4cd27da5caf0173b16e8b224e1c982fbb`로 기록한다.
- `configs/yield-normalization.json`은 학습 영역을 `USPTO gram-scale random split`으로, 출력 단위를 `standardized_fraction`으로 기록한다. 평균은 `0.7318926847478698`, 표본 표준편차(ddof=1)는 `0.20946128682168402`이다.
- `reports/benzocaine-final/evidence-run/reproducibility-manifest.json`은 routes와 yield 파일이 run 03에서 run 04로 재사용되었고, run 04에서 세 번의 새 yield 추론을 했다는 뜻이 아니라고 명시한다.
- `reports/benzocaine-final/evidence-run/latest-route-reproduction/yields-rxn_yields.json`은 네 대표 단계의 원시값과 역정규화값을 직접 기록한다. 네 값은 각각 82.9537143%, 77.6954919%, 77.5889033%, 79.7983250%이다.
- 같은 파일은 네 단계 모두 `yield_status: predicted_not_validated`, `applicability: not_assessed`, `conditions_in_input: false`로 기록한다.
- 저장소의 최종 manifest는 “actual output integrity and joins; no experimental/target-domain accuracy validation” 범위라고 제한한다.

## 모델과 수율 정의

공식 `rxn_yields` 자료는 YieldBERT 계열이 반응 SMILES로부터 수율을 회귀한다고 설명한다. USPTO 데이터 탐색 자료는 `yields_above_200622.tsv`에서 `calc_yield / 100`을 학습 레이블로 만들고 gram-scale과 milligram-scale을 구분한다. 저장소의 정규화 기록에 따르면 이 실행의 모델 출력 `raw_z`는 다음으로 복원되었다.

```text
yield_percent = 100 * (raw_z * 0.20946128682168402 + 0.7318926847478698)
```

이 계산은 숫자 단위와 provenance를 확인하는 데 유효하지만, 정확도나 외삽 가능성을 증명하지 않는다. 공식 논문도 평가를 별도의 test set에서 MAE/RMSE/R² 등으로 수행한다. 현재 네 벤조카인 단계에 대해 그런 독립 실험값, 표적 유사도/거리, 단계별 calibration, 불확실성 검증은 저장소에서 확인되지 않는다.

## 네 단계별 평가

| 단계 | 저장소에서 확인된 입력/출력 | 적용 근거 | 주요 한계 | 판정 |
|---|---|---|---|---|
| `route-01/step-01` | `CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1`; 82.9537% | 반응 SMILES가 완전하고 토큰 수 46/300이며 물리적 범위 안이다. nitro→amine이라는 구조 변환을 표현한다. | 모델 학습 분포에서 이 변환의 유사 반응 포함 여부, target-domain 거리, 조건·촉매·수소원 반영 여부, 독립 실험 비교가 확인되지 않았다. | **수치 산출 가능; 적용 가능성 판정 불가** |
| `route-02/step-01` | `CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1`; 77.6955% | 반응 SMILES가 완전하고 토큰 수 47/300이며 deprotection 형태를 표현한다. | 실제 반응 조건이 입력되지 않았고, 학습 데이터의 해당 변환·기질 유사도와 표적별 성능이 확인되지 않았다. | **수치 산출 가능; 적용 가능성 판정 불가** |
| `route-05/step-01` | `CC(=O)O>>CCO`; 77.5889% | 형식적으로 유효한 반응 SMILES이고 토큰 수 13/300이다. | 아세트산→에탄올 변환은 벤조카인 경로의 화학적 핵심 단계를 나타내지 않는다. template-derived route의 산출물이며, 학습 분포·실험적 의미·조건이 확인되지 않았다. | **화학적 적용 근거 부족; 보고서 수율로 사용 불가** |
| `route-05/step-02` | `CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1`; 79.7983% | 산과 에탄올의 esterification 형태를 SMILES로 표현하고 토큰 수 43/300이다. | 첨부된 condition 후보는 yield 모델 입력이 아니며, 실제 산 촉매·탈수 조건·당량·시간·온도와 연결되지 않는다. template disconnection이고 omitted agents가 복원되지 않았다는 저장소 caveat가 있다. | **수치 산출 가능; 조건부 실험 수율로 해석 불가** |

## 무엇이 추가로 필요할까

적용 가능성을 더 강하게 판정하려면 최소한 다음이 필요하다.

1. 정확한 checkpoint 디렉터리의 전체 파일과 SHA-256, tokenizer/config/model args, 실행 환경의 패키지 잠금 기록.
2. 네 반응과 학습 데이터의 원본 반응 SMILES 중복·유사도·scaffold/반응 클래스 분포 및 시간 분할/외부 테스트 성능.
3. 네 단계 각각의 실제 실험 수율과 실험 조건(촉매, 용매, 시약, 당량, 온도, 시간, workup/purification 정의).
4. 동일한 입력 정의로 수행한 독립 벤치마크와 불확실성 또는 calibration 결과.
5. `route-05/step-01`이 실제 계획된 반응인지, 잘못된 template/route join인지 확인할 원본 route 생성 근거.

현재 자료만으로는 “모델이 이 단계에서 적용 가능하다” 또는 “예측 수율이 실제 수율을 대표한다”고 결론내릴 수 없다. 안전한 보고서 문구는 **“USPTO gram-scale random-split YieldBERT 체크포인트가 반응 SMILES 기반 예측값을 생성했고, 실행 무결성과 역정규화는 확인되었으나 표적 단계별 적용 가능성과 실험 수율 정확도는 검증되지 않았다”**이다.

## 기존 파일 보존

이 폴더만 새로 만들었으며 `reports/benzocaine-final/`, `skill/`, 원시 결과 파일은 수정하지 않았다. 집 PC에서 만든 `yield-applicability-review` 폴더는 저장소에서 확인되지 않았다.

## 출처 URL

- 프로젝트 저장소: https://github.com/liamaalkhteb04-eng/benzocaine-synthesis-project/tree/801ace04d7e9ca528584c41429712faa0c84f399
- rxn_yields 공식 저장소: https://github.com/rxn4chemistry/rxn_yields
- rxn_yields 학습 코드(정규화): https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/training_scripts/launch_uspto_training.py
- USPTO 수율 탐색/학습 입력: https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/nbs/02_uspto_data_exploration.ipynb
- 공식 학습 데이터 안내: https://ibm.ent.box.com/v/uspto-yields-data
- YieldBERT 논문: https://pmc.ncbi.nlm.nih.gov/articles/PMC8750748/
- 공개 모델 목록: https://github.com/rxn4chemistry/rxn-models/blob/main/README.md

