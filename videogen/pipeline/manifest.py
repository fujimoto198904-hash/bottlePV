"""
manifest.py — 映像生成ジョブの状態管理（Irodori manifest.jsonl の映像版）

Irodori の設計思想をそのまま踏襲:
  * 決定的シード: ジョブ id から sha1 で安定採番（同じ id なら毎回同じ seed）。
  * キャッシュ判定: prompt / negative / 参照 / 尺 / aspect の sha1 = job_hash。
    値が変わったジョブだけ stale（再生成対象）になる。手編集した status は維持。
  * アトミック書き込み: temp → os.replace。

manifest は 1 個の JSON（ジョブ配列）。stdlib のみ。
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from . import jobs as jobsmod

# 生成ライフサイクル（Chrome 操作でも API でも共通）
STATUSES = (
    "pending",       # 未着手
    "generating",    # 生成投入中
    "needs_review",  # 生成済み・人手承認待ち（顔一貫性チェック前後）
    "approved",      # 承認済み（次段へ進んでよい）
    "done",          # 最終成果物として確定
    "failed",        # 規定回数リトライしても不可
)

# job_hash に含めるキー（これが変わると stale = 要再生成）
_HASH_KEYS = ("prompt", "negative", "reference_images", "duration_s", "aspect_ratio")


def _sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def derived_seed(job_id: str) -> int:
    """ジョブ id から決定的に seed を導出（Irodori derived_seed と同方式）。

    id が同じなら常に同じ seed。参照機能を持つツール（Kling 等）に渡すと
    同一キャラの再現性が上がる。seed 非対応ツール（DomoAI I2V）では単なる記録。
    """
    return int(_sha1(job_id)[:16], 16) & ((1 << 63) - 1)


def job_hash(job: dict) -> str:
    payload = json.dumps({k: job.get(k) for k in _HASH_KEYS}, ensure_ascii=False, sort_keys=True)
    return _sha1(payload)[:12]


def build(manifest_path: str | Path, *, overwrite: bool = False) -> list[dict]:
    """ジョブグラフから manifest を（再）構築。既存の手編集ステータスは引き継ぐ。

    - 新規ジョブ: status=pending, seed=決定的採番。
    - 既存ジョブ: job_hash が一致すれば status / seed / notes / result を維持。
      job_hash が変われば stale とみなし status=pending に戻す（成果物は作り直し）。
    - overwrite=True で手編集を捨てて全再構築。
    """
    manifest_path = Path(manifest_path)
    prev: dict[str, dict] = {}
    if manifest_path.exists() and not overwrite:
        for row in _load_rows(manifest_path):
            prev[row["id"]] = row

    rows: list[dict] = []
    for job in jobsmod.build_job_graph():
        jid = job["id"]
        h = job_hash(job)
        row = dict(job)  # 不変設計データをコピー
        row["job_hash"] = h
        row["seed"] = derived_seed(jid)

        old = prev.get(jid)
        if old and old.get("job_hash") == h and not overwrite:
            # 手編集を尊重して引き継ぐ
            row["status"] = old.get("status", "pending")
            row["notes"] = old.get("notes", "")
            row["result"] = old.get("result", {})
            row["attempts"] = old.get("attempts", 0)
            if old.get("seed") is not None:
                row["seed"] = old["seed"]  # 承認済みの seed を保持
        else:
            # 新規 or 内容変更 → 作り直し対象
            row["status"] = "pending"
            row["notes"] = old.get("notes", "") if old else ""
            row["result"] = {}   # {"path":..., "width":..., "height":..., "duration_s":..., "tool":...}
            row["attempts"] = 0
        rows.append(row)

    save(manifest_path, rows)
    return rows


def _load_rows(manifest_path: str | Path) -> list[dict]:
    data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    return data["jobs"] if isinstance(data, dict) else data


def load(manifest_path: str | Path) -> list[dict]:
    return _load_rows(manifest_path)


def save(manifest_path: str | Path, rows: list[dict]) -> None:
    manifest_path = Path(manifest_path)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    doc = {"version": 1, "jobs": rows}
    tmp = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, manifest_path)


def update(manifest_path: str | Path, job_id: str, **fields) -> dict:
    """1 ジョブのフィールドを更新して保存（status / seed / notes / result / attempts）。"""
    rows = load(manifest_path)
    hit = None
    for row in rows:
        if row["id"] == job_id:
            row.update(fields)
            hit = row
            break
    if hit is None:
        raise KeyError(f"job not found: {job_id}")
    save(manifest_path, rows)
    return hit


def ready_jobs(rows: list[dict]) -> list[dict]:
    """依存が満たされ（依存先が approved/done）、まだ pending なジョブ = 次に着手できるもの。"""
    by_id = {r["id"]: r for r in rows}
    out = []
    for r in rows:
        if r["status"] != "pending":
            continue
        deps = r.get("depends_on", [])
        if all(by_id.get(d, {}).get("status") in ("approved", "done") for d in deps):
            out.append(r)
    return out
