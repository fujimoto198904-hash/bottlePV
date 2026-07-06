"""backends — 差し替え可能な生成バックエンド（chrome=手動 / fal=自動）。"""
from __future__ import annotations

from .base import Backend, GenerationError  # noqa: F401
from .chrome import ChromeBackend
from .fal_backend import FalBackend

_REGISTRY = {
    "chrome": ChromeBackend,
    "fal": FalBackend,
}


def get_backend(name: str) -> Backend:
    cls = _REGISTRY.get(name)
    if cls is None:
        raise KeyError(f"未知のバックエンド: {name}（{', '.join(_REGISTRY)}）")
    return cls()


def names() -> list[str]:
    return list(_REGISTRY)
