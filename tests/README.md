# tests — 자동 테스트

**역할:** 사람이 디오라마로 하는 테스트([04-test-cases](../docs/04-test-cases.md))와 별개로, 코드만으로 확인할 수 있는 부분을 자동으로 검사합니다.
**주 담당:** 통합·문서

## 여기에 넣는 것
- `pytest`로 실행하는 테스트 파일 (`test_*.py`)
- 상태 머신 전환, CSV 저장·복원처럼 하드웨어 없이 확인 가능한 것

## 넣지 않는 것
- 하드웨어가 필요한 테스트 결과 → `docs/04-test-cases.md`

## 실행
```bash
pip install pytest
python -m pytest tests/
```

> 이 폴더 규칙은 [CONTRIBUTING.md](../CONTRIBUTING.md)와 [AGENTS.md](../AGENTS.md)를 따릅니다.
