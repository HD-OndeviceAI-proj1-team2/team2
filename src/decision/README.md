# src/decision — 경보 판단 (상태 머신) · 대피로

**역할:** 세 입력(사람·열·가스)을 모아 경보 단계를 정하고 대피 경로를 계산해 `SystemState`로 내보냅니다.
**주 담당:** SW/AI

## 여기에 넣는 것
- 상태 머신 ([02-state-machine](../../docs/02-state-machine.md) 그대로 구현)
- 대피로 계산 (통로 그래프)
- 관련 REQ: REQ-003, REQ-008, REQ-009, REQ-013, REQ-018

## 넣지 않는 것
- 센서·카메라를 직접 읽는 코드 (입력은 `messages.py` 객체로만 받음)

> 이 폴더 규칙은 [CONTRIBUTING.md](../../CONTRIBUTING.md)와 [AGENTS.md](../../AGENTS.md)를 따릅니다.
