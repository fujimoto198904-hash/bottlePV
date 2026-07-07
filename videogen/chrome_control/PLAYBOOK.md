# Chrome操作プレイブック（採用バックエンド）

ログイン済みChromeのWeb UIを操作して映像を生成するときの運用手順。
人が手で操作しても、ブラウザ操作可能なClaudeセッション（`claude-in-chrome` MCP）が
半自動で回しても、同じフローで動くように設計している。

> **前提と注意**
> - このセッション（bottlePVを主に開く環境）は**ネットワークが絞られており domoai.app 等に
>   到達できない**（403で実証済み）。実際のブラウザ操作は**ネット開放された環境の
>   Claude Code / 手動**で行い、成果物を `videogen/output/` に戻す。
> - **DomoAIのToSはbot自動化・スクレイピングを禁止**。完全自動化はBANリスクがある。
>   推奨は**半自動**：Claudeがプロンプト整形・ジョブ順序・保存/検証/納品を担い、
>   ブラウザ上の「生成」ボタン押下やダウンロードなど規約に触れうる操作は人が行う（or
>   claude-in-chromeを使う場合も、無料枠濫用・多重アカウント・高速連打を避ける）。

---

## 全体ループ

```
┌─ python3 videogen/cli.py next            次に着手できるジョブとプロンプトを得る
│
├─ Chromeで生成（下記ツール別フロー）        9:16 を明示。参照画像を渡す
│
├─ ダウンロードして videogen/output/<出力名> に保存
│     出力名は cli.py show <id> が表示する厳密名（例 base_kenji.png / still_SHOT01.png /
│     SHOT01_manami-order.mp4）
│
├─ python3 videogen/cli.py validate <id>    9:16/尺の機械検証
├─ python3 videogen/cli.py faceguard <id>   顔一貫性（②③のみ。要insightface。無ければ人手）
│
├─ OK → python3 videogen/cli.py set <id> approved
│  NG → python3 videogen/cli.py set <id> failed   → 別seed/テイクで再生成
│
└─ ①②が approved になると依存する次段が next に出る。③が揃ったら deliver
```

## 段別のツール指定

| 段 | Web UIでやること | 重要設定 |
|---|---|---|
| ① 基準顔 T2I | プロンプトを貼り、人物ポートレートを2〜3枚生成→ベスト1枚 | Realistic/Cinematic、顔くっきり、背景シンプル |
| ② 状況静止画 編集 | **基準顔を入力画像/参照に**し、背景・ポーズ・表情を編集 | **Aspect 9:16**、編集強度は控えめ（顔を保つ）、参照に基準顔 |
| ③ I2V | 承認済み静止画をimage-to-videoへ、動作プロンプトを指定 | **Aspect 9:16**、**Motion Low〜Mid**、尺3–5s、余白（S07はスマホ画面） |

## claude-in-chrome で半自動化する場合の型

ネット開放環境で、`claude-in-chrome` MCP（`tabs_context_mcp` / `navigate` / `read_page` /
`computer` / `form_input` 等）を使う場合の推奨手順：

1. `list_connected_browsers` → 対象のログイン済みChromeを選ぶ
2. `python3 videogen/cli.py next` の出力（プロンプト/出力名/参照）を作業指示にする
3. 生成ページへ `navigate`、`read_page`/`find` で入力欄と9:16設定を特定
4. `form_input` でプロンプト貼付、9:16選択、参照画像アップロード
5. 生成完了を `read_page` でポーリング（キュー待ちに耐える）
6. 生成物をダウンロード → `videogen/output/<出力名>` に配置
7. `validate` / `faceguard` → `set approved|failed`

> **規約の線引き**：高速連打・多重アカウント・無料枠の機械的濫用・スクレイピングはしない。
> あくまで「人の代わりに1件ずつ丁寧に操作する」範囲。心配なら生成ボタンは人が押す。

## トラブル対処
- **顔が別人化**：②の編集強度を下げ、基準顔を確実に参照に。だめなら基準顔から作り直し。
- **手/指の崩れ**：③のMotionを下げて再生成。
- **アスペクトが崩れる**：9:16を明示。`validate` で1080×1920/9:16を必ず確認。
- **2キャラ同居（S05/S09）が難しい**：多めに生成して選別。主役の顔を優先。

ツール固有の具体フローは [domoai.md](domoai.md)。
