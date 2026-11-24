# src/alerts — 경보 출력 (부저 · LED)

**역할:** `SystemState`를 받아 단계별 부저 주기·LED 색·대피로 LED를 출력합니다.
**주 담당:** HW

## 여기에 넣는 것
- 패시브 부저 PWM, LED 제어, 대피로 LED 표시 코드
- 관련 REQ: REQ-009, REQ-020

## 넣지 않는 것
- 경보 단계를 정하는 로직 → `src/decision/`

> 이 폴더 규칙은 [CONTRIBUTING.md](../../CONTRIBUTING.md)와 [AGENTS.md](../../AGENTS.md)를 따릅니다.
