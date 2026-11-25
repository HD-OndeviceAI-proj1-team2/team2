"""MLX90640 열화상 카메라 (I2C)."""
import time

import numpy as np

from core.models import Frame
from sensors.base import FrameSource


class ThermalCamera(FrameSource):
    def __init__(self, refresh_hz: int = 4):
        super().__init__("thermal", (32, 24), refresh_hz)
        self.mlx = None

    def open(self) -> None:
        ...

    def read(self) -> Frame:
       ...

    def close(self) -> None:
        ...

    def isOpened(self) -> bool:
        return self.mlx is not None
