# 別バージョンD ─ 「記念日サプライズ版」（35秒 / 9:16 / 実写シネマティック）

ベース版と同じ世界観・ブランド・通知音を流用。感情に振った“泣ける寄り”のバージョン。
登場：ケンジ（新人）＋ カップルの常連客（2名）。キャラトークンは `../01_production-bible.md` 準拠、
カップルは新規（下記）。

- テーマ：**大切な一本を、大切な瞬間に。** ボトルキープ＝思い出。それを一瞬で差し出せる感動
- オチ：「記念日、おめでとうございます」＝スピードではなく“気持ちのおもてなし”に昇華

---

## 新キャラトークン
- `GUEST_M_TOKEN`：`a warm Japanese man in his 30s in a smart casual jacket, seated at the bar with his partner`
- `GUEST_F_TOKEN`：`a Japanese woman in her early 30s in an elegant dress, seated beside her partner, gentle expression`

## 尺配分

| シーン | 区間 | 内容 | ショット |
|-------|------|------|---------|
| 1 | 0:00–0:07 | カップル来店。男性「1年前、ここで一本キープしたんだけど…」 | D01–D02 |
| 2 | 0:07–0:15 | ケンジ「承知しております」スマホを構える。棚は膨大 | D03–D04 |
| 3 | 0:15–0:23 | スキャン→即発見。そっと一本を取り出す | D05–D06 |
| 4 | 0:23–0:32 | 「こちらですね。記念日、おめでとうございます」女性が感動 | D07–D08 |
| 5 | 0:32–0:35 | CTA（共通・サブコピーは下記に差し替え可） | D09 |

## セリフ（Irodori・`VO_altD_...`）

| ID | 話者 | セリフ | 読み | 感情/速度 |
|----|------|--------|------|-----------|
| `VO_altD_guestM_01` | 男性客 | 1年前、ここで一本キープしたんだけど… | いちねんまえ、ここでいっぽんキープしたんだけど… | 少し照れ・懐かしむ・普通速 |
| `VO_altD_kenji_01` | ケンジ | はい、承知しております | はい、しょうちしております | 丁寧・落ち着き・やわらかい |
| `VO_altD_kenji_02` | ケンジ | こちらですね。記念日、おめでとうございます | こちらですね。きねんび、おめでとうございます | あたたかい・心のこもった |
| `VO_altD_guestF_01` | 女性客 | 覚えててくれたの… | おぼえててくれたの… | 感動・小声・じんわり |

## テロップ差し替え（任意・CTA前）
- サブコピー案：**「大切な一本を、大切な瞬間に。」**（`06_graphics-telop-spec.md` のCTAサブに差し替え可）

## DomoAIプロンプト差分（主要ショット）

### D05 ─ ケンジがスキャンして思い出の一本を発見（★ / 0:15–0:20）
```
Cinematic over-the-shoulder shot of a Japanese man in his mid-20s, white shirt and black
waistcoat, gently holding up a smartphone toward a wall of kept whisky bottles, a soft caring
expression, cool mint-cyan glow, an emotional warm mood, inside an upscale whisky bar at night,
brass, bottle bokeh, soft warm lighting,
```
### D07 ─ 一本を差し出す／女性が感動（0:23–0:28）
```
Cinematic two-shot of a young Japanese bartender gently presenting a special whisky bottle to a
touched Japanese couple in their 30s at the bar, the woman's eyes glistening with emotion, an
intimate heartfelt moment, warm candlelit lighting, shallow depth of field, brass, bottle bokeh,
```
> AR枠・トーストは共通SVG。ここでは通知音ピロンを**やや控えめ**にし、感動の余韻を優先。

## 音・演出メモ
- BGMは温かいピアノ主体のエモーショナルな曲。ピロンは小さめに、余韻重視。
- D08で女性の表情、男性の微笑み、ケンジの誠実な会釈を丁寧に。泣かせにいくより“じんわり”。
