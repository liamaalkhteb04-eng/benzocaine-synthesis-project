---
name: synthesis-report
description: 물질명과 SMILES로 실제 합성 경로·단계별 조건·수율을 정리하고, 추가 분석 근거와 함께 Solar Pro 4 한국어 보고서를 준비한다.
---

작업 전에 [synthesis_report_skill.md](synthesis_report_skill.md)를 읽는다. 입력 물질과 실제 결과에 따라 동작하며, 특정 약물명·수율·경로 수를 전제하지 않는다. 현재 실행 허용 범위는 configs/report-plan.json을 확인한다. 예측 전용 실행은 scripts/run_pipeline.py이며 유료 API를 호출하지 않는다. 보고서 작성과 새 도구 설치는 별도 허용 범위다.
