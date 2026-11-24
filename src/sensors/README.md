# src/sensors — 가스 센서

**역할:** 가스 센서 값을 읽고 예열 여부·기준 대비 비율을 계산해 `GasReading`으로 내보냅니다.
**주 담당:** HW

## 여기에 넣는 것
- 센서 읽기, 예열 판단, 기준 전압 측정 코드
- 관련 REQ: REQ-004, REQ-017

## 넣지 않는 것
- MCU에서 도는 코드 → `mcu/`
- 배선도·회로도 → `docs/hardware/`

> 이 폴더 규칙은 [CONTRIBUTING.md](../../CONTRIBUTING.md)와 [AGENTS.md](../../AGENTS.md)를 따릅니다.
