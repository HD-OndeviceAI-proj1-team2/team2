# AGENTS.md — AI 도구 공통 작업 규칙

> 이 파일은 Codex, Claude Code, Gemini CLI 등 **모든 AI 코딩 도구가 공통으로 읽는 규칙**입니다.
> `CLAUDE.md`와 `GEMINI.md`는 이 파일을 불러오기만 합니다. **규칙은 이 파일에서만 고칩니다.**
> 사람용 팀 규칙은 [CONTRIBUTING.md](CONTRIBUTING.md)에 있습니다.

## 1. 프로젝트 요약

- **이름:** 열화상 비전과 실시간 동적 ROI 기반의 지능형 안전 방재 시스템
- **현장:** 배터리 공장 셀 보관·대기 구역 한 곳을 일반 카메라 + 열화상 카메라로 한 방향에서 감시
- **핵심:** 열화상 고온 영역으로 **위험 구역(ROI)을 실시간 생성**하고, 가스 센서와 함께 **정상·주의·경보·대피 4단계**로 판단해 부저·LED·스피커로 알리고 출구 LED로 대피를 안내. 일반 카메라(YOLO)로 작업자 위치와 불·연기를 찾아, 작업자가 ROI에 가까우면 안내 방송을 하고 경보 중 불·연기가 보이면 대피 단계로 올림
- **장치:** 라즈베리파이 4 한 대, 인터넷 없이 동작 (온디바이스)
- **시연:** 축소 모형 (캡톤 히터 = 배터리 셀, 사람 피규어 = 작업자). 온도 기준은 실제 셀 기준이며 시연은 히터 안전 범위 안에서 축소 재현
- **팀:** 2조 '열일', 6명 (조장, 통합·문서, SW/AI 2, HW 2).

## 2. 작업 전에 반드시 읽을 문서 (정식 문서는 `docs/`에만 있음)

**최상위 기준은 `docs/00-project-guide.md`(OT 가이드 요약)입니다.** 목표·범위·일정·제출물·평가 기준·FINAL CHECKLIST에 관한 질문은 이 문서를 근거로 답하고, 어느 항목(쪽 번호)에 근거했는지 밝힌다.

| 작업 내용 | 먼저 읽을 문서 |
|---|---|
| 평가·제출·일정 관련 판단 | `docs/00-project-guide.md`, `docs/09-submission.md` |
| 어떤 기능이든 | `docs/01-requirements.md` — 이 작업이 어느 REQ 번호에 해당하는지 확인 |
| 경보 단계·전환 로직·기준값 | `docs/02-state-machine.md` |
| 클래스 간 데이터, 로그(DB) 저장, 핀 | `docs/03-interface.md`, `core/models.py`, `logging_/event_logger.py` |
| 테스트 | `docs/04-test-cases.md` |
| 고장 대비 | `docs/05-fmea.md` |
| 구조·모델·부품 선정 | `docs/06-system-design.md` |
| 성능 측정 | `docs/07-performance.md` |
| 문제 해결·피드백 기록 | `docs/08-progress-log.md` |
| 설정값(온도·시간·핀·부저 주기) | `config.yaml` — 코드에 숫자를 직접 쓰지 않는다 |

**작업이 어느 REQ에도 해당하지 않으면 코드를 쓰기 전에 사용자에게 알린다.** 요구사항 밖의 기능을 임의로 추가하지 않는다.

### 2-1. 문서와 코드가 다를 때

코드 뼈대는 최종 기획안보다 먼저 만들어져서, 아직 문서와 다른 곳이 있습니다. 목록은 **[`docs/03-interface.md` 8번 '코드 반영 필요 목록'](docs/03-interface.md)**에 있습니다.
- **기준은 문서(01·02·03)입니다.** 코드가 문서와 다르면 문서 쪽을 따른다.
- 그 목록에 있는 차이를 고치는 작업이 아니라면, 다른 작업 중에 그 부분을 임의로 같이 고치지 않는다. 필요하면 사용자에게 먼저 알린다.
- 목록의 항목을 고쳤으면 그 줄을 지우거나 "완료"로 바꾸자고 사용자에게 제안한다.

## 3. 폴더 구조

```
AGENTS.md / CLAUDE.md / GEMINI.md   AI 규칙 (AGENTS.md가 원본)
CONTRIBUTING.md · README.md         사람용 팀 규칙 · 프로젝트 소개
main.py                             시작점 (실행: 저장소 루트에서 python main.py)
config.yaml                         설정값 (임계값·시간·핀·부저 주기·모델 경로)
requirements.txt                    파이썬 패키지 목록
core/                               controller.py(전체 흐름) · event_bus.py(이벤트 전달) · models.py(데이터 형식)
sensors/                            base.py · rgb_camera.py · thermal_camera.py(MLX90640) · gas_sensor.py (HW)
vision/                             object_detector.py(YOLO 사람·불·연기 인식) · thermal_analyzer.py(고온 후보 구역) (SW/AI)
decision/                           policies.py(판단 규칙) · alert_evaluator.py(단계 판단) · roi_manager.py(위험 구역) · person_monitor.py(작업자 접근) (SW/AI)
actuators/                          notifier.py(부저·LED·스피커·출구 LED) (HW)
logging_/                           event_logger.py(SQLite DB·스냅샷 기록)
models/                             학습된 모델 파일 (깃 제외, readme.md만 올림)
tests/                              자동 테스트 (pytest)
logs/                               실행 중 생기는 DB·스냅샷 (깃 제외, 실행하면 자동 생성)
docs/                               정식 문서 00~09, hardware/, ADR/ (회의 기록은 GitHub 이슈, `meeting` 라벨)
.github/                            이슈·PR 템플릿
```

- **import는 저장소 루트 기준 패키지 경로로 쓴다.** 예: `from core.models import AlertLevel`, `from decision.policies import ThresholdPolicy`. 그래서 항상 루트에서 `python main.py`로 실행한다.
- **`logging_` 폴더의 밑줄은 오타가 아니다.** 파이썬 기본 모듈 `logging`과 이름이 같으면 `import logging`이 우리 폴더를 먼저 불러와 다른 라이브러리가 깨진다. 밑줄을 지우지 않는다.
- **모델 학습 코드 위치는 아직 정하지 않았다.** OT 제출 규칙상 학습 코드도 제출해야 하므로, 학습 코드를 만들 때는 폴더 위치를 먼저 사용자에게 확인한다 ([09-submission](docs/09-submission.md) 2번).
- 새 폴더나 최상위 파일이 필요하면 만들기 전에 사용자에게 이유를 설명하고 확인받는다.

## 4. 코드 규칙

### 4-1. 데이터 형식 (가장 중요)
- 클래스끼리 주고받는 데이터는 **반드시 `core/models.py`의 dataclass·Enum**으로 주고받는다. dict를 임의로 만들지 않는다.
- 결과는 `core.event_bus.EventBus`로 `Event`를 발행하고, 출력·기록 클래스는 `EventListener`를 상속해 `onEvent()`로 받는다. 출력 클래스가 판단 클래스를 직접 부르지 않는다.
- 기록은 **`logging_/event_logger.py`의 `EventLogger`**로 SQLite DB(`logs/*.db`)와 스냅샷(`logs/snapshots/`)에 남긴다. 사람이 볼 리포트는 같은 클래스의 CSV 내보내기로 만든다 ([ADR-0003](docs/ADR/0003-로그는-SQLite와-스냅샷.md)).
- 단위: 온도 **℃**, 온도 변화 **℃/초**, 시간 **`time.time()` 유닉스 초** (사람에게 보여 줄 때는 한국시간 KST), 확률 **0~1**, 위치 **픽셀** (열화상 32×24 / 일반 카메라 해상도). 두 카메라 위치를 비교할 때는 열화상 좌표를 일반 카메라 좌표로 바꾼 뒤 비교한다 ([03-interface](docs/03-interface.md) 2번).
- 값이 없으면 `None`. 0으로 채우지 않는다.

### 4-2. 인터페이스를 바꿔야 할 때
- `core/models.py`, `docs/03-interface.md`는 **항상 같은 커밋에서 함께** 바꾼다. DB 테이블 구조를 바꾸면 `logging_/event_logger.py`도 같이 바꾼다.
- 필드 추가·삭제·이름 변경은 다른 팀원 코드에 영향을 주므로, **바꾸기 전에 사용자에게 영향 범위를 설명하고 확인받는다.**
- 바꾸면 `03-interface.md`의 문서 버전과 변경 이력을 갱신한다.

### 4-3. 파이썬 스타일 (지금 코드에 맞춘 규칙)
- 클래스: `PascalCase` (`AlertEvaluator`) / **메서드·함수: `camelCase`** (`findHotZones`, `onEvent`) / 내부용 메서드: 앞에 밑줄 (`_releaseIfNormal`)
- 변수·인자·파일·폴더·`config.yaml` 키: `snake_case` (`release_hold_sec`) / 상수·Enum 값: `UPPER_CASE` (`AlertLevel.CAUTION`)
- **파이썬 기본 모듈과 같은 파일·폴더 이름 금지:** `logging`, `csv`, `types`, `time`, `json` 등 (그래서 `logging_`)
- 한 파일은 한 가지 책임만. 기준값(온도 등)은 코드에 숫자로 박지 말고 `config.yaml`에서 읽는다.
- 라즈베리파이 전용 라이브러리(`gpiozero`, `picamera2`, MLX90640 드라이버)는 **함수·생성자 안에서 import**한다 (지금 코드 방식). 그래야 노트북에서도 다른 모듈을 import·테스트할 수 있다.
- 새 외부 라이브러리를 추가하면 `requirements.txt`에 반영하고, 라즈베리파이 4에서 설치·실행 가능한지 언급한다.
- 커밋 전 확인: `python -m pyflakes .` (안 쓰는 import·오타 검사)

### 4-4. 안전 로직은 임의로 약하게 만들지 않는다
아래는 안전 요구사항이다 ([02-state-machine](docs/02-state-machine.md), [ADR-0002](docs/ADR/0002-경보-3단계와-판단-기준.md), [ADR-0004](docs/ADR/0004-대피-단계-추가.md)). 디버깅 편의를 위해서라도 끄거나 우회하는 코드를 커밋하지 않는다.
- **경보 조건 4가지:** 100℃ 이상 10초 유지 · 130℃ 이상 즉시 · 가스 기준값 2배 이상 · 주의 원인 중 하나가 1분 이상 지속 (REQ-003, 022, 023, 024)
- **대피 조건:** 경보 단계에서 불·연기 감지 (REQ-026). 경보를 거치지 않고 대피로 가는 조건을 추가하려면 먼저 사용자에게 알리고 ADR로 남긴다
- 경보·대피 래칭: 리셋 버튼 전까지 해제 금지, 리셋하면 주의로 복귀. 원인이 남아 있으면 즉시 다시 그 단계 (REQ-008)
- 주의 해제: 원인이 모두 사라진 뒤 20초 유지돼야 정상 (REQ-013)
- **고장은 단계가 아니다** ([ADR-0005](docs/ADR/0005-고장은-예외-처리와-관제-로그.md)): 센서·카메라가 데이터를 주지 않으면 예외 처리로 프로그램을 멈추지 않고, 그 값은 `None`으로 두고 나머지로 판단을 계속하며, 관제 센터에 고장 로그를 보낸다. 고장 때문에 단계를 낮추지 않는다 (REQ-010)
- 주의·경보·대피가 되면 관제 센터에 사유와 당시 데이터 로그를 보낸다 (REQ-027)
- 가스 센서 예열 전 값은 판단에 쓰지 않음 (REQ-017)
- 기준값을 바꾸는 것은 안전 로직을 바꾸는 것이다. `config.yaml`의 판단 기준값을 바꾸면 이유를 `docs/08-progress-log.md`에 남기자고 사용자에게 제안한다.

## 5. 범위

### 5-1. 범위 밖 — 제안하거나 구현하지 않는다
- 레이저로 위험 지점 지시
- 클라우드·외부 서버·원격 알림 (온디바이스 단독 동작)
- **차단문·진화장치 제어** (`config.yaml`의 `response`, `ResponseController`) — 최종 기획안에 없음. 기획안이 바뀌면 다시 정한다

**보류 중:** MCU 사용 여부. 사용이 확정되기 전까지 MCU 전제 설계를 기본안으로 제안하지 않는다.

## 6. Git 규칙
- **`main`에 직접 커밋·푸시하지 않는다.** 작업은 `dev`에서 갈라진 브랜치에서 한다.
- 브랜치 이름: `feature/REQ-014-dynamic-roi`, `fix/...`, `docs/...`, `hw/...`
- 커밋 메시지: `[역할] 무엇을 했는지` — 역할 태그는 `[PM] [HW] [SW] [AI] [DOC] [TEST] [REFACTOR]`
  - 예: `[AI] REQ-014 고온 영역 ROI 생성 초안`
- `logs/`(DB·스냅샷), 모델 파일(`*.pt`, `*.onnx`, `*.tflite`, NCNN 변환 폴더)은 커밋하지 않는다.
- 작업이 커밋하기 좋은 단위로 끝나면, 사용자에게 **커밋 시점과 메시지 예시**를 알려준다.

## 7. 문서 규칙
- 정식 문서는 `docs/` 아래 마크다운만. 다른 곳에 정식 문서를 새로 만들지 않는다. (폴더 readme는 그 폴더 안내용)
- OT 원본 PDF는 저장소에 올리지 않는다 (다른 조 수강생 이름 포함). 내용은 `docs/00-project-guide.md`로 본다.
- 문제를 해결했거나 피드백을 반영했으면 `docs/08-progress-log.md`에 한 줄 추가를 제안한다 (OT 평가 '문제 해결·개선').
- 같은 내용을 두 문서에 중복해서 적지 않는다. 다른 문서를 링크한다.
- **팀원 개인의 환경 문제(계정·자격 증명·개인 PC 설정 등)는 프로젝트 문서(특히 08)에 기록하지 않고, 사용자에게만 알린다.**
- 회의록 파일을 만들지 않는다. 회의 기록은 GitHub 이슈(`meeting` 라벨)에 남기고, 문서에서는 이슈 번호로 링크한다.
- **`docs/04-test-cases.md`, `docs/05-fmea.md`는 사용자가 요청할 때만 수정한다.** 테스트가 시작되면 사람이 채우는 문서다.
- 문서를 고치면 그 문서의 버전과 변경 이력을 갱신한다. 날짜는 한국시간(KST).
- 그림은 이미지 파일 대신 Mermaid로 그린다 (깃허브에서 바로 그림으로 보임).

## 8. 답변 방식
- **한국어로 답한다.**
- 팀원이 배우는 프로젝트다. 코드를 바꿀 때 **무엇을, 왜 바꾸는지** 짧게 설명하고, 다음에 할 일을 알려준다.
- **확실하지 않은 내용은 단정하지 않는다.** 라즈베리파이에서의 속도, 센서 사양, 라이브러리 동작처럼 확인이 필요한 것은 "확인 필요"라고 밝히고 확인 방법을 제시한다.
- 하드웨어 배선·전원과 관련된 제안은 부품 손상·화상 위험이 없는지 함께 언급한다 (캡톤 히터, 전원 용량, 5V/3.3V 혼용 등).
