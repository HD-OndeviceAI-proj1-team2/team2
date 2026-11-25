""" 전체 흐름을 순서대로 호출하는 메인 클래스 """

import time

import yaml

from core.event_bus import EventBus
from core.models import AlertLevel, Event

from sensors.thermal_camera import ThermalCamera
from sensors.rgb_camera import RGBCamera
from vision.thermal_analyzer import ThermalAnalyzer
from vision.object_detector import ObjectDetector
from decision.policies import ThresholdPolicy, RateOfRisePolicy, FireDetectionPolicy
from decision.alert_evaluator import AlertEvaluator
from decision.roi_manager import ROIManager
from decision.person_monitor import PersonWarningMonitor
from actuators.notifier import AlertNotifier, Buzzer, StatusLED
from actuators.response import ResponseController
from logging_.event_logger import EventLogger


class SystemController:
    def __init__(self, config_path: str):
        with open(config_path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        self.cfg = cfg
        th = cfg["thermal"]

        """
        -- 각 객체 생성 예시 --

        # 1) 입력
        self.thermal_cam = ThermalCamera(refresh_hz=th["refresh_hz"])
        self.rgb_cam = RGBCamera(**cfg["rgb"])

        # 2) 분석
        self.analyzer = ThermalAnalyzer(
            candidate_temp=th["normal_temp"] + th["candidate_offset"],
            candidate_rise=th["candidate_rise"],
            min_pixels=th["min_pixels"],
        )
        self.detector = ObjectDetector(**cfg["yolo"])

        # 3) 판단
        self.evaluator = AlertEvaluator(
            zone_policies=[
                ThresholdPolicy(th["normal_temp"], th["l1_offset"], th["l3_temp"]),
                RateOfRisePolicy(th["rise_rate"]),
            ],
            global_policies=[
                FireDetectionPolicy(cfg["yolo"]["fire_min_conf"]),
            ],
        )
        self.roi_manager = ROIManager(release_hold_sec=th["release_hold_sec"])
        self.person_monitor = PersonWarningMonitor(**cfg["person_warning"])

        # 4) 대처·기록은 EventBus에 등록만
        self.bus = EventBus()
        self.logger = EventLogger(**cfg["logging"])
        n = cfg["notifier"]
        self.bus.subscribe(AlertNotifier(
            buzzer=Buzzer(n["buzzer_pin"]),
            led=StatusLED(**n["led_pins"]),
            periods=n["buzzer_period"],
        ))
        self.response = ResponseController.fromConfig(cfg["response"])
        self.bus.subscribe(self.response)
        self.bus.subscribe(self.logger)

        self.current_level = AlertLevel.NORMAL
        self.running = False
        """

    # ── 시작 / 종료 ───────────────────────
    def start(self) -> None:
        self.thermal_cam.open()
        self.rgb_cam.open()
        self.running = True
        self.loop()

    def stop(self) -> None:
        self.running = False
        self.thermal_cam.close()
        self.rgb_cam.close()
        self.logger.close()
        

    # ── 반복 루프 ─────────────────────────
    def loop(self) -> None:
        while self.running:
            now = time.time()

            """
            -- 전체 실행 예시 --

            # ① 입력
            thermal = self.thermal_cam.read()
            rgb = self.rgb_cam.read()

            # ② 평상시 온도 기록
            self.logger.logTemperature(thermal)

            # ③ 후보 구역 묶기 (아직 위험구역 아님)
            candidates = self.analyzer.findHotZones(thermal)

            # ④ YOLO 감지 (사람 모형·불·연기)
            detections = self.detector.detect(rgb)

            # ⑤ 후보마다 레벨 판단
            judged = [(c, self.evaluator.evaluateZone(c)) for c in candidates]

            # ⑥ L1 이상만 위험구역 지정, 정상 유지된 구역은 해제
            self.roi_manager.update(judged, now)
            zones = self.roi_manager.getActiveZones()

            # ⑦ 전체 레벨 (불·연기 포함)
            level = self.evaluator.overallLevel(zones, detections)

            # ⑧ 위험구역이 있는데 사람이 보이는지
            person_warning = self.person_monitor.check(detections, zones, now)

            # ⑨ 변화가 있을 때만 이벤트 발행
            if level != self.current_level or person_warning:
                self.bus.publish(Event(level, zones, person_warning, now, rgb.data))
                self.current_level = level

            time.sleep(self.cfg["loop_interval_sec"])
            """
