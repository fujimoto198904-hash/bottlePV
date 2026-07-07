# キックオフ ─ 開放環境のChrome操作Claudeへ（無料・Chrome操作ルート）

Bottle Scanner PV の映像生成を、**ネット開放環境**（DomoAI等に到達できる Claude Code）で
Chrome操作により回すための引き継ぎ。`bottlePV` を主に開く環境は domoai.app に到達できない（403）ため、
生成はこちらの開放環境で行い、成果物を同じリポジトリに戻す。

このシステム（`videogen/`）は Irodori 音声パイプラインの設計を流用した**ジョブ管理ハーネス**。
`09_domoai-generation-brief.md` の手順を、進捗管理・命名・検証つきで機械化したもの。

---

## ▼ 新しい開放環境チャットに貼るキックオフ文（コピペ）

```
リポジトリ https://github.com/fujimoto198904-hash/bottlePV をクローンし、
ブランチ claude/videogen-chrome-pipeline を checkout して。
videogen/README.md と videogen/chrome_control/PLAYBOOK.md の手順で、
DomoAI（私のログイン済みChrome）を claude-in-chrome で操作し、
Bottle Scanner PV の実写クリップを生成して。

進め方:
1. python3 videogen/cli.py status で全体確認
2. python3 videogen/cli.py generate --backend chrome --stage 1
   → 基準顔3枚(ケンジ/マナミ/タカシ)のプロンプトが出る
3. Web UIで生成(9:16 / Realistic / 顔くっきり) → videogen/output/base_kenji.png 等に保存
4. python3 videogen/cli.py validate <id> で寸法確認 → set <id> approved
5. ★まず基準顔3枚を私に見せて「この顔で確定」を取ってから ②③へ(手戻り防止)
6. ②状況静止画(編集で顔固定, 9:16) → ③クリップ(I2V, Motion Low〜Mid, 3〜5秒)
   各段 generate --backend chrome --stage {2|3} でプロンプト取得
7. python3 videogen/cli.py deliver --kinds base_face,still,clip
   → bottle-scanner-video/domoai-exports/ に納品して commit & push
   (このブランチに。claude/pv-assets-subtitles-altversions / PR #1 には触らない)

注意: DomoAIのToSはbot自動化・スクレイピングを禁止。半自動で丁寧に1件ずつ、
機械的連打・多重アカウント・無料枠の濫用はしない。心配な操作は人が実行。
全プロンプトは videogen/chrome_control/all-prompts.md に一覧あり。
```

---

## オペレータ手順（詳細）

### 0. 準備
```bash
git clone https://github.com/fujimoto198904-hash/bottlePV
cd bottlePV
git checkout claude/videogen-chrome-pipeline
python3 videogen/cli.py status    # 21ジョブ(基準顔3+静止画9+クリップ9)
```

### 1. 生成ループ（1ジョブ）
```bash
python3 videogen/cli.py generate --backend chrome --stage 1   # 次にやるジョブのプロンプト
# （or 個別に: python3 videogen/cli.py show base_kenji）
```
→ 出たプロンプトを Web UI に貼って生成（**9:16 / Realistic**）。
→ 生成物を **`videogen/output/<出力名>`** に保存（出力名はブロック表示のとおり厳密に）。
```bash
python3 videogen/cli.py validate  <id>    # 縦型9:16・尺の機械チェック
python3 videogen/cli.py faceguard <id>    # 顔一貫性(insightface無ければskip=人手判断)
python3 videogen/cli.py set <id> approved # OKなら承認 / NGは failed で作り直し
```

### 2. 段の進め方
- **① 基準顔3枚 → 承認 → 制作者に見せて確定**（ここが一貫性の全て）
- ①が approved になると **② 状況静止画** が `generate --stage 2` に出る（基準顔を参照に、同じ顔で場面へ）
- ②が approved になると **③ クリップ** が出る（承認静止画を I2V、Motion Low〜Mid、3〜5秒）
- `status` で常に全体像。凡例: ・pending ?needs_review ✓approved ★done ✗failed

### 3. 納品
```bash
python3 videogen/cli.py deliver --kinds base_face,still,clip   # domoai-exports/へ
git add bottle-scanner-video/domoai-exports/
git commit -m "domoai-exports: 生成クリップ納品"
git push
```

### 参照
- 詳細フロー: [PLAYBOOK.md](PLAYBOOK.md)（Chrome操作・claude-in-chromeの型・トラブル対処）
- DomoAI固有: [domoai.md](domoai.md)
- 全プロンプト一覧: [all-prompts.md](all-prompts.md)
- 設計/一貫性戦略/リスク: [../DESIGN.md](../DESIGN.md)

> AR枠・通知トースト・CTAは生成しない（FCPXで `assets/*.svg` を重ねる）。SHOT07はスマホ画面にUI用の余白を残す。
