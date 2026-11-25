""" 경보 판단 규칙 """

from abc import ABC, abstractmethod
from typing import List, Optional

from core.models import AlertLevel, Detection, DetectionClass, HotZone


class AlertPolicy(ABC):
    @abstractmethod
    def evaluate(self, zone: Optional[HotZone],
                 detections: List[Detection]) -> AlertLevel:
        ...


# ── 구역 규칙 1: 온도 높이 → L1 / L3 ──────
class ThresholdPolicy(AlertPolicy):
    def __init__(self, normal_temp: float, l1_offset: float, l3_temp: float):
        self.l1_temp = normal_temp + l1_offset
        self.l3_temp = l3_temp

    def evaluate(self, zone, detections):
        """ 온도 판단 - Normal / L1 / L3"""
        if zone is None:
            return AlertLevel.NORMAL
        if zone.max_temp >= self.l3_temp:
            return AlertLevel.L3_CRITICAL
        if zone.max_temp >= self.l1_temp:
            return AlertLevel.L1_HIGH
        return AlertLevel.NORMAL


# ── 구역 규칙 2: 상승 속도 → L2 ───────────
class RateOfRisePolicy(AlertPolicy):
    def __init__(self, rise_rate: float):
        self.rise_rate = rise_rate      # °C/s

    def evaluate(self, zone, detections):
        """ 온도가 갑자기 상승하는지를 판단 """


# ── 전체 규칙: 불·연기 → L4 ───────────────
class FireDetectionPolicy(AlertPolicy):
    def __init__(self, min_conf: float = 0.5):
        self.min_conf = min_conf

    def evaluate(self, zone, detections):
        """ 불, 연기 객체 판단 """