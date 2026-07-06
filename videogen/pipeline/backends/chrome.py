"""
backends/chrome.py — Chrome 操作（Web UI）バックエンド＝採用の既定

人手 or claude-in-chrome が Web UI を操作して生成する方式。自動でファイルは作らない
（それがこのバックエンドの本質）。generate が呼ばれたら「手動で作って output/ に置き、
set <id> needs_review せよ」を示す。実際の運用手順は chrome_control/PLAYBOOK.md。
"""
from __future__ import annotations

from pathlib import Path

from .base import Backend, GenerationError


class ChromeBackend(Backend):
    name = "chrome"
    mode = "manual"

    def available(self) -> tuple[bool, str]:
        return True, "手動/Chrome操作バックエンド（Web UIを人 or claude-in-chromeが操作）"

    def generate(self, job: dict, output_dir: Path, *, dry_run: bool = False) -> dict:
        raise GenerationError(
            "chrome は手動バックエンド。`cli.py show " + job["id"] + "` の指示どおり Web UI で生成し、"
            f"{output_dir}/{job['output']} に保存後、`cli.py set {job['id']} needs_review` を実行。"
            " 手順: chrome_control/PLAYBOOK.md"
        )
