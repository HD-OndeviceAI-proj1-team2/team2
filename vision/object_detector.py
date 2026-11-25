"""YOLO로 사람 모형, 불, 연기 찾기"""
from typing import List

from core.models import Detection, DetectionClass, Frame, Rect


class ObjectDetector:
    # 학습할 때 정한 클래스 이름 → Enum
    CLASS_MAP = {
        "person_model": DetectionClass.PERSON_MODEL,
        "fire": DetectionClass.FIRE,
        "smoke": DetectionClass.SMOKE,
    }

    def __init__(self, model_path: str, conf: float = 0.4, imgsz: int = 416,
                 fire_min_conf: float = 0.5):
        from ultralytics import YOLO
        self.model = YOLO(model_path, task="detect")    # 불러온 yolo 모델
        self.conf = conf    # 최소 신뢰도 - 미만인 감지는 버림
        self.imgsz = imgsz  # 모델 입력 크기

    def detect(self, frame: Frame) -> List[Detection]:
        """ 사람, 불, 연기 객체 탐지하고 리턴 """
