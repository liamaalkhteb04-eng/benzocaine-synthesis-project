# 학교 PC 검토 자료 — 2026-11-24

집 PC에서 이어보기 위한 공개용 검토 묶음이다. 원래 보고서, 스킬, 원시 결과, 모델 가중치, 가상환경은 이 커밋에 포함하지 않는다.

## 완료한 검토

- [수율 적용성](yield-applicability-review.md): USPTO gram-scale YieldBERT checkpoint의 입력·학습 범위·정규화와 네 단계별 적용 한계를 정리했다.
- [수율 보완](yield-improvement-review.md): 네 예측값과 원래 반응을 유지하고, Organic Syntheses/McMaster 문헌 조건·수율 정의를 별도 비교했다. 새 추론은 실행하지 않았다.
- [Parrot 조건](parrot-condition-review.md): 대표 후보의 원시 슬롯·rank·SMILES를 보존하고 물질 정체성과 실험 역할을 구분했다.
- [route-05/step-01 provenance](route05-step01-provenance-review.md): `CC(=O)O>>CCO`가 route tree의 ethanol 공급 branch를 forward yield query로 materialize한 것임을 확인했다. 유효한 실험 수율 비교 대상에서는 제외했다.
- [수율·EPI 통합 요약](yield-epi-integration-review.md): 수율의 보고서 사용 범위와 EPI MP/BP 모델 추정값·DB 값을 구분했다.
- [Visualizer 최소 보완 준비](visualizer-route05-measurement.md): PABA conformer 4와 ethanol conformer 2의 구조·원자 번호 사본을 준비했다.

## 판단 보류 및 미수행 작업

- 수율 모델의 target-specific 정확도, 신뢰구간, 실험 수율 검증은 미확인이다.
- route-02의 정확한 deacetylation 문헌 수율은 확보하지 못했다.
- route-05/step-01은 route graph 연결은 확인했지만 실제 acetic acid→ethanol 합성 단계로 검증하지 않았다.
- EPI 순물질 MP/BP만으로 반응 용액의 석출·기화·반응성을 판단하지 않았다.
- 같은 수율 checkpoint 재실행, augmentation, 대안 모델 설치는 하지 않았다.
- Visualizer는 구조·원자 매핑 준비까지만 완료했다. 새 두 분자 관찰·측정·캡처는 수행하지 않았다.
- Visualizer·MOPAC의 추가 작업은 이 커밋 범위에 포함하지 않았다.

## 집에서 이어갈 순서

1. 이 README와 각 문서를 먼저 읽는다.
2. 필요하면 원래 저장소의 `reports/benzocaine-final/evidence-run/`와 `analyses/epi-suite/`, `analyses/visualizer/`를 로컬에서 대조한다.
3. 수율은 먼저 route-02 문헌 근거와 route-05/step-01 route generator provenance를 확인한다.
4. 실행을 승인할 때만 기존 checkpoint 재현성/augmentation 여부를 별도로 결정한다.
5. 그 다음 EPI의 mixture phase-behavior 필요성을 검토한다.
6. Visualizer는 GUI가 가능한 환경에서 PABA C6–ethanol O3 설명용 상대 배치를 측정하되, 반응 복합체나 장벽으로 해석하지 않는다.

## 공개 사본·보안 점검

공개 폴더에는 개인 절대 경로, 이메일, API 키, 인증정보, 모델 가중치, 가상환경을 넣지 않았다. 공개가 불명확한 강의 원문과 가중치는 복사하지 않고 문서 내 출처 URL로 남겼다. Visualizer 구조 사본은 공개 검토에 필요한 PABA/ethanol conformer 입력만 포함한다.

