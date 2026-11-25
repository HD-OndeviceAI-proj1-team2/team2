"""위험구역이 있는데 사람 모형이 보이는지 판단"""
from typing import List

from core.models import DangerZone, Detection, DetectionClass


class PersonWarningMonitor:
    def __init__(self, min_frames: int = 3, cooldown_sec: float = 5.0):
        self.min_frames = min_frames        # 연속 몇 프레임 보여야 "사람 있음"
        self.cooldown_sec = cooldown_sec    # 한 번 경고 후 다시 경고까지 대기
        self._count = 0
        self._last_warn = -1e9

        

    def check(self, detections: List[Detection], zones: List[DangerZone],
              now: float) -> bool:
        """ 위험 구역 근처 사람 있는지 판단하는 함수 """

