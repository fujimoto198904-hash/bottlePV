# DomoAI Web UI 固有フロー

既存ブリーフ（`09_domoai-generation-brief.md`）が想定するツール。**Web UIは
T2I＋Nano Banana Pro画像編集＋image2videoを持つ**ので、①②③を1アカウントで回せる。

> ⚠️ **重要な前提差（公式API vs Web UI）**：DomoAIの**公式API（api.domoai.com）は動画専用**で、
> T2Iも画像編集もseedも参照顔固定も無い。つまり「基準顔を作る/顔を固定して配置する」①②は
> **API不可・Web UIのみ**。だから本件でDomoAIを使うなら **Web UI操作が必須**になる。
> そのWeb UI自動操作はToSで禁止（→ [PLAYBOOK.md](PLAYBOOK.md) の注意）。この矛盾を理解した上で、
> **一貫性が要る①②はNano Banana系の画像UI、③のI2VだけDomoAI**、という分担も検討に値する。

## ①②③ を DomoAI Web UI で回す場合

### ① 基準顔（T2I）
1. 画像生成（Text-to-Image）を開く
2. `cli.py show base_kenji` のPROMPT/NEGATIVEを貼る
3. Realistic系スタイル、顔くっきり・背景シンプルで2〜3枚生成
4. ベスト1枚を `videogen/output/base_kenji.png` として保存（manami/takashiも同様）
5. **3枚を制作者に見せて「この顔で確定」を取ってから②へ**（手戻り防止）
   → `cli.py set base_kenji approved`

### ② 状況静止画（画像編集＝Nano Banana Pro）
1. 画像編集を開き、**入力/参照に該当キャラの `base_*.png`** を与える
2. `cli.py show still_SHOT01` のPROMPTを編集指示に、**Aspect 9:16** で出力
3. 顔がブレたら編集強度（denoise）を下げ、基準顔を参照に固定
4. `videogen/output/still_SHOT01.png` に保存 → `validate` / `faceguard`
5. 顔OK＆目視OKで `cli.py set still_SHOT01 approved`

### ③ I2V（image2video）
1. Image-to-Video を開き、承認済み `still_SHOTxx.png` を入力
2. `cli.py show clip_SHOT01` のPROMPT（I2V MOTION）を動作指示に
3. **Aspect 9:16 / Duration 3–5s / Motion Low〜Mid**（顔・手の崩れ防止）
4. `videogen/output/SHOT01_manami-order.mp4` に保存 → `validate` / `faceguard`
5. OKで `set approved`。9本揃ったら `cli.py deliver`

## 設定早見（03_domoai-prompts.md より）
| 設定 | 値 |
|---|---|
| Aspect ratio | **9:16**（既定1:1のことがあるので必ず明示） |
| Duration | 3–5s（ショット尺に合わせる。manifestの`duration_s`参照） |
| Motion strength | **Low〜Mid** |
| Style | Realistic / Cinematic（アニメ変換OFF） |
| Seed | 良い顔が出たら固定して流用（DomoAIはseed非公開のことあり→再生成ガードで担保） |

## 注意
- **AR枠・通知トースト・CTAは生成しない**。FCPXで `assets/*.svg` を重ねる（S07/S10）。
- SHOT07はスマホ画面にUIを載せる**余白**を残す構図で。
- 無料(Relax)は遅い＝作り直しを減らす設計に。ToS上、機械的な連打・多重アカウントは避ける。
