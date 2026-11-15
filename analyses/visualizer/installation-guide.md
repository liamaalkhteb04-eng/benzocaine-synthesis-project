# BIOVIA Discovery Studio Visualizer 설치 및 첫 구조 열기

상태: 사용자 다운로드 대기. 설치 파일이 아직 제공되지 않았고 프로그램 설치·실행은 확인되지 않음. 구조 분석도 시작되지 않음.

## 1. 공식 배포본 받기 (사용자가 직접 수행)

1. 브라우저 주소창에서 Dassault Systèmes의 공식 주소를 직접 연다: https://discover.3ds.com/discovery-studio-visualizer-download
2. 페이지의 **Register to download** 양식을 작성한다. 양식에서 요구하는 이름/연락 이메일/조직 및 국가 정보만 입력한다. 이 turn의 공개 페이지에는 양식 필드가 노출되지 않으므로, 화면에 표시되는 항목에 따른다.
3. 페이지가 Dassault Systèmes 계정 로그인/가입을 요구하면 공식 계정 가입 절차와 이메일 확인을 완료한 다음 다운로드 페이지로 돌아와 제출한다.
4. 다운로드 화면 또는 등록 이메일에서 **Windows**용 Discovery Studio Visualizer 설치 패키지를 선택한다. 주소가 `3ds.com`, `discover.3ds.com`, 또는 공식 Dassault Systèmes 배포 페이지인지 확인한다. 제3자 다운로드 사이트의 파일은 사용하지 않는다.
5. 설치 파일은 아직 실행하지 않는다. 파일을 받은 뒤 이 대화에 파일을 첨부하거나 전체 경로(예: `C:\Users\<user>\Downloads\installer.exe`)를 알려준다. 파일을 공유하기 어렵다면 사용자 PC에서 `Get-AuthenticodeSignature -LiteralPath '전체경로' | Format-List Status,StatusMessage,SignerCertificate`와 `Get-FileHash -Algorithm SHA256 -LiteralPath '전체경로'`를 실행해 결과를 전달할 수 있다. 서명/해시 중 하나만으로 공식 여부를 단정하지 않는다.

BIOVIA 공식 제품 소개는 Visualizer를 무료 소분자/단백질 구조 보기·분석 도구로 설명하고, 다운로드 페이지는 양식 제출을 안내한다. 설치 패키지는 내려받은 뒤 서명 상태, 게시자 인증서, 파일 버전/제품 정보, SHA-256, 공식 배포 경로를 확인한다. EPA/MOPAC이나 다른 프로그램은 설치하거나 변경하지 않는다.

## 2. 파일 확인 후 설치

파일이 제공되면 실행 전에 검사 결과를 먼저 확인한다. 공식 배포 경로와 게시자/서명이 검증 가능하고 파일이 손상되지 않았을 때만 다음 단계로 간다. 서명이 없거나 발행자를 확인할 수 없거나 출처가 불분명하면 설치를 보류하고 공식 페이지에서 다시 받는다.

검증 후 사용자가 Windows에서 설치 파일을 실행한다. 설치 마법사에서 Visualizer 제품명, 설치 경로, 라이선스 안내를 확인해 진행한다. 설치 중 관리자 권한을 요구하거나 다른 기존 제품의 제거/업그레이드를 제안하면 진행을 멈추고 그 화면을 확인한다. 설치 완료 뒤 Start 메뉴에서 **BIOVIA Discovery Studio Visualizer**를 실행하고 **Help > About** 화면의 제품명과 버전을 확인한다. 이 세션에는 GUI 자동 조작 기능이 없으므로 설치 창을 사용자가 직접 조작해야 한다.

## 3. 설치 후 벤조카인 구조 파일 하나 열기

첫 파일:

`.\analyses\visualizer\inputs\benzocaine-mopac-pm7-conformers.sdf`

1. Visualizer에서 **File > Open**을 선택한다.
2. 위 SDF 경로를 입력하거나 해당 파일을 찾아 열고, 파일 형식이 SDF/MDL Molfile로 인식되는지 확인한다.
3. 파일에는 벤조카인 PM7 배좌 5개가 들어 있다. 프로그램이 다중 구조 파일을 계층/문서 목록으로 표시하면 첫 번째 항목을 선택한다. 첫 구조는 준비 manifest에서 PM7 계산 배좌 중 선택 구조로 표시되어 있다.
4. 분자가 3D 화면에 표시되는지만 확인한다. 원자 라벨/측정 도구를 사용하거나 캡처하기 전이라도, 단지 파일이 열린 것만으로 분석 완료로 기록하지 않는다.
5. 설치 실행 확인을 위해 Start 메뉴 프로그램명과 **Help > About** 제품 버전 화면을 캡처해 `analyses/visualizer/screenshots/`에 저장한다. 구조 열기 화면도 `benzocaine-opened-in-visualizer.png`로 저장한다. 캡처는 Visualizer 화면만 사용한다.

## 4. 다음 보고

설치 파일을 첨부하거나 전체 경로를 알려주면, 먼저 공식 출처·서명·제품 메타데이터·해시를 확인한다. 파일 검증 뒤에는 설치 화면에서 사용자가 직접 누를 버튼을 차례로 안내하고, 설치 후 실행 여부와 SDF 열기 여부를 별도로 점검한다. 실제 반응 부위 관찰·측정·캡처가 이루어지기 전까지 `analysis-results.json` 상태는 미완료로 둔다.
