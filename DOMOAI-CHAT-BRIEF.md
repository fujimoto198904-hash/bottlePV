# DomoAIチャット用ブリーフ ─ Bottle Scanner PV 映像生成

> **あなた（このブリーフを読んでいるDomoAI操作担当のClaude）へ。**
> このリポジトリ `fujimoto198904-hash/bottlePV` は、Bar向けアプリ「Bottle Scanner」の35秒プロモ動画の
> 制作パッケージです。**素材の設計・グラフィック・音・台本・プロンプトは全て完成済み**。
> 唯一残っているのが **DomoAIによる実写映像の生成**。それをあなたが担当します。
>
> **なぜあなたなのか**：この案件のメインチャットはネットワークが遮断された環境で、DomoAI(domoai.app)に
> 到達できません（403で実証済み）。あなたは**ネット開放環境**なので、ブラウザでDomoAIを操作できます。
> あなたが生成し、成果物をこのリポジトリに戻せば、メインチャット側がFCPX設計とQAを引き取ります。

---

## 1. あなたのミッション（要約）
DomoAI（**Relax＝無料モード**）で、本編9ショット分の実写クリップを生成し、`domoai-exports/` に保存して
コミット＆プッシュする。手順は **T2I（人を作る）→ 画像編集（状況＋背景）→ I2V（動かす）** の3段。
**キャラの一貫性が最優先**（3人が全ショットで同一人物に見えること）。

---

## 2. プロジェクト全貌

| 項目 | 内容 |
|---|---|
| プロダクト | **Bottle Scanner**（ボトルキープをARで一瞬で探せるBar向けアプリ） |
| 成果物 | 35秒ショートドラマ広告（5シーン・10ショット） |
| 画角 | **9:16 縦型**（1080×1920）／ 30fps |
| 画づくり | **実写シネマティック**（高級Barの実写ドラマ調） |
| 音声 | 日本語（別ツールIrodoriで生成・あなたの担当外） |
| ブランド色 | アンバー `#E8B451`（おもてなし）× ミント `#3FE0C5`（スキャナのテック） |
| 最終合成 | 制作者がFCPXで実施（あなたは映像クリップまで） |

### 台本（35秒の流れ）
新人バーテンダー**ケンジ**が、常連**マナミ**の「山崎」注文でボトルキープの壁の前で固まる →
焦って探す（店長**タカシ**が心配）→ スマホでBottle Scanner起動 → **ARで一発発見「…あった！」**（暗→明の転換）
→ 迷わず提供、マナミ「頼りになる」（信頼獲得のオチ）→ CTA「探す時間を、おもてなしの時間に。」

### 登場人物（外見は下のプロンプトで固定）
- **ケンジ**：新人・20代男 ／ **マナミ**：常連・30代女 ／ **タカシ**：ベテラン店長・40代後半男

---

## 3. リポジトリの歩き方（まずクローン）
```
git clone https://github.com/fujimoto198904-hash/bottlePV
```
主要ファイル（`bottle-scanner-video/` 配下）：
- `01_production-bible.md` … キャラの固定記述子・照明/色・スタイルサフィックス（**一貫性の源**）
- `02_shot-list.md` … 10ショットの絵コンテ（タイムコード・画角・芝居）
- `03_domoai-prompts.md` … 各ショットの **keyframe / I2V MOTION / T2V** プロンプト（← Phase3で使う）
- `domoai-prompt-bank-100.md` … 画角違い・言い換え100本（当たりを引く用）
- `09_domoai-generation-brief.md` … 生成手順の詳細版（このブリーフの実務パート）
- **保存先** `domoai-exports/` … あなたの生成物をここへ

> 生成物を戻すブランチ：`claude/pv-assets-subtitles-altversions`（PR #1）。別ブランチでも可、その場合はPRを作る。

---

## 4. 生成手順（Relaxモード）

### Phase 1｜基準顔を作る（T2I・各キャラ2〜3枚→ベスト1枚を保存）
> 顔をはっきり作り、以降は編集で流用する。ここが一貫性の全て。

**① ケンジ**
```
Photorealistic portrait of a Japanese man in his mid-20s, short neat black hair, clean-shaven, slim, youthful earnest face, wearing a crisp white dress shirt and a fitted black waistcoat with a black bartender apron, warm soft lighting, simple dark neutral background, natural detailed skin texture, sharp focus on the face, 85mm portrait lens, cinematic, high detail
```
**② マナミ**
```
Photorealistic portrait of an elegant Japanese woman in her early 30s, shoulder-length wavy dark-brown hair, refined natural makeup, wearing a deep wine-red silk blouse, warm composed expression, soft flattering lighting, simple dark neutral background, natural detailed skin texture, sharp focus on the face, 85mm portrait lens, cinematic, high detail
```
**③ タカシ**
```
Photorealistic portrait of a distinguished Japanese man in his late 40s, short salt-and-pepper hair, a well-groomed short grey beard, wearing a black shirt and a dark sommelier apron, calm experienced expression, warm soft lighting, simple dark neutral background, natural detailed skin texture, sharp focus on the face, 85mm portrait lens, cinematic, high detail
```
**共通ネガティブ**
```
cartoon, anime, illustration, 3d, cgi, plastic skin, extra fingers, deformed hands, distorted face, text, watermark, low quality, blurry
```
→ ベストを `domoai-exports/base_kenji.png` `base_manami.png` `base_takashi.png` に保存。
→ **まずこの3枚を制作者に見せて「この顔で確定」を取ってから Phase 2 へ**（手戻り防止）。

### Phase 2｜状況ショット化（画像編集：基準画像＋背景/ポーズ/表情・9:16出力）
基準画像を入力に、同じ顔のままBarの背景・芝居へ。各ショットの内容は `02_shot-list.md` 準拠（要約表）：

| SHOT | キャラ | 状況 |
|------|--------|------|
| 01 | マナミ | カウンターで穏やかに注文、手前にグラス |
| 02 | ケンジ | 棚を振り返りボトルの壁で固まる |
| 03 | ケンジ | ラベルを指で追う、焦り・汗（手元クロース） |
| 04 | マナミ | 時計をチラッと見る |
| 05 | タカシ | 眉をひそめ小声で気遣う（奥にケンジ） |
| 06 | ケンジ | ひらめいてスマホを取り出す |
| 07 | ケンジ | スマホを棚にかざし顔が明るくなる（AR枠は後でFCPX合成） |
| 08 | ケンジ | ボトルを取りカウンターへ提供 |
| 09 | マナミ＋タカシ | マナミ笑顔、奥でタカシがうなずく |

共通背景（編集プロンプトに付与）：
```
inside an upscale intimate Japanese whisky bar at night, dark polished wood counter, brass fixtures, a back-shelf wall of kept whisky bottles with name tags, warm amber low-key lighting, photoreal, cinematic, shallow depth of field, vertical 9:16
```
→ `domoai-exports/still_SHOT01.png` … で保存。顔がブレたら編集強度(denoise)を下げ、基準画像を参照に。

### Phase 3｜I2V（各状況ショットを動画に）
各 `still_SHOTxx.png` をImage-to-Videoへ。動作は `03_domoai-prompts.md` の該当ショットの **I2V MOTION** を使用。
**Motion Low〜Mid**（顔崩れ防止）、尺3〜5秒、9:16。
→ `domoai-exports/SHOT01_manami-order.mp4` … の命名で保存 → `git add && commit && push`。

---

## 5. 命名規則
| 種別 | 命名 |
|------|------|
| 基準顔 | `domoai-exports/base_{kenji\|manami\|takashi}.png` |
| 状況ショット | `domoai-exports/still_SHOT{番号}.png` |
| 完成クリップ | `domoai-exports/SHOT{番号}_{内容}.mp4`（例 `SHOT03_kenji-checking.mp4`） |

---

## 6. QA連携（メインチャットと）
- Phase 1 の基準顔3枚、各ショットの状況画、完成クリップを **随時 push** すること。
- メインチャット側が pull して **顔の一貫性・崩れ・演出一致**をQAし、直しプロンプトを返す。
- 迷ったら push して「見て」と言えばよい。完璧を待たず、こまめに共有。

## 7. 完了条件
- [ ] 基準顔3枚（確定済み）
- [ ] SHOT01〜09 の状況ショット9枚
- [ ] SHOT01〜09 の完成クリップ9本（9:16・キャラ一貫・崩れなし）
- [ ] すべて `domoai-exports/` に push 済み

> ⚠️ DomoAIの生成のみ担当。声（Irodori）・SE・グラフィック・字幕・最終合成は担当外（別で完成済み/制作者が実施）。
