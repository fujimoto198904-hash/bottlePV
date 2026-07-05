# 01 ─ プロダクション・バイブル

「Bottle Scanner」ショートドラマの企画・世界観・キャラクター・ライティングの共通仕様。
**全ショットのプロンプトはここで定義した記述子を共通適用する。** ここがブレると一貫性が崩れる。

---

## 1. 企画コンセプト

| 項目 | 内容 |
|------|------|
| プロダクト | **Bottle Scanner**（ボトルキープをARで一瞬で探せるアプリ） |
| ターゲット | Bar・スナック・居酒屋の店舗オーナー／スタッフ、飲食DXに関心のある層 |
| 課題（Before） | 何十本ものボトルキープから目的の1本を探すのに時間がかかる。新人は特に苦戦し、接客が止まる |
| 提供価値（After） | カメラをかざすだけでARが目的のボトルを即特定。**「探す時間」を「おもてなしの時間」に変える** |
| 感情設計 | 共感（新人あるある）→ 焦り → ひらめき → **爽快な解決** → 信頼獲得の小さなオチ |
| トーン | 実写シネマティック。上質・あたたかい・少しユーモラス（コミカルに寄せすぎない） |
| CTA | 「詳しくはプロフィールから」（SNSプロフィール導線） |

---

## 2. キャッチコピー / メッセージ

- **メインコピー**：探す時間を、おもてなしの時間に。
- サブ：Bottle Scanner ─ ボトルキープ、もう迷わない。
- CTA：詳しくはプロフィールから

---

## 3. キャラクターシート（★全プロンプト共通・改変厳禁）

実写AIドラマの一貫性は「毎回まったく同じ外見記述子を貼る」ことで守る。
DomoAI/画像生成では以下の英語トークンを**そのままコピペ**で使う（`03_domoai-prompts.md` が全ショット組み込み済み）。

### KENJI（ケンジ／Bar新人スタッフ・20代）
- 役割：緊張しがちな新人。成長して信頼を勝ち取る主人公
- 表情アーク：緊張 → パニック（焦り）→ ひらめき → 安堵 → 自信
- **英語トークン（KENJI_TOKEN）**：
  ```
  a Japanese man in his mid-20s, short neat black hair, clean-shaven, slim build,
  wearing a crisp white dress shirt with rolled sleeves and a fitted black waistcoat,
  a black bartender apron, youthful earnest face
  ```

### MANAMI（マナミ／常連客・30代）
- 役割：上品な常連。ラストの「頼りになる」でオチをつける
- 表情アーク：くつろぎ → さりげなく時間を気にする → あたたかい笑顔
- **英語トークン（MANAMI_TOKEN）**：
  ```
  an elegant Japanese woman in her early 30s, shoulder-length wavy dark-brown hair,
  refined natural makeup, wearing a deep wine-red silk blouse, seated at the bar counter,
  a whisky glass in front of her, warm and composed
  ```

### TAKASHI（タカシ／ベテラン店長・40代後半）
- 役割：見守る店長。心配 → 満足げにうなずく
- 表情アーク：気づく → 眉をひそめる（心配）→ 満足げなうなずき
- **英語トークン（TAKASHI_TOKEN）**：
  ```
  a distinguished Japanese man in his late 40s, short salt-and-pepper hair,
  a well-groomed short grey beard, wearing a black shirt and a dark sommelier apron,
  calm and experienced expression
  ```

---

## 4. 舞台設定（★全プロンプト共通）

- 夜の上質なウイスキーBar。常連が集う落ち着いたカウンター
- 磨かれたダークウッドのカウンター、真鍮の金具、間接照明
- 背後の棚：**ボトルキープの壁**。何十本ものウイスキーボトルが並び、各本に小さなネームタグ
- 背景にボトルのボケ（bokeh）、しっとりした空気感

**英語トークン（SET_TOKEN）**：
```
inside an upscale intimate Japanese whisky bar at night, dark polished wood counter,
brass fixtures, a large back-shelf wall filled with rows of kept whisky bottles each
with a small paper name tag, warm bottle bokeh in the background, moody low-key ambience
```

---

## 5. ライティング／カラー指針（感情に連動）

| 区間 | ライティング | 意図 |
|------|------------|------|
| シーン1〜2（0:00–0:18） | **低照度・暖色寄りで影多め**。ケンジに軽い緊張の陰影 | 不安・焦りの空気 |
| シーン3・スキャン瞬間（0:18–0:24） | **スキャン成功でパッと明るく**。ミント/シアンのUI光が顔に差す | 暗→明の反転でカタルシス |
| シーン4（0:24–0:32） | **あたたかく明るい**。安心と信頼のトーン | 解決・信頼獲得 |
| シーン5 CTA（0:32–0:35） | ブランドカラーのクリーンな画面 | 想起・行動喚起 |

### ブランドカラー
| 用途 | 色 | HEX |
|------|-----|-----|
| プライマリ（おもてなし・暖色） | アンバーゴールド | `#E8B451` |
| アクセント（スキャナのテック色） | ミント／シアン | `#3FE0C5` |
| 背景ダーク | チャコール | `#14110E` |
| 文字（明） | オフホワイト | `#F5EFE6` |

> ブランドストーリー：**アンバー＝おもてなしの温かさ / ミント＝スキャナのテック**。
> 「テックが、奪われていた“おもてなしの時間”を取り戻す」を配色で表現。

---

## 6. スタイルサフィックス（★全keyframe画像プロンプト末尾に共通付与）

**STYLE_SUFFIX**：
```
shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade,
warm amber tungsten key light, low-key moody lighting, shallow depth of field,
subtle film grain, photorealistic, ultra detailed skin texture,
vertical 9:16 composition, professional cinematography, 8k
```

**NEGATIVE_PROMPT（共通）**：
```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin,
extra fingers, deformed hands, mutated hands, distorted face, cross-eyed,
text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash,
low quality, blurry, jpeg artifacts, duplicated person
```

---

## 7. 演出メモ（台本より・納品品質の肝）

1. **シーン2の「焦り」はコミカルに寄せすぎない**。ドタバタではなく“新人あるある”のリアルな焦り＝汗・視線の泳ぎ・小さな早口。共感が強くなる。
2. **シーン3の「見つかった瞬間」**は暗→明のライティング反転＋軽快SEでギャップを作る＝気持ちよさ。
3. **マナミの「頼りになる」**がケンジの成長・信頼構築を示す小さなオチ。ここは笑顔をしっかり見せる。
4. **AR画面**はAI生成に頼らず `assets/ar-scan-overlay.svg` をFCPXで重ねる（ブランドUIの精度確保）。
5. **カット割りは基本ハードカット**（ドラマのテンポ）。CTAのみフェードイン。

---

## 8. 尺配分サマリ（詳細は `02_shot-list.md`）

| シーン | 区間 | 内容 | ショット |
|-------|------|------|---------|
| 1 | 0:00–0:08 | 注文を受ける → ボトルの壁で固まる | SHOT01–02 |
| 2 | 0:08–0:18 | ラベルを探す焦り／マナミ・タカシの反応 | SHOT03–05 |
| 3 | 0:18–0:24 | スマホでBottle Scanner起動 → AR発見 | SHOT06–07 |
| 4 | 0:24–0:32 | 迷わず提供／「頼りになる」 | SHOT08–09 |
| 5 | 0:32–0:35 | ロゴ＋キャッチコピー（CTA） | SHOT10 |
