"""온도 행렬에서 판단할 후보 구역(HotZone)을 묶는다. 위험구역 지정은 하지 않는다."""
from typing import List, Optional

import numpy as np

from core.models import Frame, HotZone, Rect


class ThermalAnalyzer:
    def __init__(self, candidate_temp: float, candidate_rise: float, min_pixels: int = 2):
        self.candidate_temp = candidate_temp    # 이 온도 이상이면 후보
        self.candidate_rise = candidate_rise    # 이 변화율(°C/s) 이상이어도 후보
        self.min_pixels = min_pixels            # 너무 작은 점(노이즈)은 무시
        self.prev: Optional[Frame] = None

    def findHotZones(self, frame: Frame) -> List[HotZone]:
        import cv2

        slope = self.calcSlope(frame)
        mask = (frame.data >= self.candidate_temp) | (slope >= self.candidate_rise)

        n, labels, stats, _ = cv2.connectedComponentsWithStats(
            mask.astype(np.uint8), connectivity=8)

        zones = []
        for i in range(1, n):                   # 0번은 배경
            x, y, w, h, area = stats[i]
            if area < self.min_pixels:
                continue
            region = labels == i
            zones.append(HotZone(
                bbox=Rect(int(x), int(y), int(w), int(h)),
                max_temp=float(frame.data[region].max()),
                slope=float(slope[region].max()),
            ))
        return zones

    def calcSlope(self, frame: Frame) -> np.ndarray:
        """픽셀별 온도 변화율 (°C/s)"""
        if self.prev is None:
            slope = np.zeros_like(frame.data)
        else:
            dt = max(frame.timestamp - self.prev.timestamp, 1e-3)
            slope = (frame.data - self.prev.data) / dt
        self.prev = frame
        # TODO: 노이즈가 심하면 최근 몇 프레임 평균으로 계산
        return slope
