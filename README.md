# bottlePV

Bar向けアプリ「**Bottle Scanner**」プロモ用ショートドラマ動画（35秒 / 9:16縦型 / 実写シネマティック）の
制作リポジトリ。DomoAI（映像）× Irodori（音声）× Final Cut Pro X（合成・納品）のワークフローで制作する。

## 構成

- **`bottle-scanner-video/`** … 制作素材・指示書・管理システム一式（本体）
  - まずは `bottle-scanner-video/README.md` を読む
  - 制作中は `bottle-scanner-video/dashboard/index.html` をブラウザで開く（プロンプト/台本コピー・進捗管理）
- **`HANDOFF.md`** … プロジェクトの現状・確定事項・引き継ぎメモ
- **`NEW-CHAT-KICKOFF.md`** … 別チャットで再開する際のキックオフ用プロンプト

## 確定仕様

| 項目 | 値 |
|------|-----|
| アスペクト比 | 9:16 縦型（1080×1920） |
| フレームレート | 30fps |
| 尺 | 35秒（5シーン・10ショット） |
| ビジュアル | 実写シネマティック |
| 音声 | 日本語（Irodori） |
| ブランド色 | アンバー `#E8B451` × ミント `#3FE0C5` |

## 制作手順（推奨順）

1. 声（Irodori） → 2. 映像（DomoAI） → 3. 音（SE/BGM） → 4. 文字/UI → 5. FCPX合成 → 6. グレーディング → 7. 書き出し

詳細は `bottle-scanner-video/README.md` と各指示書（01〜07）を参照。
