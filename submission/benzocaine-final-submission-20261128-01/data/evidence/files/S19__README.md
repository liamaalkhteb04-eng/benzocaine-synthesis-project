# 집 PC Visualizer 추가 관찰 — 2026-11-24

**새 실제 GUI 관찰·캡처를 완료했다.** 학교 인계에서 미수행이던 PABA 배좌4와 ethanol 배좌2를 집의 Visualizer에서 각각 열어 보고 기록한 것이다. 기존 수율·Parrot·EPI 검토는 다시 수행하지 않았다.

먼저 [PABA 새 화면](19_paba_ball_and_stick.png)과 [ethanol 새 화면](13_ethanol_ball_and_stick.png)을 연다. [관찰 CSV](new_observations.csv), [GUI 원자 추적](GUI_identity_trace.csv), [보존 검증](preservation_verification.json)에 근거가 있다. 프로그램은 두 구조가 별도 탭으로 열린 상태로 두었고 마지막 활성 탭은 PABA다.

## 이번에 실제로 본 것

| 분자·준비 배좌 | 새로 관찰한 내용 | 실제 화면 근거 | 해석 범위 |
|---|---|---|---|
| PABA4, C6/O7/O8 | 카르복실기가 고리의 바깥쪽 끝에 보인다. 시점을 기울이면 고리 투영폭과 주변 원자·결합의 겹침이 달라진다. | [초기](19_paba_ball_and_stick.png), [기울인 시점](24_paba_rotated_stopped.png), [원자 표](21_paba_atom_mapping_GUI.png) | 현재 볼/스틱 표시의 정성적 단일 분자 노출·가림 |
| ethanol2, O3 | OH가 에틸 골격의 말단 쪽에 보인다. 시점 변경으로 에틸 H/C의 겹침은 달라져도 OH는 확인한 투영들에서 가장자리 쪽에 식별된다. | [초기](13_ethanol_ball_and_stick.png), [변경 시점](16_ethanol_rotated_stopped.png), [원자 표](26_ethanol_O3_mapping_GUI.png) | O3 주변을 본 화면 기록; 반응 상대의 접근이나 친핵성 검증 아님 |

PABA의 C6/O7/O8은 실제 Atom 표의 Name·ID와 준비 매핑을 연결했다. Ethanol O3도 같은 방식으로 확인했다. H9은 Name이 H9이지만 GUI ID열은0으로 표시되므로 그 ID를 SDF serial9와 혼동하지 않는다. `22_paba_C6_selected.png`는 C6 **표 셀**이 선택된 화면으로, 3D 원자를 별도로 강조 표시했다고 주장하지 않는다.

## 수행한 GUI 작업과 입력 보존

- 설치돼 있던 `DiscoveryStudio2025.exe`(파일 버전25,1,0,24284)를 실행했다. 새 설치는 하지 않았다.
- 학교 커밋의 SDF를 `school_handoff/`에 보존하고 `working_structures/`의 바이트 동일 사본을 열었다. 별도 문서 탭 두 개이며 하나의 반응 장면에 합치지 않았다.
- View→Graphics, 원소 색상 ball-and-stick 표시, Atom 표와 화면 분할 조절, View→Spin→Spin의 시점 변경/정지, View→Transform→Zoom In 같은 표시 작업만 했다.
- 구조 좌표·원자 순서·결합은 편집하지 않았고, SDF를 저장하거나 재최적화하지 않았다. UI 표의 기존 생성열/heat 값/partial-charge 열을 새 계산 결과로 읽지 않았다.
- 각 PNG는 실제 Visualizer 창 범위를 캡처한 원본 화면이다. 분자를 코드로 다시 그린 그림, 다른 날의 기존 캡처 또는 임의 측정값을 새 증거로 쓰지 않았다. 메뉴·초기화 화면은 관찰 증거와 구분해 [캡처 목록](capture_manifest.csv)에 분류했다.
- Windows UIAutomation provider 접근은 실패했으나, 검증된 앱 창에 대한 native 마우스/키보드 입력과 실제 캡처는 성공했다. [실제 조작 로그](gui_actions.jsonl)를 남겼다.

초기 설정 화면에서 대화상자가 전환된 원인은 확인하지 못했고 스크립트는 초기 기본 연결/최적화 옵션을 선택하지 않았다. 이후 표시된 `Run Graphics Tests`는 Cancel로 취소했다. `Cannot create directory ... Invalid argument` 경고는 OK로 닫았고, 폴더/레지스트리 경로를 수정하지 않았다. 그 뒤 구조 화면은 정상으로 나타났다. [초기 경고](03_visualizer_after_cancel.png)는 성공 관찰 화면과 구분한다.

## 하지 않은 것과 남는 한계

새 분자 간 거리·각도 측정은 **0건**이다. 두 분자를 임의 배치하지 않았으며 PABA C6–ethanol O3의 접근거리/각도로 접근성을 검증하지 않았다. 볼 크기와 스틱은 표현 설정이므로 van der Waals 가림, solvent-accessible area 또는 입체장애의 정량값이 아니다. 한 고립 PM7 배좌의 여러 카메라 투영이며 새 배좌·반응 복합체·용액 배향 분포를 계산한 것이 아니다.

따라서 실제 에스터화의 접근 경로·선택성·산 촉매 효과·장벽·속도·성공 또는 수율은 이 결과로 판단할 수 없다. 관찰 기록은 “고리 밖 카르복실기/말단 OH를 이 화면들에서 볼 수 있었다”까지다. 정확한 카메라 행렬이나 회전 각도 수치는 저장하지 않아 동일 시점의 자동 재현을 보장하지 않는다.

## 집 변경·원본 보존

집의 미커밋 수정·기존 미추적 파일을 먼저 해시 기록하고 작업 후 다시 대조했다. HEAD와 기존 tracked 상태도 그대로다. `pull`, `checkout`, `stash`, `reset`, `clean`, commit/push는 하지 않았다. 지정 커밋은 원격 raw 자료의 **별도 사본**으로 확인했으며 집 작업 트리를 덮지 않았다.

학교 원본 참조는 [인계 README](school_handoff/README.md), [학교 준비 기록](school_handoff/visualizer-route05-measurement.md), [원격 URL·커밋·해시](school_sources.json)에 있다. 학교 문서에 남은 두 분자 상대 배치 측정 계획은 이번 사용자의 정성적 관찰 요청 및 해석 제한에 따라 실행하지 않았다.

이번 산출물은 이 새 폴더 안의 기록·사본·화면뿐이다. 새 화학 계산·설치·Solar 호출·보고서/스킬 수정·GitHub push는 수행하지 않았다. [기계 판독 결과](new_session_result.json)를 참고한다.
