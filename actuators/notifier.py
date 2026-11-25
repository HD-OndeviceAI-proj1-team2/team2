# 부저, 경보, led 제어

from typing import Dict, Optional

from core.event_bus import EventListener
from core.models import AlertLevel, Event


class Buzzer:
    def __init__(self, pin: int):
        from gpiozero import Buzzer as GZBuzzer
        self.dev = GZBuzzer(pin)
        self.period: Optional[float] = None

    def setPeriod(self, period: Optional[float]) -> None:
        # 부저 주기 설정
        ...


class StatusLED:
    COLORS = {
        # -- 각 경보마다 LED 색깔 지정 예시 --
        """
        AlertLevel.NORMAL: (0, 1, 0),         # 초록
        AlertLevel.L1_HIGH: (1, 1, 0),        # 노랑
        """
    }

    def __init__(self, red: int, green: int, blue: int):
        from gpiozero import RGBLED
        self.dev = RGBLED(red, green, blue)

    def setColor(self, level: AlertLevel) -> None:
        self.dev.color = self.COLORS[level]


class AlertNotifier(EventListener):
    def __init__(self, buzzer: Buzzer, led: StatusLED, periods: Dict[str, Optional[float]]):
        self.buzzer = buzzer
        self.led = led
        self.periods = periods              # config의 buzzer_period (레벨 이름 → 주기)

    # 레벨에 맞게 부저, LED 제어
    def onEvent(self, event: Event) -> None:
        self.buzzer.setPeriod(self.periods[event.level.name])
        self.led.setColor(event.level)
        if event.person_warning:
            self.warnPerson()

    def warnPerson(self) -> None:
        # 위험구역에 사람 있을 때.
        ...
