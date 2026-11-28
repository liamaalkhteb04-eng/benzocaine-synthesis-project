# 로컬 정리 전후

```text
변경 전
README.md → 2026-11-21 이전 제출 패키지 안내
submission/
  benzocaine-professor-reproduction-package-20261121/
  benzocaine-final-submission-20261128-01/
    report/benzocaine-pressure-corrected.pdf·docx
    report/baseline.md, records/과거 수정 기록, assets/original·history
    data/evidence/files/S01__report.md
    skill/used-revision-system.txt
    work/로컬 시험 복사본

변경 후
README.md → 학번20251312·이름리야마·최종 PDF/DOCX·스킬·실행 방법
submission/benzocaine-final-submission-20261128-01/
  report/20251312_리야마_벤조카인_최종보고서.pdf·docx
  report/report.md, assets/확정 그림13개, records/현재 참조 자료
  skill/, code/, configs/, data/, authoring/, provenance/, validation/
  archive/
    baselines/재조판 보호 기준 원고
    history/과거 시안·수정/실패 이력·중간 그림·과거 system
    duplicates/중복 그림 원본·교정 증명·옛 출처표
    local-checks/로컬 시험 결과(업로드 제외)
archive/
  legacy-submissions/2026-11-21 이전 제출 패키지(업로드 제외)
  history/기존 루트README의 미커밋 사본(로컬 보존)
```

다른 미커밋 코드와 연결된 루트 `reports/`, `reviews/`, `results/`, 코드·설정·스킬은 원위치에 남겨 동작 경로를 보존했다. 최종 제출 진입점과 GitHub 반영 범위는 별도 목록으로 제한했다.

최종PDF/DOCX·최종 원고는 바이트 동일하다. 문서 재작성·Solar호출·영구 삭제·stage/commit/push는 없다. [이동 전 해시](validation/reorganization-before.json), [실제 이동 목록](validation/reorganization-moves.json), [이동 후 보존/경로 판정](validation/reorganization-final.json)을 보관했다.

[GitHub 반영 범위](GITHUB_INCLUDE.md) · [저장소 기준 반영 경로 전체](GITHUB_REPOSITORY_FILES.txt).
