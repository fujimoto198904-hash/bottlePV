# 全ジョブ プロンプト集（貼り付け用・自動生成）

`videogen/cli.py export` が manifest から生成。①→②→③の順に生成する。
命名は各ブロックの出力名どおり `videogen/output/` に保存 → `set <id> approved`。
手順: [PLAYBOOK.md](PLAYBOOK.md) / [domoai.md](domoai.md)。

## ① 基準顔(T2I)

### `base_kenji` → `base_kenji.png`  (9:16)  seed=4172721470836038799
- 概要: ケンジ（新人・20代男）
- 参照画像: なし

**PROMPT**
```
Photorealistic portrait of a Japanese man in his mid-20s, short neat black hair, clean-shaven, slim, youthful earnest face, wearing a crisp white dress shirt and a fitted black waistcoat with a black bartender apron, warm soft lighting, simple dark neutral background, natural detailed skin texture, sharp focus on the face, 85mm portrait lens, cinematic, high detail
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d, cgi, plastic skin, extra fingers, deformed hands, distorted face, text, watermark, low quality, blurry
```

### `base_manami` → `base_manami.png`  (9:16)  seed=3782389537458934708
- 概要: マナミ（常連・30代女）
- 参照画像: なし

**PROMPT**
```
Photorealistic portrait of an elegant Japanese woman in her early 30s, shoulder-length wavy dark-brown hair, refined natural makeup, wearing a deep wine-red silk blouse, warm composed expression, soft flattering lighting, simple dark neutral background, natural detailed skin texture, sharp focus on the face, 85mm portrait lens, cinematic, high detail
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d, cgi, plastic skin, extra fingers, deformed hands, distorted face, text, watermark, low quality, blurry
```

### `base_takashi` → `base_takashi.png`  (9:16)  seed=7027939734085636924
- 概要: タカシ（店長・40代後半男）
- 参照画像: なし

**PROMPT**
```
Photorealistic portrait of a distinguished Japanese man in his late 40s, short salt-and-pepper hair, a well-groomed short grey beard, wearing a black shirt and a dark sommelier apron, calm experienced expression, warm soft lighting, simple dark neutral background, natural detailed skin texture, sharp focus on the face, 85mm portrait lens, cinematic, high detail
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d, cgi, plastic skin, extra fingers, deformed hands, distorted face, text, watermark, low quality, blurry
```


## ② 状況静止画(編集)

### `still_SHOT01` → `still_SHOT01.png`  (9:16)  seed=7637203380119297307
- 概要: establishing / マナミの穏やかな注文
- 参照画像(一貫性): base_manami.png

**PROMPT**
```
Cinematic medium shot, an elegant Japanese woman in her early 30s, shoulder-length wavy dark-brown hair, refined natural makeup, wearing a deep wine-red silk blouse, seated at the bar counter with a whisky glass in front of her, warm and composed, gently placing an order, inside an upscale intimate Japanese whisky bar at night, dark polished wood counter, brass fixtures, a large back-shelf wall filled with rows of kept whisky bottles each with a small paper name tag, warm bottle bokeh in the background, moody low-key ambience, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm amber tungsten key light, low-key moody lighting, shallow depth of field, subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `still_SHOT02` → `still_SHOT02.png`  (9:16)  seed=7446696083898428886
- 概要: ケンジが棚を振り返りボトルの壁で固まる
- 参照画像(一貫性): base_kenji.png

**PROMPT**
```
Cinematic bust shot from behind the bar, a Japanese man in his mid-20s, short neat black hair, clean-shaven, slim build, wearing a crisp white dress shirt with rolled sleeves and a fitted black waistcoat and a black bartender apron, youthful earnest face, just turned around to face a huge back-shelf wall filled with dozens of rows of kept whisky bottles each with a small paper name tag, his expression stiffening with quiet panic, overwhelmed, inside an upscale intimate Japanese whisky bar at night, dark polished wood counter, brass fixtures, warm bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm amber tungsten key light, low-key moody lighting, shallow depth of field, subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `still_SHOT03` → `still_SHOT03.png`  (9:16)  seed=6455249726747549874
- 概要: ラベルを一本ずつ確認する焦り（手元クロース）
- 参照画像(一貫性): base_kenji.png

**PROMPT**
```
Cinematic close-up of a Japanese man in his mid-20s, short neat black hair, clean-shaven, in a white dress shirt with rolled sleeves and black waistcoat, his finger tracing along the small paper name tags of kept whisky bottles on a shelf, eyes darting nervously, a faint sweat on his forehead, growing anxiety, inside an upscale whisky bar at night, dark wood, brass, warm bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm amber tungsten key light, low-key moody lighting, shallow depth of field, subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `still_SHOT04` → `still_SHOT04.png`  (9:16)  seed=2299400874388846728
- 概要: マナミがチラッと時間を見る
- 参照画像(一貫性): base_manami.png

**PROMPT**
```
Cinematic close-up of an elegant Japanese woman in her early 30s, wavy dark-brown hair, wine-red silk blouse, seated at a bar counter, glancing down at her wristwatch with a subtle patient look, not annoyed, refined, inside an upscale whisky bar at night, warm amber lighting, brass fixtures, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm amber tungsten key light, low-key moody lighting, shallow depth of field, subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `still_SHOT05` → `still_SHOT05.png`  (9:16)  seed=3563051269282477763
- 概要: タカシが気づいて小声で気遣う（奥にケンジ）
- 参照画像(一貫性): base_takashi.png, base_kenji.png

**PROMPT**
```
Cinematic shot of a distinguished Japanese man in his late 40s, short salt-and-pepper hair, a well-groomed short grey beard, wearing a black shirt and dark sommelier apron, standing a little apart behind the bar, glancing with a slightly furrowed concerned brow toward a young bartender blurred in the background, inside an upscale whisky bar at night, warm amber lighting, brass, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm amber tungsten key light, low-key moody lighting, shallow depth of field, subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `still_SHOT06` → `still_SHOT06.png`  (9:16)  seed=7672774854249785131
- 概要: ひらめいてスマホを取り出す
- 参照画像(一貫性): base_kenji.png

**PROMPT**
```
Cinematic close-up of a Japanese man in his mid-20s, short neat black hair, white dress shirt and black waistcoat, a sudden spark of realization on his face, reaching into his apron pocket to pull out a smartphone, inside an upscale whisky bar at night, warm amber lighting starting to mix with a faint cool phone-screen glow on his face, brass, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, shallow depth of field, subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `still_SHOT07` → `still_SHOT07.png`  (9:16)  seed=6781380932259153316
- 概要: ★ヒーローショット AR発見（スマホ画面はFCPXでUI合成／余白を残す）
- 参照画像(一貫性): base_kenji.png

**PROMPT**
```
Cinematic over-the-shoulder shot of a Japanese man in his mid-20s, white dress shirt and black waistcoat, holding up a smartphone toward a wall of kept whisky bottles, his face lit brighter now with a cool mint-cyan glow from the screen mixing with warm amber, an expression of relief and delight beginning, the bottle shelf in front sharp and inviting, inside an upscale whisky bar at night, brass, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, brighter uplifting lighting, shallow depth of field, subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `still_SHOT08` → `still_SHOT08.png`  (9:16)  seed=8210512811547340958
- 概要: ボトルを取りカウンターへ提供（自信）
- 参照画像(一貫性): base_kenji.png

**PROMPT**
```
Cinematic medium shot of a Japanese man in his mid-20s, white dress shirt and black waistcoat and bartender apron, confidently taking a specific whisky bottle from the shelf and setting it down on the polished bar counter in front of a customer, self-assured posture, inside an upscale whisky bar at night, warm and now brighter inviting lighting, brass, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, shallow depth of field, subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `still_SHOT09` → `still_SHOT09.png`  (9:16)  seed=7299827985366017179
- 概要: マナミの笑顔／奥でタカシのうなずき（オチ）
- 参照画像(一貫性): base_manami.png, base_takashi.png

**PROMPT**
```
Cinematic close-up of an elegant Japanese woman in her early 30s, wavy dark-brown hair, wine-red silk blouse, seated at the bar, looking up with a genuine warm delighted smile, and softly out of focus in the background a distinguished late-40s Japanese man with salt-and-pepper hair and grey beard in a black shirt nodding with quiet satisfaction, inside an upscale whisky bar at night, warm bright happy lighting, brass, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, shallow depth of field, subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional cinematography, 8k
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```


## ③ クリップ(I2V)

### `clip_SHOT01` → `SHOT01_manami-order.mp4`  (9:16, 4s)  seed=2124193064778562833
- 概要: establishing / マナミの穏やかな注文
- 参照画像(一貫性): still_SHOT01.png, base_manami.png

**PROMPT**
```
slow subtle dolly-in toward the woman, she calmly speaks and gives a small warm gesture, gentle candle flicker on the bottles behind, very subtle head movement, cinematic, minimal camera shake, natural micro-expressions
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `clip_SHOT02` → `SHOT02_kenji-freeze.mp4`  (9:16, 4s)  seed=7434535728593211079
- 概要: ケンジが棚を振り返りボトルの壁で固まる
- 参照画像(一貫性): still_SHOT02.png, base_kenji.png

**PROMPT**
```
the young bartender turns his head toward the bottle wall then freezes, rack focus from his face to the overwhelming wall of bottles behind, tiny nervous swallow, subtle breathing, very slight handheld feel, cinematic, no large movement
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `clip_SHOT03` → `SHOT03_kenji-checking.mp4`  (9:16, 4s)  seed=6263564213529758185
- 概要: ラベルを一本ずつ確認する焦り（手元クロース）
- 参照画像(一貫性): still_SHOT03.png, base_kenji.png

**PROMPT**
```
his finger slides across the bottle name tags one by one, eyes flicking left and right with rising worry, subtle nervous breathing, tiny handheld camera sway to build tension, cinematic, small realistic movements only
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `clip_SHOT04` → `SHOT04_manami-glance.mp4`  (9:16, 3s)  seed=3142700538356774627
- 概要: マナミがチラッと時間を見る
- 参照画像(一貫性): still_SHOT04.png, base_manami.png

**PROMPT**
```
she subtly lowers her eyes to check the time then looks back up toward the bar, a small patient breath, very gentle movement, warm candle flicker, cinematic, minimal motion
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `clip_SHOT05` → `SHOT05_takashi-concern.mp4`  (9:16, 3s)  seed=2282486551376111969
- 概要: タカシが気づいて小声で気遣う（奥にケンジ）
- 参照画像(一貫性): still_SHOT05.png, base_takashi.png, base_kenji.png

**PROMPT**
```
the veteran manager notices, brow furrows slightly with concern, he leans in a touch and speaks quietly, very subtle head turn toward the younger staff, cinematic, small realistic movement
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `clip_SHOT06` → `SHOT06_kenji-idea.mp4`  (9:16, 3s)  seed=6287204543655025245
- 概要: ひらめいてスマホを取り出す
- 参照画像(一貫性): still_SHOT06.png, base_kenji.png

**PROMPT**
```
his eyes light up with an idea, he quickly pulls a smartphone from his pocket and raises it, a faint cool glow begins to touch his face, decisive small movement, cinematic, natural motion
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `clip_SHOT07` → `SHOT07_kenji-scan.mp4`  (9:16, 3s)  seed=462503598817679771
- 概要: ★ヒーローショット AR発見（スマホ画面はFCPXでUI合成／余白を残す）
- 参照画像(一貫性): still_SHOT07.png, base_kenji.png

**PROMPT**
```
he holds the phone steady toward the shelf, his face brightens into relief and a small smile, the lighting subtly lifts from dark to bright, a gentle push-in toward the target bottle, cinematic, smooth minimal motion, leave clean space on the phone screen for a UI overlay
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `clip_SHOT08` → `SHOT08_kenji-serve.mp4`  (9:16, 4s)  seed=6463924586865839301
- 概要: ボトルを取りカウンターへ提供（自信）
- 参照画像(一貫性): still_SHOT08.png, base_kenji.png

**PROMPT**
```
he decisively takes the bottle, turns and places it gently on the counter with a confident motion, a slight professional nod, warmer brighter light, cinematic, smooth natural movement
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

### `clip_SHOT09` → `SHOT09_manami-thanks.mp4`  (9:16, 4s)  seed=9015402735628850090
- 概要: マナミの笑顔／奥でタカシのうなずき（オチ）
- 参照画像(一貫性): still_SHOT09.png, base_manami.png, base_takashi.png

**PROMPT**
```
the woman looks up and breaks into a warm genuine smile, in the soft background the veteran manager gives a small satisfied nod, gentle warm ambience, cinematic, natural micro-expressions, minimal camera motion
```
**NEGATIVE**
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, low quality, blurry, jpeg artifacts, duplicated person
```

