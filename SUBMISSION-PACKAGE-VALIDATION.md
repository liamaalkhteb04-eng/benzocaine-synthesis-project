# 제출 패키지 오프라인 검증

검증일: 2026-11-21 (UTC)

## 고정한 보고서

후보 원본은 `reports/benzocaine-route01-co-cleanup-20261121/report.pdf`와 `report.docx`입니다. 제출 패키지에는 파일명만 읽기 쉽게 정리해 `reports/benzocaine-final/`에 복사했습니다. 복사 전후 SHA-256이 일치합니다.

- PDF: `4d5521f3594706453ee413f0c7cfc1edf952ca4ae44b66eb9f1ddb6e27cf7445`
- DOCX: `b8b408829f833848bfcd422697f7ca0035f9be11d299fc30fe4c757a43dee926`

후보 보고서의 과학 본문·수치·그림·표는 수정하지 않았습니다.

## 스킬과 Solar 요청 구성

- 전체 파이프라인 스킬: `skill/SKILL.md`
- 보고서 작성 스킬: `skill/report-writing/SKILL.md`
- 과거 Solar 실행에서 사용한 스킬: `provenance/skills/`에 원본과 해시·경로 대응표를 보존했습니다. 현재 스킬을 과거 보고서의 작성 지침으로 소급 표시하지 않습니다.
- `validation/offline-authoring-request-check.json`은 패키지 복사본에서 준비한 Solar 요청을 실제 전송 없이 검사한 결과입니다. system 메시지가 현재 보고서 스킬과 일치하고, user 메시지에 사용자의 물질 선택 근거, 구조 정체성, route/step/reaction 연결 키, 조건·수율, 문헌·강의 근거, MOPAC·EPI Suite·Visualizer·하네스 자료, figure manifest와 citation source map이 들어갔음을 확인했습니다.
- 요청 준비 명령의 출력은 `prepared_not_sent`, 외부 요청 0회입니다. 현재 스킬의 Solar 응답 품질은 실호출로 검증하지 않았습니다.

## 저장 응답에서 문서 재생성

`reports/rebuild-check-02/`의 DOCX/PDF는 저장된 `report-source.md`와 기존 증거를 사용해 다시 조판한 결과입니다. 새 Solar 요청이나 화학 추론은 없었습니다.

- PDF 20쪽, 20쪽 렌더 미리보기와 전체 contact sheet 존재
- 원본과 재생성 PDF의 정규화 텍스트 동일
- 원본과 재생성 DOCX의 문단·표 텍스트 동일
- 그림 10개, 표 4개, 잘림 항목 0개
- 메탄올 구조 정체성 문구 확인, 이전 CO 오기 문구 부재
- `document-rebuild-validation-initial-failed.json`에 PDF 한글 텍스트 추출만으로 참/거짓 문구를 검사해 생긴 최초 오판을 보존했습니다. `document-rebuild-validation-corrected.json`은 DOCX 텍스트 직접 검사와 PDF 전체 추출 텍스트 동등성으로 정정한 통과 기록입니다.

시각 검토는 전체 페이지 contact sheet와 5쪽 확대 화면에서 수행했습니다. 이 검증은 저장 원고의 문서 재생성을 확인한 것이며, 최신 스킬로 새 Solar 보고서를 작성했을 때의 문장 품질이나 새 PC의 설치 재현을 보증하지 않습니다.

## 새 물질 보고서 실행기의 오프라인 검사

패키지 `scripts/generate_report.py`도 호출 수·입출력 한도, VAT 포함 최악 예약액, 24시간 이내의 검증된 무료 크레딧 전용 snapshot, 기본 비활성 config를 검사하도록 연결했습니다. 기존 벤조카인 실행 산출물을 읽기 전용 복사해 증거 JSON을 결정론적으로 다시 만들고 요청 준비까지 확인했습니다. 7개 예산 가드 단위 검사가 통과했고, 기본 설정의 실제 `--execute-solar` 시도는 승인 플래그 부재로 네트워크 전에 거부됐습니다. API 응답 파일은 생성되지 않았습니다. 상세 기록은 `validation/report-wrapper-budget-smoke-03/validation.json`입니다. 이 검사는 새 화학 추론이나 새 Solar 호출이 아닙니다.

## 공개 사본 정리

- `.env`, 실제 API 키, 가상환경, 대용량 모델 가중치는 포함하지 않았습니다. `.env.example`만 포함합니다.
- 강의자료 및 논문·특허 원문 파일은 재배포 권한을 확인할 수 없어 제외하고, 출처·페이지·확보 방법을 메모로 제공합니다.
- 텍스트 기록의 Windows 사용자 경로는 패키지 사본에서만 익명화했습니다. 원본은 그대로 두고 `provenance/package-redaction-map.json`에 소스/사전 사본/익명화 사본 해시를 연결했습니다.
- 이메일 패턴, 사용자 프로필 절대경로, 비어 있지 않은 `UPSTAGE_API_KEY` 설정은 패키지 텍스트에서 발견되지 않았습니다.
- README 상대 링크와 필수 스킬·입력·설정·의존성·모델 준비 안내를 오프라인 검사했습니다. 전체 package SHA-256 목록은 `PACKAGE-MANIFEST.json`, 그 매니페스트 자체 해시는 `PACKAGE-MANIFEST.sha256`입니다.

## 아직 검증하지 않은 작업

- 현재 스킬로 Solar Pro 4를 새로 호출해 보고서 응답 품질을 확인하는 일
- 새 물질 또는 새 PC에서 예측·설치·문서 전체 파이프라인을 실행하는 일
- 모델 가중치와 전체 AiZynthFinder 재고 데이터 취득 및 체크섬 검증을 다른 PC에서 수행하는 일
- GitHub 커밋/push와 학교 과제 제출
