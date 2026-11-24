# route-05/step-02 Visualizer 측정 기록

## 실행 상태

이번 요청에서는 기존 Visualizer 프로그램의 실제 화면 조작을 시도할 수 있는 데스크톱 GUI 제어 수단이 현재 Codex 세션에 제공되지 않았다. `exec`로 프로그램을 시작하거나 파일을 읽는 것만으로는 Visualizer의 두 분자 배치·원자 선택·DistanceMonitor/AngleMonitor 값을 관찰했다고 기록할 수 없으므로, 임의 수치와 가짜 화면 캡처를 만들지 않았다.

따라서 이번 폴더에는 **실행 준비 사본과 원자 매핑, 측정 미수행 사유**만 저장한다. 기존 실제 측정값과 혼동하지 않는다.

## 구조·배좌·원자 확인

### PABA

- 사본: `inputs/route05-p-aminobenzoic-acid-conf4.sdf`
- 제목: `p-aminobenzoic-acid | MOPAC PM7 conformer 4`
- 구조 출처: MOPAC PM7 gas-phase isolated-molecule geometry optimization
- SDF atom serial / element:
  - carbonyl carbon: serial 6 (`C`)
  - carbonyl oxygen: serial 7 (`O`)
  - hydroxyl oxygen: serial 8 (`O`)
  - amino nitrogen: serial 1 (`N`)

### Ethanol

- 사본: `inputs/route05-ethanol-conf2.sdf`
- 제목: `ethanol | MOPAC PM7 conformer 2`
- 구조 출처: MOPAC PM7 gas-phase isolated-molecule geometry optimization
- SDF atom serial / element:
  - hydroxyl oxygen: serial 3 (`O`)
  - ethyl carbons: serial 1, 2 (`C`)
  - hydroxyl hydrogen: serial 9 (`H`)

PABA carbonyl carbon과 ethanol hydroxyl oxygen을 접근성 측정 후보로 선정한 것은 반응 구조의 원자 정체성에 기반한 측정 계획일 뿐, 실제 반응 메커니즘이나 공격 경로를 확정하는 것이 아니다.

## 원래 요청한 측정과 현재 상태

| 항목 | 상태 | 비고 |
|---|---|---|
| PABA conformer 4 단독 관찰 | 구조 사본 확인 가능 | 실제 이번 화면 캡처 없음 |
| ethanol conformer 2 단독 관찰 | 구조 사본 확인 가능 | 실제 이번 화면 캡처 없음 |
| 두 분자 한 장면 배치 | 미수행 | GUI 제어 부재; 배치 기준·상대 orientation을 만들지 않음 |
| PABA C6–ethanol O3 거리 | 미측정 | 임의 배치 수치 생성하지 않음 |
| 설명용 angle | 미측정 | 임의 배치 수치 생성하지 않음 |
| 화면 캡처 | 미생성 | 기존 캡처를 이번 측정 증거로 재사용하지 않음 |

## 실행 시 필요한 최소 절차

1. Visualizer 25.1.0에서 두 사본을 별도 molecule object로 연다.
2. PABA conformer 4와 ethanol conformer 2를 확인한다.
3. 상대 배치 기준을 사전에 정한다. 예: PABA carboxyl carbon C6와 ethanol O3가 화면에서 서로 향하도록 두되, 이 배치는 설명용 상대 배치임을 기록한다.
4. PABA C6–ethanol O3의 DistanceMonitor 값을 측정한다.
5. 세 원자 angle은 PABA C6–ethanol O3–ethanol H9처럼 실제 선택 가능한 원자에 대해 측정하되, 설명용 배치의 각도임을 표시한다.
6. 두 분자·배좌·원자 serial·배치 기준·값·단위를 기록하고 화면을 캡처한다.

## 해석 제한

이 실행을 완료하더라도 값은 사용자가 정한 한 상대 배치의 기하값이다. 최적 접근거리, 반응 복합체, 전이상태, 활성화 장벽, 반응 성공, 전환율 또는 수율의 근거로 해석하지 않는다. 고립 PM7 conformer를 겹쳐 놓은 것은 용액의 실제 상대 배향이나 산 촉매가 있는 esterification complex를 재현하지 않는다.

## 기존 실제 Visualizer 근거와 구분

기존 실제 측정은 `analyses/visualizer/visualizer-measurements.csv`와 `reports/benzocaine-final/evidence-run/visualizer-measurement-interpretation.md`에 있는 route-01 ethyl 4-nitrobenzoate 단독 분자의 내부 거리·각도뿐이다. 이번 파일에는 그 값을 새 측정값으로 복사하지 않았다.

