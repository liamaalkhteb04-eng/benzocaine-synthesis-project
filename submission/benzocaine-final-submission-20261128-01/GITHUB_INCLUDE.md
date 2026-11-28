# GitHub 반영 대상

기존 제출본과 원시 기록은 유지하고, 최종 폴더 `submission/benzocaine-final-submission-20261128-01/`의 공개용 파일을 추가 후보로 삼는다. 파일명만 바뀐 확정PDF/DOCX는 원본과 같은 바이트다.

현재 저장소 첫 화면을 위해 루트 `README.md`, `archive/README.md`, `archive/history/.gitignore`, `archive/legacy-submissions/.gitignore`도 반영 대상이다. 루트의 다른 기존 미커밋 코드·설정·스킬은 이번 대상에 섞지 않는다. 이전 중복 패키지는 `archive/legacy-submissions/`에 로컬 보관하며 그 내용은 반영 대상에서 제외한다.

- `README.md`, `GITHUB_INCLUDE.md`, `GITHUB_FILES.txt`, `PACKAGE-MANIFEST.json`, `PACKAGE-MANIFEST.sha256`
- `.gitignore`, `.gitattributes`, `.env.example`, `requirements-report.txt` (패키지의 줄바꿈 변환을 막아 보호 해시를 유지)
- `report/`: `20251312_리야마_벤조카인_최종보고서.pdf/.docx`·최종 원고·확정 그림13개·현재 자료 링크
- `skill/`: 실제 관련 일반 스킬·참조 지침·기존 수정 모드 이력
- `data/`: 저장 근거·CSV·원자/결합·하네스 사실·최종 압력 정정 overlay
- `code/`: 저장 원고 재조판·Word출력·PNG복원·패키지 점검
- `configs/`: 빈 승인/보고서 설정 예시·외부 화학 자산 식별 예시
- `authoring/section-pipeline/`: 새 작성 시험용 코드·근거·스킬. 승인된 즉시 실행이나 반복 재현 성공을 뜻하지 않음
- `provenance/`, `validation/`: 마지막 실제 교정의 증거와 패키징 점검·이동성 기록
- `archive/baselines/`, `archive/history/`, `archive/duplicates/`, `archive/README.md`: 필요한 교정 전 기준 원고·과거 시안/수정 이력·출처·중복 자산. 보관하되 현재 작성 입력과 구분

제외: `work/`와 `archive/local-checks/`(로컬 경로/오프라인 준비 smoke 결과), `.env`, `private/`, 실제 승인서, 가상환경, 캐시·`__pycache__`, 체크포인트·stock·원문 수업PDF 및 재배포 조건 미확인 문헌 스캔. 원래 저장소의 다른 수정 파일을 함께 반영하지 않는다.

실제 파일별 상대경로는 [GITHUB_FILES.txt](GITHUB_FILES.txt), 해시는 [PACKAGE-MANIFEST.json](PACKAGE-MANIFEST.json), 점검 결과는 [validation/package-check.json](validation/package-check.json)에 있다. 반영 대상 목록과 실제 commit·push·원격 검증 기록은 구분한다.

[저장소 기준 전체 반영 경로](GITHUB_REPOSITORY_FILES.txt) · [이번 정리 전후·보존 기록](validation/reorganization-final.json). 파일 수를 줄이기 위해 필요한 자료를 영구 삭제하지 않았다.
