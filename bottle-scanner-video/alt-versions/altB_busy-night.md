# 別バージョンB ─ 「満席の忙しい夜」版（35秒 / 9:16 / 実写シネマティック）

ベース版と同じキャラ・世界観・ブランドを流用。**キャラトークン／スタイルサフィックス／ネガティブは
`../01_production-bible.md` を共通使用**。通知音「ピロン」も共通。

- 舞台：**満席・活気ある忙しい夜のBar**。オーダーが飛び交う
- テーマ：忙しい夜こそ差が出る。スキャンで回転が速くなり、**忙しくてもおもてなしが止まらない**
- 構成：アンサンブル＋テンポの良いモンタージュ（ピロン連打で気持ちよさ）

---

## 尺配分（5シーン / 10ショット）

| シーン | 区間 | 内容 | ショット |
|-------|------|------|---------|
| 1 | 0:00–0:06 | 満席の店内。次々にオーダーが飛ぶ活気 | B01–B02 |
| 2 | 0:06–0:14 | 通常なら手こずる場面。ケンジが素早くスキャン→即提供 | B03–B04 |
| 3 | 0:14–0:24 | モンタージュ：3人が次々スキャンしてボトルを出す（ピロン連打） | B05–B07 |
| 4 | 0:24–0:32 | 満席でも回転が速い。客の満足、タカシ満足げ | B08–B09 |
| 5 | 0:32–0:35 | CTAエンドカード（共通） | B10 |

---

## セリフ／SE（Irodori台本・命名規則 `VO_altB_...`）

| ID | 話者 | セリフ | 読み | 感情/速度 |
|----|------|--------|------|-----------|
| `VO_altB_guestA_01` | 客A | 山崎、ロックで！ | やまざき、ロックで！ | 明るく元気・やや速め |
| `VO_altB_guestB_01` | 客B | こっち白州ハイボール！ | こっちはくしゅうハイボール！ | 弾む・速め |
| `VO_altB_kenji_01` | ケンジ | はい、ただいま！ | はい、ただいま！ | 明るく機敏・速め・自信 |
| `VO_altB_takashi_01` | タカシ | 忙しい夜こそ、差が出る | いそがしいよるこそ、さがでる | 落ち着き・低め・満足げ |

> ※本編はセリフ少なめ＋オーダーの掛け声・ピロン連打・BGMでテンポを作る構成。
> 白州（はくしゅう）＝サントリーのウイスキー。読み違い注意。

---

## DomoAIプロンプト差分（主要ショット）

> keyframe末尾に `STYLE_SUFFIX`、`NEGATIVE_PROMPT` 共通。満席＝背景に人物ボケを足し、活気を演出。

### B01 ─ 満席の店内・活気（0:00–0:03）
```
Cinematic wide shot inside a packed lively upscale Japanese whisky bar at night, every counter
seat taken with warmly-lit patrons chatting and raising glasses, bartenders busy behind the
counter, a large back-shelf wall of kept whisky bottles, energetic but classy atmosphere,
warm amber tungsten light, brass, rich bottle bokeh,
```

### B04 ─ ケンジ素早くスキャン→即提供（0:10–0:14）
```
Cinematic medium shot of a Japanese man in his mid-20s, white dress shirt and black waistcoat,
swiftly holding a smartphone toward the bottle shelf then grabbing a bottle in one fluid
confident motion, energy and speed, busy blurred patrons in the background, cool mint screen
glow, inside a packed whisky bar at night, warm bright lighting, brass, bottle bokeh,
```

### B05–B07 ─ モンタージュ（各3ショット・0:14–0:24）
3人（ケンジ／タカシ／もう1名のスタッフでも可）がそれぞれスキャン→ボトルを出す短いカットを積む。
各カットで共通 **ピロン** を1回ずつ鳴らし、テンポを作る。
```
Cinematic quick close-up of hands holding a smartphone scanning a shelf of whisky bottles with
a mint-cyan AR glow, then confidently pulling the exact bottle, fast-paced energetic montage
style, packed bar at night, warm lighting, brass, bottle bokeh,
```
> AR枠・トーストは共通SVG（`../assets/png/`）をFCPXで各カットに合成。モンタージュはFCPX側でテンポ編集。

### B08 ─ 満席でも速い回転・客の満足（0:24–0:28）
```
Cinematic shot of a busy upscale whisky bar counter where multiple satisfied patrons receive
their drinks quickly, smiling, a smooth fast service flow, bartenders in motion, warm happy
energetic lighting, brass, bottle bokeh,
```

---

## 音・演出メモ
- BGMはベース版よりアップテンポで躍動感のあるラウンジ/ジャズ。
- モンタージュ区間（0:14–0:24）は**ピロンを3回**、カットの頭に合わせて配置＝気持ちよさの畳みかけ。
- 満席のガヤ（`SE_bg_ambience` を賑やか版に）を厚めに。
- オチはタカシの「忙しい夜こそ、差が出る」→ CTAへ。ドヤりすぎず、余裕のトーンで。
