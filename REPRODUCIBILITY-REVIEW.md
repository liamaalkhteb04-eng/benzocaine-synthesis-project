# 재현성 점검 기록 — 제출 정리본 (2026-11-15)

이 문서는 이번 Desktop/GitHub 제출 사본에서 실제 확인한 재현 범위와 한계를 요약한다. 코드·기록의 run ID와 모델 자산 식별자는 원시 기록에서 그대로 유지했다.

## 저장된 응답으로 DOCX/PDF 재생성 — 실행 확인

- 최신 입력은 `reports/benzocaine-page-layout-and-instruction-cleanup-20261115/report.md`, `solar-call/solar-response.raw.json`, `solar-call/solar-status.json`, `merge-validation.json`, `evidence-run/`이다.
- 인용 감사가 통과했고, 기존 저장 응답으로 DOCX 및 Microsoft Word PDF를 오프라인 재생성했다. Solar API와 화학 모델은 호출하지 않았다.
- 제출용 이름으로 재생성한 DOCX와 PDF는 각각 19쪽이다. DOCX에서 구조 그림 10개와 표 4개를 확인했고, PDF 전체 페이지의 텍스트/그림 경계·핵심 SMILES·조건/수치·링크·작성 지시문 검사를 통과했다. 통합 조건·수율 표 제목과 표가 같은 쪽에 있다. 세부 결과: `reports/benzocaine-page-layout-and-instruction-cleanup-20261115/document-validation.json`, `citation-audit-repacked.json`, `word-export.json`.
- 이 제출 사본을 위해 바뀐 보고서 문장은 강의 PDF 및 문헌 스캔의 로컬 경로를 공개 패키지 안의 원문 확보 안내로 연결하는 부분뿐이다. 분석·수치·그림·결론은 바꾸지 않았다. 대응 기록은 `경로대응표.md`에 있다.

## 벤조카인 로컬 예측 재실행 — 같은 PC/같은 물질만 확인

- 제출 코드의 정상 진입점으로 `benzocaine-live-repro-20261105-01` 실행 결과를 보존했다. AiZynthFinder·Parrot·Yield-BERT의 상태, route_id/step_id 정합성, 단계 예측과 원시 로그는 `results/benzocaine-live-repro-20261105-01/`에 있다.
- 대표 기준 실행 `benzocaine-live-20261031-03` 및 `-04`와의 자산·설정 대조는 재실행 보정 기록에서 확인한다. corrected validation과 상충했던 원본 기록을 둘 다 보존했다. 설정 JSON 바이트 해시는 다르고, 경로 구분자 정규화 후 설정 객체는 같으며, 바이트 차이의 정확한 원인은 미확정이다.
- 이것은 기존 PC의 벤조카인 입력 재실행이다. 다른 물질이나 신규 PC의 추론 검증으로 확대 해석하지 않는다.

## 자산·도구 사전검사 및 한계

- 입력 구조, runtime imports, 체크포인트/모델 해시, normalization metadata와 AiZynth stock bucket manifest는 기록된 기존 자산에 대해 점검했다. 체크섬과 당시 로컬 경로는 `validation/model-asset-reuse-audit-20261105.json`, `validation/model-preflight-repro-20261105-01.json`에 있다. 패키지에는 가중치·가상환경·약 0.5 GB의 stock bucket을 복사하지 않았다.
- 타 PC 설치는 공식 upstream 안내에 따라 사용자가 실행해야 한다. 이번 정리에서는 설치·새 물질 추론·Solar 호출을 하지 않았다.
- 저장된 보고서 재생성은 실행 검증했고, 새 물질 입력 경로는 코드와 안내를 점검했으나 이 검증 작업에서 새 분자 추론은 수행하지 않았다.

## 공개 자료 제외

재배포 조건이 확인되지 않은 수업 원문 및 문헌 스캔은 GitHub 사본에서 제외했다. 출처 URL, 제목, 인용 페이지, 원본 해시와 확보 방법은 `reports/benzocaine-page-layout-and-instruction-cleanup-20261115/evidence-run/course-material-acquisition.md`와 D9의 `source-acquisition.md`에 있다. 전체 원본은 기준 프로젝트에 그대로 보존되어 있다.

새 물질 추론, 새 Solar 호출, 새 프로그램 설치, GitHub 저장소 생성/푸시, 학교 제출은 수행하지 않았다.

## 문서 렌더러 일반화 회귀 확인 — 2026-11-18

- 아세트아미노펜은 기존 PC의 `acetaminophen-live-20261115-01` 결과와 저장 Solar 응답 `acetaminophen-report-live-20261117-02`를 재사용했다. 현재 렌더러가 manifest의 정확한 figure ID·파일 해시로 그림 5개를 연결하고, 검증된 route/step·반응 SMILES·Parrot 슬롯·수율 자료에서 표 4행을 생성했다. 코드가 과학적 문장을 다시 쓰지 않았다.
- DOCX/PDF가 각각 생성됐고, 검증기는 PDF 10쪽, 그림 5개, 단계 연결 4개, 누락·잘림 0건을 확인했다. 전체 페이지 미리보기 파일도 해당 검증 결과와 함께 로컬 검증 작업공간에 보존되어 있다. 공개 요약과 SHA-256은 `validation/acetaminophen-document-render-regression-20261118.json`이다.
- 이 렌더링 때 Solar API와 화학 모델을 호출하지 않았다. 다만 이 물질의 예측 및 Solar 본문 작성은 앞선 실행에서 성공한 저장 결과이며, 본 확인은 저장 응답 문서화의 재현이다.
- 벤조카인 저장 보고서를 별도 임시 출력 폴더에서 재생성했다. DOCX는 그림 10개·표 4개, PDF는 19쪽이며 문서·인용 검사가 통과했다. 처음엔 패키지 기본 인용표를 적용해 [17]을 잘못 판정했으나, 해당 보고서와 함께 보관된 인용표([17]=강의자료)를 사용하도록 검증기를 일반화한 뒤 같은 산출물 검사가 통과했다. 초기 실패도 덮어쓰지 않고 `validation/benzocaine-document-render-regression-20261118.json`에 남겼다.
- 기존 벤조카인 최종 PDF/DOCX는 기록된 SHA-256과 현재 파일 SHA-256이 일치한다. 회귀 작업은 별도 임시 디렉터리에서 수행했으며 최종 파일을 수정하지 않았다.
- 두 물질 모두 기존 PC에서 확인된 범위다. 새 PC 설치·재현 및 모든 물질 입력에 대한 성공 보장은 하지 않는다. 아세트아미노펜의 MOPAC·EPI Suite·Visualizer·하네스 분석도 수행되지 않았다.

이번 저장소 갱신에서는 새 모델 추론, Solar 호출, 프로그램 설치, 학교 제출을 수행하지 않는다. GitHub 반영 여부는 해당 변경 작업의 별도 기록을 따른다.

## ?? ??? ??????? ??

- ?? ??? ??? ??? ?? ??? ?? ?? 0?, ???? ??? ?? 0??? ????.
- ?? ??? ?? ???????? ?? PC ?? ??? ?????. ??? ?? Git blob? ?? ???? SHA-256 ??? `validation/privacy-redaction-log-20261118.json`? ????. ?? ????? ?? ???? PDF/DOCX? ????.
- ?? ?? ?? ??? ?? ?? ?? ???? ?? ????. ?? ???? ??? ???? ??? ???? ??? ????? ??? ???? ?? ???? ????.
