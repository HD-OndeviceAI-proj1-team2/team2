"""카메라 공통 인터페이스."""
from abc import ABC, abstractmethod
from typing import Tuple

from core.models import Frame


class FrameSource(ABC):
    def __init__(self, name: str, resolution: Tuple[int, int], fps: float):
        self.name = name                # "thermal" / "rgb"
        self.resolution = resolution    # (가로, 세로)
        self.fps = fps

    @abstractmethod
    def open(self) -> None:
        """장치 연결"""

    @abstractmethod
    def read(self) -> Frame:
        """한 프레임 읽기"""

    @abstractmethod
    def close(self) -> None:
        """장치 연결 해제"""

    @abstractmethod
    def isOpened(self) -> bool:
        """연결 상태 확인"""
