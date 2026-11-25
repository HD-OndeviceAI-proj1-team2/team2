"""평상시 온도 기록 + 경보 이벤트 기록 + 사고 리포트."""
import csv
import os
import sqlite3
import time
from typing import Optional

from core.event_bus import EventListener
from core.models import AlertLevel, Event, Frame


class EventLogger(EventListener):
    def __init__(self, db_path: str = "logs/fire_guard.db",
                 snapshot_dir: str = "logs/snapshots",
                 temp_interval_sec: float = 5.0):
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        os.makedirs(snapshot_dir, exist_ok=True)
        self.snapshot_dir = snapshot_dir
        self.temp_interval_sec = temp_interval_sec
        self._last_temp_log = 0.0
        self._incident_id: Optional[int] = None

        # 메인 루프와 이벤트 처리가 다른 스레드가 되어도 쓸 수 있게
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self._createTables()


    # ── database table 만들기 ──────────
    def _createTables(self) -> None:
        ...


    # ── 평상시 온도 기록 함수 ──────────
    def logTemperature(self, frame: Frame) -> None:
        ...


    # ── 경보 이벤트 기록 ──────────
    def onEvent(self, event: Event) -> None:
        # 사고 시작: 정상 → 경보
        ...

        # 사고 종료: 경보 → 정상
        ...

        # db commit

    def _saveSnapshot(self, event: Event) -> Optional[str]:
        if event.snapshot is None:
            return None
        import cv2
        path = os.path.join(self.snapshot_dir, f"{event.timestamp:.0f}_L{int(event.level)}.jpg")
        cv2.imwrite(path, event.snapshot)
        return path

    # ── 사고 리포트 ───────────────────────
    def exportIncidentReport(self, incident_id: int) -> str:
        """사고 하나의 타임라인을 CSV로 저장"""
        ...

        

    def close(self) -> None:
        self.db.close()
