"""
faceguard.py — 顔一貫性ガード（Irodori tsuki_noise.py の映像版）

Irodori のノイズガードが「波形が発話として壊れていないか」を測って自動再生成した
のと同じ役割を、映像では「生成された顔が基準顔（キャラシート）と同一人物か」を測る。

3 段構え（tsuki_noise.py と同じ思想）:
  1. 検知: 生成物（静止画 or 動画の代表フレーム）から顔埋め込みを取り、
     基準顔の埋め込みとの cosine 類似度を測る。
  2. 判定: 類似度 < threshold なら「別人化」= 不合格。
  3. 修復は呼び出し側（cli / 運用）の責務: 別 seed / 別テイクで再生成し、
     ダメなら needs_review で人手に上げる。

依存はオプション。insightface が無ければ NULL 実装（常に skipped）で、
機械判定を飛ばして人手承認（needs_review）に回す設計。土台としては
インターフェースと運用フローを固定し、重い依存は入れたい時に入れる。

  推奨: uv pip install insightface onnxruntime opencv-python-headless
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_THRESHOLD = 0.45  # ArcFace cosine。0.4〜0.5 目安（要キャリブレーション）


@dataclass
class FaceVerdict:
    ok: bool | None          # True=同一人物 / False=別人 / None=判定不能(skipped)
    similarity: float | None
    reason: str


def _load_app():
    """insightface の FaceAnalysis を遅延ロード。無ければ None。"""
    try:
        from insightface.app import FaceAnalysis  # type: ignore
    except Exception:
        return None
    try:
        app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        app.prepare(ctx_id=-1, det_size=(640, 640))
        return app
    except Exception:
        return None


def _largest_face_embedding(app, image_path: Path):
    import numpy as np  # insightface があれば numpy もある

    try:
        import cv2  # type: ignore
        img = cv2.imread(str(image_path))
    except Exception:
        return None
    if img is None:
        return None
    faces = app.get(img)
    if not faces:
        return None
    face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    emb = face.normed_embedding
    return emb / (np.linalg.norm(emb) + 1e-9)


def _extract_frame(video_path: Path, out_png: Path, at_s: float = 0.3) -> bool:
    """動画から代表フレームを 1 枚抜く（ffmpeg）。顔チェックの入力にする。"""
    import shutil
    import subprocess
    exe = shutil.which("ffmpeg")
    if not exe:
        return False
    try:
        subprocess.run(
            [exe, "-y", "-ss", str(at_s), "-i", str(video_path),
             "-frames:v", "1", str(out_png)],
            capture_output=True, timeout=60, check=True,
        )
        return out_png.exists()
    except (subprocess.SubprocessError, OSError):
        return False


def check_identity(candidate: str | Path, reference: str | Path,
                   threshold: float = DEFAULT_THRESHOLD) -> FaceVerdict:
    """候補画像/動画が基準顔と同一人物かを判定。

    candidate が .mp4 等なら代表フレームを抜いて評価。
    insightface 未導入なら ok=None（skipped）を返し、人手承認に委ねる。
    """
    app = _load_app()
    if app is None:
        return FaceVerdict(None, None, "insightface 未導入: 機械判定スキップ（人手承認へ）")

    cand = Path(candidate)
    if cand.suffix.lower() in (".mp4", ".mov", ".webm", ".mkv"):
        frame = cand.with_suffix(".frame.png")
        if not _extract_frame(cand, frame):
            return FaceVerdict(None, None, "動画からフレーム抽出失敗")
        cand = frame

    try:
        import numpy as np
    except Exception:
        return FaceVerdict(None, None, "numpy 未導入")

    ce = _largest_face_embedding(app, cand)
    re = _largest_face_embedding(app, Path(reference))
    if ce is None or re is None:
        return FaceVerdict(None, None, "顔検出できず（構図/ボケ/複数人の可能性）")

    sim = float(np.dot(ce, re))
    ok = sim >= threshold
    return FaceVerdict(ok, sim, f"cosine={sim:.3f} {'>=' if ok else '<'} {threshold}")


def available() -> bool:
    return _load_app() is not None
