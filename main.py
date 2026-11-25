"""프로그램 시작점."""
from core.controller import SystemController

if __name__ == "__main__":
    controller = SystemController("config.yaml")
    try:
        controller.start()     # 카메라 열기
    except KeyboardInterrupt:
        print("종료합니다")
    finally:
        controller.stop()      # 카메라, DB 정리
