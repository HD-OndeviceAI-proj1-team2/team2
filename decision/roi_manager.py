"""판단 결과가 L1 이상인 후보만 위험구역으로 지정하고, 정상이 유지되면 해제"""
from typing import Dict, List, Optional, Tuple

from core.models import AlertLevel, DangerZone, HotZone


class ROIManager:
    def __init__(self, release_hold_sec: float = 5.0):
        self.release_hold_sec = release_hold_sec    # 정상온도가 이만큼 유지되면 위험구역 해제
        self.zones: Dict[int, DangerZone] = {}      # 현재 위험구역 list
        self._next_id = 1       # 다음에 만들 위험구역 번호

    def update(self, judged: List[Tuple[HotZone, AlertLevel]], now: float) -> None:
        seen = set()

        for hot, level in judged:
            if level < AlertLevel.L1_HIGH:
                continue                        # 기준 안 넘으면 지정 안 함
            zone = self._match(hot)
            if zone is None:                    # 새 위험구역
                zone = DangerZone(self._next_id, hot.bbox, level, hot.max_temp, now)
                self.zones[zone.id] = zone
                self._next_id += 1
            else:                               # 기존 위험구역 갱신
                zone.bbox = hot.bbox
                zone.level = level
                zone.max_temp = hot.max_temp
                zone.normal_since = None
            seen.add(zone.id)

        # 이번에 기준을 넘지 않은 구역은 정상 시작 시각 기록
        for zone in self.zones.values():
            if zone.id not in seen and zone.normal_since is None:
                zone.normal_since = now

        self._releaseIfNormal(now)

    # 현재 위험구역 목록 반환
    def getActiveZones(self) -> List[DangerZone]:
        return list(self.zones.values())

    def _match(self, hot: HotZone) -> Optional[DangerZone]:
        # 겹치는 기존 위험구역이 있으면 같은 구역으로
        for zone in self.zones.values():
            if zone.bbox.overlaps(hot.bbox):
                return zone
        return None

    def _releaseIfNormal(self, now: float) -> None:
        # 정상이 release_hold_sec 이상 유지된 구역 해제
        expired = [zid for zid, z in self.zones.items()
                   if z.normal_since is not None
                   and now - z.normal_since >= self.release_hold_sec]
        for zid in expired:
            del self.zones[zid]
