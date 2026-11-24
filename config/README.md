# config — 기준값 · 보정값

**역할:** 코드 안에 숫자를 박지 않고, 바뀔 수 있는 값을 여기 모읍니다. 값을 바꾸면 **왜 바꿨는지** 커밋 메시지나 ADR에 남깁니다.
**주 담당:** SW/AI + HW

## 여기에 넣는 것
- `thresholds.csv` — 경보 기준값 (온도·시간·비율). 엑셀로 열어 수정 가능
- `calibration_rgb.csv`, `calibration_thermal.csv` — 픽셀→바닥 cm 변환 행렬 (보정 후 생성)

## 넣지 않는 것
- 비밀번호·토큰 같은 비밀 정보

> 이 폴더 규칙은 [CONTRIBUTING.md](../CONTRIBUTING.md)와 [AGENTS.md](../AGENTS.md)를 따릅니다.
