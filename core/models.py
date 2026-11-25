""" 클래스끼리 주고받는 데이터 형식 총괄 """
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import List, Optional

import numpy as np


# 데이터 형식은 예시입니다 ~

# ── 경보 단계 ─────────────────────────────
class AlertLevel(IntEnum):
    NORMAL = 0
    L1_HIGH = 1          # 정상온도보다 높음
    L2_RAPID_RISE = 2    # 갑자기 오름
    L3_CRITICAL = 3      # 훨씬 높음
    L4_FIRE = 4          # 불·연기 감지


# ── YOLO가 찾는 물체 종류 ─────────────────
class DetectionClass(Enum):
    PERSON_MODEL = "person_model"
    FIRE = "fire"
    SMOKE = "smoke"


# ── 사각형 영역 ───────────────────────────
@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int

    """
    -- 필요 코드 에시 --

    def overlaps(self, other: "Rect") -> bool:
        # 두 사각형이 겹치는지
        return not (self.x + self.w <= other.x or other.x + other.w <= self.x or
                    self.y + self.h <= other.y or other.y + other.h <= self.y)
    """


# ── 카메라가 읽은 한 장면 ─────────────────
@dataclass
class Frame:
    data: np.ndarray     # 열화상: 온도 행렬(24x32, °C) / 일반: 영상(H x W x 3)
    timestamp: float     # 찍힌 시각 (time.time())
    source: str          # "thermal" / "rgb"


# ── 후보 구역 (판단 전) ───────────────────
@dataclass
class HotZone:
    bbox: Rect           # 열화상 좌표
    max_temp: float      # 구역 안 최고온도 (°C)
    slope: float         # 구역 안 최대 온도 변화율 (°C/s)


# ── YOLO 감지 결과 하나 ───────────────────
@dataclass
class Detection:
    cls: DetectionClass
    conf: float          # 0~1
    bbox: Rect           # 일반 카메라 좌표


# ── 위험구역 (판단 후, L1 이상만) ─────────
@dataclass
class DangerZone:
    id: int
    bbox: Rect                              # 열화상 좌표
    level: AlertLevel
    max_temp: float
    created_at: float
    normal_since: Optional[float] = None    # 기준 아래로 내려간 시각 (해제 판단용)


# ── EventBus로 보내는 알림 ────────────────
@dataclass
class Event:
    level: AlertLevel                                   # 전체 경보 레벨
    zones: List[DangerZone] = field(default_factory=list)
    person_warning: bool = False                        # 위험구역 있는데 사람 감지됨
    timestamp: float = 0.0
    snapshot: Optional[np.ndarray] = None               # 그 순간 일반 카메라 영상
