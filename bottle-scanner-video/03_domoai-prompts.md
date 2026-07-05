# 03 ─ DomoAI プロンプト集（実写シネマティック / 9:16）

各ショットに **3種類** のプロンプトを用意：

1. **KEYFRAME（静止画）** … まず1枚の静止画で構図とキャラを固定する（DomoAIの画像生成 or 手持ちの画像生成ツール）
2. **I2V MOTION（画像→動画）** … その静止画をDomoAIで動かすときの「動きの指示」
3. **T2V FALLBACK（文章→動画）** … 静止画を挟まず直接動画にする場合の予備プロンプト

> **推奨は KEYFRAME → I2V の2段構え。** 実写AIドラマのキャラ一貫性は、
> 先にキーフレーム画像を固めてから animateするのが最も安定する。
>
> **共通ルール**：
> - `KENJI_TOKEN` / `MANAMI_TOKEN` / `TAKASHI_TOKEN` / `SET_TOKEN` / `STYLE_SUFFIX` は
>   `01_production-bible.md` で定義済み。下記プロンプトには**展開済みで貼ってある**のでそのままコピペ可。
> - **NEGATIVE_PROMPT** は全ショット共通（§末尾に再掲）。
> - DomoAI設定の目安：**Aspect 9:16 / Duration 4–5s / Motion（動き強度）は Low–Mid**（顔崩れ防止）。

---

## DomoAI 共通設定（各生成で指定）

| 設定 | 値 | 理由 |
|------|-----|------|
| Aspect ratio | **9:16** | 縦型納品 |
| Duration | 3–5秒（ショット尺に合わせる） | 尺の無駄を出さない |
| Motion strength | **Low〜Mid** | 高いと顔・手が崩れる。ドラマは小さな動きで十分 |
| Style | **Realistic / Cinematic**（アニメ変換はOFF） | 実写指定 |
| Seed | 気に入ったキャラが出たら**固定**して他ショットに流用 | 一貫性 |

> **キャラ一貫性のコツ**：SHOT01でケンジ／マナミの良い顔が出たら、その画像を
> I2Vの入力に使い回し、他ショットのキーフレームにも「同一人物」を参照として与える。
> DomoAIにキャラ参照機能があれば同一 reference を全ショットに指定する。

---

## SHOT01 ─ establishing / マナミの注文（0:00–0:04）

**KEYFRAME（静止画）**
```
Cinematic medium shot, an elegant Japanese woman in her early 30s, shoulder-length wavy
dark-brown hair, refined natural makeup, wearing a deep wine-red silk blouse, seated at the
bar counter with a whisky glass in front of her, warm and composed, gently placing an order,
inside an upscale intimate Japanese whisky bar at night, dark polished wood counter, brass
fixtures, a large back-shelf wall filled with rows of kept whisky bottles each with a small
paper name tag, warm bottle bokeh in the background, moody low-key ambience,
shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm amber tungsten
key light, low-key moody lighting, shallow depth of field, subtle film grain, photorealistic,
ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**I2V MOTION**
```
slow subtle dolly-in toward the woman, she calmly speaks and gives a small warm gesture,
gentle candle flicker on the bottles behind, very subtle head movement, cinematic,
minimal camera shake, natural micro-expressions
```
**T2V FALLBACK**
```
Cinematic vertical video, slow dolly-in on an elegant Japanese woman in her early 30s with
wavy dark-brown hair in a wine-red silk blouse, seated at a moody upscale whisky bar counter
at night, warm amber lighting, a wall of kept whisky bottles bokeh behind her, she calmly
places an order, photoreal, shallow depth of field, film grain, 9:16
```

---

## SHOT02 ─ ケンジが棚を振り返り固まる（0:04–0:08）

**KEYFRAME（静止画）**
```
Cinematic bust shot from behind the bar, a Japanese man in his mid-20s, short neat black hair,
clean-shaven, slim build, wearing a crisp white dress shirt with rolled sleeves and a fitted
black waistcoat and a black bartender apron, youthful earnest face, just turned around to face
a huge back-shelf wall filled with dozens of rows of kept whisky bottles each with a small paper
name tag, his expression stiffening with quiet panic, overwhelmed, inside an upscale intimate
Japanese whisky bar at night, dark polished wood counter, brass fixtures, warm bottle bokeh,
shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm amber tungsten key
light, low-key moody lighting, shallow depth of field, subtle film grain, photorealistic, ultra
detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**I2V MOTION**
```
the young bartender turns his head toward the bottle wall then freezes, rack focus from his
face to the overwhelming wall of bottles behind, tiny nervous swallow, subtle breathing,
very slight handheld feel, cinematic, no large movement
```
**T2V FALLBACK**
```
Cinematic vertical video, a nervous Japanese man in his mid-20s in a white shirt and black
waistcoat and bartender apron turns around behind a bar and freezes facing a huge wall of
dozens of kept whisky bottles, rack focus to the bottles, warm moody low-key lighting,
photoreal, film grain, shallow depth of field, 9:16
```

---

## SHOT03 ─ ラベルを一本ずつ確認する焦り（0:08–0:12）

**KEYFRAME（静止画）**
```
Cinematic close-up of a Japanese man in his mid-20s, short neat black hair, clean-shaven,
in a white dress shirt with rolled sleeves and black waistcoat, his finger tracing along the
small paper name tags of kept whisky bottles on a shelf, eyes darting nervously, a faint sweat
on his forehead, growing anxiety, inside an upscale whisky bar at night, dark wood, brass,
warm bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm
amber tungsten key light, low-key moody lighting, shallow depth of field, subtle film grain,
photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**I2V MOTION**
```
his finger slides across the bottle name tags one by one, eyes flicking left and right with
rising worry, subtle nervous breathing, tiny handheld camera sway to build tension,
cinematic, small realistic movements only
```
**T2V FALLBACK**
```
Cinematic vertical close-up video, a worried young Japanese bartender's finger checking name
tags on a shelf of whisky bottles one by one, eyes darting, faint sweat, warm moody low-key
bar lighting, handheld tension, photoreal, film grain, 9:16
```

---

## SHOT04 ─ マナミがチラッと時間を見る（0:12–0:15）

**KEYFRAME（静止画）**
```
Cinematic close-up of an elegant Japanese woman in her early 30s, wavy dark-brown hair, wine-red
silk blouse, seated at a bar counter, glancing down at her wristwatch with a subtle patient look,
not annoyed, refined, inside an upscale whisky bar at night, warm amber lighting, brass fixtures,
bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm amber
tungsten key light, low-key moody lighting, shallow depth of field, subtle film grain,
photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**I2V MOTION**
```
she subtly lowers her eyes to check the time then looks back up toward the bar, a small patient
breath, very gentle movement, warm candle flicker, cinematic, minimal motion
```
**T2V FALLBACK**
```
Cinematic vertical video, an elegant Japanese woman in a wine-red blouse at a moody bar counter
subtly glances at her wristwatch then looks back up, patient expression, warm amber lighting,
photoreal, shallow depth of field, film grain, 9:16
```

---

## SHOT05 ─ タカシが気づいて小声で気遣う（0:15–0:18）

**KEYFRAME（静止画）**
```
Cinematic shot of a distinguished Japanese man in his late 40s, short salt-and-pepper hair, a
well-groomed short grey beard, wearing a black shirt and dark sommelier apron, standing a little
apart behind the bar, glancing with a slightly furrowed concerned brow toward a young bartender
blurred in the background, inside an upscale whisky bar at night, warm amber lighting, brass,
bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm amber
tungsten key light, low-key moody lighting, shallow depth of field, subtle film grain,
photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**I2V MOTION**
```
the veteran manager notices, brow furrows slightly with concern, he leans in a touch and speaks
quietly, very subtle head turn toward the younger staff, cinematic, small realistic movement
```
**T2V FALLBACK**
```
Cinematic vertical video, a distinguished late-40s Japanese bar manager with salt-and-pepper hair
and grey beard in a black shirt notices and quietly speaks with a concerned look toward a blurred
young bartender behind him, warm moody bar lighting, photoreal, film grain, 9:16
```

---

## SHOT06 ─ ひらめき → スマホを取り出す（0:18–0:21）

**KEYFRAME（静止画）**
```
Cinematic close-up of a Japanese man in his mid-20s, short neat black hair, white dress shirt
and black waistcoat, a sudden spark of realization on his face, reaching into his apron pocket
to pull out a smartphone, inside an upscale whisky bar at night, warm amber lighting starting to
mix with a faint cool phone-screen glow on his face, brass, bottle bokeh, shot on ARRI Alexa,
35mm anamorphic lens, cinematic film color grade, shallow depth of field, subtle film grain,
photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**I2V MOTION**
```
his eyes light up with an idea, he quickly pulls a smartphone from his pocket and raises it,
a faint cool glow begins to touch his face, decisive small movement, cinematic, natural motion
```
**T2V FALLBACK**
```
Cinematic vertical video, a young Japanese bartender suddenly gets an idea, his face brightens,
he pulls a smartphone from his apron pocket and raises it, warm bar lighting with a hint of cool
screen glow, photoreal, shallow depth of field, film grain, 9:16
```

---

## SHOT07 ─ AR発見 ★ヒーローショット（0:21–0:24）

> **重要**：AR枠・通知トーストは **DomoAIで作らず** FCPXで `assets/ar-scan-overlay.svg`
> `assets/notification-toast.svg` を重ねる。DomoAIでは「スマホを構えるケンジ＋棚と、明るくなる顔」を撮る。

**KEYFRAME（静止画）**
```
Cinematic over-the-shoulder shot of a Japanese man in his mid-20s, white dress shirt and black
waistcoat, holding up a smartphone toward a wall of kept whisky bottles, his face lit brighter
now with a cool mint-cyan glow from the screen mixing with warm amber, an expression of relief
and delight beginning, the bottle shelf in front sharp and inviting, inside an upscale whisky bar
at night, brass, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color
grade, brighter uplifting lighting, shallow depth of field, subtle film grain, photorealistic,
ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**I2V MOTION**
```
he holds the phone steady toward the shelf, his face brightens into relief and a small smile,
the lighting subtly lifts from dark to bright, a gentle push-in toward the target bottle,
cinematic, smooth minimal motion, leave clean space on the phone screen for a UI overlay
```
**T2V FALLBACK**
```
Cinematic vertical video, a young Japanese bartender holds up a smartphone toward a wall of
whisky bottles, his face brightening with relief lit by a cool mint glow, lighting lifts from
dark to bright, gentle push-in on the target bottle, photoreal, film grain, 9:16, keep phone
screen area clean
```

---

## SHOT08 ─ ボトルを取り、マナミの前へ提供（0:24–0:28）

**KEYFRAME（静止画）**
```
Cinematic medium shot of a Japanese man in his mid-20s, white dress shirt and black waistcoat and
bartender apron, confidently taking a specific whisky bottle from the shelf and setting it down on
the polished bar counter in front of a customer, self-assured posture, inside an upscale whisky
bar at night, warm and now brighter inviting lighting, brass, bottle bokeh, shot on ARRI Alexa,
35mm anamorphic lens, cinematic film color grade, shallow depth of field, subtle film grain,
photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**I2V MOTION**
```
he decisively takes the bottle, turns and places it gently on the counter with a confident
motion, a slight professional nod, warmer brighter light, cinematic, smooth natural movement
```
**T2V FALLBACK**
```
Cinematic vertical video, a now-confident young Japanese bartender takes a whisky bottle from the
shelf and places it on the bar counter in front of a seated customer, warm inviting lighting,
photoreal, shallow depth of field, film grain, 9:16
```

---

## SHOT09 ─ マナミの笑顔／奥でタカシのうなずき（0:28–0:32）

**KEYFRAME（静止画）**
```
Cinematic close-up of an elegant Japanese woman in her early 30s, wavy dark-brown hair, wine-red
silk blouse, seated at the bar, looking up with a genuine warm delighted smile, and softly out of
focus in the background a distinguished late-40s Japanese man with salt-and-pepper hair and grey
beard in a black shirt nodding with quiet satisfaction, inside an upscale whisky bar at night,
warm bright happy lighting, brass, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens,
cinematic film color grade, shallow depth of field, subtle film grain, photorealistic, ultra
detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**I2V MOTION**
```
the woman looks up and breaks into a warm genuine smile, in the soft background the veteran
manager gives a small satisfied nod, gentle warm ambience, cinematic, natural micro-expressions,
minimal camera motion
```
**T2V FALLBACK**
```
Cinematic vertical video, an elegant Japanese woman at a bar counter looks up with a warm genuine
smile, while a distinguished bar manager nods with satisfaction blurred in the background, warm
happy lighting, photoreal, shallow depth of field, film grain, 9:16
```

---

## SHOT10 ─ CTAエンドカード（0:32–0:35）

DomoAIでの生成は**不要**。`assets/cta-endcard.svg` をFCPXでフェードインさせる（`06_graphics-telop-spec.md` 参照）。
背景に軽い動きが欲しい場合のみ、下記の抽象アンビエンス素材を任意で作ってエンドカードの裏に薄く敷く。

**任意・背景アンビエンス T2V**
```
Abstract cinematic vertical background, slow drifting warm amber and mint bokeh lights on a dark
charcoal background, soft out-of-focus whisky bottle reflections, elegant and premium, subtle
motion, no people, no text, 9:16
```

---

## NEGATIVE_PROMPT（全ショット共通・再掲）
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers,
deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles,
oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

---

## 生成チェックリスト（各ショット）
- [ ] 9:16 で生成したか
- [ ] キャラの顔が他ショットと同一人物に見えるか（seed/参照を流用）
- [ ] 手・指が崩れていないか（Motionを下げて再生成）
- [ ] ライティングが台本の明暗設計に合っているか（S1–5暗め / S3以降明転）
- [ ] SHOT07はスマホ画面にUIを載せる余白があるか
- [ ] `domoai-exports/SHOT{番号}_{内容}.mp4` で保存したか
