# subtitles/

| ファイル | 対象 |
|---------|------|
| `bottle-scanner_ja.srt` | 本編（日本語・7セリフ） |
| `altA_veteran-brag_ja.srt` | 別版A ベテラン自慢版（日本語） |
| `altB_busy-night_ja.srt` | 別版B 満席の忙しい夜版（日本語） |
| `altE_english.srt` | 別版E 英語ナレーション版（English） |

タイムコードは各台本／`07_fcpx-assembly-guide.md` の配置表準拠。

## FCPXへの読み込み
1. FCPXのメニュー **ファイル → 字幕を読み込む → SRTファイル** で `bottle-scanner_ja.srt` を選択
2. 役割（ロール）に字幕トラックが作られる。位置・フォントは `06_graphics-telop-spec.md` のスタイルに合わせて調整
   - フォント：Noto Sans JP Bold 等 / サイズ 64〜72px / 黒フチ＋シャドウ / 下から約420pxライン中央

## 注意
- 声（Irodori）の実尺が確定したら、SRTのタイムコードを実尺に微調整してください（特に③心の声・⑤「あった！」）。
- ③は心の声のため `（　）` 括弧で内語表現にしています。FCPX側で斜体にするとさらに伝わります。
- SNSは音声オフ視聴が多いため、字幕は基本オンで納品推奨。
