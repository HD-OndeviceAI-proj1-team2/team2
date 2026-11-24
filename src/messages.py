"""모듈 사이에 주고받는 메시지 정의.

docs/03-interface.md 의 표를 그대로 코드로 옮긴 파일입니다.
★ 규칙: 이 파일을 바꾸면 docs/03-interface.md 도 같은 커밋에서 같이 바꾼다.
저장(CSV)은 이 파일에서 하지 않습니다 → csv_logger.py 담당.
"""
import time
from dataclasses import dataclass, field
from datetime import timedelta, timezone
from itertools import count
from typing import List, Optional

VERSION = 1
KST = timezone(timedelta(hours=9))
_seq = count(1)                     # 메시지마다 1, 2, 3 ... 번호를 붙인다


def _next_seq():
    return next(_seq)


# ── 비전1: 일반 카메라 (사람 인식) ─────────────────────
@dataclass
class Person:
    x: float            # cm, 바닥 지도 기준 발 위치
    y: float            # cm
    conf: float         # 0~1
    lying: bool = False # 누운 자세 여부


@dataclass
class PersonResult:
    persons: List[Person] = field(default_factory=list)
    ok: bool = True
    t: float = field(default_factory=time.time)
    seq: int = field(default_factory=_next_seq)
    v: int = VERSION


# ── 비전2: 열화상 (동적 위험 ROI) ──────────────────────
@dataclass
class HotRoi:
    id: int
    x: float        # cm
    y: float        # cm
    r: float        # cm, 위험 반경
    tmax: float     # ℃
    rate: float     # ℃/초, 음수면 식는 중
    hot_sec: float  # 초, 기준 이상 지속 시간


@dataclass
class ThermalResult:
    hot_rois: List[HotRoi] = field(default_factory=list)
    ambient: Optional[float] = None
    ok: bool = True
    t: float = field(default_factory=time.time)
    seq: int = field(default_factory=_next_seq)
    v: int = VERSION


# ── 가스 센서 ──────────────────────────────────────────
@dataclass
class GasReading:
    raw_v: float        # V
    ratio: float        # 기준 대비 배수 (1.0 = 평소)
    warmed_up: bool     # False면 판단에 쓰지 않음
    ok: bool = True
    t: float = field(default_factory=time.time)
    seq: int = field(default_factory=_next_seq)
    v: int = VERSION


# ── 판단 결과 ──────────────────────────────────────────
LEVELS = ("NORMAL", "CAUTION", "WARNING", "EVACUATE", "FAULT")
REASONS = ("HOT_SUSTAINED", "HOT_RISING", "HOT_EXTREME", "GAS",
           "PERSON_IN_ROI", "PERSON_DOWN", "SENSOR_FAULT")


@dataclass
class SystemState:
    level: str
    reasons: List[str] = field(default_factory=list)
    persons_in_zone: int = 0
    route: List[str] = field(default_factory=list)
    blocked_edges: List[str] = field(default_factory=list)
    latched: bool = False
    t: float = field(default_factory=time.time)
    seq: int = field(default_factory=_next_seq)
    v: int = VERSION

    def __post_init__(self):
        # 문서에 없는 값이 들어오면 바로 에러 → 오타·약속 위반을 일찍 발견
        if self.level not in LEVELS:
            raise ValueError(f"알 수 없는 level: {self.level}")
        for r in self.reasons:
            if r not in REASONS:
                raise ValueError(f"알 수 없는 reason: {r}")


# ── 직접 실행하면 메시지 예시와 약속 위반 검사를 보여 준다 ──
if __name__ == "__main__":
    print(ThermalResult(hot_rois=[HotRoi(id=3, x=30.0, y=18.5, r=6.2,
                                         tmax=64.2, rate=0.8, hot_sec=12.0)], ambient=23.1))
    print(SystemState(level="WARNING", reasons=["HOT_RISING", "PERSON_IN_ROI"]))
    try:
        SystemState(level="DANGER")          # 문서에 없는 단계 이름
    except ValueError as e:
        print("약속 위반은 에러로 잡힘:", e)
