"""
backends/mock.py — テスト用の合成バックエンド（API不要）

ffmpeg で 1080x1920（9:16）のプレースホルダを生成するだけ。実際の絵は出ないが、
ハーネス全体（generate → validate → faceguard skip → 承認 → deliver）を鍵・課金・
ネットワークなしでエンドツーエンドに通せる。CI/動作確認・回帰用。

  python3 videogen/cli.py generate --backend mock --auto-approve --stage 1
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .base import Backend, GenerationError

# 段ごとに色を変えて視認しやすく（validate は寸法/尺しか見ないので中身は任意）
_TINT = {"base_face": "0x14504a", "still": "0xE8B451", "clip": "0x14110E"}


class MockBackend(Backend):
    name = "mock"
    mode = "auto"

    def available(self) -> tuple[bool, str]:
        if not shutil.which("ffmpeg"):
            return False, "ffmpeg 未導入"
        return True, "テスト用合成バックエンド（1080x1920プレースホルダ）"

    def generate(self, job: dict, output_dir: Path, *, dry_run: bool = False) -> dict:
        model = "mock:ffmpeg"
        dest = output_dir / job["output"]
        color = _TINT.get(job["kind"], "0x222222")
        if dry_run:
            return {"path": None, "tool": model, "dry_run": True,
                    "arguments": {"synth": f"{color} 1080x1920",
                                  "duration_s": job.get("duration_s")}}
        dest.parent.mkdir(parents=True, exist_ok=True)
        ff = shutil.which("ffmpeg")
        if job["kind"] == "clip":
            dur = job.get("duration_s") or 4
            cmd = [ff, "-y", "-f", "lavfi",
                   "-i", f"color=c={color}:s=1080x1920:d={dur}:r=30",
                   "-pix_fmt", "yuv420p", str(dest)]
        else:
            cmd = [ff, "-y", "-f", "lavfi",
                   "-i", f"color=c={color}:s=1080x1920", "-frames:v", "1", str(dest)]
        try:
            subprocess.run(cmd, capture_output=True, timeout=120, check=True)
        except (subprocess.SubprocessError, OSError) as e:
            raise GenerationError(f"ffmpeg 合成失敗: {e}") from e
        if not dest.exists():
            raise GenerationError("合成後にファイルが無い")
        return {"path": str(dest), "tool": model, "raw": {"url": None}}
