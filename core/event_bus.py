""" 이벤트를 전달 -> notifier (Observer) """

from abc import ABC, abstractmethod
from typing import List

from core.models import Event


class EventListener(ABC):
    @abstractmethod
    def onEvent(self, event: Event) -> None:
        """ 각 클래스가 이벤트를 받았을 때 할 일. 오래 걸리는 작업은 하지 말고 바로 끝낼 것 """
        ...


class EventBus:
    def __init__(self):
        self.listeners: List[EventListener] = []        # 이벤트 받을 클래스 명단

    def subscribe(self, listener: EventListener) -> None:       # 명단에 클래스 하나 추가
        self.listeners.append(listener)

    def publish(self, event: Event) -> None:        # 명단에 있는 클래스의 onEvent 차례로 호출
        for listener in self.listeners:
            try:
                listener.onEvent(event)
            except Exception as e:
                # 하나가 고장 나도 나머지는 계속 동작하도록
                print(f"[EventBus] {type(listener).__name__} 오류: {e}")


