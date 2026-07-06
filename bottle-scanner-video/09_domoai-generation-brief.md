# 09 ─ DomoAI 生成ブリーフ（ネット開放環境のClaude向け）

このファイルは、**ブラウザでDomoAIを操作できる（＝ネットワーク開放された）Claude Codeチャット**に
そのまま実行させるための指示書。DomoAIの実生成はそのチャットで行い、成果物をこの `bottlePV` に戻す。

> なぜ分けるのか：Claude Code環境は1つ1つ別のネットワークポリシーを持つ。`bottlePV` を主に開いている
> 環境は許可リストで縛られていて DomoAI に到達できない（403）。DomoAIに到達できる開放環境で生成し、
> 成果物を `domoai-exports/` にコミットして共有する。

---

## 前提・モード
- **DomoAI は Relax（無料）モードで実行。** 1回が遅い＝作り直しを減らす設計に。
- 生成手順は **T2I（人を作る）→ 画像編集（状況＋背景）→ I2V（動かす）** の3段。
- キャラ一貫性が最重要。**基準顔を先に固定し、以降は編集で流用**する。
- 参照：`01_production-bible.md`（キャラトークン/スタイル）、`02_shot-list.md`（ショット）、
  `03_domoai-prompts.md`（各ショットのI2V動作/T2V）、`domoai-prompt-bank-100.md`（言い換え100本）。

---

## Phase 1｜基準顔を作る（T2I・各キャラ2〜3枚→ベスト1枚を保存）

**① ケンジ（新人・20代男）**
```
Photorealistic portrait of a Japanese man in his mid-20s, short neat black hair, clean-shaven, slim, youthful earnest face, wearing a crisp white dress shirt and a fitted black waistcoat with a black bartender apron, warm soft lighting, simple dark neutral background, natural detailed skin texture, sharp focus on the face, 85mm portrait lens, cinematic, high detail
```
**② マナミ（常連・30代女）**
```
Photorealistic portrait of an elegant Japanese woman in her early 30s, shoulder-length wavy dark-brown hair, refined natural makeup, wearing a deep wine-red silk blouse, warm composed expression, soft flattering lighting, simple dark neutral background, natural detailed skin texture, sharp focus on the face, 85mm portrait lens, cinematic, high detail
```
**③ タカシ（店長・40代後半男）**
```
Photorealistic portrait of a distinguished Japanese man in his late 40s, short salt-and-pepper hair, a well-groomed short grey beard, wearing a black shirt and a dark sommelier apron, calm experienced expression, warm soft lighting, simple dark neutral background, natural detailed skin texture, sharp focus on the face, 85mm portrait lens, cinematic, high detail
```
**共通ネガティブ**
```
cartoon, anime, illustration, 3d, cgi, plastic skin, extra fingers, deformed hands, distorted face, text, watermark, low quality, blurry
```
→ 各キャラのベスト1枚を `domoai-exports/base_kenji.png` `base_manami.png` `base_takashi.png` として保存。

---

## Phase 2｜状況ショット化（画像編集：基準画像＋背景/ポーズ/表情）

基準画像を入力に、**同じ顔のまま**Barの背景・芝居に差し替える。**9:16で出力**。
各ショットの背景・ポーズ・表情は `02_shot-list.md` に準拠（下表は要約）。

| SHOT | キャラ | 状況（編集で指定） |
|------|--------|------------------|
| 01 | マナミ | カウンターに座り穏やかに注文。手前にグラス |
| 02 | ケンジ | 棚を振り返りボトルの壁の前で固まる |
| 03 | ケンジ | ラベルを指で追う、焦り・汗、手元クロース |
| 04 | マナミ | 時計をチラッと見る |
| 05 | タカシ | 眉をひそめ小声で気遣う（奥にケンジ） |
| 06 | ケンジ | ひらめいてスマホを取り出す |
| 07 | ケンジ | スマホを棚にかざす、顔が明るくなる（AR枠はFCPXで合成） |
| 08 | ケンジ | ボトルを取りカウンターへ提供 |
| 09 | マナミ＋タカシ | マナミ笑顔、奥でタカシがうなずく |

共通の背景記述（編集プロンプトに付与）：
```
inside an upscale intimate Japanese whisky bar at night, dark polished wood counter, brass fixtures, a back-shelf wall of kept whisky bottles with name tags, warm amber low-key lighting, photoreal, cinematic, shallow depth of field, vertical 9:16
```
→ `domoai-exports/still_SHOT01.png` … のように保存。顔がブレたら編集強度（denoise）を下げ、基準画像を参照に。

---

## Phase 3｜I2V（各状況ショットを動画に）

各 `still_SHOTxx.png` を Image-to-Video に入れ、`03_domoai-prompts.md` の該当ショットの
**I2V MOTION** をそのまま動作プロンプトに使う。**Motionは Low〜Mid**（顔崩れ防止）、尺3〜5秒、9:16。
→ `domoai-exports/SHOT01_manami-order.mp4` … の命名で保存し、`git add`→`commit`→`push`。

---

## 完了条件
- SHOT01〜09 の9クリップが `domoai-exports/` に揃い、push 済み。
- 各クリップでキャラが同一人物に見える（基準顔を流用できている）。
- 崩れたショットは Phase 2 からやり直し。

---

## ▼ 動いてる方のチャットに貼るキックオフ文（コピペ）
```
このリポジトリ fujimoto198904-hash/bottlePV をクローンして、
bottle-scanner-video/09_domoai-generation-brief.md の手順どおりに DomoAI（Relax）で
Phase 1→2→3 を実行して。ブラウザ操作は君がやる。生成物は domoai-exports/ に命名規則どおり
保存してコミット＆プッシュ。まず Phase 1 の基準顔3枚を作って、各ベスト1枚を見せて。
```
