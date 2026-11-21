# Discovery Studio Visualizer: 실제 측정 정리

작성일: 2026-11-01 (Asia/Seoul)

## 실제 관찰·측정의 범위

Discovery Studio Visualizer 2025 Client 25.1.0에서 `analyses/visualizer/inputs/ethyl-4-nitrobenzoate-mopac-pm7-conformers.sdf`를 열고, 앱의 Select/Measure 기능과 DistanceMonitor/AngleMonitor 표에서 읽은 측정만 포함한다. SDF atom serial은 1-based이며, heavy atom map은 `atom-serial-crosswalk.csv`와 연결했다. 수소는 map 0이므로 H21은 SDF 원자 serial 21로 표기한다.

| ID | 실제 대상 | 원자 번호 | Visualizer 값 | 캡처 |
|---|---|---|---:|---|
| D-01 | Ethyl 4-nitrobenzoate, PM7 배좌 1 | N10–H21 (SDF serial 10, 21; N map 10, H map 0) | 2.684 Å | `screenshots/route01-distance-monitor-table.png`; 구조 선택 확인 `screenshots/route01-distance-measured.png` |
| A-01 | 같은 물질, PM7 배좌 1 | C8–C9–N10 (map 8, 9, 10) | 119.102° | `screenshots/route01-angle-monitor-table.png`; 선택 캡처 `screenshots/route01-angle-three-atoms-selected.png` |
| D-02 | Ethyl 4-nitrobenzoate, PM7 배좌 2 | N10–H21 (SDF serial 10, 21; N map 10, H map 0) | 2.682 Å | `screenshots/route01-conf2-distance-monitor.png`; 배좌/구조 `screenshots/route01-conformer2-only.png` |
| A-02 | 같은 물질, PM7 배좌 2 | C8–C9–N10 (map 8, 9, 10) | 119.062° | `screenshots/route01-conf2-angle-monitor.png`; 배좌/구조 `screenshots/route01-conformer2-only.png` |

대표 경로는 모델 예측의 route-01 `ethyl 4-nitrobenzoate → ethyl 4-aminobenzoate (benzocaine)` 한 단계 환원이다. 선택 근거와 한계는 `route-selection.json`에 있다. 측정 대상은 반응 전구체 한 분자뿐이다. 벤조카인, 환원 시약, 촉매, 용매, 반응 복합체, 전이상태는 이 측정에 들어 있지 않다.

## 근거에 맞는 해석

관찰된 두 표본 배좌에서 nitro N10과 같은 분자 내 ortho H21의 거리는 2.684 Å와 2.682 Å로 거의 같다. C8–C9–N10 국소각은 119.102°와 119.062°다. 따라서 현재 Visualizer 기록은 선택된 두 PM7 최적화 기하에서 해당 nitro/aryl 주변의 국소 내부 배치가 서로 유사하다는 것까지만 보여 준다. 각도는 aryl C8–C9 결합과 nitro N10이 이루는 분자 내부 각이며, 반응 공격각이 아니다.

이 거리·각도는 외부 반응물이 분자에 접근할 공간, 결합 형성 가능성, 입체장애 장벽, 반응속도, 전환율 또는 수율을 측정하지 않는다. 두 배좌 결과만으로 전체 배좌 집단이나 용액 상태를 일반화하지 않는다. route-05의 PABA/ethanol 및 route-01 나머지 배좌는 실제 측정이 없어 해석하지 않는다.

## 완료·미완료 기록

- 완료: 배좌 1과 2의 거리·각도 4개 측정, 해당 Monitor 표 캡처, 원본 SDF 해시가 세션 전후 일치함을 기록.
- 화면 복구: `final-clean-single-conformer-view.png`에서 배좌 1만 보이게 복구. 복수 Visible 배좌가 겹쳐 보이는 시험 화면도 `route01-multiconformer-visible-test.png`에 보존.
- 미완료: 배좌 3–5와 route-05의 모든 측정. 배좌 전환 후 화면 재렌더링/선택 대상 연결이 간헐적으로 모호해졌고, 재열기 이후 기본 배좌가 1로 돌아오는 사례가 있어 잘못된 배좌에 수치를 연결할 위험이 있었다. 같은 조작을 반복하지 않았다.
- 별도 코드/도구로 계산한 값은 Visualizer 측정값에 섞지 않았다.
- 추가 GUI 관찰은 현재 해석에 필수적이지 않아 수행하지 않았다.

세션 및 원시 근거: `visualizer-measurements.csv`, `actual-visualizer-measurements.json`, `visualizer-recovery-and-measurement-session.md`, `visualizer-session-status.json`, `atom-serial-crosswalk.csv`.