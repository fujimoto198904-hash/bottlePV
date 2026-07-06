#!/usr/bin/env python3
"""
cli.py — Bottle Scanner PV 映像生成ハーネスの操作入口

Irodori(tsuki_narrate.py) の CLI 思想をそのまま映像に写した司令塔。
Chrome 操作でも将来の API 化でも共通で使える「ジョブ管理・検証・納品」層。

使い方（uv 不要・システム python3 で動く / 顔ガードのみ任意依存）:

    python3 videogen/cli.py build           # ジョブグラフ → manifest.json を構築/更新
    python3 videogen/cli.py status          # 進捗ボード（段別・次に着手できるジョブ）
    python3 videogen/cli.py next             # 依存が満たされ次に生成すべきジョブを表示
    python3 videogen/cli.py show still_SHOT01 # 1 ジョブの貼り付け用ブロック（プロンプト等）
    python3 videogen/cli.py set  still_SHOT01 approved   # ステータス更新
    python3 videogen/cli.py validate         # output/ の成果物を機械検証（9:16/尺）
    python3 videogen/cli.py faceguard clip_SHOT02        # 顔一貫性チェック（要 insightface）
    python3 videogen/cli.py deliver          # approved クリップを domoai-exports/ へ納品

ステータス遷移（運用）:
    pending → (生成) → needs_review → (顔OK & 目視OK) → approved → (納品) → done
    ダメなら failed。base/still が approved になると、依存する次段が next に出る。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# videogen/ を import path に載せる（どこから呼んでも動くように）
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from pipeline import backends as backends_mod  # noqa: E402
from pipeline import deliver as deliver_mod  # noqa: E402
from pipeline import faceguard as fg  # noqa: E402
from pipeline import manifest as mani  # noqa: E402
from pipeline import validate as val  # noqa: E402
from pipeline.backends import GenerationError  # noqa: E402

MANIFEST = ROOT / "manifest.json"
OUTPUT_DIR = ROOT / "output"
# 既定の納品先（フル素材は別ブランチのため、運用時は --dest で上書き推奨）
DEFAULT_DEST = ROOT.parent / "bottle-scanner-video" / "domoai-exports"

STAGE_NAME = {1: "① 基準顔(T2I)", 2: "② 状況静止画(編集)", 3: "③ クリップ(I2V)"}
STATUS_MARK = {
    "pending": "・", "generating": "▷", "needs_review": "?",
    "approved": "✓", "done": "★", "failed": "✗",
}


def _rows() -> list[dict]:
    if not MANIFEST.exists():
        print("manifest.json が無い。まず `build` を実行。", file=sys.stderr)
        sys.exit(2)
    return mani.load(MANIFEST)


def cmd_build(args) -> None:
    rows = mani.build(MANIFEST, overwrite=args.overwrite)
    n = {"base_face": 0, "still": 0, "clip": 0}
    for r in rows:
        n[r["kind"]] += 1
    print(f"built {MANIFEST.relative_to(ROOT.parent)} — "
          f"base {n['base_face']} / still {n['still']} / clip {n['clip']} = {len(rows)} jobs")


def cmd_status(args) -> None:
    rows = _rows()
    print(f"\n進捗ボード（{MANIFEST.name}）")
    for stage in (1, 2, 3):
        srows = [r for r in rows if r["stage"] == stage]
        line = "  ".join(f"{STATUS_MARK[r['status']]}{r['id'].replace('base_','').replace('_SHOT','·S').replace('clip','C').replace('still','s')}"
                         for r in srows)
        counts: dict[str, int] = {}
        for r in srows:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        summary = " ".join(f"{k}:{v}" for k, v in counts.items())
        print(f"\n {STAGE_NAME[stage]}  [{summary}]")
        print(f"   {line}")
    ready = mani.ready_jobs(rows)
    print(f"\n凡例: {' '.join(f'{m}={s}' for s, m in STATUS_MARK.items())}")
    if ready:
        print(f"\n▶ 次に着手できるジョブ {len(ready)} 件: " + ", ".join(r["id"] for r in ready))
        print("  → `python3 videogen/cli.py show <id>` で貼り付け用プロンプトを表示")
    else:
        undone = [r for r in rows if r["status"] not in ("done",)]
        if not undone:
            print("\n🎉 全ジョブ done。")
        else:
            print("\n（次に自動で着手できるジョブなし。needs_review を承認すると次段が開く）")
    print()


def _paste_block(r: dict) -> str:
    refs = r.get("reference_images") or []
    ref_line = ("参照画像(一貫性): " + ", ".join(refs)) if refs else "参照画像: なし（T2Iで顔を決める）"
    lines = [
        "─" * 70,
        f"[{r['id']}]  {STAGE_NAME[r['stage']]}   status={r['status']}  seed={r.get('seed')}",
        f"出力名   : {r['output']}   ({r['aspect_ratio']}"
        + (f", {r['duration_s']}s" if r.get("duration_s") else "") + ")",
        f"概要     : {r.get('label','')}",
        ref_line,
        "─" * 70,
        "PROMPT ↓（そのままコピペ）",
        r["prompt"],
    ]
    if r.get("negative"):
        lines += ["", "NEGATIVE ↓", r["negative"]]
    lines += ["─" * 70]
    return "\n".join(lines)


def cmd_show(args) -> None:
    rows = _rows()
    hit = next((r for r in rows if r["id"] == args.job_id), None)
    if not hit:
        print(f"ジョブが無い: {args.job_id}", file=sys.stderr)
        sys.exit(2)
    print(_paste_block(hit))


def cmd_next(args) -> None:
    rows = _rows()
    ready = mani.ready_jobs(rows)
    if not ready:
        print("次に着手できる pending ジョブはなし（needs_review を承認すると次段が開く）。")
        return
    for r in ready[: args.limit]:
        print(_paste_block(r))
        print()


def cmd_set(args) -> None:
    if args.status not in mani.STATUSES:
        print(f"status は {mani.STATUSES} のいずれか", file=sys.stderr)
        sys.exit(2)
    mani.update(MANIFEST, args.job_id, status=args.status)
    print(f"{args.job_id} → {args.status}")


def cmd_validate(args) -> None:
    rows = _rows()
    targets = [r for r in rows if (not args.job_id or r["id"] == args.job_id)]
    if args.job_id and not targets:
        print(f"ジョブが無い: {args.job_id}", file=sys.stderr)
        sys.exit(2)
    any_bad = False
    checked = 0
    for r in targets:
        out = OUTPUT_DIR / r["output"]
        if not out.exists():
            continue  # 未生成はスキップ（status で見える）
        checked += 1
        ok, problems = val.check(r, OUTPUT_DIR)
        mark = "✓" if ok else "✗"
        print(f"{mark} {r['id']:16} {r['output']}")
        for p in problems:
            print(f"      - {p}")
        any_bad = any_bad or not ok
    if checked == 0:
        print("（検証対象の成果物が output/ に未配置）")
    sys.exit(1 if any_bad else 0)


def cmd_faceguard(args) -> None:
    rows = _rows()
    hit = next((r for r in rows if r["id"] == args.job_id), None)
    if not hit:
        print(f"ジョブが無い: {args.job_id}", file=sys.stderr)
        sys.exit(2)
    if hit["kind"] == "base_face":
        print("base_face は基準そのものなので顔ガード対象外。")
        return
    cand = OUTPUT_DIR / hit["output"]
    if not cand.exists():
        print(f"成果物が未生成: {cand}", file=sys.stderr)
        sys.exit(2)
    ref = OUTPUT_DIR / f"base_{hit['character']}.png"
    if not ref.exists():
        print(f"基準顔が無い: {ref}（先に base_{hit['character']} を承認・配置）", file=sys.stderr)
        sys.exit(2)
    v = fg.check_identity(cand, ref)
    tag = {True: "OK 同一人物", False: "NG 別人化", None: "SKIP 判定不能"}[v.ok]
    print(f"[{hit['id']}] {tag} — {v.reason}")
    if v.ok is None:
        print("  → insightface 未導入 or 顔検出不可。人手で needs_review 承認を。")
        print("     導入: uv pip install insightface onnxruntime opencv-python-headless")


def _run_faceguard(job: dict, path: str):
    """still/clip の顔一貫性チェック。base_face や基準顔欠落なら None。"""
    if job["kind"] not in ("still", "clip"):
        return None
    ref = OUTPUT_DIR / f"base_{job['character']}.png"
    if not ref.exists():
        return None
    return fg.check_identity(path, ref)


def cmd_generate(args) -> None:
    rows = _rows()
    try:
        backend = backends_mod.get_backend(args.backend)
    except KeyError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    ok, why = backend.available()
    print(f"backend={backend.name} ({backend.mode}) — {why}")
    if not ok and not args.dry_run:
        print("→ 利用不可。依存導入/鍵設定の上で再実行、または --backend chrome を使う。", file=sys.stderr)
        sys.exit(2)

    # 対象選定
    if args.id:
        targets = [r for r in rows if r["id"] == args.id]
        if not targets:
            print(f"ジョブが無い: {args.id}", file=sys.stderr)
            sys.exit(2)
    else:
        targets = mani.ready_jobs(rows)
        if args.stage:
            targets = [r for r in targets if r["stage"] == args.stage]
        targets = targets[: args.limit]
    if not targets:
        print("対象ジョブなし（依存待ち or 全完了）。`status` で確認。")
        return

    # 手動バックエンド: 指示を出すだけ
    if backend.mode == "manual":
        print(f"\n▼ 手動生成する {len(targets)} 件（Web UIで生成→output/へ保存→`set <id> needs_review`）\n")
        for r in targets:
            print(_paste_block(r))
            print()
        print("手順詳細: videogen/chrome_control/PLAYBOOK.md")
        return

    # 自動バックエンド（fal 等）: 生成→検証→顔ガード→リトライ
    for r in targets:
        print(f"\n=== {r['id']} ({r['output']}) ===")
        base_seed = r.get("seed") or 0
        for attempt in range(1, args.max_retries + 1):
            job = dict(r, seed=base_seed + (attempt - 1))  # リトライで別テイク
            if not args.dry_run:
                mani.update(MANIFEST, r["id"], status="generating", attempts=attempt)
            try:
                res = backend.generate(job, OUTPUT_DIR, dry_run=args.dry_run)
            except GenerationError as e:
                print(f"  attempt {attempt}: 失敗 — {e}")
                if attempt >= args.max_retries and not args.dry_run:
                    mani.update(MANIFEST, r["id"], status="failed",
                                notes=f"生成失敗: {e}")
                continue

            if args.dry_run:
                print(f"  [dry-run] model={res['tool']}")
                print(f"  args={res.get('arguments')}")
                break

            ok_v, problems = val.check(r, OUTPUT_DIR)
            fv = _run_faceguard(r, res["path"])
            fv_txt = "" if fv is None else f" / face:{ {True:'OK',False:'NG',None:'skip'}[fv.ok] }({fv.similarity})"
            print(f"  attempt {attempt}: 生成OK [{res['tool']}] valid={'OK' if ok_v else 'NG'}{fv_txt}")
            for p in problems:
                print(f"      - {p}")

            hard_bad = not ok_v
            face_bad = fv is not None and fv.ok is False
            if (hard_bad or face_bad) and attempt < args.max_retries:
                print("      → 再生成（別seed/テイク）")
                continue

            # 確定
            result = {"url": res.get("raw", {}).get("url"), "tool": res["tool"],
                      "used_seed": job["seed"], "face_similarity": (fv.similarity if fv else None)}
            if args.auto_approve and ok_v and (fv is None or fv.ok is not False):
                status = "approved"
            else:
                status = "needs_review"
            note = ""
            if face_bad:
                note = f"顔ガードNG({fv.similarity}) 人手確認要"
            elif hard_bad:
                note = "検証NG 人手確認要"
            mani.update(MANIFEST, r["id"], status=status, result=result,
                        seed=job["seed"], notes=note)
            print(f"  → {status}" + (f"（{note}）" if note else ""))
            break
    print("\n完了。`status` で確認、承認は `set <id> approved`、納品は `deliver`。")


def cmd_deliver(args) -> None:
    rows = _rows()
    dest = Path(args.dest) if args.dest else DEFAULT_DEST
    approved_clips = [r for r in rows if r["kind"] == "clip" and r["status"] == "approved"]
    if not approved_clips:
        print("納品対象（approved なクリップ）なし。")
        return
    for r in approved_clips:
        src = OUTPUT_DIR / r["output"]
        try:
            final = deliver_mod.deliver_one(src, dest)
        except FileNotFoundError as e:
            print(f"✗ {r['id']}: {e}")
            continue
        mani.update(MANIFEST, r["id"], status="done")
        print(f"★ {r['id']} → {final}")
    print(f"\n納品先: {dest}")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="videogen", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="ジョブグラフ→manifest 構築/更新")
    b.add_argument("--overwrite", action="store_true", help="手編集を捨てて全再構築")
    b.set_defaults(func=cmd_build)

    sub.add_parser("status", help="進捗ボード").set_defaults(func=cmd_status)

    n = sub.add_parser("next", help="次に着手できるジョブを表示")
    n.add_argument("--limit", type=int, default=3)
    n.set_defaults(func=cmd_next)

    sh = sub.add_parser("show", help="1 ジョブの貼り付け用ブロック")
    sh.add_argument("job_id")
    sh.set_defaults(func=cmd_show)

    st = sub.add_parser("set", help="ステータス更新")
    st.add_argument("job_id")
    st.add_argument("status")
    st.set_defaults(func=cmd_set)

    v = sub.add_parser("validate", help="成果物の機械検証(9:16/尺)")
    v.add_argument("job_id", nargs="?")
    v.set_defaults(func=cmd_validate)

    f = sub.add_parser("faceguard", help="顔一貫性チェック")
    f.add_argument("job_id")
    f.set_defaults(func=cmd_faceguard)

    g = sub.add_parser("generate", help="生成を実行（chrome=指示出し / fal=自動生成）")
    g.add_argument("--backend", default="chrome", choices=backends_mod.names(),
                   help="生成バックエンド（既定 chrome=手動）")
    g.add_argument("--id", help="特定ジョブのみ（省略時は次に着手できるジョブ）")
    g.add_argument("--stage", type=int, choices=(1, 2, 3), help="この段のみ")
    g.add_argument("--limit", type=int, default=3, help="自動対象の最大件数")
    g.add_argument("--max-retries", type=int, default=3, dest="max_retries",
                   help="1ジョブの再生成上限（顔NG/検証NG時）")
    g.add_argument("--auto-approve", action="store_true",
                   help="検証OK&顔ガードNGでなければ approved にする（既定は needs_review）")
    g.add_argument("--dry-run", action="store_true", help="呼び出す内容だけ表示（鍵不要）")
    g.set_defaults(func=cmd_generate)

    d = sub.add_parser("deliver", help="approved クリップを納品")
    d.add_argument("--dest", help="納品先（既定: bottle-scanner-video/domoai-exports/）")
    d.set_defaults(func=cmd_deliver)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
