# 別バージョンA ─ 「ベテランが後輩に自慢する」版（35秒 / 9:16 / 実写シネマティック）

ベース版と同じキャラ・世界観・ブランドを流用。**キャラトークン／スタイルサフィックス／ネガティブは
`../01_production-bible.md` を共通使用**（外見・照明・色は一切変えない）。通知音「ピロン」も共通。

- 主役の入れ替え：**タカシ（ベテラン店長）が主役**、ケンジ（新人）が驚き役
- テーマ：ベテランの余裕と、道具で誰でも“できる人”になれるという小さな粋
- オチ：「使えるモンは、使わなきゃな」＝自慢しつつ後輩に道具を勧める温かさ

---

## 尺配分（5シーン / 10ショット）

| シーン | 区間 | 内容 | ショット |
|-------|------|------|---------|
| 1 | 0:00–0:07 | ケンジが棚で探して手こずる。タカシがニヤリと見ている | A01–A02 |
| 2 | 0:07–0:15 | タカシ「貸してみ」と登場。余裕の表情 | A03–A04 |
| 3 | 0:15–0:24 | タカシがスキャン→一発発見「ほい、これだろ？」 | A05–A06 |
| 4 | 0:24–0:32 | ケンジ驚愕→タカシ自慢げにアプリを見せる | A07–A08 |
| 5 | 0:32–0:35 | CTAエンドカード（共通） | A09 |

---

## セリフ（Irodori台本・命名規則 `VO_altA_...`）

| ID | 話者 | セリフ | 読み | 感情/速度 |
|----|------|--------|------|-----------|
| `VO_altA_kenji_01` | ケンジ | あれ…どこだっけ… | あれ…どこだっけ… | 困り・小声・つぶやき |
| `VO_altA_takashi_01` | タカシ | ん？　貸してみ | ん？　かしてみ | 余裕・低め・ゆっくり |
| `VO_altA_takashi_02` | タカシ | ほい、これだろ？ | ほい、これだろ？ | 軽やか・自信・少し得意げ |
| `VO_altA_kenji_02` | ケンジ | えっ、なんで一発で…！？ | えっ、なんでいっぱつで…！？ | 驚愕・やや速め・高め |
| `VO_altA_takashi_03` | タカシ | Bottle Scanner。使えるモンは、使わなきゃな | ボトルスキャナー。つかえるモンは、つかわなきゃな | 自慢げ・あたたかい・ゆっくり |

---

## DomoAIプロンプト差分（ベースから変える主要ショットのみ）

> keyframe末尾に `STYLE_SUFFIX` を付与、`NEGATIVE_PROMPT` 共通（`../03_domoai-prompts.md` 参照）。

### A05 ─ タカシがスキャンして一発発見（★ヒーロー / 0:15–0:18）
```
Cinematic over-the-shoulder shot of a distinguished Japanese man in his late 40s, short
salt-and-pepper hair, well-groomed short grey beard, black shirt and dark sommelier apron,
calmly holding up a smartphone toward a wall of kept whisky bottles with a confident faint
smirk, cool mint-cyan screen glow mixing with warm amber, a younger bartender watching in
awe blurred behind him, inside an upscale whisky bar at night, brass, bottle bokeh, brighter
uplifting lighting,
```
> AR枠・トーストは共通SVG（`../assets/png/ar-scan-overlay.png` / `notification-toast.png`）をFCPXで合成。

### A07 ─ ケンジ驚愕（0:24–0:28）
```
Cinematic close-up of a Japanese man in his mid-20s, short neat black hair, white dress shirt
and black waistcoat, eyes wide with astonishment and admiration, mouth slightly open, looking
at a smartphone held by an older colleague, inside an upscale whisky bar at night, warm bright
lighting, brass, bottle bokeh,
```

### A08 ─ タカシ自慢げにアプリを見せる（0:28–0:32）
```
Cinematic medium shot of a distinguished late-40s Japanese bartender with salt-and-pepper hair
and grey beard, black shirt, turning his smartphone screen toward the camera/colleague with a
proud warm grin, a subtle knowing look, inside an upscale whisky bar at night, warm happy
lighting, brass, bottle bokeh,
```

---

## 音・演出メモ
- タカシの「ほい、これだろ？」の直前に共通の **ピロン（`SE_0021_notify-piron`）**。
- BGMはベース版よりやや軽妙・ジャジー寄りに（ベテランの余裕）。
- オチA08は自慢げだが嫌味にならないよう、最後に一瞬やわらかい表情を入れる。
