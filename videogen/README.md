# videogen ― Bottle Scanner PV 映像生成ハーネス

Bottle Scanner PV（35秒・9:16・実写シネマティック）の **映像クリップ生成** を回すための
自己完結パイプライン。音声側の **Irodori-TTS** で実証済みのオーケストレーション設計
（watcher → manifest → generate → 品質ガード → 納品）を**そのまま映像に写した**もの。

> **このシステムが担当するのは映像素材（`base_*.png` / `still_SHOT*.png` / `SHOT*.mp4`）の
> 生成・管理・検証・納品だけ。** 声(Irodori)・SE/BGM・字幕・AR枠・CTA・FCPX最終合成は担当外。

---

## なぜこの形か（結論だけ）

| 検討案 | 判定 |
|---|---|
| (a) Irodori本体を改造して映像も出す | **却下**。Irodoriは音声コーデック潜在のRF-DiT。映像とは別モデルクラスで転用不可 |
| (b) Irodoriの**ハーネス設計を流用**した新システム | **採用**。再利用価値はモデルでなく運用設計（manifest/決定的seed/品質ガード/納品） |
| (c) 画像/動画生成の外部バックエンドを叩く | **採用**。生成の中身は差し替え可能なバックエンドに分離 |

→ **(b)＋(c)のハイブリッド**。この`videogen/`が(b)、生成バックエンドが(c)。
詳細な意思決定記録は [DESIGN.md](DESIGN.md)。

### 生成バックエンド：**Chrome操作**（採用）
ログイン済みのChromeでWeb UI（DomoAI等）を操作して生成する方式。API課金なしで
既存アカウントを使える。**ハーネス（このコード）はバックエンド非依存**なので、将来
API（fal.ai等）へ差し替えても manifest / 検証 / 納品はそのまま使える。

> ⚠️ **注意（既知のトレードオフ）**：DomoAIの利用規約はbot/スクリプトによる自動操作・
> スクレイピングを禁止しており、Web UI自動操作はBANリスク・不安定性がある。かつ
> DomoAIの公式APIは**動画専用**でT2I・画像編集・顔固定を持たない。運用はこの前提を
> 理解した上で行うこと（→ [DESIGN.md](DESIGN.md) のリスク節、[chrome_control/PLAYBOOK.md](chrome_control/PLAYBOOK.md)）。

---

## 生成の3段（Irodoriの build→generate→stitch の映像版）

```
① 基準顔 T2I         base_{kenji,manami,takashi}.png   ← キャラ一貫性の“源”。人手で顔を確定
        │  (承認した顔を参照として固定)
        ▼
② 状況静止画 編集     still_SHOT01..09.png (9:16)        ← 同じ顔のままBar背景/ポーズ/表情へ
        │  (各静止画を人手承認 = 一貫性の最後の完全制御点)
        ▼
③ I2V クリップ        SHOT01..09_{slug}.mp4 (9:16/3–5s)  ← 承認静止画を動かす
        │  (顔ガードで別人化を検知 → 再生成)
        ▼
     output/ → 納品 → bottle-scanner-video/domoai-exports/
```

**キャラ一貫性は“動画”でなく“静止画”段で解く**のが最重要設計。どの動画モデルも
別生成をまたいで顔を覚えていない。基準顔を凍結し、各静止画に参照として渡し、
人手承認してからアニメ化する。詳細は [DESIGN.md](DESIGN.md#一貫性戦略)。

---

## クイックスタート

```bash
# 依存: システム python3 のみで動く（顔ガードだけ任意で insightface）
python3 videogen/cli.py build      # ジョブグラフ → manifest.json（21ジョブ）
python3 videogen/cli.py status     # 進捗ボード＋次に着手できるジョブ
python3 videogen/cli.py next       # 次ジョブの貼り付け用プロンプトを表示
```

**運用ループ（1ジョブ）**
1. `python3 videogen/cli.py next` で次ジョブのプロンプトを取得
2. Chrome操作でWeb UIに貼って生成（手順 → [chrome_control/PLAYBOOK.md](chrome_control/PLAYBOOK.md)）
3. 生成物を `videogen/output/<出力名>` に保存（命名は show が表示するとおり）
4. `python3 videogen/cli.py validate <id>`（9:16/尺チェック）
5. `python3 videogen/cli.py faceguard <id>`（顔一貫性。insightface未導入ならスキップ→人手判断）
6. OKなら `python3 videogen/cli.py set <id> approved`（NGは `failed` → 別seed/テイクで再生成）
7. base/still を approved にすると、依存する次段が `next` に出る
8. クリップが揃ったら `python3 videogen/cli.py deliver`

---

## コマンド一覧

| コマンド | 役割 |
|---|---|
| `build [--overwrite]` | ジョブグラフ→manifest構築/更新（手編集ステータスは既定で引き継ぐ） |
| `status` | 段別の進捗ボードと次に着手できるジョブ |
| `next [--limit N]` | 依存が満たされ次に生成すべきジョブの貼り付けブロック |
| `show <id>` | 1ジョブのプロンプト/参照/出力名/seed |
| `generate --backend {chrome,fal} [--id/--stage/--dry-run/--auto-approve]` | 生成実行（chrome=指示出し / fal=自動生成+検証+顔ガード+リトライ） |
| `set <id> <status>` | ステータス更新（pending/generating/needs_review/approved/done/failed） |
| `validate [id]` | output/ の成果物を機械検証（縦型9:16・尺） |
| `faceguard <id>` | 生成物と基準顔の顔一貫性（cosine類似度、要insightface） |
| `deliver [--dest DIR]` | approvedクリップを domoai-exports/ へアトミック納品 |

### 生成バックエンド（差し替え可能）
- **`chrome`（既定・採用）**: 手動/claude-in-chrome で Web UI を操作。`generate --backend chrome` は
  対象ジョブの貼り付けブロックを出すだけ（実生成は人/ブラウザ）。手順 → [chrome_control/PLAYBOOK.md](chrome_control/PLAYBOOK.md)。
- **`fal`（任意・API化）**: `pip install fal-client` ＋ `export FAL_KEY=...` で自動生成。
  Nano Banana Pro（①基準顔／②編集で顔固定）→ Kling O1 Reference（③I2V）。
  鍵なしでも `--dry-run` で送信内容を確認できる:
  ```bash
  python3 videogen/cli.py generate --backend fal --dry-run --id still_SHOT01
  python3 videogen/cli.py generate --backend fal --auto-approve --stage 1   # 実行（要FAL_KEY）
  ```
  モデルは `pipeline/backends/fal_backend.py` の `MODELS` か環境変数で差し替え可
  （例 `VIDEOGEN_FAL_EDIT=fal-ai/bytedance/seedream/v4.5/edit`）。

---

## ファイル構成

```
videogen/
├── README.md              このファイル
├── DESIGN.md              a/b/c 意思決定記録・ハーネス対応・リスク
├── cli.py                 操作入口（司令塔）
├── manifest.json          生成される全ジョブ状態（build で作成）
├── requirements.txt       任意依存（顔ガード用）
├── pipeline/
│   ├── jobs.py            ジョブグラフ（3顔+9静止画+9クリップ、プロンプト埋め込み）
│   ├── manifest.py        決定的seed・キャッシュ・状態管理（Irodori manifest の映像版）
│   ├── validate.py        ffprobeで9:16/尺を検証
│   ├── faceguard.py       顔一貫性ガード（Irodori tsuki_noise の映像版）
│   ├── deliver.py         アトミック納品
│   └── backends/          差し替え可能な生成バックエンド
│       ├── chrome.py      手動/Chrome操作（既定）
│       └── fal_backend.py fal.ai 自動生成（任意・Nano Banana Pro→Kling O1）
├── chrome_control/
│   ├── PLAYBOOK.md        Chrome操作の運用手順（採用バックエンド）
│   └── domoai.md          DomoAI Web UI 固有のフロー
└── output/                生成物の一時置き場（gitignore、確定物のみ納品へ）
```

## 完了条件（DOMOAI-CHAT-BRIEF.md 準拠）
- [ ] 基準顔3枚（確定済み）
- [ ] SHOT01〜09 の状況静止画9枚
- [ ] SHOT01〜09 の完成クリップ9本（9:16・キャラ一貫・崩れなし）
- [ ] すべて `domoai-exports/` に納品済み
