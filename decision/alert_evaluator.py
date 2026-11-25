# 경보 단계 판단

from typing import List

from core.models import AlertLevel, DangerZone, Detection, HotZone
from decision.policies import AlertPolicy

class AlertEvaluator:
    def __init__(self, zone_policies: List[AlertPolicy],
                 global_policies: List[AlertPolicy]):
        self.zone_policies = zone_policies      # 구역 하나를 보고 판단 (온도, 속도)
        self.global_policies = global_policies  # 화면 전체를 보고 판단 (불·연기)

    
    def evaluateZone(self, zone: HotZone) -> AlertLevel:
        # 온도만 보고 레벨 판단
        ...


    def overallLevel(self, zones: List[DangerZone],
                     detections: List[Detection]) -> AlertLevel:
        # 위에 판단한 레벨 + 감지한 불, 연기 같이보기
        ...
