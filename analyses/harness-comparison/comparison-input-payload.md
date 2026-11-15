# Solar Pro 4 harness comparison: single-call draft request

Create one Korean comparison draft from this single attachment. No tools, external search, file operations, or follow-up requests. This is not the final submission report. Preserve uncertainty and report only evidence included below. The eventual final report must be authored by Solar Pro 4 from the skill and actual results, include additional analyses, and remain within 20 pages including references.



--- BEGIN SOURCE: analyses/harness-comparison/comparison-task.md ---
# 동일 하네스 비교 요청문 (두 하네스에 동일 바이트로 전달)

아래에 함께 첨부된 고정 입력 번들 안의 `skill/synthesis_report_skill.md` 원문 지침을 따르고, 같은 번들의 예측·분석 근거로 **비교용 한국어 보고서 초안**을 작성하라. 이 초안은 제출 최종 보고서가 아니며 DOCX/PDF로 변환하지 않는다. 현재 응답 한 번으로 초안을 마쳐라. 도구, 파일 접근, 웹 검색, MCP, 하위 에이전트, 추가 모델 호출을 사용하지 않는다. 입력은 이미 번들 안에 있으므로 외부 파일을 열지 않는다. 결과는 하네스별 별도 결과 경로에 저장한다.

비교 입력 번들은 같은 프로젝트 파일에서 한 번 생성되고 SHA-256을 기록한다. 구성 원본은 `skill/synthesis_report_skill.md`, `results/benzocaine-live-20261031-04/report-evidence.json`, `results/benzocaine-live-20261031-04/validation_notes.json`, `analyses/mopac/results-interpretation.md`, `analyses/epi-suite/analysis.md`, `analyses/visualizer/visualizer-measurement-interpretation.md`, `analyses/visualizer/visualizer-measurements.csv`, `analyses/visualizer/route-selection.json`, `analyses/visualizer/visualizer-session-status.json`, `results/benzocaine-live-20261031-04/additional-analysis-status.json`이다. report-evidence는 route/step, 조건, 수율을 포함하는 공통 정규화 근거다.

Visualizer 사실은 실제 측정 완료 범위와 미완료 범위를 분리하여 기술한다. 실제 측정치는 ethyl 4-nitrobenzoate PM7 배좌 1과 2의 N10–H21 내부거리 2.684 Å/2.682 Å 및 C8–C9–N10 내부각 119.102°/119.062°뿐이다. 이 값들은 분자 내부 기하이지 반응물의 접근거리/공격각이 아니다. route-05, 배좌 3–5 측정은 미완료다. MOPAC, EPI Suite, 정적 구조 관찰로 반응 성공·속도·수율을 입증한다고 쓰지 않는다.

기존 예측의 결과와 실패/불확실성을 있는 그대로 연결하고, 출처는 제공된 프로젝트 파일 또는 그 파일에 기록된 URL만 사용한다. 불확실하거나 입력에 없는 값은 생성하지 않는다. 후속 최종 제출 보고서는 Solar Pro 4가 skill 및 검증된 전체 결과를 읽어 작성하며, 가산점 분석을 포함해 참고문헌까지 총 20쪽 이내여야 한다는 조건을 마지막에 짧게 명시한다.

초안에는 경로·단계별 예측, 조건과 수율의 route/step 연결, 계산·물성·Visualizer 추가분석, 각 모델의 한계, 증거·출처를 포함한다. 사실이 빠졌거나 근거가 없으면 단정 대신 미제공/미검증/미완료로 표시한다.
--- END SOURCE: analyses/harness-comparison/comparison-task.md ---


--- BEGIN SOURCE: analyses/harness-comparison/comparison-system-prompt.txt ---
Act as a careful Korean scientific-writing assistant. Use only the evidence supplied in the user message. Follow the supplied synthesis report skill. Preserve unknowns and limitations; never invent references, experimental conditions, measurements, yields, or model performance. Do not call tools, search externally, or make follow-up requests. Produce a comparison draft, not the final submission report; the later final report must be created by Solar Pro 4 from the skill and actual results and must stay within 20 pages including supplementary analyses.
--- END SOURCE: analyses/harness-comparison/comparison-system-prompt.txt ---


--- BEGIN SOURCE: skill/synthesis_report_skill.md ---
# 실제 근거 기반 합성·추가 분석 보고서

## 실행 범위

입력 JSON의 물질명·SMILES·화학적 형태와 실제 model evidence를 읽는다. 타깃·경로 수·단계 수·수율·그림 수는 입력에서 결정된다. 다른 약물의 과거 예측이나 문헌 경로를 이번 모델 결과로 대체하지 않는다. 실패·미실행·적용 범위 불확실성은 그대로 보존한다.

로컬 예측은 `python -B scripts/run_pipeline.py --input inputs/<target>.json --run-id <new-id>`로 수행한다. 이 명령은 보고서나 유료 호출을 실행하지 않는다. 환경과 모델 자산은 configs/runtime.json의 경로를 읽고 가중치·외부 설치 코드를 수정하지 않는다. 모든 새 출력은 현재 프로젝트 안의 새 실행 폴더에 기록한다.

최종 한국어 보고서 작성자는 Solar Pro 4이며 기본 snapshot은 configs/report-plan.json에 있다. 본문은 Solar 원문으로 보존하고 사람이 고치지 않는다. 필요한 수정은 스킬/입력 프롬프트를 개선한 뒤 새 작성 호출로 수행한다. `generate_report.py --prepare-only`는 입력 요청만 준비한다. 새 작성은 명시적인 실행 플래그와 report-plan의 허용 설정, 개인 API 키가 모두 필요하다. 현재 금지된 호출·설치·최종 보고서·GitHub 작업을 암묵적으로 수행하지 않는다.

## 실제 모델과 준비 요건

| 목적 | 소스 | 실행/현재 요건 |
|---|---|---|
| 역합성 | https://github.com/MolecularAI/aizynthfinder | predict_routes.py --model aizynthfinder; ONNX 정책·템플릿·stock·설정 필요 |
| 역합성 | https://github.com/schwallergroup/synthex/tree/submission | 현재 adapter/인증 준비가 끝나지 않았으면 not_implemented |
| 조건 | https://gitlab.com/mlpds_mit/askcosv2/context_recommender | 호환 서비스가 실제 실행 중이어야 함 |
| 조건 | https://github.com/wangxr0526/Parrot | predict_conditions.py --model parrot; 실제 체크포인트·라벨 매핑 사용 |
| 수율 | https://github.com/rxn4chemistry/rxn_yields | predict_yields.py --model rxn_yields; 체크포인트 해시와 단위/정규화 메타데이터 필요 |
| 수율용 지문 | https://github.com/reymond-group/drfp | 지문 외에 학습된 회귀기·적용 범위·단위가 필요; 없으면 수율을 만들지 않음 |

어댑터는 `--input <actual-file> --output <new-file>`을 사용한다. 실제 버전·실행 명령·자산 해시는 결과 JSON/로그와 runtime 설정에서 확인한다. 저장소 주소·논문·성능 지표를 만들지 않는다.

## 단계 연결과 과학적 해석

routes.json의 각 반응은 route_id/step_id로 식별하며 depends_on이 공급하는 중간체를 확인한다. 가지가 있는 경로를 일렬 순서로 오인하지 않는다. 조건과 수율은 동일 route_id/step_id뿐 아니라 reaction_smiles가 일치해야 연결한다. 중복 반응의 실제 모델 추론을 공유했다면 모든 대응 단계를 명시한다. 누락 단계나 실패 출력을 정상값으로 채우지 않는다.

수율 표에는 경로·단계 식별자, 실제 숫자·단위와 모델 예측/실험 미검증 표시를 포함한다. 정규화는 해당 checkpoint의 검증된 메타데이터에서 읽는다. 토큰 잘림, 범위 밖 값, 미확인 적용성을 설명한다. 정규화 성공은 타깃 정확도 검증이 아니다. 입력에 조건이 포함되지 않았다면 특정 촉매/용매에서의 달성 수율로 연결하지 않는다. 다단계 수율을 단순 곱해 검증된 전체 수율이라고 부르지 않는다.

Parrot 공란은 미표기다. 온도·시간·당량이 없으면 미제공이다. stock 해결과 경로/sequence 점수는 실험 성공 확률이나 현재 구매 가능성의 증명이 아니다. 구조에서 관찰한 변화, 모델 조건, 문헌 정보, 작성자의 검토를 구분한다. 반응물·시약·용매·후처리 역할을 근거 없이 확정하지 않는다.

## 가산점 근거

하네스 비교는 같은 스킬 바이트/SHA, 입력과 고정 evidence, 같은 Solar snapshot/설정을 사용한다. 실제 메시지 역할·wrapper·도구·재시도·압축·보조 호출·usage·시간·오류·provider 반환 모델을 기록한다. 새 작성, 동일 초안 수정, 저장 응답의 문서 재생성을 별도 모드로 취급한다. 모든 하네스가 공통 API 스크립트를 실행한 경우에는 워크플로 비교이며 네이티브 작성 능력 차이로 단정하지 않는다.

MOPAC은 실제 입력/출력/로그와 버전·전하·다중도·배좌·방법·용매·수렴 근거를 읽는다. 분자식/전하/기준이 다른 에너지를 단순 비교하지 않는다. 구조·전하·궤도·형성열은 활성화장벽·속도·수율·성공의 증명이 아니다. 진동수 검증 없이 최소점을 검증했다고 표현하지 않는다.

EPI Suite는 실제 BP/MP/증기압 출력과 실측 DB 값을 구분한다. 온도·압력·농도·용매·화학적 형태·용해도·분해 가능성·불확실성을 명시한다. 순물질 MP/BP로 혼합물의 실제 상이나 반응 가능성을 확정하지 않는다. 온도 미제공 시 문헌 또는 명시한 가정에서만 조건부로 해석한다.

Discovery Studio Visualizer는 실제 열어 본 구조·배좌·원자 번호·거리/각도·화면/관찰 기록을 근거로 접근성과 차폐를 논의한다. 구조 생성 도구와 관찰 도구를 구분한다. 수동 배치 구조는 전이상태가 아니며 단일 정지 화면이 수율을 입증하지 않는다. 프로그램을 실행하지 않았다면 DS 관찰을 수행했다고 쓰지 않는다.

## 보고서 본문과 문서 검증

물질 선정 이유 → 모델/설정 → 대표와 대안의 실제 단계별 경로·조건·수율 → 네 추가 분석의 실제 결과/미실행 사유 → 종합 결론·한계 → 재현 방법·출처로 자연스러운 한국어 보고서를 작성한다. 작성 규칙·편집 지시·입력 필드명 해설을 본문에 반복하지 않는다. 원자/물질 이름을 확신할 수 없으면 SMILES와 단계 그림으로 식별한다.

그림은 report-evidence의 실제 자산만 사용한다. 최종 보고서에 선택한 경로의 모든 단계 구조와 목표 구조를 포함하고, 실제로 확보한 추가 분석 그림을 넣는다. 선택하지 않은 전체 원시 경로도 보존하며 선택 기준을 설명한다. 조건·수율 표는 실제 단계와 연결하고 중복 표를 피한다. 그림·표 수를 고정하지 않는다.

출처 번호·실제 URL을 근거 주장에 연결한다. 문헌 수율을 모델 예측값으로 바꾸지 않는다. 환경/명령은 실제 runtime과 실행 manifest에서 읽고, 새 환경 전체 재현과 기존 결과 문서화 재현을 구분한다. 개인 키는 기록하지 않는다.

본문·추가 분석·부록·참고문헌을 합쳐 최대 20쪽이다. configs/report-plan.json의 페이지 예산과 선택 경로를 따른다. DOCX/PDF 변환 도구는 Solar 원문을 다시 쓰지 않는다. 실제 페이지 수, 단계별 예측값, 그림/표/출처, 원문 동일성, 한글과 잘림을 검증하고 렌더링을 시각 점검한다. 이번 단계에서는 최종 본문·DOCX·PDF를 생성하지 않는다.
--- END SOURCE: skill/synthesis_report_skill.md ---


--- BEGIN SOURCE: results/benzocaine-live-20261031-04/report-evidence.json ---
{
  "schema_version": "1.0",
  "target": {
    "target_id": "benzocaine",
    "name": "Benzocaine",
    "name_ko": "벤조카인",
    "smiles": "CCOC(=O)c1ccc(N)cc1",
    "expected_formula": "C9H11NO2",
    "pubchem_cid": 2337,
    "identity_reference": "https://pubchem.ncbi.nlm.nih.gov/compound/2337",
    "chemical_form": "neutral free base",
    "purpose": "Final course target; actual synthesis predictions and evidence-based additional analyses"
  },
  "model_status": {
    "routes": "success",
    "conditions": "success",
    "yields": "success"
  },
  "route_summary": [
    {
      "route_id": "route-01",
      "step_count": 1,
      "scores": {
        "state score": 0.9976287063411217,
        "number of reactions": 1,
        "number of pre-cursors": 1,
        "number of pre-cursors in stock": 1
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-02",
      "step_count": 1,
      "scores": {
        "state score": 0.9976287063411217,
        "number of reactions": 1,
        "number of pre-cursors": 1,
        "number of pre-cursors in stock": 1
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-03",
      "step_count": 1,
      "scores": {
        "state score": 0.9976287063411217,
        "number of reactions": 1,
        "number of pre-cursors": 2,
        "number of pre-cursors in stock": 2
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-04",
      "step_count": 1,
      "scores": {
        "state score": 0.9976287063411217,
        "number of reactions": 1,
        "number of pre-cursors": 2,
        "number of pre-cursors in stock": 2
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-05",
      "step_count": 2,
      "scores": {
        "state score": 0.994039853898894,
        "number of reactions": 2,
        "number of pre-cursors": 2,
        "number of pre-cursors in stock": 2
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-06",
      "step_count": 2,
      "scores": {
        "state score": 0.994039853898894,
        "number of reactions": 2,
        "number of pre-cursors": 2,
        "number of pre-cursors in stock": 2
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-07",
      "step_count": 2,
      "scores": {
        "state score": 0.994039853898894,
        "number of reactions": 2,
        "number of pre-cursors": 2,
        "number of pre-cursors in stock": 2
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-08",
      "step_count": 2,
      "scores": {
        "state score": 0.994039853898894,
        "number of reactions": 2,
        "number of pre-cursors": 2,
        "number of pre-cursors in stock": 2
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-09",
      "step_count": 2,
      "scores": {
        "state score": 0.994039853898894,
        "number of reactions": 2,
        "number of pre-cursors": 2,
        "number of pre-cursors in stock": 2
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-10",
      "step_count": 2,
      "scores": {
        "state score": 0.994039853898894,
        "number of reactions": 2,
        "number of pre-cursors": 2,
        "number of pre-cursors in stock": 2
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-11",
      "step_count": 2,
      "scores": {
        "state score": 0.994039853898894,
        "number of reactions": 2,
        "number of pre-cursors": 2,
        "number of pre-cursors in stock": 2
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    },
    {
      "route_id": "route-12",
      "step_count": 2,
      "scores": {
        "state score": 0.994039853898894,
        "number of reactions": 2,
        "number of pre-cursors": 2,
        "number of pre-cursors in stock": 2
      },
      "is_solved": true,
      "overall_yield_percent": null,
      "overall_yield_reason": "No experimentally validated overall yield; branching and independently predicted steps are not combined."
    }
  ],
  "steps": [
    {
      "route_id": "route-01",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true
      ],
      "reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCOC(=O)c1ccc([N+](=O)[O-])cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "664f7756f7526ad6c07e82dd3b3c15f7aabccbc99837dd22105068a2cfc385b5",
        "classification": "0.0 Unrecognized",
        "library_occurence": 33350,
        "policy_probability": 0.42239999771118164,
        "policy_probability_rank": 0,
        "policy_name": "uspto",
        "template_code": 17064,
        "template": "[NH2;D1;+0:1]-[c:2]>>O=[N+;H0;D3:1](-[O-])-[c:2]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([N+:10](=[O:13])[O-:14])[cH:11][cH:12]1"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -1.700762152671814
          },
          {
            "rank": 2,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.0481550693511963
          },
          {
            "rank": 3,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.7931230068206787
          },
          {
            "rank": 4,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -2.878655195236206
          },
          {
            "rank": 5,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -3.4926724433898926
          },
          {
            "rank": 6,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -3.8862576484680176
          },
          {
            "rank": 7,
            "catalyst1": "[Fe]",
            "solvent1": "CCO",
            "solvent2": "O",
            "reagent1": "[Cl-].[NH4+]",
            "reagent2": "",
            "sequence_score": -3.8886513710021973
          },
          {
            "rank": 8,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "O=C[O-].[NH4+]",
            "reagent2": "",
            "sequence_score": -4.486337661743164
          },
          {
            "rank": 9,
            "catalyst1": "[Fe]",
            "solvent1": "CC(=O)O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.683133125305176
          },
          {
            "rank": 10,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "O=C[O-].[NH4+]",
            "reagent2": "",
            "sequence_score": -5.087017059326172
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "CCO",
            "reagent2": "",
            "sequence_score": -5.712345600128174
          },
          {
            "rank": 12,
            "catalyst1": "[Fe]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "[Cl-].[NH4+]",
            "reagent2": "",
            "sequence_score": -6.493983268737793
          },
          {
            "rank": 13,
            "catalyst1": "[Fe]",
            "solvent1": "CCO",
            "solvent2": "O",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.5203938484191895
          },
          {
            "rank": 14,
            "catalyst1": "[Fe]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.688980579376221
          },
          {
            "rank": 15,
            "catalyst1": "[Fe]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "[Cl-].[NH4+]",
            "sequence_score": -6.779082298278809
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-01",
        "step_id": "step-01",
        "reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.46616947650909424,
        "yield_percent": 82.95371431744555,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 46,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-02",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true
      ],
      "reaction_smiles": "CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCOC(=O)c1ccc(NC(C)=O)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "8063032398e59c77d82569a4231c9d8f1dc9cd333085943b3f9ae7b5eafd5071",
        "classification": "0.0 Unrecognized",
        "library_occurence": 1668,
        "policy_probability": 0.011800000444054604,
        "policy_probability_rank": 5,
        "policy_name": "uspto",
        "template_code": 21399,
        "template": "[NH2;D1;+0:1]-[c:2]>>C-C(=O)-[NH;D2;+0:1]-[c:2]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH:10][C:13]([CH3:14])=[O:15])[cH:11][cH:12]1"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -1.3239554166793823
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "Cl",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.660543441772461
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -3.2928555011749268
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "Cl",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -3.6584954261779785
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "Cl",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -3.7139711380004883
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "O=S(=O)(O)O",
            "sequence_score": -4.38345193862915
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CCO",
            "reagent2": "Cl",
            "sequence_score": -4.546271324157715
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -4.650010585784912
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(=O)(O)O",
            "reagent2": "",
            "sequence_score": -6.109102249145508
          },
          {
            "rank": 10,
            "catalyst1": "Cl",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -6.133055210113525
          },
          {
            "rank": 11,
            "catalyst1": "Cl",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "",
            "sequence_score": -8.281896591186523
          },
          {
            "rank": 12,
            "catalyst1": "Cl",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CCO",
            "reagent2": "",
            "sequence_score": -9.194323539733887
          },
          {
            "rank": 13,
            "catalyst1": "Cl",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -9.742517471313477
          },
          {
            "rank": 14,
            "catalyst1": "Cl",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -9.823410987854004
          },
          {
            "rank": 15,
            "catalyst1": "Cl",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CCOC(C)=O",
            "reagent2": "O=C([O-])O.[Na+]",
            "sequence_score": -10.718693733215332
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-02",
        "step_id": "step-01",
        "reaction_smiles": "CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.21513395011425018,
        "yield_percent": 77.69549187778327,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 47,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-03",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true,
        true
      ],
      "reaction_smiles": "C[Si](C)(C)N[Si](C)(C)C.CCOC(=O)c1ccc(Br)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "C[Si](C)(C)N[Si](C)(C)C",
        "CCOC(=O)c1ccc(Br)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "da486c14b949364bbad0a80d030bfb42636d243c23ed7c3a39e69b37c1cd5b78",
        "classification": "0.0 Unrecognized",
        "library_occurence": 61,
        "policy_probability": 0.0013000000035390258,
        "policy_probability_rank": 19,
        "policy_name": "uspto",
        "template_code": 36294,
        "template": "[NH2;D1;+0:4]-[c;H0;D3;+0:1](:[c:2]):[c:3]>>Br-[c;H0;D3;+0:1](:[c:2]):[c:3].C-[Si](-C)(-C)-[NH;D2;+0:4]-[Si](-C)(-C)-C",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([Br:13])[cH:11][cH:12]1.[NH:10]([Si:14]([CH3:15])([CH3:16])[CH3:17])[Si:18]([CH3:19])([CH3:20])[CH3:21]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "C[Si](C)(C)N[Si](C)(C)C.CCOC(=O)c1ccc(Br)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCOC(=O)c1ccc(Br)cc1.C[Si](C)(C)N[Si](C)(C)C>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "CNCCNC",
            "reagent2": "O=P([O-])([O-])[O-].[K+].[K+].[K+]",
            "sequence_score": -2.1571593284606934
          },
          {
            "rank": 2,
            "catalyst1": "I[Cu]I",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "CNCCNC",
            "reagent2": "O=P([O-])([O-])[O-].[K+].[K+].[K+]",
            "sequence_score": -3.3405747413635254
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "O=C([O-])[O-].[Cs+].[Cs+]",
            "reagent2": "",
            "sequence_score": -3.3863651752471924
          },
          {
            "rank": 4,
            "catalyst1": "I[Cu]I",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.122430324554443
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.343253135681152
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.805835247039795
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.908517360687256
          },
          {
            "rank": 8,
            "catalyst1": "I[Cu]I",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "O=P([O-])([O-])[O-].[K+].[K+].[K+]",
            "reagent2": "",
            "sequence_score": -5.606592178344727
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "Cc1ccccc1",
            "reagent2": "O=P([O-])([O-])[O-].[K+].[K+].[K+]",
            "sequence_score": -5.694052696228027
          },
          {
            "rank": 10,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "c1ccncc1",
            "reagent2": "",
            "sequence_score": -5.862532615661621
          },
          {
            "rank": 11,
            "catalyst1": "I[Cu]I",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "O=C([O-])[O-].[Cs+].[Cs+]",
            "reagent2": "",
            "sequence_score": -5.94991397857666
          },
          {
            "rank": 12,
            "catalyst1": "I[Cu]I",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "O=P([O-])([O-])[O-].[K+].[K+].[K+]",
            "reagent2": "",
            "sequence_score": -6.159550666809082
          },
          {
            "rank": 13,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cc1ccccc1",
            "reagent2": "",
            "sequence_score": -6.474880218505859
          },
          {
            "rank": 14,
            "catalyst1": "I[Cu]I",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "Cc1ccccc1",
            "reagent2": "O=P([O-])([O-])[O-].[K+].[K+].[K+]",
            "sequence_score": -6.5210981369018555
          },
          {
            "rank": 15,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "C1COCCO1",
            "reagent2": "",
            "sequence_score": -6.566495895385742
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-03",
        "step_id": "step-01",
        "reaction_smiles": "C[Si](C)(C)N[Si](C)(C)C.CCOC(=O)c1ccc(Br)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": -0.1407427340745926,
        "yield_percent": 70.24125305578036,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 59,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-04",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true,
        true
      ],
      "reaction_smiles": "CCOC(=O)c1ccc(C(=O)O)cc1.[N-]=[N+]=NP(=O)(c1ccccc1)c1ccccc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCOC(=O)c1ccc(C(=O)O)cc1",
        "[N-]=[N+]=NP(=O)(c1ccccc1)c1ccccc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "ce6d7f4d8f151411474dd8b20aa72a759717b847f7a70371bc1f8953b7a24100",
        "classification": "0.0 Unrecognized",
        "library_occurence": 70,
        "policy_probability": 0.00019999999494757503,
        "policy_probability_rank": 49,
        "policy_name": "uspto",
        "template_code": 34347,
        "template": "[NH2;D1;+0:4]-[c;H0;D3;+0:1](:[c:2]):[c:3]>>O-C(=O)-[c;H0;D3;+0:1](:[c:2]):[c:3].O=P(-[N;H0;D2;+0:4]=[N+]=[N-])(-c1:c:c:c:c:c:1)-c1:c:c:c:c:c:1",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([C:13]([OH:14])=[O:15])[cH:11][cH:12]1.[N:10]([P:16](=[O:17])([c:18]1[cH:19][cH:20][cH:21][cH:22][cH:23]1)[c:24]1[cH:25][cH:26][cH:27][cH:28][cH:29]1)=[N+:30]=[N-:31]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOC(=O)c1ccc(C(=O)O)cc1.[N-]=[N+]=NP(=O)(c1ccccc1)c1ccccc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCOC(=O)c1ccc(C(=O)O)cc1.[N-]=[N+]=NP(=O)(c1ccccc1)c1ccccc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "CC(C)(C)O",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -0.8248026967048645
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CC(C)(C)O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -3.1628024578094482
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "CN(C)C=O",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "O",
            "sequence_score": -3.585378408432007
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "CC(C)(C)O",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "",
            "sequence_score": -3.888746976852417
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -4.628708839416504
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "CN(C)C=O",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "",
            "sequence_score": -5.177088737487793
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "CN(C)C=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -5.913084983825684
          },
          {
            "rank": 8,
            "catalyst1": "Cl[Cu]",
            "solvent1": "CC(C)(C)O",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -6.799911022186279
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.032540321350098
          },
          {
            "rank": 10,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "",
            "sequence_score": -7.450817108154297
          },
          {
            "rank": 11,
            "catalyst1": "Cl[Cu]",
            "solvent1": "CC(C)(C)O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -9.830256462097168
          },
          {
            "rank": 12,
            "catalyst1": "Cl[Cu]",
            "solvent1": "CC(C)(C)O",
            "solvent2": "",
            "reagent1": "CCN(C(C)C)C(C)C",
            "reagent2": "",
            "sequence_score": -10.234187126159668
          },
          {
            "rank": 13,
            "catalyst1": "Cl[Cu]",
            "solvent1": "CN(C)C=O",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -11.263615608215332
          },
          {
            "rank": 14,
            "catalyst1": "Cl[Cu]",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "O",
            "sequence_score": -11.529948234558105
          },
          {
            "rank": 15,
            "catalyst1": "Cl[Cu]",
            "solvent1": "CN(C)C=O",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "",
            "sequence_score": -14.083959579467773
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-04",
        "step_id": "step-01",
        "reaction_smiles": "CCOC(=O)c1ccc(C(=O)O)cc1.[N-]=[N+]=NP(=O)(c1ccccc1)c1ccccc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": -0.02788764238357544,
        "yield_percent": 72.60513032877832,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 75,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-05",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true
      ],
      "reaction_smiles": "CC(=O)O>>CCO",
      "precursor_smiles": [
        "CC(=O)O"
      ],
      "product_smiles": "CCO",
      "metadata": {
        "template_hash": "c42f96a0658c03bc12dc20efce06e66daaeccc675d73631eea24ea610a7227b8",
        "classification": "0.0 Unrecognized",
        "library_occurence": 3921,
        "policy_probability": 0.09149999916553497,
        "policy_probability_rank": 0,
        "policy_name": "uspto",
        "template_code": 32658,
        "template": "[C:2]-[CH2;D2;+0:1]-[O;D1;H1:3]>>O=[C;H0;D3;+0:1](-[C:2])-[O;D1;H1:3]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][OH:3]>>[CH3:1][C:2]([OH:3])=[O:4]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CC(=O)O>>CCO",
        "canonical_reaction_smiles": "CC(=O)O>>CCO",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -1.8564977645874023
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -2.797421455383301
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.994331121444702
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[K+]",
            "reagent2": "",
            "sequence_score": -3.930743455886841
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -4.180272579193115
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "C1CCOC1",
            "reagent2": "",
            "sequence_score": -4.333145618438721
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -4.794863700866699
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[Na+]",
            "reagent2": "",
            "sequence_score": -5.26922607421875
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "C1CCOC1",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -5.376748085021973
          },
          {
            "rank": 10,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.290542602539062
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[K+]",
            "reagent2": "",
            "sequence_score": -8.367009162902832
          },
          {
            "rank": 12,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[Na+]",
            "reagent2": "",
            "sequence_score": -8.964522361755371
          },
          {
            "rank": 13,
            "catalyst1": "[Pd]",
            "solvent1": "CC(=O)O",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[K+]",
            "reagent2": "",
            "sequence_score": -9.066823959350586
          },
          {
            "rank": 14,
            "catalyst1": "[Pd]",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[K+]",
            "reagent2": "",
            "sequence_score": -9.778876304626465
          },
          {
            "rank": 15,
            "catalyst1": "[Pd]",
            "solvent1": "CC(=O)O",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[Na+]",
            "reagent2": "",
            "sequence_score": -10.121355056762695
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-05",
        "step_id": "step-01",
        "reaction_smiles": "CC(=O)O>>CCO",
        "raw_value": 0.2100452482700348,
        "yield_percent": 77.58890327412914,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 13,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-05",
      "step_id": "step-02",
      "depends_on": [
        "step-01"
      ],
      "precursor_stock_flags": [
        false,
        true
      ],
      "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCO",
        "Nc1ccc(C(=O)O)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "bf6bd9047791f3252d0082f87523bda9bf230f930fe417ac7de9fa8c502cbf89",
        "classification": "0.0 Unrecognized",
        "library_occurence": 6214,
        "policy_probability": 0.1680999994277954,
        "policy_probability_rank": 2,
        "policy_name": "uspto",
        "template_code": 31869,
        "template": "[C:4]-[O;H0;D2;+0:5]-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3]>>O-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3].[C:4]-[OH;D1;+0:5]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[C:4](=[O:5])([c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1)[OH:13].[CH3:1][CH2:2][OH:3]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CCOCC",
            "reagent2": "FB(F)F",
            "sequence_score": -2.1754837036132812
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CC(=O)Cl",
            "reagent2": "",
            "sequence_score": -2.3472180366516113
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.6159138679504395
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(=O)(O)O",
            "reagent2": "",
            "sequence_score": -2.7508246898651123
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cc1ccc(S(=O)(=O)O)cc1",
            "reagent2": "O",
            "sequence_score": -2.9795284271240234
          },
          {
            "rank": 6,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -3.796043872833252
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(Cl)Cl",
            "reagent2": "",
            "sequence_score": -5.475196838378906
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -5.52998161315918
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -5.658388137817383
          },
          {
            "rank": 10,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -6.2488322257995605
          },
          {
            "rank": 11,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.724697113037109
          },
          {
            "rank": 12,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.166314601898193
          },
          {
            "rank": 13,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -7.498518466949463
          },
          {
            "rank": 14,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.016460418701172
          },
          {
            "rank": 15,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -8.648869514465332
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-05",
        "step_id": "step-02",
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.31552639603614807,
        "yield_percent": 79.79832496878097,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 43,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-06",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true
      ],
      "reaction_smiles": "CCOC(C)=O>>CCO",
      "precursor_smiles": [
        "CCOC(C)=O"
      ],
      "product_smiles": "CCO",
      "metadata": {
        "template_hash": "13a53dfded53d8e3e9188e0a246098e61687a926572896c49176fbd03c843f33",
        "classification": "0.0 Unrecognized",
        "library_occurence": 5091,
        "policy_probability": 0.07039999961853027,
        "policy_probability_rank": 1,
        "policy_name": "uspto",
        "template_code": 3300,
        "template": "[C:3]-[C:2]-[OH;D1;+0:1]>>C-C(=O)-[O;H0;D2;+0:1]-[C:2]-[C:3]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][OH:3]>>[CH3:1][CH2:2][O:3][C:4]([CH3:5])=[O:6]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOC(C)=O>>CCO",
        "canonical_reaction_smiles": "CCOC(C)=O>>CCO",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -1.2221254110336304
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -1.3163814544677734
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -3.3732333183288574
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -3.429737091064453
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -3.750460386276245
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "[H-].[Na+]",
            "reagent2": "",
            "sequence_score": -3.8066563606262207
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.729113578796387
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -4.859377384185791
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -4.943013668060303
          },
          {
            "rank": 10,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -5.748725414276123
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -7.56317138671875
          },
          {
            "rank": 12,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -7.875537395477295
          },
          {
            "rank": 13,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.461974143981934
          },
          {
            "rank": 14,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -9.101846694946289
          },
          {
            "rank": 15,
            "catalyst1": "[Pd]",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -9.288086891174316
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-06",
        "step_id": "step-01",
        "reaction_smiles": "CCOC(C)=O>>CCO",
        "raw_value": 0.29851022362709045,
        "yield_percent": 79.44190203182289,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 15,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-06",
      "step_id": "step-02",
      "depends_on": [
        "step-01"
      ],
      "precursor_stock_flags": [
        false,
        true
      ],
      "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCO",
        "Nc1ccc(C(=O)O)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "bf6bd9047791f3252d0082f87523bda9bf230f930fe417ac7de9fa8c502cbf89",
        "classification": "0.0 Unrecognized",
        "library_occurence": 6214,
        "policy_probability": 0.1680999994277954,
        "policy_probability_rank": 2,
        "policy_name": "uspto",
        "template_code": 31869,
        "template": "[C:4]-[O;H0;D2;+0:5]-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3]>>O-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3].[C:4]-[OH;D1;+0:5]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[C:4](=[O:5])([c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1)[OH:13].[CH3:1][CH2:2][OH:3]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CCOCC",
            "reagent2": "FB(F)F",
            "sequence_score": -2.1754837036132812
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CC(=O)Cl",
            "reagent2": "",
            "sequence_score": -2.3472180366516113
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.6159138679504395
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(=O)(O)O",
            "reagent2": "",
            "sequence_score": -2.7508246898651123
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cc1ccc(S(=O)(=O)O)cc1",
            "reagent2": "O",
            "sequence_score": -2.9795284271240234
          },
          {
            "rank": 6,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -3.796043872833252
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(Cl)Cl",
            "reagent2": "",
            "sequence_score": -5.475196838378906
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -5.52998161315918
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -5.658388137817383
          },
          {
            "rank": 10,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -6.2488322257995605
          },
          {
            "rank": 11,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.724697113037109
          },
          {
            "rank": 12,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.166314601898193
          },
          {
            "rank": 13,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -7.498518466949463
          },
          {
            "rank": 14,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.016460418701172
          },
          {
            "rank": 15,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -8.648869514465332
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-06",
        "step_id": "step-02",
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.31552639603614807,
        "yield_percent": 79.79832496878097,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 43,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-07",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true
      ],
      "reaction_smiles": "CCOCc1ccccc1>>CCO",
      "precursor_smiles": [
        "CCOCc1ccccc1"
      ],
      "product_smiles": "CCO",
      "metadata": {
        "template_hash": "81e5d479b07120952b3f1fc090d28c2998576f7437fc81cc6464bff14c12c10a",
        "classification": "0.0 Unrecognized",
        "library_occurence": 1954,
        "policy_probability": 0.027899999171495438,
        "policy_probability_rank": 3,
        "policy_name": "uspto",
        "template_code": 21642,
        "template": "[C:1]-[OH;D1;+0:2]>>[C:1]-[O;H0;D2;+0:2]-C-c1:c:c:c:c:c:1",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][OH:3]>>[CH3:1][CH2:2][O:3][CH2:4][c:5]1[cH:6][cH:7][cH:8][cH:9][cH:10]1"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOCc1ccccc1>>CCO",
        "canonical_reaction_smiles": "CCOCc1ccccc1>>CCO",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -1.4996020793914795
          },
          {
            "rank": 2,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -2.1760787963867188
          },
          {
            "rank": 3,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.4178550243377686
          },
          {
            "rank": 4,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.674546957015991
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -3.034674882888794
          },
          {
            "rank": 6,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -3.235321283340454
          },
          {
            "rank": 7,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -3.5359725952148438
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.0752272605896
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.450875282287598
          },
          {
            "rank": 10,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "C",
            "reagent2": "C[O-].[Na+]",
            "sequence_score": -4.977729320526123
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "C1=CCCCC1",
            "reagent2": "",
            "sequence_score": -5.179065704345703
          },
          {
            "rank": 12,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "CCO",
            "reagent2": "",
            "sequence_score": -5.334011077880859
          },
          {
            "rank": 13,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -5.365540981292725
          },
          {
            "rank": 14,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "CCOCC",
            "reagent2": "FB(F)F",
            "sequence_score": -6.804378509521484
          },
          {
            "rank": 15,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "O=C1CCC(=O)N1Br",
            "reagent2": "",
            "sequence_score": -6.853660583496094
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-07",
        "step_id": "step-01",
        "reaction_smiles": "CCOCc1ccccc1>>CCO",
        "raw_value": 0.4255966544151306,
        "yield_percent": 82.10387076486666,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 18,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-07",
      "step_id": "step-02",
      "depends_on": [
        "step-01"
      ],
      "precursor_stock_flags": [
        false,
        true
      ],
      "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCO",
        "Nc1ccc(C(=O)O)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "bf6bd9047791f3252d0082f87523bda9bf230f930fe417ac7de9fa8c502cbf89",
        "classification": "0.0 Unrecognized",
        "library_occurence": 6214,
        "policy_probability": 0.1680999994277954,
        "policy_probability_rank": 2,
        "policy_name": "uspto",
        "template_code": 31869,
        "template": "[C:4]-[O;H0;D2;+0:5]-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3]>>O-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3].[C:4]-[OH;D1;+0:5]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[C:4](=[O:5])([c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1)[OH:13].[CH3:1][CH2:2][OH:3]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CCOCC",
            "reagent2": "FB(F)F",
            "sequence_score": -2.1754837036132812
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CC(=O)Cl",
            "reagent2": "",
            "sequence_score": -2.3472180366516113
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.6159138679504395
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(=O)(O)O",
            "reagent2": "",
            "sequence_score": -2.7508246898651123
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cc1ccc(S(=O)(=O)O)cc1",
            "reagent2": "O",
            "sequence_score": -2.9795284271240234
          },
          {
            "rank": 6,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -3.796043872833252
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(Cl)Cl",
            "reagent2": "",
            "sequence_score": -5.475196838378906
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -5.52998161315918
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -5.658388137817383
          },
          {
            "rank": 10,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -6.2488322257995605
          },
          {
            "rank": 11,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.724697113037109
          },
          {
            "rank": 12,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.166314601898193
          },
          {
            "rank": 13,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -7.498518466949463
          },
          {
            "rank": 14,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.016460418701172
          },
          {
            "rank": 15,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -8.648869514465332
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-07",
        "step_id": "step-02",
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.31552639603614807,
        "yield_percent": 79.79832496878097,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 43,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-08",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true
      ],
      "reaction_smiles": "COC(C)=O>>CCO",
      "precursor_smiles": [
        "COC(C)=O"
      ],
      "product_smiles": "CCO",
      "metadata": {
        "template_hash": "fa0d851e142c3b477b32521aea18d9f060fb648ef723206a28e37b25b71593bd",
        "classification": "0.0 Unrecognized",
        "library_occurence": 2881,
        "policy_probability": 0.020099999383091927,
        "policy_probability_rank": 5,
        "policy_name": "uspto",
        "template_code": 41576,
        "template": "[C:3]-[CH2;D2;+0:2]-[OH;D1;+0:1]>>C-[O;H0;D2;+0:1]-[C;H0;D3;+0:2](=O)-[C:3]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][OH:3]>>[CH3:1][C:2]([O:3][CH3:4])=[O:5]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "COC(C)=O>>CCO",
        "canonical_reaction_smiles": "COC(C)=O>>CCO",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -1.083698034286499
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -1.4739887714385986
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -3.3740928173065186
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -3.6971192359924316
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "[H-].[Na+]",
            "reagent2": "",
            "sequence_score": -4.233254909515381
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -4.515024185180664
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -5.214523792266846
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -5.36590576171875
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CCOCC",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -5.953917503356934
          },
          {
            "rank": 10,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.57941198348999
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -10.0001802444458
          },
          {
            "rank": 12,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "CO",
            "reagent2": "",
            "sequence_score": -10.685522079467773
          },
          {
            "rank": 13,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -10.78955078125
          },
          {
            "rank": 14,
            "catalyst1": "[Pd]",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -11.431573867797852
          },
          {
            "rank": 15,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -11.83074951171875
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-08",
        "step_id": "step-01",
        "reaction_smiles": "COC(C)=O>>CCO",
        "raw_value": 0.15397490561008453,
        "yield_percent": 76.41444666152056,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 14,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-08",
      "step_id": "step-02",
      "depends_on": [
        "step-01"
      ],
      "precursor_stock_flags": [
        false,
        true
      ],
      "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCO",
        "Nc1ccc(C(=O)O)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "bf6bd9047791f3252d0082f87523bda9bf230f930fe417ac7de9fa8c502cbf89",
        "classification": "0.0 Unrecognized",
        "library_occurence": 6214,
        "policy_probability": 0.1680999994277954,
        "policy_probability_rank": 2,
        "policy_name": "uspto",
        "template_code": 31869,
        "template": "[C:4]-[O;H0;D2;+0:5]-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3]>>O-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3].[C:4]-[OH;D1;+0:5]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[C:4](=[O:5])([c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1)[OH:13].[CH3:1][CH2:2][OH:3]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CCOCC",
            "reagent2": "FB(F)F",
            "sequence_score": -2.1754837036132812
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CC(=O)Cl",
            "reagent2": "",
            "sequence_score": -2.3472180366516113
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.6159138679504395
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(=O)(O)O",
            "reagent2": "",
            "sequence_score": -2.7508246898651123
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cc1ccc(S(=O)(=O)O)cc1",
            "reagent2": "O",
            "sequence_score": -2.9795284271240234
          },
          {
            "rank": 6,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -3.796043872833252
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(Cl)Cl",
            "reagent2": "",
            "sequence_score": -5.475196838378906
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -5.52998161315918
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -5.658388137817383
          },
          {
            "rank": 10,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -6.2488322257995605
          },
          {
            "rank": 11,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.724697113037109
          },
          {
            "rank": 12,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.166314601898193
          },
          {
            "rank": 13,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -7.498518466949463
          },
          {
            "rank": 14,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.016460418701172
          },
          {
            "rank": 15,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -8.648869514465332
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-08",
        "step_id": "step-02",
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.31552639603614807,
        "yield_percent": 79.79832496878097,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 43,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-09",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true
      ],
      "reaction_smiles": "CCO[Si](C)(C)C(C)(C)C>>CCO",
      "precursor_smiles": [
        "CCO[Si](C)(C)C(C)(C)C"
      ],
      "product_smiles": "CCO",
      "metadata": {
        "template_hash": "5a6df5201d3deedc0c8a2e95760ac64e7b20bed15455d053a10230fddcd650d2",
        "classification": "0.0 Unrecognized",
        "library_occurence": 5956,
        "policy_probability": 0.008799999952316284,
        "policy_probability_rank": 7,
        "policy_name": "uspto",
        "template_code": 15128,
        "template": "[C:2]-[OH;D1;+0:1]>>C-C(-C)(-C)-[Si](-C)(-C)-[O;H0;D2;+0:1]-[C:2]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][OH:3]>>[CH3:1][CH2:2][O:3][Si:4]([C:5]([CH3:6])([CH3:7])[CH3:8])([CH3:9])[CH3:10]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCO[Si](C)(C)C(C)(C)C>>CCO",
        "canonical_reaction_smiles": "CCO[Si](C)(C)C(C)(C)C>>CCO",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "CCCC[N+](CCCC)(CCCC)CCCC.[F-]",
            "reagent2": "",
            "sequence_score": -1.603074073791504
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -2.5312907695770264
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "CCCC[N+](CCCC)(CCCC)CCCC.[F-]",
            "sequence_score": -2.708242177963257
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -3.4517018795013428
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -3.7617411613464355
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.6967387199401855
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "CCOCC",
            "reagent2": "Cl",
            "sequence_score": -4.927858829498291
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -4.979980945587158
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[K+].[OH-]",
            "reagent2": "",
            "sequence_score": -5.1338791847229
          },
          {
            "rank": 10,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -6.192807674407959
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -6.632704734802246
          },
          {
            "rank": 12,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.957650661468506
          },
          {
            "rank": 13,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.30918025970459
          },
          {
            "rank": 14,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -7.365476131439209
          },
          {
            "rank": 15,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -8.29153060913086
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-09",
        "step_id": "step-01",
        "reaction_smiles": "CCO[Si](C)(C)C(C)(C)C>>CCO",
        "raw_value": 0.4711652398109436,
        "yield_percent": 83.05835621843174,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 24,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-09",
      "step_id": "step-02",
      "depends_on": [
        "step-01"
      ],
      "precursor_stock_flags": [
        false,
        true
      ],
      "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCO",
        "Nc1ccc(C(=O)O)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "bf6bd9047791f3252d0082f87523bda9bf230f930fe417ac7de9fa8c502cbf89",
        "classification": "0.0 Unrecognized",
        "library_occurence": 6214,
        "policy_probability": 0.1680999994277954,
        "policy_probability_rank": 2,
        "policy_name": "uspto",
        "template_code": 31869,
        "template": "[C:4]-[O;H0;D2;+0:5]-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3]>>O-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3].[C:4]-[OH;D1;+0:5]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[C:4](=[O:5])([c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1)[OH:13].[CH3:1][CH2:2][OH:3]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CCOCC",
            "reagent2": "FB(F)F",
            "sequence_score": -2.1754837036132812
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CC(=O)Cl",
            "reagent2": "",
            "sequence_score": -2.3472180366516113
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.6159138679504395
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(=O)(O)O",
            "reagent2": "",
            "sequence_score": -2.7508246898651123
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cc1ccc(S(=O)(=O)O)cc1",
            "reagent2": "O",
            "sequence_score": -2.9795284271240234
          },
          {
            "rank": 6,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -3.796043872833252
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(Cl)Cl",
            "reagent2": "",
            "sequence_score": -5.475196838378906
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -5.52998161315918
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -5.658388137817383
          },
          {
            "rank": 10,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -6.2488322257995605
          },
          {
            "rank": 11,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.724697113037109
          },
          {
            "rank": 12,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.166314601898193
          },
          {
            "rank": 13,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -7.498518466949463
          },
          {
            "rank": 14,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.016460418701172
          },
          {
            "rank": 15,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -8.648869514465332
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-09",
        "step_id": "step-02",
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.31552639603614807,
        "yield_percent": 79.79832496878097,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 43,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-10",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true,
        true
      ],
      "reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1.CC(C)(C)OC(=O)OC(=O)OC(C)(C)C>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
      "precursor_smiles": [
        "CCOC(=O)c1ccc([N+](=O)[O-])cc1",
        "CC(C)(C)OC(=O)OC(=O)OC(C)(C)C"
      ],
      "product_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
      "metadata": {
        "template_hash": "6c1f0998f5a1204d803a7d26455d4b60ade442865bd5ae920a2684c3975f067c",
        "classification": "0.0 Unrecognized",
        "library_occurence": 47,
        "policy_probability": 0.008200000040233135,
        "policy_probability_rank": 16,
        "policy_name": "uspto",
        "template_code": 18019,
        "template": "[C;D1;H3:5]-[C:4](-[C;D1;H3:6])(-[C;D1;H3:7])-[#8:3]-[C;H0;D3;+0:1](=[O;D1;H0:2])-[NH;D2;+0:8]-[c:9]>>C-C(-C)(-C)-O-C(=O)-O-[C;H0;D3;+0:1](=[O;D1;H0:2])-[#8:3]-[C:4](-[C;D1;H3:5])(-[C;D1;H3:6])-[C;D1;H3:7].O=[N+;H0;D3:8](-[O-])-[c:9]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH:10][C:13]([O:14][C:15]([CH3:16])([CH3:17])[CH3:18])=[O:19])[cH:11][cH:12]1>>[C:13]([O:14][C:15]([CH3:16])([CH3:17])[CH3:18])(=[O:19])[O:20][C:21]([O:22][C:23]([CH3:24])([CH3:25])[CH3:26])=[O:27].[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([N+:10](=[O:28])[O-:29])[cH:11][cH:12]1"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1.CC(C)(C)OC(=O)OC(=O)OC(C)(C)C>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
        "canonical_reaction_smiles": "CC(C)(C)OC(=O)OC(=O)OC(C)(C)C.CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -1.4688613414764404
          },
          {
            "rank": 2,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.1484031677246094
          },
          {
            "rank": 3,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -2.6139049530029297
          },
          {
            "rank": 4,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.623936891555786
          },
          {
            "rank": 5,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -3.271146774291992
          },
          {
            "rank": 6,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -3.631624698638916
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.515300273895264
          },
          {
            "rank": 8,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -5.079000949859619
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -5.292091369628906
          },
          {
            "rank": 10,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -5.527890682220459
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -5.579928398132324
          },
          {
            "rank": 12,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "CCO",
            "reagent2": "",
            "sequence_score": -5.60085916519165
          },
          {
            "rank": 13,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -5.994451522827148
          },
          {
            "rank": 14,
            "catalyst1": "",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -6.929775714874268
          },
          {
            "rank": 15,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -7.044196128845215
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-10",
        "step_id": "step-01",
        "reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1.CC(C)(C)OC(=O)OC(=O)OC(C)(C)C>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
        "raw_value": -0.30631986260414124,
        "yield_percent": 66.7730532147765,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 90,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-10",
      "step_id": "step-02",
      "depends_on": [
        "step-01"
      ],
      "precursor_stock_flags": [
        false
      ],
      "reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "303ca079c60ed19d48241eab345c45a0301370b759b04d5bf70d770b04fd164b",
        "classification": "0.0 Unrecognized",
        "library_occurence": 1947,
        "policy_probability": 0.0052999998442828655,
        "policy_probability_rank": 7,
        "policy_name": "uspto",
        "template_code": 8083,
        "template": "[NH2;D1;+0:1]-[c:2]>>C-C(-C)(-C)-O-C(=O)-[NH;D2;+0:1]-[c:2]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH:10][C:13]([O:14][C:15]([CH3:16])([CH3:17])[CH3:18])=[O:19])[cH:11][cH:12]1"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "O=C(O)C(F)(F)F",
            "reagent2": "",
            "sequence_score": -0.9713290333747864
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -2.1432390213012695
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -2.4259133338928223
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "C1COCCO1",
            "reagent2": "Cl",
            "sequence_score": -4.477711200714111
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "O=C(O)C(F)(F)F",
            "sequence_score": -4.5558342933654785
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.963832855224609
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "C1COCCO1",
            "reagent2": "Cl",
            "sequence_score": -5.00631046295166
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -5.375456809997559
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "CCOC(C)=O",
            "reagent2": "Cl",
            "sequence_score": -5.666500568389893
          },
          {
            "rank": 10,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.624959945678711
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.614686965942383
          },
          {
            "rank": 12,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -9.368593215942383
          },
          {
            "rank": 13,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -9.488094329833984
          },
          {
            "rank": 14,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -10.797574996948242
          },
          {
            "rank": 15,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -10.971100807189941
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-10",
        "step_id": "step-02",
        "reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.5715302228927612,
        "yield_percent": 85.16061406924716,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 55,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-11",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true,
        true
      ],
      "reaction_smiles": "CC(C)(C)OC(N)=O.CCOC(=O)c1ccc(Br)cc1>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
      "precursor_smiles": [
        "CC(C)(C)OC(N)=O",
        "CCOC(=O)c1ccc(Br)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
      "metadata": {
        "template_hash": "75721415d53dcdeab06befe74ff673721c6b194c12e47ced2154269ce281cede",
        "classification": "0.0 Unrecognized",
        "library_occurence": 59,
        "policy_probability": 0.0032999999821186066,
        "policy_probability_rank": 23,
        "policy_name": "uspto",
        "template_code": 19596,
        "template": "[C;D1;H3:4]-[C:5](-[C;D1;H3:6])(-[C;D1;H3:7])-[#8:8]-[C:9](=[O;D1;H0:11])-[NH;D2;+0:10]-[c;H0;D3;+0:1](:[c:2]):[c:3]>>Br-[c;H0;D3;+0:1](:[c:2]):[c:3].[C;D1;H3:4]-[C:5](-[C;D1;H3:6])(-[C;D1;H3:7])-[#8:8]-[C:9](-[NH2;D1;+0:10])=[O;D1;H0:11]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH:10][C:13]([O:14][C:15]([CH3:16])([CH3:17])[CH3:18])=[O:19])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([Br:20])[cH:11][cH:12]1.[NH2:10][C:13]([O:14][C:15]([CH3:16])([CH3:17])[CH3:18])=[O:19]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CC(C)(C)OC(N)=O.CCOC(=O)c1ccc(Br)cc1>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
        "canonical_reaction_smiles": "CC(C)(C)OC(N)=O.CCOC(=O)c1ccc(Br)cc1>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "[Cu]I",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "CNCCNC",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -1.0220422744750977
          },
          {
            "rank": 2,
            "catalyst1": "[Cu]I",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "CNCCNC",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -2.820655584335327
          },
          {
            "rank": 3,
            "catalyst1": "[Cu]I",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "N[C@@H]1CCCC[C@H]1N",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -3.03572678565979
          },
          {
            "rank": 4,
            "catalyst1": "I[Cu]I",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "CNCCNC",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -3.646731376647949
          },
          {
            "rank": 5,
            "catalyst1": "[Cu]I",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "N[C@@H]1CCCC[C@H]1N",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -4.312783718109131
          },
          {
            "rank": 6,
            "catalyst1": "I[Cu]I",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "N[C@@H]1CCCC[C@H]1N",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -4.796841621398926
          },
          {
            "rank": 7,
            "catalyst1": "[Cu]I",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "CNCCNC",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -5.288001537322998
          },
          {
            "rank": 8,
            "catalyst1": "[Cu]I",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "O=C([O-])[O-].[Cs+].[Cs+]",
            "reagent2": "",
            "sequence_score": -5.337760925292969
          },
          {
            "rank": 9,
            "catalyst1": "[Cu]I",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "N[C@@H]1CCCC[C@H]1N",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -5.960392951965332
          },
          {
            "rank": 10,
            "catalyst1": "I[Cu]I",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "CNCCNC",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -5.961459159851074
          },
          {
            "rank": 11,
            "catalyst1": "[Cu]I",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "CN[C@@H]1CCCC[C@H]1NC",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -6.04400110244751
          },
          {
            "rank": 12,
            "catalyst1": "[Cu]I",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "O=C([O-])[O-].[K+].[K+]",
            "reagent2": "",
            "sequence_score": -6.3879714012146
          },
          {
            "rank": 13,
            "catalyst1": "I[Cu]I",
            "solvent1": "CCOC(C)=O",
            "solvent2": "Cc1ccccc1",
            "reagent1": "CNCCNC",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -6.52508544921875
          },
          {
            "rank": 14,
            "catalyst1": "I[Cu]I",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "N[C@@H]1CCCC[C@H]1N",
            "reagent2": "O=C([O-])[O-].[K+].[K+]",
            "sequence_score": -6.709542274475098
          },
          {
            "rank": 15,
            "catalyst1": "I[Cu]I",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "O=C([O-])[O-].[Cs+].[Cs+]",
            "reagent2": "",
            "sequence_score": -7.512386798858643
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-11",
        "step_id": "step-01",
        "reaction_smiles": "CC(C)(C)OC(N)=O.CCOC(=O)c1ccc(Br)cc1>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
        "raw_value": -0.17951302230358124,
        "yield_percent": 69.4291656094912,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 71,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-11",
      "step_id": "step-02",
      "depends_on": [
        "step-01"
      ],
      "precursor_stock_flags": [
        false
      ],
      "reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "303ca079c60ed19d48241eab345c45a0301370b759b04d5bf70d770b04fd164b",
        "classification": "0.0 Unrecognized",
        "library_occurence": 1947,
        "policy_probability": 0.0052999998442828655,
        "policy_probability_rank": 7,
        "policy_name": "uspto",
        "template_code": 8083,
        "template": "[NH2;D1;+0:1]-[c:2]>>C-C(-C)(-C)-O-C(=O)-[NH;D2;+0:1]-[c:2]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH:10][C:13]([O:14][C:15]([CH3:16])([CH3:17])[CH3:18])=[O:19])[cH:11][cH:12]1"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "O=C(O)C(F)(F)F",
            "reagent2": "",
            "sequence_score": -0.9713290333747864
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -2.1432390213012695
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -2.4259133338928223
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "C1COCCO1",
            "reagent2": "Cl",
            "sequence_score": -4.477711200714111
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "O=C(O)C(F)(F)F",
            "sequence_score": -4.5558342933654785
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.963832855224609
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "C1COCCO1",
            "reagent2": "Cl",
            "sequence_score": -5.00631046295166
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -5.375456809997559
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "CCOC(C)=O",
            "reagent2": "Cl",
            "sequence_score": -5.666500568389893
          },
          {
            "rank": 10,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.624959945678711
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.614686965942383
          },
          {
            "rank": 12,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -9.368593215942383
          },
          {
            "rank": 13,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -9.488094329833984
          },
          {
            "rank": 14,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -10.797574996948242
          },
          {
            "rank": 15,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -10.971100807189941
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-11",
        "step_id": "step-02",
        "reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.5715302228927612,
        "yield_percent": 85.16061406924716,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 55,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-12",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true,
        true
      ],
      "reaction_smiles": "CC(C)(C)O.CCOC(=O)c1ccc(N=C=O)cc1>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
      "precursor_smiles": [
        "CC(C)(C)O",
        "CCOC(=O)c1ccc(N=C=O)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
      "metadata": {
        "template_hash": "8b76950ffe2d69e2b5c3a150443a9d193a187a5fe22642a78f99bf6e6890e3b9",
        "classification": "0.0 Unrecognized",
        "library_occurence": 436,
        "policy_probability": 0.003100000089034438,
        "policy_probability_rank": 27,
        "policy_name": "uspto",
        "template_code": 23231,
        "template": "[C:1]-[O;H0;D2;+0:2]-[C;H0;D3;+0:4](=[O;D1;H0:3])-[NH;D2;+0:5]-[c:6]>>[C:1]-[OH;D1;+0:2].[O;D1;H0:3]=[C;H0;D2;+0:4]=[N;H0;D2;+0:5]-[c:6]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH:10][C:13]([O:14][C:15]([CH3:16])([CH3:17])[CH3:18])=[O:19])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([N:10]=[C:13]=[O:19])[cH:11][cH:12]1.[OH:14][C:15]([CH3:16])([CH3:17])[CH3:18]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CC(C)(C)O.CCOC(=O)c1ccc(N=C=O)cc1>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
        "canonical_reaction_smiles": "CC(C)(C)O.CCOC(=O)c1ccc(N=C=O)cc1>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -1.7368918657302856
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -2.621133804321289
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.852628231048584
          },
          {
            "rank": 4,
            "catalyst1": "CN(C)c1ccncc1",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -3.01552152633667
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -3.1860570907592773
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -3.4168710708618164
          },
          {
            "rank": 7,
            "catalyst1": "CN(C)c1ccncc1",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -3.5705270767211914
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "c1ccncc1",
            "reagent2": "",
            "sequence_score": -3.683016300201416
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.112870693206787
          },
          {
            "rank": 10,
            "catalyst1": "CN(C)c1ccncc1",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -4.674372673034668
          },
          {
            "rank": 11,
            "catalyst1": "",
            "solvent1": "Cc1ccccc1",
            "solvent2": "",
            "reagent1": "c1ccncc1",
            "reagent2": "",
            "sequence_score": -4.7290496826171875
          },
          {
            "rank": 12,
            "catalyst1": "CN(C)c1ccncc1",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "CCN(CC)CC",
            "reagent2": "",
            "sequence_score": -5.139808654785156
          },
          {
            "rank": 13,
            "catalyst1": "CN(C)c1ccncc1",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -5.533695697784424
          },
          {
            "rank": 14,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "c1ccncc1",
            "reagent2": "",
            "sequence_score": -5.558281421661377
          },
          {
            "rank": 15,
            "catalyst1": "CN(C)c1ccncc1",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -5.583839416503906
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-12",
        "step_id": "step-01",
        "reaction_smiles": "CC(C)(C)O.CCOC(=O)c1ccc(N=C=O)cc1>>CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1",
        "raw_value": 0.29192715883255005,
        "yield_percent": 79.3040123095134,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 69,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-12",
      "step_id": "step-02",
      "depends_on": [
        "step-01"
      ],
      "precursor_stock_flags": [
        false
      ],
      "reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "303ca079c60ed19d48241eab345c45a0301370b759b04d5bf70d770b04fd164b",
        "classification": "0.0 Unrecognized",
        "library_occurence": 1947,
        "policy_probability": 0.0052999998442828655,
        "policy_probability_rank": 7,
        "policy_name": "uspto",
        "template_code": 8083,
        "template": "[NH2;D1;+0:1]-[c:2]>>C-C(-C)(-C)-O-C(=O)-[NH;D2;+0:1]-[c:2]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH:10][C:13]([O:14][C:15]([CH3:16])([CH3:17])[CH3:18])=[O:19])[cH:11][cH:12]1"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "O=C(O)C(F)(F)F",
            "reagent2": "",
            "sequence_score": -0.9713290333747864
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -2.1432390213012695
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -2.4259133338928223
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "C1COCCO1",
            "reagent2": "Cl",
            "sequence_score": -4.477711200714111
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "ClCCl",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "O=C(O)C(F)(F)F",
            "sequence_score": -4.5558342933654785
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.963832855224609
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "C1COCCO1",
            "reagent2": "Cl",
            "sequence_score": -5.00631046295166
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -5.375456809997559
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "C1COCCO1",
            "solvent2": "",
            "reagent1": "CCOC(C)=O",
            "reagent2": "Cl",
            "sequence_score": -5.666500568389893
          },
          {
            "rank": 10,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.624959945678711
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.614686965942383
          },
          {
            "rank": 12,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -9.368593215942383
          },
          {
            "rank": 13,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -9.488094329833984
          },
          {
            "rank": 14,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -10.797574996948242
          },
          {
            "rank": 15,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -10.971100807189941
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-12",
        "step_id": "step-02",
        "reaction_smiles": "CCOC(=O)c1ccc(NC(=O)OC(C)(C)C)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.5715302228927612,
        "yield_percent": 85.16061406924716,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 55,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    }
  ],
  "selected_route_ids": [
    "route-01",
    "route-02",
    "route-05"
  ],
  "report_steps": [
    {
      "route_id": "route-01",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true
      ],
      "reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCOC(=O)c1ccc([N+](=O)[O-])cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "664f7756f7526ad6c07e82dd3b3c15f7aabccbc99837dd22105068a2cfc385b5",
        "classification": "0.0 Unrecognized",
        "library_occurence": 33350,
        "policy_probability": 0.42239999771118164,
        "policy_probability_rank": 0,
        "policy_name": "uspto",
        "template_code": 17064,
        "template": "[NH2;D1;+0:1]-[c:2]>>O=[N+;H0;D3:1](-[O-])-[c:2]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([N+:10](=[O:13])[O-:14])[cH:11][cH:12]1"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -1.700762152671814
          },
          {
            "rank": 2,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.0481550693511963
          },
          {
            "rank": 3,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.7931230068206787
          },
          {
            "rank": 4,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -2.878655195236206
          },
          {
            "rank": 5,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -3.4926724433898926
          },
          {
            "rank": 6,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "[H][H]",
            "reagent2": "",
            "sequence_score": -3.8862576484680176
          },
          {
            "rank": 7,
            "catalyst1": "[Fe]",
            "solvent1": "CCO",
            "solvent2": "O",
            "reagent1": "[Cl-].[NH4+]",
            "reagent2": "",
            "sequence_score": -3.8886513710021973
          },
          {
            "rank": 8,
            "catalyst1": "[Pd]",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "O=C[O-].[NH4+]",
            "reagent2": "",
            "sequence_score": -4.486337661743164
          },
          {
            "rank": 9,
            "catalyst1": "[Fe]",
            "solvent1": "CC(=O)O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -4.683133125305176
          },
          {
            "rank": 10,
            "catalyst1": "[Pd]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "O=C[O-].[NH4+]",
            "reagent2": "",
            "sequence_score": -5.087017059326172
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "CCOC(C)=O",
            "solvent2": "",
            "reagent1": "CCO",
            "reagent2": "",
            "sequence_score": -5.712345600128174
          },
          {
            "rank": 12,
            "catalyst1": "[Fe]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "[Cl-].[NH4+]",
            "reagent2": "",
            "sequence_score": -6.493983268737793
          },
          {
            "rank": 13,
            "catalyst1": "[Fe]",
            "solvent1": "CCO",
            "solvent2": "O",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.5203938484191895
          },
          {
            "rank": 14,
            "catalyst1": "[Fe]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.688980579376221
          },
          {
            "rank": 15,
            "catalyst1": "[Fe]",
            "solvent1": "CO",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "[Cl-].[NH4+]",
            "sequence_score": -6.779082298278809
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-01",
        "step_id": "step-01",
        "reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.46616947650909424,
        "yield_percent": 82.95371431744555,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 46,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-02",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true
      ],
      "reaction_smiles": "CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCOC(=O)c1ccc(NC(C)=O)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "8063032398e59c77d82569a4231c9d8f1dc9cd333085943b3f9ae7b5eafd5071",
        "classification": "0.0 Unrecognized",
        "library_occurence": 1668,
        "policy_probability": 0.011800000444054604,
        "policy_probability_rank": 5,
        "policy_name": "uspto",
        "template_code": 21399,
        "template": "[NH2;D1;+0:1]-[c:2]>>C-C(=O)-[NH;D2;+0:1]-[c:2]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH:10][C:13]([CH3:14])=[O:15])[cH:11][cH:12]1"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -1.3239554166793823
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "Cl",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.660543441772461
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -3.2928555011749268
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "Cl",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -3.6584954261779785
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "Cl",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -3.7139711380004883
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "O=S(=O)(O)O",
            "sequence_score": -4.38345193862915
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CCO",
            "reagent2": "Cl",
            "sequence_score": -4.546271324157715
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -4.650010585784912
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(=O)(O)O",
            "reagent2": "",
            "sequence_score": -6.109102249145508
          },
          {
            "rank": 10,
            "catalyst1": "Cl",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -6.133055210113525
          },
          {
            "rank": 11,
            "catalyst1": "Cl",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "",
            "sequence_score": -8.281896591186523
          },
          {
            "rank": 12,
            "catalyst1": "Cl",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CCO",
            "reagent2": "",
            "sequence_score": -9.194323539733887
          },
          {
            "rank": 13,
            "catalyst1": "Cl",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -9.742517471313477
          },
          {
            "rank": 14,
            "catalyst1": "Cl",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -9.823410987854004
          },
          {
            "rank": 15,
            "catalyst1": "Cl",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CCOC(C)=O",
            "reagent2": "O=C([O-])O.[Na+]",
            "sequence_score": -10.718693733215332
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-02",
        "step_id": "step-01",
        "reaction_smiles": "CCOC(=O)c1ccc(NC(C)=O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.21513395011425018,
        "yield_percent": 77.69549187778327,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 47,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-05",
      "step_id": "step-01",
      "depends_on": [],
      "precursor_stock_flags": [
        true
      ],
      "reaction_smiles": "CC(=O)O>>CCO",
      "precursor_smiles": [
        "CC(=O)O"
      ],
      "product_smiles": "CCO",
      "metadata": {
        "template_hash": "c42f96a0658c03bc12dc20efce06e66daaeccc675d73631eea24ea610a7227b8",
        "classification": "0.0 Unrecognized",
        "library_occurence": 3921,
        "policy_probability": 0.09149999916553497,
        "policy_probability_rank": 0,
        "policy_name": "uspto",
        "template_code": 32658,
        "template": "[C:2]-[CH2;D2;+0:1]-[O;D1;H1:3]>>O=[C;H0;D3;+0:1](-[C:2])-[O;D1;H1:3]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][OH:3]>>[CH3:1][C:2]([OH:3])=[O:4]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CC(=O)O>>CCO",
        "canonical_reaction_smiles": "CC(=O)O>>CCO",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -1.8564977645874023
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -2.797421455383301
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "C1CCOC1",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.994331121444702
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[K+]",
            "reagent2": "",
            "sequence_score": -3.930743455886841
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "O",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -4.180272579193115
          },
          {
            "rank": 6,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "C1CCOC1",
            "reagent2": "",
            "sequence_score": -4.333145618438721
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "reagent2": "",
            "sequence_score": -4.794863700866699
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[Na+]",
            "reagent2": "",
            "sequence_score": -5.26922607421875
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "CCOCC",
            "solvent2": "",
            "reagent1": "C1CCOC1",
            "reagent2": "[Al+3].[H-].[H-].[H-].[H-].[Li+]",
            "sequence_score": -5.376748085021973
          },
          {
            "rank": 10,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.290542602539062
          },
          {
            "rank": 11,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[K+]",
            "reagent2": "",
            "sequence_score": -8.367009162902832
          },
          {
            "rank": 12,
            "catalyst1": "[Pd]",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[Na+]",
            "reagent2": "",
            "sequence_score": -8.964522361755371
          },
          {
            "rank": 13,
            "catalyst1": "[Pd]",
            "solvent1": "CC(=O)O",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[K+]",
            "reagent2": "",
            "sequence_score": -9.066823959350586
          },
          {
            "rank": 14,
            "catalyst1": "[Pd]",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[K+]",
            "reagent2": "",
            "sequence_score": -9.778876304626465
          },
          {
            "rank": 15,
            "catalyst1": "[Pd]",
            "solvent1": "CC(=O)O",
            "solvent2": "",
            "reagent1": "CC(=O)[O-].[Na+]",
            "reagent2": "",
            "sequence_score": -10.121355056762695
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-05",
        "step_id": "step-01",
        "reaction_smiles": "CC(=O)O>>CCO",
        "raw_value": 0.2100452482700348,
        "yield_percent": 77.58890327412914,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 13,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    },
    {
      "route_id": "route-05",
      "step_id": "step-02",
      "depends_on": [
        "step-01"
      ],
      "precursor_stock_flags": [
        false,
        true
      ],
      "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
      "precursor_smiles": [
        "CCO",
        "Nc1ccc(C(=O)O)cc1"
      ],
      "product_smiles": "CCOC(=O)c1ccc(N)cc1",
      "metadata": {
        "template_hash": "bf6bd9047791f3252d0082f87523bda9bf230f930fe417ac7de9fa8c502cbf89",
        "classification": "0.0 Unrecognized",
        "library_occurence": 6214,
        "policy_probability": 0.1680999994277954,
        "policy_probability_rank": 2,
        "policy_name": "uspto",
        "template_code": 31869,
        "template": "[C:4]-[O;H0;D2;+0:5]-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3]>>O-[C;H0;D3;+0:1](=[O;D1;H0:2])-[c:3].[C:4]-[OH;D1;+0:5]",
        "mapped_reaction_smiles": "[CH3:1][CH2:2][O:3][C:4](=[O:5])[c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1>>[C:4](=[O:5])([c:6]1[cH:7][cH:8][c:9]([NH2:10])[cH:11][cH:12]1)[OH:13].[CH3:1][CH2:2][OH:3]"
      },
      "caveat": "Template-derived disconnection; omitted agents were not reconstructed.",
      "conditions": {
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "canonical_reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "candidates": [
          {
            "rank": 1,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CCOCC",
            "reagent2": "FB(F)F",
            "sequence_score": -2.1754837036132812
          },
          {
            "rank": 2,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "CC(=O)Cl",
            "reagent2": "",
            "sequence_score": -2.3472180366516113
          },
          {
            "rank": 3,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -2.6159138679504395
          },
          {
            "rank": 4,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(=O)(O)O",
            "reagent2": "",
            "sequence_score": -2.7508246898651123
          },
          {
            "rank": 5,
            "catalyst1": "",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "Cc1ccc(S(=O)(=O)O)cc1",
            "reagent2": "O",
            "sequence_score": -2.9795284271240234
          },
          {
            "rank": 6,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -3.796043872833252
          },
          {
            "rank": 7,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=S(Cl)Cl",
            "reagent2": "",
            "sequence_score": -5.475196838378906
          },
          {
            "rank": 8,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -5.52998161315918
          },
          {
            "rank": 9,
            "catalyst1": "",
            "solvent1": "O=S(=O)(O)O",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -5.658388137817383
          },
          {
            "rank": 10,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -6.2488322257995605
          },
          {
            "rank": 11,
            "catalyst1": "",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "Cl",
            "reagent2": "",
            "sequence_score": -6.724697113037109
          },
          {
            "rank": 12,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -7.166314601898193
          },
          {
            "rank": 13,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "",
            "solvent2": "",
            "reagent1": "[Na+].[OH-]",
            "reagent2": "",
            "sequence_score": -7.498518466949463
          },
          {
            "rank": 14,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "CCO",
            "solvent2": "",
            "reagent1": "",
            "reagent2": "",
            "sequence_score": -8.016460418701172
          },
          {
            "rank": 15,
            "catalyst1": "O=S(=O)(O)O",
            "solvent1": "O",
            "solvent2": "",
            "reagent1": "O=C([O-])O.[Na+]",
            "reagent2": "",
            "sequence_score": -8.648869514465332
          }
        ],
        "temperature": null,
        "temperature_status": "not_provided_by_checkpoint",
        "time": null,
        "yield_percent": null
      },
      "yield_prediction": {
        "route_id": "route-05",
        "step_id": "step-02",
        "reaction_smiles": "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1",
        "raw_value": 0.31552639603614807,
        "yield_percent": 79.79832496878097,
        "raw_output_scale": "standardized_fraction",
        "yield_status": "predicted_not_validated",
        "within_physical_bounds": true,
        "input_tokens": 43,
        "max_input_tokens": 300,
        "input_truncated": false,
        "applicability": "not_assessed",
        "conditions_in_input": false
      }
    }
  ],
  "report_figure_assets": [
    {
      "figure_id": "target",
      "path": ".\\results\\benzocaine-live-20261031-04\\target\\target.png",
      "caption": "Benzocaine structure",
      "sha256": "257f09a109f1e38da95989f42a595f2362a5adb7628c243374e0a3cef439efaa"
    },
    {
      "figure_id": "route-01/step-01",
      "path": ".\\results\\benzocaine-live-20261031-04\\figures\\route-01-step-01.png",
      "caption": "route-01 step-01 predicted reaction",
      "sha256": "42f47032880a4b4e5936e5cf8572e3ec44232953f592b7132bb230ef21dda3d7"
    },
    {
      "figure_id": "route-02/step-01",
      "path": ".\\results\\benzocaine-live-20261031-04\\figures\\route-02-step-01.png",
      "caption": "route-02 step-01 predicted reaction",
      "sha256": "cf09de3b47f8354e1bb9bcff219bb8ded618309f2ae77477fbbe052d5b8075c2"
    },
    {
      "figure_id": "route-05/step-01",
      "path": ".\\results\\benzocaine-live-20261031-04\\figures\\route-05-step-01.png",
      "caption": "route-05 step-01 predicted reaction",
      "sha256": "eb2995a7f1ff8bdd381efa7d5485033b7bab9d1938a44439ff5d00e094ce6c1d"
    },
    {
      "figure_id": "route-05/step-02",
      "path": ".\\results\\benzocaine-live-20261031-04\\figures\\route-05-step-02.png",
      "caption": "route-05 step-02 predicted reaction",
      "sha256": "ecc5a2b821d81e10b71cebceeb8e57a3d697e0c45e611da51622ebb99cb0fadb"
    }
  ],
  "required_references": [
    {
      "title": "Benzocaine identity",
      "url": "https://pubchem.ncbi.nlm.nih.gov/compound/2337",
      "id": 1
    },
    {
      "title": "aizynthfinder",
      "url": "https://github.com/MolecularAI/aizynthfinder",
      "id": 2
    },
    {
      "title": "synthex",
      "url": "https://github.com/schwallergroup/synthex/tree/submission",
      "id": 3
    },
    {
      "title": "askcos",
      "url": "https://gitlab.com/mlpds_mit/askcosv2/context_recommender",
      "id": 4
    },
    {
      "title": "parrot",
      "url": "https://github.com/wangxr0526/Parrot",
      "id": 5
    },
    {
      "title": "rxn_yields",
      "url": "https://github.com/rxn4chemistry/rxn_yields",
      "id": 6
    },
    {
      "title": "drfp",
      "url": "https://github.com/reymond-group/drfp",
      "id": 7
    },
    {
      "title": "Yield normalization code",
      "url": "https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/training_scripts/launch_uspto_training.py",
      "id": 8
    },
    {
      "title": "Training data",
      "url": "https://ibm.ent.box.com/v/uspto-yields-data",
      "id": 9
    }
  ],
  "limitations": [
    {
      "kind": "cross_model_limit",
      "note": "Parrot conditions are not inputs to the yield model. Predicted yields are not experimentally validated."
    },
    {
      "kind": "model_applicability",
      "note": "Target-specific accuracy and domain membership are not assessed; normalization correctness is not accuracy validation."
    },
    {
      "kind": "missing_conditions",
      "note": "Temperature, time and equivalents are not supplied by the selected condition checkpoint."
    },
    {
      "kind": "route_limit",
      "note": "Stock membership and template scores do not prove practical feasibility. Search excludes target from stock; agents/byproducts can be omitted."
    }
  ],
  "additional_analyses": {
    "harness_comparison": {
      "status": "not_implemented",
      "inference_executed": false,
      "reason": "Preparation only; tool installation or paid execution is not authorized in this phase"
    },
    "mopac": {
      "status": "not_implemented",
      "inference_executed": false,
      "reason": "Preparation only; tool installation or paid execution is not authorized in this phase"
    },
    "epi_suite": {
      "status": "not_implemented",
      "inference_executed": false,
      "reason": "Preparation only; tool installation or paid execution is not authorized in this phase"
    },
    "discovery_studio": {
      "status": "not_implemented",
      "inference_executed": false,
      "reason": "Preparation only; tool installation or paid execution is not authorized in this phase"
    }
  },
  "report_plan": {
    "maximum_pages_including_references": 20,
    "planned_pages": {
      "summary_selection": 1,
      "models_reproducibility": 2,
      "routes_conditions_yields": 5,
      "harness_comparison": 2,
      "quantum_analysis": 2,
      "physical_properties": 2,
      "3d_accessibility": 2,
      "conclusions_limits": 1,
      "references": 2
    },
    "layout_reserve_pages": 1,
    "max_report_routes": 3,
    "selection_rule": "Initial score-order presentation shortlist; not a claim of chemical feasibility. Review chemistry before final authoring.",
    "final_author": "Solar Pro 4",
    "model": "solar-pro4-260806",
    "temperature": 0.0,
    "max_tokens": 10000,
    "paid_calls_authorized": false,
    "report_generation_authorized": false
  },
  "condition_results_file": ".\\results\\benzocaine-live-20261031-04\\conditions-parrot.json",
  "normalization": {
    "checkpoint_sha256": "2931dab333037a120ec4ec4de9ea91a4cd27da5caf0173b16e8b224e1c982fbb",
    "training_data_reference": "https://ibm.ent.box.com/v/uspto-yields-data",
    "training_domain": "USPTO gram-scale random split; target-specific applicability not assessed",
    "output_scale": "standardized_fraction",
    "normalization_reference": "https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/training_scripts/launch_uspto_training.py",
    "normalization_note": "Recovered from original gram random_split=train rows using the authors' preprocessing and pandas sample standard deviation. Not global-dataset substitute statistics.",
    "source_commit": "d9e6b87ce1b881978490d68bfc00021e3b48127a",
    "training_yield_mean": 0.7318926847478698,
    "training_yield_std": 0.20946128682168402,
    "training_yield_units": "fraction",
    "std_ddof": 1,
    "normalization_formula": "yield_percent = 100 * (raw_z * training_yield_std + training_yield_mean)",
    "normalization_provenance": {
      "recovered_at": "2026-10-30T13:28:49.726548+00:00",
      "source_url": "https://ibm.ent.box.com/index.php?rm=box_download_shared_file&shared_name=p08w6nysh4ua0nqie04qnspe0unri0ll&file_id=f_682273338317",
      "source_file": "models/rxn_yields/data/yields_above_200622.tsv",
      "source_sha256": "0e5952a277d4fa1ba0a24b753c3cd3c7da4b2de7af24a0164226db0aeb1274f4",
      "source_size_bytes": 95196581,
      "source_total_rows": 197619,
      "train_rows": 158095,
      "test_rows": 39524,
      "preprocessing_reference": "https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/nbs/02_uspto_data_exploration.ipynb",
      "training_reference": "https://github.com/rxn4chemistry/rxn_yields/blob/d9e6b87ce1b881978490d68bfc00021e3b48127a/training_scripts/launch_uspto_training.py",
      "selection": "random_split == 'train'; calc_yield_above / 100",
      "published_checkpoint": "uspto_gram_random_test_epochs_2_pretrained/checkpoint-19762-epoch-2",
      "pandas_version": "3.0.1"
    }
  },
  "source_hashes": {
    "input.json": "71ee5a5a194c89ed402b66f54f0812a0f71838bdc6366d7ebeb3028a74f3998b",
    "routes.json": "a5256cab92771f695bff3b594e7a29ff0193f343923a51090e9df6da7dab6e63",
    "conditions-parrot.json": "c1ec5ed4493b25c25a8d38c0c10372cf2592078e0b2d322fd1fe32f170bc0747",
    "yields-rxn_yields.json": "18fd9a6f0cd303e15b690b8936d3519eebefddb9899ea2cc1cfb2e5d3935a63a",
    "figures/manifest.json": "222a4856af4d267cc8a22bc02f9109d6842080c50d9258b48692053b802e31c4"
  }
}
--- END SOURCE: results/benzocaine-live-20261031-04/report-evidence.json ---


--- BEGIN SOURCE: results/benzocaine-live-20261031-04/validation_notes.json ---
{
  "artifact_type": "deterministic_checks_not_a_Solar_report",
  "target_id": "benzocaine",
  "notes": [
    {
      "kind": "cross_model_limit",
      "note": "Parrot conditions are not inputs to the yield model. Predicted yields are not experimentally validated."
    },
    {
      "kind": "model_applicability",
      "note": "Target-specific accuracy and domain membership are not assessed; normalization correctness is not accuracy validation."
    },
    {
      "kind": "missing_conditions",
      "note": "Temperature, time and equivalents are not supplied by the selected condition checkpoint."
    },
    {
      "kind": "route_limit",
      "note": "Stock membership and template scores do not prove practical feasibility. Search excludes target from stock; agents/byproducts can be omitted."
    }
  ],
  "applicability": "not_assessed",
  "source_hashes": {
    "input.json": "71ee5a5a194c89ed402b66f54f0812a0f71838bdc6366d7ebeb3028a74f3998b",
    "routes.json": "a5256cab92771f695bff3b594e7a29ff0193f343923a51090e9df6da7dab6e63",
    "conditions-parrot.json": "c1ec5ed4493b25c25a8d38c0c10372cf2592078e0b2d322fd1fe32f170bc0747",
    "yields-rxn_yields.json": "18fd9a6f0cd303e15b690b8936d3519eebefddb9899ea2cc1cfb2e5d3935a63a",
    "figures/manifest.json": "222a4856af4d267cc8a22bc02f9109d6842080c50d9258b48692053b802e31c4"
  }
}
--- END SOURCE: results/benzocaine-live-20261031-04/validation_notes.json ---


--- BEGIN SOURCE: analyses/mopac/results-interpretation.md ---
# MOPAC PM7 result interpretation

## What was calculated

MOPAC 23.2.5 performed PM7 isolated-molecule geometry optimizations for five neutral species. For each molecule, five RDKit ETKDGv3 conformers were first minimized with MMFF94s; all five were independently optimized with MOPAC. Inputs explicitly set `CHARGE=0 MS=0`, so the specified state is neutral singlet. MOPAC output confirms closed-shell RHF, SCF completion, normal job termination, and a final gradient norm below the requested `GNORM=0.5 kcal mol⁻¹ Å⁻¹` for all **25/25** jobs.

The primary input conformer was the one with the lowest MMFF94s starting energy among the five. Because every start was calculated, the geometry saved as `*-pm7-optimized.sdf` is instead the converged geometry with the lowest PM7 heat of formation among those five starts **for that same molecular formula and charge**. It is a best-of-five search, not a proven global minimum or a frequency-verified minimum.

All jobs were gas-phase, with no solvent, catalyst, hydrogen, counterion, reaction partner, or transition state. The calculated heats below are listed per molecule as output records. They are not compared across different formulas and are not a reactivity or stability ranking.

| Species | Formula | Converged starts | Best-of-five PM7 heat of formation (kcal/mol) | Final gradient norm (kcal mol⁻¹ Å⁻¹) | Dipole (D) | Heat spread within this species' five starts (kcal/mol) |
|---|---:|---:|---:|---:|---:|---:|
| Ethyl 4-nitrobenzoate | C9H9NO4 | 5/5 | -72.22692 | 0.42843 | 4.508 | 0.51989 |
| Benzocaine | C9H11NO2 | 5/5 | -73.05519 | 0.39984 | 4.100 | 0.49850 |
| 4-Aminobenzoic acid | C7H7NO2 | 5/5 | -70.47009 | 0.48101 | 4.785 | 0.00225 |
| Ethanol | C2H6O | 5/5 | -57.85665 | 0.38440 | 2.064 | 1.98718 |
| Acetic acid | C2H4O2 | 5/5 | -102.19677 | 0.31766 | 1.990 | 0.00047 |

The within-species spread highlights starting-geometry sensitivity in this small ensemble: ethanol's five optimized starts span about 1.99 kcal/mol, while the 4-aminobenzoic-acid and acetic-acid starts converge to nearly identical heats. This is not a thermodynamic population calculation. A narrow five-start spread does not prove global convergence.

## Structural and charge observations

Selected optimized bond distances are calculated from the final MOPAC ARC Cartesian coordinates using the input molecular graph. Distances are in Å. The charge values are MOPAC's population-derived net atomic charges in units of electron charge; they are model partitions, not directly observable atomic properties.

- **Ethyl 4-nitrobenzoate:** ester C=O 1.2050; ester C–O 1.3528; aryl C–nitro N 1.4603; the two N–O distances are 1.2198 and 1.2198. The selected conformer's N charge is +0.6117 and the two O charges are -0.3904 and -0.3888. The nearly equal N–O distances are consistent with the delocalized nitro representation in this optimized PM7 structure; they do not describe the reduction process.
- **Benzocaine:** aryl C–NH2 N 1.3772; ester C=O 1.2080; ester C–O 1.3613. The amino N charge is -0.6321; carbonyl and alkoxy O charges are -0.4421 and -0.5283.
- **4-Aminobenzoic acid:** aryl C–NH2 N 1.3760; carboxyl C=O 1.2071; carboxyl C–O 1.3654. The amino N charge is -0.6274; carboxyl O charges are -0.5262 and -0.5700.
- **Ethanol:** C–O 1.4142; O charge -0.5507.
- **Acetic acid:** C=O 1.2021; C–O 1.3612; O charges -0.5065 and -0.5675.

These geometries and charge distributions characterize the computed isolated molecules. They do not establish reactant accessibility, a reaction pathway, an activation barrier, experimental conditions, yield, or synthetic success. In particular, this work does not model Pd catalysis or the missing reducing conditions in route-01's highest-ranked Parrot condition slots.

## Output files

- `run-manifest.json`: all 25 job statuses, hashes, return codes, and output paths.
- `*/conformer-*/<species>-conf-*.out`: full raw MOPAC outputs; matching `.arc` files hold the optimized geometries and charge columns.
- `analysis-summary.json`: extracted energy, gradient, dipole, convergence and conformer-sensitivity results.
- `net-atomic-charges.csv` and `optimized-bond-lengths.csv`: per-atom population charges and bond lengths from the selected best-of-five geometry for each species, plus charge rows for all starts.
- `optimized-structures/*-pm7-optimized.sdf`: selected optimized structures for visualization.
- `validation/mopac-input-review.json`: formula/charge/spin preflight and output consistency checks.

MOPAC documentation: [PM7](https://openmopac.net/Manual/pm7.html), [geometry optimization precision and GNORM](https://openmopac.net/Manual/precision.html), [MS=0 singlet](https://openmopac.net/Manual/ms.html), and [basic usage and output files](https://openmopac.net/guides/basics/).
--- END SOURCE: analyses/mopac/results-interpretation.md ---


--- BEGIN SOURCE: analyses/epi-suite/analysis.md ---
# EPI Suite MPBPWIN results and interpretation

## Tool and execution status

EPA's current EPI Suite page says the downloadable v4.11 has technical execution difficulties and directs users to the EPI Suite Web beta. The EPI Web endpoint returned HTTP 200 for both the SMILES-only estimate batch and the five CAS-confirmed data queries. The API health document nevertheless reported `degraded` and `requestHandling.healthy=false`; results are saved with this service limitation. No local EPI Suite installation was made.

EPA identifies MPBPWIN as estimating melting point, boiling point, and vapor pressure for organic chemicals using a combination of techniques. EPA describes EPI Suite as screening-level; these estimates should not replace suitable measured values.

## Model estimates and EPI database evidence

The `estimatedValue` is the MPBPWIN v1.44 model estimate. It is shown separately from `experimentalValues` / EpiUnified evidence. EPI's `selectedValue` can select a database evidence row instead of the model estimate; it must not be called a prediction without checking its source metadata. All temperatures below are in deg C.

| Substance (formula) | MPBPWIN MP estimate | EPI Unified MP record | MP record classification | MPBPWIN BP estimate | EPI Unified BP record | BP record classification |
|---|---:|---:|---|---:|---:|---|
| Ethyl 4-nitrobenzoate (C9H9NO4) | 80.66 | — | No EPI Unified record returned | 297.25 | — | No EPI Unified record returned |
| Benzocaine (C9H11NO2) | 66.17 | — | No EPI Unified record returned | 279.90 | — | No EPI Unified record returned |
| 4-Aminobenzoic acid (C7H7NO2) | 94.08 | 188.5 | derived_or_analogue_database_entry_not_direct_measurement | 307.70 | — | No EPI Unified record returned |
| Ethanol (C2H6O) | -87.84 | -114.1 | derived_or_analogue_database_entry_not_direct_measurement | 65.11 | 78.2 | epi_database_evidence_provenance_insufficient_to_claim_direct_experiment |
| Acetic acid (C2H4O2) | -21.26 | 16.635 | literature_cited_epi_evidence_not_independently_verified_as_measurement | 122.30 | 117.9 | epi_database_evidence_provenance_insufficient_to_claim_direct_experiment |
| Tetrahydrofuran (C4H8O) | -84.89 | -108.44 | derived_or_analogue_database_entry_not_direct_measurement | 69.36 | 65.0 | epi_database_evidence_provenance_insufficient_to_claim_direct_experiment |
| Diethyl ether (C4H10O) | -101.15 | -116.3 | derived_or_analogue_database_entry_not_direct_measurement | 47.02 | 34.6 | epi_database_evidence_provenance_insufficient_to_claim_direct_experiment |

All seven model estimates are EPI responses marked `ESTIMATED`; they are not measured properties. The EPI search database had exact-structure records for five substances (4-aminobenzoic acid, ethanol, acetic acid, tetrahydrofuran, and diethyl ether). Benzocaine and ethyl 4-nitrobenzoate had no EPI search match, so their reported values are model-only.

The EPI Unified field is not uniformly a laboratory measurement: four melting-point records explicitly say `slope analogy` or `calculated based upon VP / Water Sol data`; these are derived/analogue entries, not direct observations. The acetic-acid MP record carries a 1992 author string but not the underlying paper or method in the API; its author metadata needs caution. The other boiling-point records are tagged as EpiUnified evidence but return no author/year/pressure, so their measurement provenance cannot be independently checked from this response. The API's `experimentalValues` field name alone is not enough to call every entry an experiment.

For a separate cross-check, the Australian Government National Pollutant Inventory lists acetic acid MP 16.7 deg C and BP 118 deg C, close to the EpiUnified database entries 16.635 deg C and 117.9 deg C. This source does not validate the MPBPWIN predictions; the MPBPWIN estimates for acetic acid were -21.26 deg C and 122.30 deg C.

## Structure and support review

The seven submitted structures are neutral organic compounds with net formal charge zero and are represented as the same structures used in the preparation CSV. Three inputs were not submitted: `[Pd]` is an elemental atom token rather than a defined catalyst material; `[Al+3].[H-]...[Li+]` is a disconnected ionic LiAlH4 representation rather than a defined pure neutral organic compound; and `FB(F)F` is inorganic BF3 rather than an organic chemical within MPBPWIN's stated scope. No values were fabricated for these entries.

## Reaction-condition limits

The selected Parrot condition predictions do not specify reaction temperature, pressure, or full mixture composition/amounts. The Web API returned pure-compound BP/MP estimates and database records, not mixture phase equilibria. Do not infer whether route materials precipitate, melt, boil, or react from these values alone. To assess operational phase, obtain the actual temperature and pressure, solvent/reagent equivalents and concentrations, water content, chemical forms/salts, atmosphere, and mixture vapor-liquid/solid-liquid behavior or solubility data. A pure-compound MP or BP is not evidence of reaction feasibility or yield.

## Reproducibility and files

- Input structures: `analyses/preparation/epi-suite-inputs.csv`.
- Reproduction script: `analyses/epi-suite/run_epi_web_suite.py` (SMILES-only estimates and CAS/reference resolution) and `analyses/epi-suite/run_epi_cas_confirmed.py` (CAS-identified EpiUnified lookup).
- API specification and degraded health snapshot: `raw/api-openapi.json`, `run-metadata.json`.
- Exact request and raw result payloads: `request.json`, `response.raw.json`, `raw/items/`, and `cas-confirmed-run-02/`.
- Structure/CAS audit: `input-review-final.json`; provenance-aware classification: `classified-results.json`.
- Query time and request/response hashes are in each run metadata file.

Sources: [EPA EPI Suite page and current beta notice](https://www.epa.gov/tsca-screening-tools/epi-suitetm-estimation-program-interface); [EPA EPI Suite v4.11 download notice](https://www.epa.gov/tsca-screening-tools/download-epi-suitetm-estimation-program-interface-v411); [EPI Suite Web beta](https://episuite.dev/EpiWebSuite/#/); [Australian Government acetic acid properties](https://www.dcceew.gov.au/environment/protection/npi/substances/acetic-acid-ethanoic-acid).
--- END SOURCE: analyses/epi-suite/analysis.md ---


--- BEGIN SOURCE: analyses/visualizer/visualizer-measurement-interpretation.md ---
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
--- END SOURCE: analyses/visualizer/visualizer-measurement-interpretation.md ---


--- BEGIN SOURCE: analyses/visualizer/visualizer-measurements.csv ---
measurement_id,structure_file,conformer_index,atoms_visualizer_names,atom_ids,measurement,value,unit,visualizer_version,method,screen_evidence,interpretation_limit
D-01,inputs/ethyl-4-nitrobenzoate-mopac-pm7-conformers.sdf,1,N10-H21,"10;21",distance,2.684,angstrom,Discovery Studio Visualizer 2025 25.1.0,Visualizer Measure tool DistanceMonitor table,screenshots/route01-distance-measured.png;screenshots/route01-distance-monitor-table.png;screenshots/route01-single-conformer-final-visibility.png,isolated MOPAC PM7 conformer; geometric proximity only; not a reaction complex or barrier
A-01,inputs/ethyl-4-nitrobenzoate-mopac-pm7-conformers.sdf,1,C8-C9-N10,"8;9;10",angle,119.102,degrees,Discovery Studio Visualizer 2025 25.1.0,Visualizer Measure tool AngleMonitor table,screenshots/route01-angle-three-atoms-selected.png;screenshots/route01-angle-measured.png;screenshots/route01-angle-monitor-table.png,isolated MOPAC PM7 conformer local nitro substituent geometry; not a transition-state angle
D-02,inputs/ethyl-4-nitrobenzoate-mopac-pm7-conformers.sdf,2,N10-H21,"10;21",distance,2.682,angstrom,Discovery Studio Visualizer 2025 25.1.0,Visualizer Measure tool DistanceMonitor table,screenshots/route01-conformer2-only.png;screenshots/route01-conf2-distance-atoms-selected.png;screenshots/route01-conf2-distance-monitor.png,isolated MOPAC PM7 conformer; geometric proximity only; not a reaction complex or barrier
A-02,inputs/ethyl-4-nitrobenzoate-mopac-pm7-conformers.sdf,2,C8-C9-N10,"8;9;10",angle,119.062,degrees,Discovery Studio Visualizer 2025 25.1.0,Visualizer Measure tool AngleMonitor table,screenshots/route01-conformer2-only.png;screenshots/route01-conf2-angle-atoms-selected.png;screenshots/route01-conf2-angle-monitor.png,isolated MOPAC PM7 conformer local nitro substituent geometry; not a transition-state angle
--- END SOURCE: analyses/visualizer/visualizer-measurements.csv ---


--- BEGIN SOURCE: analyses/visualizer/route-selection.json ---
{
  "status": "selected_for_manual_visualizer_review_not_yet_observed",
  "source_run": "benzocaine-live-20261031-04",
  "source_routes": "results/benzocaine-live-20261031-04/routes.json",
  "representative": {
    "route_id": "route-01",
    "reaction_smiles": "CCOC(=O)c1ccc([N+](=O)[O-])cc1>>CCOC(=O)c1ccc(N)cc1",
    "reason": "One-step predicted reduction of the para nitro group to the benzocaine amino group; both the predicted precursor and product have PM7 optimized structures and atom numbering. It is the highest state-score route among the returned routes (0.99763). This is a route-selection rationale, not evidence that the step is feasible or successful.",
    "reactive_region": "nitro nitrogen on ethyl 4-nitrobenzoate",
    "substrate_atom_map_numbers": {"nitro_N": 10, "aryl_ipso_C": 9, "aryl_ortho_C": [8, 13], "ortho_H_sdf_serials": [21, 22]},
    "structures": [
      "analyses/visualizer/inputs/ethyl-4-nitrobenzoate-mopac-pm7-conformers.sdf",
      "analyses/visualizer/inputs/benzocaine-mopac-pm7-conformers.sdf"
    ]
  },
  "comparison": {
    "route_id": "route-05",
    "reaction_steps": [
      "CC(=O)O>>CCO",
      "CCO.Nc1ccc(C(=O)O)cc1>>CCOC(=O)c1ccc(N)cc1"
    ],
    "reason": "A two-step esterification-style route using 4-aminobenzoic acid and ethanol. Both second-step input structures and the product have PM7 optimized geometries; unlike route-01 it brings two independent molecules together at a proposed acyl-substitution site. Its route state score is 0.99404. The predicted reaction is not validated.",
    "reactive_region": "4-aminobenzoic acid carboxyl carbon and ethanol oxygen",
    "p_aminobenzoic_acid_atom_map_numbers": {"carboxyl_C": 6, "carbonyl_O": 7, "hydroxyl_O": 8, "aryl_ipso_C": 5, "aryl_ortho_C": [4, 9], "ortho_H_sdf_serials": [14, 16], "hydroxyl_H_sdf_serial": 15},
    "ethanol_atom_map_numbers": {"ethyl_C": 2, "O": 3, "hydroxyl_H_sdf_serial": 9},
    "structures": [
      "analyses/visualizer/inputs/p-aminobenzoic-acid-mopac-pm7-conformers.sdf",
      "analyses/visualizer/inputs/ethanol-mopac-pm7-conformers.sdf",
      "analyses/visualizer/inputs/benzocaine-mopac-pm7-conformers.sdf"
    ],
    "caveat": "Any hand-positioned PABA/ethanol pair is illustrative only, not a calculated or optimized reaction complex. No transition state or solvent is present."
  }
}
--- END SOURCE: analyses/visualizer/route-selection.json ---


--- BEGIN SOURCE: analyses/visualizer/visualizer-session-status.json ---
{
    "application":  "BIOVIA Discovery Studio Visualizer 2025 Client",
    "version":  "25.1.0",
    "file_version":  "25,1,0,24284",
    "install_path":  "C:\\Program Files\\BIOVIA\\Discovery Studio 2025\\",
    "process_id":  12132,
    "responding":  true,
    "graphics_recovery":  [
                              "View \u003e Graphics (Ctrl+G) restored the 3D pane from Data Table view",
                              "Molecule Data Table Visible column confirmed conformer 1 alone",
                              "Enabling conformers 1 and 2 simultaneously displayed both as overlapping geometries; then one was hidden",
                              "Reopening the original saved SDF and reverting in-memory edits reset the document to conformer 1 and restored a complete 3D rendering"
                          ],
    "measured_actual_visualizer":  [
                                       {
                                           "id":  "D-01",
                                           "value":  2.684,
                                           "screenshot":  "screenshots/route01-distance-monitor-table.png",
                                           "atoms":  "N10-H21",
                                           "conformer":  1,
                                           "unit":  "angstrom"
                                       },
                                       {
                                           "id":  "A-01",
                                           "value":  119.102,
                                           "screenshot":  "screenshots/route01-angle-monitor-table.png",
                                           "atoms":  "C8-C9-N10",
                                           "conformer":  1,
                                           "unit":  "degrees"
                                       },
                                       {
                                           "id":  "D-02",
                                           "value":  2.682,
                                           "screenshot":  "screenshots/route01-conf2-distance-monitor.png",
                                           "atoms":  "N10-H21",
                                           "conformer":  2,
                                           "unit":  "angstrom"
                                       },
                                       {
                                           "id":  "A-02",
                                           "value":  119.062,
                                           "screenshot":  "screenshots/route01-conf2-angle-monitor.png",
                                           "atoms":  "C8-C9-N10",
                                           "conformer":  2,
                                           "unit":  "degrees"
                                       }
                                   ],
    "conformer3plus":  "not recorded; unstable/ambiguous rendering after conformer switching, and post-reopen defaulted to conformer 1",
    "multiple_conformers_displayed":  true,
    "source_files_hashes":  [
                                {
                                    "file":  "ethyl-4-nitrobenzoate-mopac-pm7-conformers.sdf",
                                    "sha256":  "7FD21A27E7AB18D77EFB2A417EE7BA8D6797D73BDF136F5035681B7409DA2E4C",
                                    "matches_pre_session":  true
                                },
                                {
                                    "file":  "p-aminobenzoic-acid-mopac-pm7-conformers.sdf",
                                    "sha256":  "E9707FCBB6B32BC598980CEB70E515686021EF063D62E5B758D5FA2A0A9C62B2",
                                    "matches_pre_session":  true
                                }
                            ],
    "source_sdf_saved_or_overwritten":  false,
    "other_code_measurements_used":  false,
    "interpretation_limit":  "isolated PM7 geometry only; no inference of reaction rate, barrier, success, or yield",
    "remaining":  "route01 other planned distances/angles and route05/ethanol measurements across conformers remain incomplete",
    "final_view":  {
                       "screenshot":  "screenshots/final-clean-single-conformer-view.png",
                       "visible_conformer":  1,
                       "source_document_reverted_to_saved_state":  true
                   }
}
--- END SOURCE: analyses/visualizer/visualizer-session-status.json ---


--- BEGIN SOURCE: results/benzocaine-live-20261031-04/additional-analysis-status.json ---
{
  "harness_comparison": {
    "status": "not_implemented",
    "inference_executed": false,
    "reason": "Preparation only; tool installation or paid execution is not authorized in this phase"
  },
  "mopac": {
    "status": "not_implemented",
    "inference_executed": false,
    "reason": "Preparation only; tool installation or paid execution is not authorized in this phase"
  },
  "epi_suite": {
    "status": "not_implemented",
    "inference_executed": false,
    "reason": "Preparation only; tool installation or paid execution is not authorized in this phase"
  },
  "discovery_studio": {
    "status": "not_implemented",
    "inference_executed": false,
    "reason": "Preparation only; tool installation or paid execution is not authorized in this phase"
  }
}
--- END SOURCE: results/benzocaine-live-20261031-04/additional-analysis-status.json ---
