# 경로 규칙

- 실행 코드·보고서 파일 링크·스킬 참조는 제출 폴더 상대경로를 쓴다.
- `${AIZYNTH_PYTHON}` 등 환경변수는 수신자가 설정할 외부 환경 예시다. 모델 경로를 임의로 채우지 않는다.
- `external-originals/`는 비공개 원래 PC 경로가 있었다는 과거 기록 표시이며 존재하는 실행 디렉터리가 아니다. 일부 과거 문서의 `reviews/...`, `evidence-run/...` 같은 일반 문자열도 원래 저장소에서의 출처 위치다. 실제로 열 파일은 report/records/source-index.md의 제출 폴더용 링크와 provenance/package-copy-map.json에서 찾는다.
- 최종 PDF·DOCX·원고와 보호용 baseline 원고는 원본 바이트 그대로다. 출처 원시 파일도 원래 저장소에서는 수정하지 않았다. 공개 복사본에서 PC 홈 경로만 표시화한 파일은 별도 이력과 source/current hash를 구분했다.
- `.env.example`은 빈 키 예시이며 실제 `.env`·모델 가중치·개인 환경·기존 승인서는 포함하지 않는다.
