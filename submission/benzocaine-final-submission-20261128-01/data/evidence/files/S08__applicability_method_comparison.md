# 실제 실행과 공식 방식의 대조

| 비교 항목 | 공식 방식 | 실제 실행 | 판정 | 근거 |
| --- | --- | --- | --- | --- |
| 입력 형식 | Official: reconstructed molecules>>products strings, tokenized by rxnfp family. | Actual: same two-sided string form; four strings parsed and counts<300. | 형식은 설계와 양립한다. SMILES-only라는 사실 자체는 부적합 근거가 아니다. | S4;S8;S9;S12 |
| 입력 성분 | Official left column retains all recorded molecular components, which may include agents/solvents. | Actual: retrosynthetic precursor strings; no extra Parrot fields; omitted agents not reconstructed. | 구분자가 같아도 정보 완결성은 같지 않다. 누락 성분의 영향은 미확인이다. | S4;S12; applicability_training_input_example.csv |
| 수치 조건 | Official descriptor has no explicit T/time/pressure/concentration/scale numerical fields. | Actual also lacks these separate fields. | 공식 방식과 공통된 한계다. 특정 Parrot 조건에서의 실험 수율로 읽을 수 없다. | S8;S12 |
| 수율 라벨 | Patent-reported/extracted percent, canonical duplicate averaging; train fraction scaling. | Actual raw_z is inverse-standardized back to percent with matching train constants. | 라벨 스케일은 일치한다. 균질한 분리수율·순도·성공확률을 뜻하지 않는다. | S2;S4;S5;S10;S12 |
| 학습/검증 분할 | Unsmoothed gram random train/test flags; broad patent scope, not BH HTE split. | Actual four inputs not found by declared exact/canonical search in this table. | 공개 fine-tuning 표에서 미발견. 전 학습 노출과 인접 반응 지원은 별도 미확인이다. | S1;S10;S11 |
| 추론 구현 | Official wrapper aliases rxnfp SmilesClassificationModel; args max_seq_length300. | Actual direct HF regression head, eval/no_grad, batch8, max300, tokenizer warning. | 일반 구조는 양립하지만 wrapper/전처리의 수치적 동등성까지 검증한 것은 아니다. | S9;execution_facts.csv |
| 성능과 판정 | Exact checkpoint stored R2≈0.117; no per-query validation record. | Actual successful outputs and matching inverse; no independent four-step yield benchmark. | 실행·산술 확인은 통과한다. 화학적 정량 신뢰도나 경로 순위 검증은 성립하지 않는다. | S6;S7;S12 |
