# assets/audio/ ─ 合成SE（実WAVファイル）

コードで合成した効果音の**実ファイル**（48kHz / 16bit / mono）。そのままFCPXで使えます。
本番でより高品質な音源に差し替えても、まずはこのファイルで通し確認・仮組みが可能。

| ファイル | 内容 | 使用箇所 | 仕様 |
|---------|------|---------|------|
| `SE_0021_notify-piron.wav` | **ヒーロー通知音「ピロン」** 2音上行のベル(E6→G6)＋倍音 | SHOT07 / 0:21 | 0.55s / peak≈-2.9dBFS |
| `SE_0020_scan-sweep.wav` | スキャン起動の上昇スイープ | SHOT07 / 0:20.6 | 0.38s |
| `SE_0032_brand-chime.wav` | ブランド締めの暖かいアルペジオ(C5-E5-G5-C6) | CTA / 0:32 | 1.1s |

> `SE_0021_notify-piron.wav` は **Bottle Scannerのサウンドロゴ**。全バージョン共通で使用し、
> `assets/notification-toast` の表示フレームと同期させる（`05_se-bgm-cue-sheet.md` 参照）。
>
> 生成スクリプトの仕様は `05_se-bgm-cue-sheet.md §3` のスペックに準拠（角の立たない丸い成功音）。
> BGM・環境音・人の声は含みません（BGMは音源ライブラリ、声はIrodoriで用意）。
