"""
backends/fal_backend.py — fal.ai 自動バックエンド（任意・API化する場合）

DESIGN.md の推奨スタックを実装（モデルIDと入力スキーマは 2026-07 に fal.ai の
各 API ページで確認した実値。将来ドリフトし得るので MODELS/引数生成を一箇所に集約）:

  ① base_face (T2I)  : fal-ai/nano-banana-pro            （seed対応・架空人物OK）
  ② still    (編集)  : fal-ai/nano-banana-pro/edit       （image_urls=基準顔で顔固定）
  ③ clip     (I2V)   : fal-ai/kling-video/o1/reference-to-video（@Image参照・9:16・3-10s）

代替（swap は下の MODELS を差し替えるだけ）:
  編集 → fal-ai/bytedance/seedream/v4.5/edit（新環境配置が強い / image_urls 最大10）
  I2V  → fal-ai/minimax/... (Hailuo, 顔クロース) / Luma Ray3(Replicate)

前提: `pip install fal-client` と 環境変数 `FAL_KEY`。未導入/未設定なら available()=False。
このバックエンドは追加依存なので、入れない限りハーネス本体には影響しない。
"""
from __future__ import annotations

import os
import urllib.request
from pathlib import Path

from .base import Backend, GenerationError

# ── モデル設定（swap ポイント） ─────────────────────────────────────────────
MODELS = {
    "base_face": os.environ.get("VIDEOGEN_FAL_T2I", "fal-ai/nano-banana-pro"),
    "still": os.environ.get("VIDEOGEN_FAL_EDIT", "fal-ai/nano-banana-pro/edit"),
    "clip": os.environ.get("VIDEOGEN_FAL_I2V", "fal-ai/kling-video/o1/reference-to-video"),
}
# Nano Banana の解像度（9:16 の 2K ≒ 1152x2048。1080x1920 ちょうどではないが FCPX で調整可）
NB_RESOLUTION = os.environ.get("VIDEOGEN_FAL_RESOLUTION", "2K")


def _fal():
    """fal_client を遅延 import。無ければ None。"""
    try:
        import fal_client  # type: ignore
        return fal_client
    except Exception:
        return None


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "videogen/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
        f.write(r.read())


def _first_url(result: dict, kind: str) -> str:
    """fal の結果 dict から成果物 url を取り出す（Python client は data payload を直接返す）。"""
    if kind == "clip":
        v = result.get("video")
        if isinstance(v, dict) and v.get("url"):
            return v["url"]
    imgs = result.get("images")
    if isinstance(imgs, list) and imgs and isinstance(imgs[0], dict) and imgs[0].get("url"):
        return imgs[0]["url"]
    # 保険: video フォールバック
    v = result.get("video")
    if isinstance(v, dict) and v.get("url"):
        return v["url"]
    raise GenerationError(f"結果から url を抽出できず: keys={list(result)[:6]}")


class FalBackend(Backend):
    name = "fal"
    mode = "auto"

    def available(self) -> tuple[bool, str]:
        if _fal() is None:
            return False, "fal-client 未導入（pip install fal-client）"
        if not os.environ.get("FAL_KEY"):
            return False, "環境変数 FAL_KEY が未設定"
        return True, "fal.ai 自動バックエンド"

    # ── 引数生成（1 箇所に集約） ──────────────────────────────────────────
    def _build(self, job: dict, output_dir: Path, fal, *, dry_run: bool = False
               ) -> tuple[str, dict, list[str]]:
        kind = job["kind"]
        model = MODELS[kind]
        neg = job.get("negative", "")

        if kind == "base_face":
            prompt = job["prompt"] + (f"\n\nAvoid: {neg}" if neg else "")
            args = {
                "prompt": prompt,
                "aspect_ratio": "9:16",
                "resolution": NB_RESOLUTION,
                "num_images": 1,
                "output_format": "png",
                "seed": job.get("seed"),
            }
            return model, args, []

        # still / clip は参照画像（ローカル）をアップロードして url 化
        refs = job.get("reference_images", [])
        missing = [r for r in refs if not (output_dir / r).exists()]
        if missing and not dry_run:
            raise GenerationError(f"参照画像が output/ に無い: {missing}（依存を先に承認・生成）")
        ref_urls = [fal.upload_file(str(output_dir / r)) for r in refs]

        if kind == "still":
            prompt = (
                "Recreate this scene while keeping the person's facial identity, hair, and features "
                "IDENTICAL to the reference image(s). Scene: " + job["prompt"]
                + (f"\n\nAvoid: {neg}" if neg else "")
            )
            args = {
                "prompt": prompt,
                "image_urls": ref_urls,
                "aspect_ratio": "9:16",
                "resolution": NB_RESOLUTION,
                "num_images": 1,
                "output_format": "png",
                "seed": job.get("seed"),
            }
            return model, args, ref_urls

        if kind == "clip":
            # Kling O1: image_urls[0]=@Image1（動かす静止画）, [1..]=@Image2..（基準顔）
            ident = ""
            if len(ref_urls) > 1:
                ident = " Keep the person identical to " + ", ".join(
                    f"@Image{i+2}" for i in range(len(ref_urls) - 1)) + "."
            prompt = (
                "Animate @Image1 as a live cinematic vertical shot, same framing and same person."
                + ident + " Motion: " + job["prompt"]
            )
            dur = str(job.get("duration_s") or 5)
            if dur not in {"3", "4", "5", "6", "7", "8", "9", "10"}:
                dur = "5"
            args = {"prompt": prompt, "image_urls": ref_urls, "aspect_ratio": "9:16", "duration": dur}
            return model, args, ref_urls

        raise GenerationError(f"未対応の kind: {kind}")

    def generate(self, job: dict, output_dir: Path, *, dry_run: bool = False) -> dict:
        if dry_run:
            # 鍵・依存なしで呼び出し内容だけプレビュー
            model, args, _ = self._build(job, output_dir, _DryFal(), dry_run=True)
            preview = {k: (v if k != "image_urls" else job.get("reference_images"))
                       for k, v in args.items()}
            return {"path": None, "tool": model, "dry_run": True, "arguments": preview}

        fal = _fal()
        if fal is None:
            raise GenerationError("fal-client 未導入")
        model, args, ref_urls = self._build(job, output_dir, fal)

        # None の seed 等は落とす
        args = {k: v for k, v in args.items() if v is not None}
        try:
            result = fal.subscribe(model, arguments=args, with_logs=False)
        except Exception as e:  # noqa: BLE001
            raise GenerationError(f"fal 呼び出し失敗 [{model}]: {e}") from e

        url = _first_url(result if isinstance(result, dict) else {}, job["kind"])
        dest = output_dir / job["output"]
        _download(url, dest)
        return {"path": str(dest), "tool": model, "raw": {"url": url}}


class _DryFal:
    """dry-run 用のダミー: upload_file を呼ばずローカルパスを url 代わりに返す。"""

    def upload_file(self, path: str) -> str:  # noqa: D401
        return f"file://{path}"
