# 別バージョンC ─ 「女性店長版」（35秒 / 9:16 / 実写シネマティック）

ベース版と同じ世界観・ブランド・通知音を流用。舞台・照明・色は `../01_production-bible.md` 準拠。
新キャラ **ミサキ（女性店長・30代後半）** を追加（他キャラのトークンは共通）。

- テーマ：落ち着いた大人の女性店長の**余裕とホスピタリティ**。無茶な注文もスマートに応える“かっこよさ”
- オチ：「お客様の一本、忘れませんよ」＝記憶力ではなく道具で信頼を体現する粋

---

## 新キャラトークン（MISAKI_TOKEN）
```
a poised Japanese woman in her late 30s, elegant chin-length bob haircut, refined confident
face, wearing a sharp tailored black vest over a crisp white shirt and a bar apron, calm
professional charisma, a bar manager
```

## 尺配分

| シーン | 区間 | 内容 | ショット |
|-------|------|------|---------|
| 1 | 0:00–0:07 | 常連が少し無茶な注文「去年入れたやつ、まだある？」 | C01–C02 |
| 2 | 0:07–0:15 | ミサキ笑顔で「もちろんです」スマホを構える（若手が半信半疑） | C03–C04 |
| 3 | 0:15–0:24 | スキャン→即発見。迷いなく棚から一本 | C05–C06 |
| 4 | 0:24–0:32 | 客「さすが」ミサキ「お客様の一本、忘れませんよ」＋若手が納得 | C07–C08 |
| 5 | 0:32–0:35 | CTA（共通） | C09 |

## セリフ（Irodori・`VO_altC_...`）

| ID | 話者 | セリフ | 読み | 感情/速度 |
|----|------|--------|------|-----------|
| `VO_altC_guest_01` | 常連客 | ミサキさん、あのボトルまだある？去年入れたやつ | ミサキさん、あのボトルまだある？きょねんいれたやつ | 気さくな無茶振り・普通速 |
| `VO_altC_misaki_01` | ミサキ | もちろんです | もちろんです | 余裕・あたたかい・ゆっくり・低め |
| `VO_altC_misaki_02` | ミサキ | お客様の一本、忘れませんよ | おきゃくさまのいっぽん、わすれませんよ | 品と自信・微笑み含み |
| `VO_altC_staff_01` | 若手スタッフ(小声) | …Bottle Scanner、さすがだ | …ボトルスキャナー、さすがだ | 感心・小声 |

## DomoAIプロンプト差分（主要ショット）

### C05 ─ ミサキがスキャンして即発見（★ / 0:15–0:20）
```
Cinematic over-the-shoulder shot of a poised Japanese woman in her late 30s, elegant bob
haircut, sharp black vest over white shirt, calmly and confidently holding up a smartphone
toward a wall of kept whisky bottles with a serene knowing smile, cool mint-cyan screen glow
mixing with warm amber, inside an upscale whisky bar at night, brass, bottle bokeh, brighter
uplifting lighting,
```
### C07 ─ ミサキの品ある一言（0:24–0:28）
```
Cinematic close-up of a poised late-30s Japanese woman bar manager with an elegant bob, sharp
black vest, offering a warm confident smile as she presents a whisky bottle, refined
hospitality, inside an upscale whisky bar at night, warm happy lighting, brass, bottle bokeh,
```
> AR枠・トーストは共通SVG（`../assets/png/`）。通知音ピロンはC05のスキャン成功に同期。

## 音・演出メモ
- BGMは大人っぽく落ち着いたジャジー。ミサキの余裕を音でも支える。
- オチのC07は「記憶力の凄さ」に見せて、最後にそっと画面を見せ“実は道具”と分かる粋な引き。
