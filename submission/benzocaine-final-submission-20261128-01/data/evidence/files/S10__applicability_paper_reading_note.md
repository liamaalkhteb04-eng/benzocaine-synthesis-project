# 공식 논문 판독 범위

논문: Schwaller, Vaucher, Laino, Reymond, *Prediction of chemical reaction yields using deep learning*, Machine Learning: Science and Technology 2 (2021)015016, DOI10.1088/2632-2153/abc81d.

저자 소속 대학의 게시본 URL: https://boris-portal.unibe.ch/server/api/core/bitstreams/63aa446b-c8df-4e9c-969f-48504b529d44/content

2026-11-23 웹 도구의 대학 저장소 캐시에서 정식 출판본 전체 텍스트를 읽었다. 확인 위치는 printedp2(명시적으로 넣지 않은 수치 조건과 입력), p5 §4/4.1(특허·질량·중복 수율 평균 및 분할), p7 Table3/Conclusion(USPTO 성능)이다. PDF의 표지1쪽 때문에 PDF페이지는 각각3/6/8이다. Table3의 gram/random0.117은 해당 폴더의 공식 eval_results.txt r2=0.11658362440393955와 반올림상 대응한다.

직접 HTTP 요청은200이지만 빈 본문을 반환해 로컬 PDF 파일 확보에 실패했다. 이를 정상 PDF 다운로드로 취급하지 않는다. 웹 PDF 페이지 이미지 요청도 timeout이어서 표 이미지는 보관하지 못했다. 출판사와 ChemRxiv/보충자료 접근도 제한됐다. 이번 판정은 대학 저장소에서 읽은 정식 텍스트와 직접 내려받은 체크포인트 평가/코드 및 로컬 데이터에 근거한다. 보충자료의 클래스별 성능을 직접 확보한 것처럼 쓰지 않았다. 관련 없는 다른 모델의 논문·잘못된 arXiv 레코드는 근거로 사용하지 않았다.
