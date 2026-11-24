# src/vision_thermal — 열화상 동적 위험 ROI

**역할:** 열화상 프레임에서 고온 영역을 찾아 위험 구역(ROI)을 만들고 `ThermalResult`로 내보냅니다. **프로젝트 핵심 기술**입니다.
**주 담당:** SW/AI

## 여기에 넣는 것
- 열화상 입력, 고온 영역 찾기, 위험 반경 계산, 상승률 계산 코드
- 관련 REQ: REQ-001~003, REQ-014

## 넣지 않는 것
- 기준 온도 같은 숫자 → `config/thresholds.csv`
- 경보 단계 판단 → `src/decision/`

> 이 폴더 규칙은 [CONTRIBUTING.md](../../CONTRIBUTING.md)와 [AGENTS.md](../../AGENTS.md)를 따릅니다.
