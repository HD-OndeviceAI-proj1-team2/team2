"""메시지를 CSV로 저장하고 다시 불러오는 도구.

메시지의 모양(필드)은 messages.py 가 정하고, 이 파일은 "파일에 어떻게 쓰는가"만 담당합니다.
★ 규칙: 저장 형식을 바꾸면 docs/03-interface.md 의 'CSV 저장'·'5. 저장 형식'도 같이 바꾼다.

[CSV로 저장할 때의 핵심]
CSV는 "한 줄 = 칸이 고정된 한 행"인 평평한 표다.
  - 평평한 메시지(GasReading, SystemState)  → asdict() 결과를 그대로 1행
  - 목록이 든 메시지(PersonResult, ThermalResult)
        → 메시지 자체는 *_frames.csv 에 1행
        → 목록 항목(사람 1명, 위험구역 1개)은 각각 별도 CSV에 1행씩
        → 두 파일은 seq(메시지 일련번호)로 연결한다 (엑셀 VLOOKUP·DB 조인과 같은 원리)
  - 문자열 목록(reasons, route 등)은 "|"로 이어 붙여 한 칸에 넣는다.

실행: python src/csv_logger.py  → 예시 로그를 만들고 다시 읽어 본다.
"""
import csv
import os
from dataclasses import asdict, fields
from datetime import datetime

from messages import (KST, GasReading, HotRoi, Person, PersonResult,
                      SystemState, ThermalResult)


# ── 메시지 → CSV 행으로 펼치기 ─────────────────────────
LIST_SEP = "|"


def _cell(value):
    """CSV 칸 하나에 넣을 값으로 바꾼다.
    None → 빈칸 (0으로 채우지 않음: '측정 못 함'과 '0'을 구분해야 하므로)
    bool → 1/0 (엑셀에서 합계·평균 내기 쉬움)
    문자열 목록 → "a|b|c"
    """
    if value is None:
        return ""
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, list):
        return LIST_SEP.join(str(v) for v in value)
    return value


def _common(msg):
    """모든 행 앞에 붙는 공통 칸: 일련번호, 유닉스 시간, 사람이 읽는 한국시간."""
    kst = datetime.fromtimestamp(msg.t, KST).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return {"seq": msg.seq, "t": round(msg.t, 3), "time_kst": kst}


def to_rows(msg):
    """메시지 1개 → {CSV 파일 이름: [행(dict), ...]}.

    asdict()로 dict를 만든 다음, 목록 필드만 꺼내서 따로 펼친다.
    """
    d = asdict(msg)                                  # 중첩된 dataclass까지 전부 dict로 바뀜
    base = _common(msg)

    if isinstance(msg, PersonResult):
        persons = d.pop("persons")                   # 목록은 꺼내서 따로 처리
        frame = {**base, "v": d["v"], "n_persons": len(persons), "ok": _cell(d["ok"])}
        items = [{**base, "idx": i, **{k: _cell(v) for k, v in p.items()}}
                 for i, p in enumerate(persons)]
        return {"person_frames": [frame], "persons": items}

    if isinstance(msg, ThermalResult):
        rois = d.pop("hot_rois")
        frame = {**base, "v": d["v"], "ambient": _cell(d["ambient"]),
                 "n_rois": len(rois), "ok": _cell(d["ok"])}
        items = [{**base, **{k: _cell(v) for k, v in r.items()}} for r in rois]
        return {"thermal_frames": [frame], "hot_rois": items}

    # 평평한 메시지: asdict() 결과를 그대로 한 행으로
    name = {GasReading: "gas", SystemState: "states"}[type(msg)]
    row = {**base, **{k: _cell(v) for k, v in d.items() if k not in ("seq", "t")}}
    return {name: [row]}


# 파일마다 칸(열) 순서를 고정해 둔다 → 엑셀에서 열 위치가 매번 같음
COMMON_COLS = ["seq", "t", "time_kst"]
COLUMNS = {
    "person_frames":  COMMON_COLS + ["v", "n_persons", "ok"],
    "persons":        COMMON_COLS + ["idx"] + [f.name for f in fields(Person)],
    "thermal_frames": COMMON_COLS + ["v", "ambient", "n_rois", "ok"],
    "hot_rois":       COMMON_COLS + [f.name for f in fields(HotRoi)],
    "gas":            COMMON_COLS + [f.name for f in fields(GasReading) if f.name not in ("seq", "t")],
    "states":         COMMON_COLS + [f.name for f in fields(SystemState) if f.name not in ("seq", "t")],
}


# ── CSV 기록기 ─────────────────────────────────────────
class CsvLogger:
    """실행 1번 = 폴더 1개 (data/logs/20261124_193200/). 그 안에 표 종류별 CSV 파일.

    utf-8-sig: 윈도우 엑셀에서 열었을 때 한글이 깨지지 않게 하는 인코딩.
    파일을 열어 둔 채 한 줄씩 쓰고 flush() → 프로그램이 멈춰도 앞부분은 디스크에 남는다.
    """

    def __init__(self, root="data/logs"):
        self.dir = os.path.join(root, datetime.now(KST).strftime("%Y%m%d_%H%M%S"))
        os.makedirs(self.dir, exist_ok=True)
        self._files, self._writers = {}, {}

    def _writer(self, name):
        if name not in self._writers:
            f = open(os.path.join(self.dir, f"{name}.csv"), "w", newline="", encoding="utf-8-sig")
            w = csv.DictWriter(f, fieldnames=COLUMNS[name])
            w.writeheader()                          # 첫 줄 = 열 이름
            self._files[name], self._writers[name] = f, w
        return self._writers[name]

    def write(self, msg):
        for name, rows in to_rows(msg).items():
            w = self._writer(name)                   # 목록이 비어 있어도 파일·헤더는 만들어 둔다
            for row in rows:
                w.writerow(row)
            self._files[name].flush()

    def close(self):
        for f in self._files.values():
            f.close()


# ── CSV 읽기 (분석·녹화 재생용) ────────────────────────
def read_table(log_dir, name):
    """CSV 하나를 읽어 dict 목록으로. 숫자처럼 보이는 칸은 숫자로, 빈칸은 None으로 바꾼다."""
    path = os.path.join(log_dir, f"{name}.csv")
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append({k: _parse(v) for k, v in r.items()})
    return rows


def _parse(s):
    if s == "":
        return None
    for conv in (int, float):
        try:
            return conv(s)
        except ValueError:
            pass
    return s


def load_thermal(log_dir):
    """thermal_frames.csv + hot_rois.csv 를 seq로 다시 합쳐 ThermalResult 목록으로 복원.
    (기록한 실험을 판단 로직에 똑같이 다시 넣어 보는 '녹화 재생'의 기초)"""
    rois_by_seq = {}
    for r in read_table(log_dir, "hot_rois"):
        roi = HotRoi(**{k: r[k] for k in COLUMNS["hot_rois"] if k not in COMMON_COLS})
        rois_by_seq.setdefault(r["seq"], []).append(roi)
    return [ThermalResult(hot_rois=rois_by_seq.get(fr["seq"], []), ambient=fr["ambient"],
                          ok=bool(fr["ok"]), t=fr["t"], seq=fr["seq"], v=fr["v"])
            for fr in read_table(log_dir, "thermal_frames")]


# ── 직접 실행하면 예시 로그를 만들고 다시 읽어 본다 ─────
if __name__ == "__main__":
    log = CsvLogger()
    log.write(PersonResult(persons=[Person(x=22.4, y=30.1, conf=0.91),
                                    Person(x=41.0, y=12.5, conf=0.78, lying=True)]))
    log.write(ThermalResult(hot_rois=[HotRoi(id=3, x=30.0, y=18.5, r=6.2,
                                             tmax=64.2, rate=0.8, hot_sec=12.0)],
                            ambient=23.1))
    log.write(ThermalResult(hot_rois=[], ambient=23.0))          # 위험 구역이 없는 프레임
    log.write(GasReading(raw_v=0.62, ratio=1.55, warmed_up=True))
    log.write(SystemState(level="WARNING", reasons=["HOT_RISING", "PERSON_IN_ROI"],
                          persons_in_zone=1, route=["N3", "N2", "EXIT_A"],
                          blocked_edges=["N3-N4"]))
    log.close()

    print(f"저장 폴더: {log.dir}")
    for name in sorted(os.listdir(log.dir)):
        print(f"\n── {name}")
        with open(os.path.join(log.dir, name), encoding="utf-8-sig") as f:
            print(f.read().rstrip())

    print("\n── 녹화 재생: CSV → ThermalResult 복원")
    for m in load_thermal(log.dir):
        print(" ", m)

    print("\n── 약속 위반 예시")
    try:
        SystemState(level="DANGER")
    except ValueError as e:
        print("  에러로 잡힘:", e)
