"""전체 파이프라인 실행 진입점: 감지 → 판단 → 알림.

실행 (저장소 루트에서):  python src/main.py
각 모듈이 완성되면 아래 TODO 자리에 연결합니다. 지금은 구조만 보여 주는 뼈대입니다.

흐름 (OT 가이드 p.2 "감지 → 판단 → 알림"):
  vision_rgb      → PersonResult  ┐
  vision_thermal  → ThermalResult ├→ decision → SystemState → alerts (부저·LED)
  sensors         → GasReading    ┘                         └→ csv_logger (CSV 기록)
"""
from csv_logger import CsvLogger
from messages import SystemState


def main():
    log = CsvLogger()
    print(f"로그 폴더: {log.dir}")
    # TODO(vision_rgb):     persons = ...  → log.write(persons)
    # TODO(vision_thermal): thermal = ...  → log.write(thermal)
    # TODO(sensors):        gas = ...      → log.write(gas)
    # TODO(decision):       state = decide(persons, thermal, gas)
    state = SystemState(level="NORMAL")   # 뼈대 확인용
    log.write(state)
    # TODO(alerts):         output(state)
    log.close()
    print("뼈대 실행 완료:", state.level)


if __name__ == "__main__":
    main()
