# 🔥 열화상 비전과 실시간 동적 ROI 기반의 지능형 안전 방재 시스템

배터리 공장 셀 보관·대기 구역을 **일반 카메라 + 열화상 카메라 + 가스 센서**로 감시해서, 셀의 이상 발열과 가연성·유해 가스를 눈에 보이기 전에 감지하고 **정상·주의·경보·대피 4단계**로 알려 **위험 구역을 피하는 출구**로 대피를 안내하는 온디바이스(라즈베리파이 4) 안전 시스템입니다.

## 핵심 기술
1. **동적 위험 ROI** — 열화상으로 찾은 고온 영역마다 위험 구역을 실시간으로 만들고, 위험이 사라지면 해제합니다.
2. **작업자 접근 안내** — 일반 카메라(YOLO)로 찾은 작업자가 위험 구역에 가까워지면 스피커로 안내 방송을 합니다 (주의 단계는 1.2배, 경보 단계는 1.5배 범위).
3. **단계별 경보와 대피 안내** — 단계마다 LED 색·부저 주기가 다르고, 경보·대피 단계에서는 위험 구역을 피하는 출구 LED가 켜집니다. 경보 중 불·연기가 보이면 대피 단계가 되어 대피 안내 방송을 합니다.

## 👋 처음 오셨나요?
**[CONTRIBUTING.md](CONTRIBUTING.md)부터 읽어 주세요.** 팀 규칙, 폴더 구조, 브랜치·이슈·커밋 방법, AI 도구 사용 규칙이 있어요.

## 📚 정식 문서 (`docs/`)
| 문서 | 내용 | 상태 |
|---|---|---|
| [00-project-guide](docs/00-project-guide.md) | **OT 가이드 요약 — 목표·일정·제출물·평가 기준 (최우선 기준)** | v0.2 |
| [01-requirements](docs/01-requirements.md) | 요구사항 (REQ 번호) — **작업 전 확인** | v0.4 |
| [02-state-machine](docs/02-state-machine.md) | 경보 4단계·전환 규칙·기준값 (그림) | v0.4 |
| [03-interface](docs/03-interface.md) | 클래스 간 데이터·DB 기록 형식·핀 할당 | v0.5 |
| [04-test-cases](docs/04-test-cases.md) | 테스트 (시나리오 v0.5) | 테스트 시작 후 결과 기록 |
| [05-fmea](docs/05-fmea.md) | 위험성 검토 (v0.4) | 테스트 시작 후 보완 |
| [06-system-design](docs/06-system-design.md) | 시스템 구조·파이프라인·선정 근거 | 초안 |
| [07-performance](docs/07-performance.md) | 정확도·지연시간 측정 결과 | 측정 전 |
| [08-progress-log](docs/08-progress-log.md) | 수행 경과·문제 해결·피드백 | 진행 중 |
| [09-submission](docs/09-submission.md) | 제출물 5종·FINAL CHECKLIST | 진행 중 |
| [hardware/](docs/hardware/) | BOM·회로도·구성도·사진 | 초안 |

## 🚀 코드 확인해 보기
```bash
pip install -r requirements.txt   # 처음 한 번 (picamera2는 Raspberry Pi OS에 apt로 설치)
python main.py                    # 전체 실행 (저장소 루트에서)
python -m pytest tests/           # 자동 테스트
python -m pyflakes .              # 커밋 전 검사 (안 쓰는 import·오타)
```
> 지금은 코드 뼈대 단계라 `python main.py`가 바로 동작하지 않습니다. 남은 작업은 [03-interface 8번](docs/03-interface.md)에 있어요.

## 👥 팀
HD 온디바이스 AI 1차 프로젝트 2조 · 팀장 1 · 통합·문서 1 · SW/AI 2 · HW 2 · 기간 2026-11-25 ~ 12-10
