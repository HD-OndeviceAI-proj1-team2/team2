"""CSV 저장 → 다시 읽기가 같은 값을 돌려주는지 확인 (REQ-012)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from csv_logger import CsvLogger, load_thermal  # noqa: E402
from messages import HotRoi, ThermalResult      # noqa: E402


def test_thermal_roundtrip(tmp_path):
    log = CsvLogger(root=str(tmp_path))
    msg = ThermalResult(hot_rois=[HotRoi(id=1, x=10.0, y=20.0, r=5.0,
                                         tmax=64.2, rate=0.8, hot_sec=3.0)], ambient=23.1)
    log.write(msg)
    log.write(ThermalResult(hot_rois=[], ambient=23.0))
    log.close()
    back = load_thermal(log.dir)
    assert len(back) == 2
    assert back[0].hot_rois[0].tmax == 64.2
    assert back[1].hot_rois == []
