# 최종 보고서 조립 이력

이 기록은 현재 후보 보고서가 하나의 단일 Solar 응답에서 나온 것처럼 표시하지 않도록 응답·교정 블록·코드 조립을 구분합니다. 각 source hash는 해당 실행 당시 기록된 원본 해시입니다. 공개 사본의 파일 해시는 `PACKAGE-MANIFEST.json`과 `package-source-map.json`을 기준으로 확인합니다.

| 순서 | 내용 | 실행 ID / 원본 연결 | 조립·검증 |
|---|---|---|---|
| 1 | 전체 보고서 초안 | `benzocaine-report-reproduction-20261119-01`; 요청 manifest와 원시 응답은 `solar-author-request-input-manifest.json`, `solar-author-request.redacted.json`, `solar-author-response.raw.json` | 본문은 Solar가 작성. 당시 응답의 누락·한계는 이후 검증 기록에 남음. |
| 2 | 강의 비교 블록 | `solar-course-insert-01`; request, response, status, section validation 보존 | 강의 요약과 원문 PDF는 구별. 공개 패키지는 요약·LMS 확보 안내만 포함. 블록 조립 및 route matrix는 composition 기록과 `build_route_comparison_matrix.py` 결과로 연결. |
| 3 | 지정 교정 블록 5개 | run `benzocaine-correction-v3-20261120-02`, attempt `solar-correction-v3-02`; 원시 응답 SHA-256 `5eba76f87a081d19a1250d09dd5bb4933ae3b79113a7427def3439043d1e2231` | 원문 block text/hash는 `accepted-blocks-v3-02.json`에 보존. 해당 호출의 skill excerpt는 `correction-v3-02/skill-excerpt-transmitted.md`에 별도 보존. |
| 4 | route-05 후보 범위와 §4.4 문장 | run `benzocaine-correction-v3-20261120-03`, attempt `solar-correction-v3-03`; response/validation/request 보존 | `route05-count-merge-provenance.json` 및 `previous-solar-correction-v3-03-captured.json`에 교체 범위와 기계적 marker·인용 정규화 기록. |
| 5 | route-05 후보 개수 문장 | run `benzocaine-route05-count-correction-20261121-01`, attempt `solar-route05-count-correction-01`; request/response/validation 보존 | route-05 전체 후보 15개 중 표시한 rank 1–3만 기술한다는 교정. 최종 이전 원고 SHA-256 `156a1506b35f7fb925c2aea04f0a8f7d864691adc286a7299e6496f220d3a8e8`. |
| 6 | route-01 CO 토큰 문장과 낡은 상충 문장 제거 | CO identity block은 step 3의 Solar 응답에 포함된 `ROUTE01_CO_IDENTITY_SENTENCE`; 원본 block SHA-256 `8bdfc346f6cc8124b022cad263a955fd4f0a9f86d3baaaefc08e5465398f3010` | `scripts/merge_route01_co_identity.py`가 확인된 블록을 보존하고 기존 충돌 문장 하나만 제거. `reports/benzocaine-final/route01-co-merge-validation.json`에 변경 전후와 원본 응답 hash를 기록. 새 Solar 호출 없이 실행됨. |
| 7 | 이미지·표·DOCX/PDF 변환 | 저장된 Markdown, evidence run과 figure manifest | `render_report_evidence.py`는 manifest가 정확히 가리키는 이미지를 연결하고 정규화된 route/step 데이터에서 표를 만듦. `export_report_docx.py`와 Word PDF exporter가 문서만 생성. |

## 고정 후보와 출처

- 제출 후보의 원고는 패키지의 `reports/benzocaine-final/report-source.md`이며, 파일 해시는 현재 manifest에 있습니다.
- 최종 PDF와 DOCX는 같은 위치의 한글 파일명 두 파일입니다. 이들은 최신 원본 후보를 바이트 그대로 복사했고 복사 전후 SHA-256은 각각 `4d5521f3594706453ee413f0c7cfc1edf952ca4ae44b66eb9f1ddb6e27cf7445`와 `b8b408829f833848bfcd422697f7ca0035f9be11d299fc30fe4c757a43dee926`입니다.
- `base-report-before-route01-cleanup.md`는 최종 CO 수정 직전의 원고입니다. README의 저장 응답 재생성 명령은 이 원고, 정확한 Solar response, 보존 블록, merge script를 함께 사용합니다.
- 역사적 요청 및 실행 메타데이터 중 개인 워크스테이션 경로가 있던 텍스트 파일은 이 패키지 복사본에서만 익명화했습니다. 원본 프로젝트 파일은 수정하지 않았습니다. 익명화된 파일의 원본·파생 hash 대응은 `../package-redaction-map.json`에 있습니다.

## 실행의 해석 한계

이번 패키지 정리는 새 Solar 요청이나 새 화학 추론을 하지 않았습니다. 오프라인 요청 구성 검사는 필수 source block이 실제 요청에 들어가는지를 확인하는 것이며, 현재 스킬의 Solar 응답 품질을 확인한 것은 아닙니다. 저장된 보고서의 렌더링 성공은 새 물질의 모델 실행이나 새 보고서 작성 성공을 뜻하지 않습니다.
