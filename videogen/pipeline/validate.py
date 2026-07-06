"""
validate.py — 生成物の機械的検証（ffprobe ベース、stdlib + ffmpeg のみ）

「一部 API/UI がアスペクトを黙って変える（Veo が 16:9 強制、DomoAI 既定 1:1）」
という調査で挙がったリスクへの安価なガード。静止画・動画それぞれ:
  * 解像度が縦型 9:16 か（既定 1080x1920、許容は 9:16 比率）
  * 動画は尺が想定どおりか（±0.75s 許容）

これは「顔一貫性ガード（faceguard.py）」とは別レイヤーの構文チェック。
Irodori の stitch 前チェック（SR/長さ検証）に対応する。
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

TARGET_W, TARGET_H = 1080, 1920
RATIO = 9 / 16
RATIO_TOL = 0.02
DURATION_TOL_S = 0.75


def _ffprobe(path: Path) -> dict | None:
    exe = shutil.which("ffprobe")
    if not exe:
        return None
    try:
        out = subprocess.run(
            [exe, "-v", "error", "-print_format", "json",
             "-show_streams", "-show_format", str(path)],
            capture_output=True, text=True, timeout=30, check=True,
        ).stdout
        return json.loads(out)
    except (subprocess.SubprocessError, json.JSONDecodeError, OSError):
        return None


def probe(path: str | Path) -> dict:
    """{'exists','width','height','duration_s','kind'} を返す（ffprobe 無しでも exists は返す）。"""
    p = Path(path)
    info: dict = {"exists": p.exists() and p.stat().st_size > 0, "width": None,
                  "height": None, "duration_s": None, "kind": None}
    if not info["exists"]:
        return info
    meta = _ffprobe(p)
    if not meta:
        return info
    v = next((s for s in meta.get("streams", []) if s.get("codec_type") == "video"), None)
    if v:
        info["width"] = v.get("width")
        info["height"] = v.get("height")
        info["kind"] = "video" if v.get("avg_frame_rate", "0/0") not in ("0/0", "1/1") \
            and meta.get("format", {}).get("duration") else "image"
    dur = meta.get("format", {}).get("duration")
    if dur:
        try:
            info["duration_s"] = float(dur)
        except ValueError:
            pass
    return info


def check(job: dict, output_dir: str | Path) -> tuple[bool, list[str]]:
    """ジョブの成果物を検証。(ok, [問題点]) を返す。"""
    path = Path(output_dir) / job["output"]
    problems: list[str] = []
    info = probe(path)

    if not info["exists"]:
        return False, [f"missing or empty: {path.name}"]

    w, h = info["width"], info["height"]
    if w and h:
        if h <= w:
            problems.append(f"not vertical: {w}x{h}（9:16 縦型が必要）")
        else:
            r = w / h
            if abs(r - RATIO) > RATIO_TOL:
                problems.append(f"aspect off: {w}x{h}（比 {r:.3f} ≠ 0.5625）")
            if (w, h) != (TARGET_W, TARGET_H):
                problems.append(f"note: {w}x{h}（推奨 {TARGET_W}x{TARGET_H}、FCPXで拡縮可）")
    else:
        problems.append("dimensions unknown（ffprobe 不可）")

    if job["kind"] == "clip":
        want = job.get("duration_s")
        got = info["duration_s"]
        if want and got is not None and abs(got - want) > DURATION_TOL_S:
            problems.append(f"duration off: {got:.1f}s（想定 {want}s、FCPXでトリム）")

    # "note:" だけなら合格扱い（警告）。それ以外の問題があれば不合格。
    hard = [p for p in problems if not p.startswith("note:")]
    return (len(hard) == 0), problems
