"""
backends/base.py — 生成バックエンドの共通インターフェース

ハーネス（manifest / 検証 / 顔ガード / 納品）はバックエンド非依存。
各バックエンドは 1 ジョブを受け取り、成果物を output/<出力名> に落として結果を返す
（or 手動バックエンドは「人が Web UI で作る」ことを示す）だけを担う。

mode:
  "manual" … Chrome 操作など人手介在（generate は指示を出すだけ）
  "auto"   … API 等で自動生成（generate が実ファイルを作る）
"""
from __future__ import annotations

from pathlib import Path


class GenerationError(Exception):
    """生成の失敗（呼び出し側はリトライ or needs_review に落とす）。"""


class Backend:
    name = "base"
    mode = "manual"

    def available(self) -> tuple[bool, str]:
        """(利用可能か, 説明/理由)。auto バックエンドは鍵・依存の有無をここで判定。"""
        return True, ""

    def generate(self, job: dict, output_dir: Path, *, dry_run: bool = False) -> dict:
        """1 ジョブを生成。成功時 {"path","tool","raw"} を返す。失敗時 GenerationError。

        auto バックエンドのみ実装。manual バックエンドは呼ばれたら GenerationError で
        「手動で作れ」を示す。
        """
        raise NotImplementedError
