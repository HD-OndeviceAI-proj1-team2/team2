# 팀 작업 규칙 (CONTRIBUTING)

> 모든 팀원이 작업 전에 한 번 읽어 주세요. 폴더 구조, 규칙 등을 확인한 뒤에도 궁금한 점이 있으면 언제든 문의·건의 부탁드립니다!

## 📌 먼저 꼭 알아 둘 것

0. **평가·제출·일정의 기준은 [`docs/00-project-guide.md`](docs/00-project-guide.md)(OT 가이드 요약)입니다.**
1. **정식 문서는 깃허브 `docs/` 폴더 아래에 있습니다.**
2. **폴더 구조와 규칙을 확인한 뒤에도 궁금한 점이 있으면 문의·건의 부탁드립니다.**
3. **작업할 때는 [`docs/01-requirements.md`](docs/01-requirements.md)의 REQ(작업 요구사항) 표를 보시고, 직접 깃허브 이슈를 만들거나 이슈를 만들어 달라고 요청해 주세요.** (만드는 방법은 아래 4번)
4. **[`docs/03-interface.md`](docs/03-interface.md)에 클래스끼리 주고받을 데이터와 기록(DB) 형식, 핀 할당을 적어 두었습니다.** 코드는 `core/models.py`(데이터 형식)와 `logging_/event_logger.py`(DB·스냅샷 기록)에 있어요. 아직 문서와 코드가 다른 곳은 03번 문서 8번 '코드 반영 필요 목록'에 모아 두었어요. 바꿔야 할 부분이 있으면 말씀해 주세요!
5. **`docs/04-test-cases.md`(테스트)와 `docs/05-fmea.md`(위험성 검토)는 테스트가 시작된 뒤에 채우는 문서입니다. 지금은 그대로 두세요!**
   - 04번: 기능이 중간중간 잘 동작하는지 확인하는 테스트 목록
   - 05번: 한 부분이 고장 났을 때 어떻게 알아채고 대비할지 정리한 표

> 💡 경보 4단계(정상·주의·경보·대피)와 전환 규칙, 기준값은 깃허브에서 [`docs/02-state-machine.md`](docs/02-state-machine.md)를 열면 그림으로 볼 수 있어요.

---

## 1. 폴더 구조

```
├─ README.md              프로젝트 소개
├─ CONTRIBUTING.md        이 문서 (팀 규칙)
├─ AGENTS.md              AI 도구 공통 규칙 (원본)
├─ CLAUDE.md / GEMINI.md  AGENTS.md를 불러오는 연결 파일 (직접 고치지 않음)
├─ docs/                  ★ 정식 문서
│  ├─ 00-project-guide.md   OT 가이드 요약 — 목표·일정·제출물·평가 기준 (최우선 기준)
│  ├─ 01-requirements.md    요구사항 (REQ 번호)
│  ├─ 02-state-machine.md   경보 단계·전환 규칙 (그림)
│  ├─ 03-interface.md       클래스 간 데이터·DB 기록 형식·핀 할당
│  ├─ 04-test-cases.md      테스트 (테스트 시작 후 작성)
│  ├─ 05-fmea.md            위험성 검토 (테스트 시작 후 작성)
│  ├─ 06-system-design.md   구조·파이프라인·모델·부품 선정 근거
│  ├─ 07-performance.md     정확도·지연시간 측정 결과
│  ├─ 08-progress-log.md    수행 경과·문제 해결·피드백 기록 ← 그날그날 한 줄씩!
│  ├─ 09-submission.md      제출물 5종·FINAL CHECKLIST 점검
│  ├─ hardware/             BOM·회로도·구성도·사진 (세부 산출물)
│  └─ ADR/                  설계 결정 기록
├─ main.py                시작점 (저장소 루트에서 python main.py)
├─ config.yaml            설정값 — 임계값·시간·핀·부저 주기 (숫자는 여기서만!)
├─ requirements.txt       파이썬 패키지 목록
├─ core/                  전체 흐름(controller) · 이벤트 전달(event_bus) · 데이터 형식(models)
├─ sensors/               일반 카메라 · 열화상(MLX90640) · 가스 센서 입력 (HW)
├─ vision/                YOLO 사람·불·연기 인식 · 열화상 고온 후보 구역 (SW/AI)
├─ decision/              판단 규칙 · 경보 단계 · 위험 구역(ROI) · 작업자 접근 (SW/AI)
├─ actuators/             부저 · LED · 스피커 · 출구 LED (HW)
├─ logging_/              DB·스냅샷 기록 (밑줄은 일부러 — 아래 6번)
├─ models/                학습된 모델 파일 (깃 제외)
├─ tests/                 자동 테스트 (pytest)
├─ logs/                  실행하면 생기는 DB·사진 (깃 제외)
└─ .github/               이슈·PR 템플릿
```

**한 번의 반복에서 일어나는 일:** 센서 읽기(`sensors`) → 분석(`vision`) → 판단(`decision`) → `EventBus`로 알림 발행 → 출력(`actuators`)·기록(`logging_`)이 각자 받아서 처리. 순서는 `core/controller.py`의 `loop()`에 주석으로 적혀 있어요.

## 2. 브랜치 규칙

#### "main·dev는 PR 때 승인 1명 필요"

| 브랜치 | 역할 | 규칙 |
|---|---|---|
| `main` | 항상 시연 가능한 안정 버전 | **직접 커밋·푸시 금지.** 버전 배포 시점에만 `dev`에서 합침 |
| `dev` | 팀원 작업을 모으는 통합 브랜치 | 작업 브랜치에서 PR로만 합침 |
| 작업 브랜치 | 한 사람이 한 가지 작업 | `dev`에서 갈라져 나와 작업 후 PR |

**작업 브랜치 이름:** `종류/REQ번호-짧은설명`

| 종류 | 언제 | 예 |
|---|---|---|
| `feature/` | 새 기능 | `feature/REQ-014-dynamic-roi` |
| `fix/` | 버그 수정 | `fix/gas-warmup-false-alarm` |
| `docs/` | 문서만 수정 | `docs/02-state-machine` |
| `hw/` | 배선·핀맵 등 하드웨어 기록 | `hw/pin-assignment` |

## 3. 작업 흐름 (처음부터 끝까지)

```bash
# ① 최신 dev 받기 (작업 시작 전 항상!)
git switch dev
git pull

# ② 작업 브랜치 만들기
git switch -c feature/REQ-014-dynamic-roi

# ③ 작업하고 커밋 (여러 번 OK)
git add vision/thermal_analyzer.py
git commit -m "[AI] REQ-014 고온 영역 ROI 생성 초안"

# ④ 깃허브에 올리기
git push -u origin feature/REQ-014-dynamic-roi
```
⑤ 깃허브에서 **Pull Request** 만들기 (`dev` ← 작업 브랜치) → 팀원 1명 확인 → Merge → 작업 브랜치 삭제

**팁:** 브랜치는 하루이틀 안에 PR로 합칠 수 있는 크기로 작게 나눠 주세요. 오래 들고 있을수록 합칠 때 충돌이 커져요.

## 4. 이슈 만드는 법

1. `docs/01-requirements.md`에서 하려는 작업의 **REQ 번호**를 찾아요.
2. 깃허브 **Issues → New issue → "작업 (REQ 기반)"** 템플릿을 골라요.
3. 아래 항목을 채워요.

| 항목 | 쓰는 법 | 예 |
|---|---|---|
| Title | `[REQ-번호] 할 일` | `[REQ-014] 열화상 고온 영역으로 위험 구역 ROI 생성` |
| Description | 템플릿 칸 채우기 (무엇을, 완료 조건, 관련 TC) | 템플릿 참고 |
| Assignees | 담당자 깃허브 계정 | |
| Labels | 역할 1개 + 종류 1개 | `SW/AI`, `feature` |
| Type | 깃허브 이슈 유형 (설정된 경우) | Feature / Task / Bug |

REQ에 없는 작업이 필요하면 먼저 팀장이나 통합·문서 담당에게 말해 주세요. 요구사항 문서에 추가한 뒤 이슈를 만들어요.

**라벨 목록** (통합·문서 담당이 처음에 한 번 만들어 둠)

| 역할 | 종류 |
|---|---|
| `PM` `HW` `SW/AI` `DOC` | `feature` `bug` `docs` `test` `question` `meeting` |

**회의 기록:** 회의록 파일은 만들지 않고 이슈로 남겨요. Title은 `[회의] 11/26 주제`, 라벨은 `meeting`, 본문에는 정한 것·할 일(담당자)·다음 회의를 적어요. 회의에서 정한 일이 문서를 바꾸면, 그 PR이나 [`docs/08-progress-log.md`](docs/08-progress-log.md)에 회의 이슈 번호(`#12`)를 적어 주세요.

## 5. 커밋 메시지

`[역할] 무엇을 했는지 (+ 필요하면 왜)`

| 태그 | 언제 |
|---|---|
| `[PM]` | 일정·계획 |
| `[HW]` | 배선·하드웨어 코드·핀맵 |
| `[SW]` | 일반 소프트웨어 (출력, 상태 머신 등) |
| `[AI]` | 인식 모델·열화상 처리 |
| `[DOC]` | 문서 |
| `[TEST]` | 테스트 코드·결과 |
| `[REFACTOR]` | 동작은 그대로, 구조만 정리 |

예: `[SW] T_HOT 50→60 변경: 손 피규어를 고온으로 오검출해서`

## 6. 꼭 지켜 주세요

- **인터페이스를 바꿀 때:** `core/models.py`와 `docs/03-interface.md`는 **같은 커밋에서 같이** 바꿔요. 다른 팀원 코드에 영향을 주니 바꾸기 전에 단톡에 한 번 알려 주세요.
- **기록은 `EventLogger`로:** 경보 이벤트와 온도는 `logging_/event_logger.py`의 `EventLogger`가 SQLite DB(`logs/`)에 저장하고, 경보 순간 사진도 남겨요. 엑셀로 볼 리포트는 CSV로 내보내요.
- **올리면 안 되는 것:** `logs/`(DB·사진), 모델 파일(`*.pt`, `*.onnx`, `*.tflite`, NCNN 변환 폴더), 비밀번호·토큰. (`.gitignore`로 대부분 막아 뒀어요)
- **이름 짓기 (지금 코드 방식):** 클래스 `AlertEvaluator`처럼 대문자로 시작 · 메서드 `findHotZones`처럼 camelCase · 변수·파일·config 키 `release_hold_sec`처럼 소문자+밑줄.
- **기본 모듈과 같은 이름 금지:** `logging`, `csv`, `types` 같은 이름의 파일·폴더를 만들면 import가 꼬여요. 그래서 기록 폴더가 `logging_`예요.
- **안전 로직은 끄지 않기:** 경보·대피 래칭, 센서 고장 예외 처리·관제 로그 같은 안전 기능은 테스트 중에도 끈 채로 커밋하지 않아요.
- **설정값은 `config.yaml`에서만:** 온도·시간·핀 번호를 코드에 직접 쓰지 않아요.
- **막혔다 풀렸으면 08번에 한 줄:** 문제·원인·해결·결과를 [`docs/08-progress-log.md`](docs/08-progress-log.md)에 남겨 주세요. 평가 항목이에요.
- **하드웨어:** 배선은 전원을 끄고. 캡톤 히터는 켜 둔 채 자리를 비우지 않기.

## 7. AI 도구 사용 규칙

Codex, Claude, Gemini를 써도 좋아요. 팀 규칙을 AI가 알 수 있게 파일을 준비해 뒀어요.

### 7-1. 터미널·에디터에서 쓰는 AI (Codex, Claude Code, Gemini CLI)
저장소 폴더에서 실행하면 **자동으로 규칙을 읽어요.** 따로 할 일은 없어요.

| 도구 | 자동으로 읽는 파일 |
|---|---|
| Codex | `AGENTS.md` |
| Claude Code | `CLAUDE.md` → `AGENTS.md`를 불러옴 |
| Gemini CLI | `GEMINI.md` → `AGENTS.md`를 불러옴 |

**규칙을 고치고 싶으면 `AGENTS.md`만 고쳐요.** `CLAUDE.md`, `GEMINI.md`는 연결용이라 건드리지 않아요.

### 7-2. 웹·앱 채팅으로 쓰는 AI (ChatGPT, Claude, Gemini 웹사이트)
웹 채팅은 저장소 파일을 자동으로 읽지 못해요. 대화를 시작할 때 아래처럼 해 주세요.

1. `AGENTS.md` 파일을 **첨부**하거나 내용을 복사해 붙여 넣기
2. 작업과 관련된 문서도 같이 첨부 (예: 인식 작업이면 `01-requirements.md`, `03-interface.md`, `core/models.py`)
3. 첫 메시지에 이렇게 쓰기:
   > 첨부한 AGENTS.md의 규칙을 따라 줘. 나는 [역할]이고, 지금 하려는 작업은 [REQ-번호: 할 일]이야.

### 7-3. AI 결과물을 쓸 때 사람이 확인할 것
- AI가 만든 코드도 **내가 설명할 수 있어야** 커밋해요. 모르는 부분은 AI에게 "왜 이렇게 했는지" 물어보고 이해한 뒤에 올려요.
- AI가 `core/models.py`나 `03-interface.md`를 바꾸려고 하면 멈추고 팀에 먼저 공유해요.
- 라즈베리파이 성능, 센서 사양처럼 AI가 틀리기 쉬운 내용은 직접 확인해요.

## 8. 문의
폴더 구조, 규칙, 문서 내용에 대해 궁금한 점이나 바꾸고 싶은 점이 있으면 **통합·문서 담당**에게 말하거나 `question` 라벨로 이슈를 만들어 주세요.
