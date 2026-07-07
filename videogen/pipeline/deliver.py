"""
deliver.py — 完成クリップのアトミック納品（Irodori watcher の _deliver 相当）

生成物（videogen/output/*.mp4）を、DOMOAI-CHAT-BRIEF.md の納品先である
bottle-scanner-video/domoai-exports/ へ命名規則どおりにコピーする。
中間はローカルに置き、確定物だけを一時ファイル経由で os.replace で置く。

納品先は既定でリポジトリ内 bottle-scanner-video/domoai-exports/ だが、
--dest で任意に差し替え可能（フル素材は別ブランチにあるため、運用時は
そのブランチの domoai-exports/ を指す想定。デフォルトは自ブランチ内の
placeholder パスで、無ければ作成する）。
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path


def deliver_one(src: str | Path, dest_dir: str | Path) -> Path:
    src = Path(src)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    if not (src.exists() and src.stat().st_size > 0):
        raise FileNotFoundError(f"納品元が無い/空: {src}")
    final = dest_dir / src.name
    tmp = dest_dir / (src.name + ".tmp")
    shutil.copy2(src, tmp)
    os.replace(tmp, final)  # アトミック置換
    return final
