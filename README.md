# 🔥 열화상 비전과 실시간 동적 ROI 기반의 지능형 안전 방재 시스템

배터리 공장 한 구역을 **일반 카메라 + 열화상 카메라**로 감시해서, 배터리 셀의 이상 발열과 가스를 조기에 감지하고 경보를 울려 **위험 구역을 피하는 대피로**를 안내하는 온디바이스(라즈베리파이 4) 안전 시스템입니다.

## 핵심 기술
1. **동적 위험 ROI** — 열화상으로 찾은 고온 영역마다 위험 구역을 실시간으로 만들고, 온도가 높을수록 넓힙니다.
2. **사람 위치 비교** — 일반 카메라로 찾은 사람이 위험 구역 안에 있는지 판단합니다.
3. **단계별 경보와 대피 안내** — 위급할수록 빠른 부저 주기, LED로 안전한 출구까지 안내합니다.

## 👋 처음 오셨나요?
**[CONTRIBUTING.md](CONTRIBUTING.md)부터 읽어 주세요.** 팀 규칙, 폴더 구조, 브랜치·이슈·커밋 방법, AI 도구 사용 규칙이 있어요.

## 📚 정식 문서 (`docs/`)
| 문서 | 내용 | 상태 |
|---|---|---|
| [00-project-guide](docs/00-project-guide.md) | **OT 가이드 요약 — 목표·일정·제출물·평가 기준 (최우선 기준)** | v0.1 |
| [01-requirements](docs/01-requirements.md) | 요구사항 (REQ 번호) — **작업 전 확인** | v0.2 |
| [02-state-machine](docs/02-state-machine.md) | 경보 단계·전환 규칙 (그림) | v0.2 |
| [03-interface](docs/03-interface.md) | 모듈 간 데이터·CSV 로그 형식 | v0.3 |
| [04-test-cases](docs/04-test-cases.md) | 테스트 | 테스트 시작 후 작성 |
| [05-fmea](docs/05-fmea.md) | 위험성 검토 | 테스트 시작 후 작성 |
| [06-system-design](docs/06-system-design.md) | 시스템 구조·파이프라인·선정 근거 | 초안 |
| [07-performance](docs/07-performance.md) | 정확도·지연시간 측정 결과 | 측정 전 |
| [08-progress-log](docs/08-progress-log.md) | 수행 경과·문제 해결·피드백 | 진행 중 |
| [09-submission](docs/09-submission.md) | 제출물 5종·FINAL CHECKLIST | 진행 중 |
| [hardware/](docs/hardware/) | BOM·회로도·구성도·사진 | 초안 |

## 🚀 코드 확인해 보기
```bash
python src/main.py          # 전체 파이프라인 뼈대 실행
python src/csv_logger.py    # 예시 CSV 로그 생성 (data/logs/ 아래)
python -m pytest tests/     # 자동 테스트 (pip install pytest 필요)
```

## 👥 팀
HD 온디바이스 AI 1차 프로젝트 2조 · 팀장 1 · 통합·문서 1 · SW/AI 2 · HW 2 · 기간 2026-11-25 ~ 12-10
