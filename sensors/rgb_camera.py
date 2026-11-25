"""일반 카메라. 라즈베리파이 카메라 모듈(picamera2) 또는 USB 카메라(opencv)."""
import time

from core.models import Frame
from sensors.base import FrameSource


class RGBCamera(FrameSource):
    def __init__(self, width: int = 640, height: int = 480, fps: int = 15,
                 backend: str = "picamera2", device: int = 0):
        super().__init__("rgb", (width, height), fps)
        self.backend = backend
        self.device = device
        self.cam = None

    def open(self) -> None:
        """
        카메라에서 장치 열기
        """

    def read(self) -> Frame:
        """
        카메라에서 현재 장면 읽기
        """

    def close(self) -> None:
       """
        카메라에서 닫기
        """

    # 카메라 열려있는지 확인
    def isOpened(self) -> bool:
        return self.cam is not None
