## 관련 이슈·REQ
- Closes #(이슈 번호)
- REQ:

## 무엇을 바꿨나요
-

## 어떻게 확인했나요
- 실행한 명령·테스트:
- 관련 TC:

## 체크리스트
- [ ] PR 대상(base)이 `dev`인지 확인했다 (`main` 아님)
- [ ] `python -m pyflakes src/` 통과
- [ ] `data/logs/`, 모델 가중치 파일 등 올리면 안 되는 파일이 없다
- [ ] 인터페이스를 바꿨다면 `messages.py`, `csv_logger.py`, `docs/03-interface.md`를 함께 바꿨다 (해당 없으면 체크)
- [ ] 안전 로직(대피 래칭, FAULT 표시 등)을 끄거나 우회하지 않았다
- [ ] AI로 만든 코드가 있다면 내용을 이해하고 설명할 수 있다
