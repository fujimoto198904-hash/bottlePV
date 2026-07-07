"""
jobs.py — Bottle Scanner PV の映像生成ジョブグラフ（自己完結データ）

このモジュールは 35 秒 PV の映像素材（実写シネマティック・9:16）を生成するための
「全ジョブの設計図」を Python データとして保持する。プロンプト本文は元ブリーフ
（bottle-scanner-video/01_production-bible.md, 02_shot-list.md, 03_domoai-prompts.md,
09_domoai-generation-brief.md）から**そのまま転記**してあり、Chrome 操作の担当者
（人間 or claude-in-chrome）がそのままコピペで貼れる。

ジョブは 3 段（Irodori の build-manifest → generate → stitch の映像版）:
  Stage 1  base_face : 3 人の基準顔を T2I で作る（キャラ一貫性の源）
  Stage 2  still     : 基準顔を編集して各ショットの状況静止画（9:16）にする
  Stage 3  clip      : 各静止画を I2V で動かす（尺 3〜5 秒・9:16）

命名規則（DOMOAI-CHAT-BRIEF.md 準拠）:
  base_{kenji|manami|takashi}.png / still_SHOT{nn}.png / SHOT{nn}_{slug}.mp4
"""
from __future__ import annotations

# ── 共通トークン（01_production-bible.md より） ─────────────────────────────

ASPECT = "9:16"  # 全ジョブ縦型 1080x1920

# 基準顔（T2I）用ネガティブ（09_domoai-generation-brief.md）
NEG_BASE = (
    "cartoon, anime, illustration, 3d, cgi, plastic skin, extra fingers, "
    "deformed hands, distorted face, text, watermark, low quality, blurry"
)

# 静止画・動画共通ネガティブ（01_production-bible.md §6）
NEG_SCENE = (
    "cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy skin, "
    "extra fingers, deformed hands, mutated hands, distorted face, cross-eyed, "
    "text, watermark, logo, subtitles, oversaturated, flat lighting, harsh flash, "
    "low quality, blurry, jpeg artifacts, duplicated person"
)

# ── Stage 1: 基準顔 3 枚（T2I） ─────────────────────────────────────────────

CHARACTERS = {
    "kenji": {
        "label": "ケンジ（新人・20代男）",
        "prompt": (
            "Photorealistic portrait of a Japanese man in his mid-20s, short neat black hair, "
            "clean-shaven, slim, youthful earnest face, wearing a crisp white dress shirt and a "
            "fitted black waistcoat with a black bartender apron, warm soft lighting, simple dark "
            "neutral background, natural detailed skin texture, sharp focus on the face, "
            "85mm portrait lens, cinematic, high detail"
        ),
    },
    "manami": {
        "label": "マナミ（常連・30代女）",
        "prompt": (
            "Photorealistic portrait of an elegant Japanese woman in her early 30s, shoulder-length "
            "wavy dark-brown hair, refined natural makeup, wearing a deep wine-red silk blouse, warm "
            "composed expression, soft flattering lighting, simple dark neutral background, natural "
            "detailed skin texture, sharp focus on the face, 85mm portrait lens, cinematic, high detail"
        ),
    },
    "takashi": {
        "label": "タカシ（店長・40代後半男）",
        "prompt": (
            "Photorealistic portrait of a distinguished Japanese man in his late 40s, short "
            "salt-and-pepper hair, a well-groomed short grey beard, wearing a black shirt and a dark "
            "sommelier apron, calm experienced expression, warm soft lighting, simple dark neutral "
            "background, natural detailed skin texture, sharp focus on the face, 85mm portrait lens, "
            "cinematic, high detail"
        ),
    },
}

# ── Stage 2+3: 9 ショット（KEYFRAME 静止画 + I2V MOTION） ───────────────────
# prompt      = 03_domoai-prompts.md の KEYFRAME（トークン展開済み・そのまま貼れる）
# motion      = 03_domoai-prompts.md の I2V MOTION
# characters  = 一貫性参照に使う基準顔（先頭が主役＝命名に使用）
# duration_s  = 02_shot-list.md の尺

SHOTS = [
    {
        "shot": "SHOT01",
        "slug": "manami-order",
        "characters": ["manami"],
        "duration_s": 4,
        "summary": "establishing / マナミの穏やかな注文",
        "prompt": (
            "Cinematic medium shot, an elegant Japanese woman in her early 30s, shoulder-length wavy "
            "dark-brown hair, refined natural makeup, wearing a deep wine-red silk blouse, seated at "
            "the bar counter with a whisky glass in front of her, warm and composed, gently placing an "
            "order, inside an upscale intimate Japanese whisky bar at night, dark polished wood counter, "
            "brass fixtures, a large back-shelf wall filled with rows of kept whisky bottles each with a "
            "small paper name tag, warm bottle bokeh in the background, moody low-key ambience, shot on "
            "ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm amber tungsten key light, "
            "low-key moody lighting, shallow depth of field, subtle film grain, photorealistic, ultra "
            "detailed skin texture, vertical 9:16 composition, professional cinematography, 8k"
        ),
        "motion": (
            "slow subtle dolly-in toward the woman, she calmly speaks and gives a small warm gesture, "
            "gentle candle flicker on the bottles behind, very subtle head movement, cinematic, "
            "minimal camera shake, natural micro-expressions"
        ),
    },
    {
        "shot": "SHOT02",
        "slug": "kenji-freeze",
        "characters": ["kenji"],
        "duration_s": 4,
        "summary": "ケンジが棚を振り返りボトルの壁で固まる",
        "prompt": (
            "Cinematic bust shot from behind the bar, a Japanese man in his mid-20s, short neat black "
            "hair, clean-shaven, slim build, wearing a crisp white dress shirt with rolled sleeves and a "
            "fitted black waistcoat and a black bartender apron, youthful earnest face, just turned "
            "around to face a huge back-shelf wall filled with dozens of rows of kept whisky bottles each "
            "with a small paper name tag, his expression stiffening with quiet panic, overwhelmed, inside "
            "an upscale intimate Japanese whisky bar at night, dark polished wood counter, brass fixtures, "
            "warm bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, warm "
            "amber tungsten key light, low-key moody lighting, shallow depth of field, subtle film grain, "
            "photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional "
            "cinematography, 8k"
        ),
        "motion": (
            "the young bartender turns his head toward the bottle wall then freezes, rack focus from his "
            "face to the overwhelming wall of bottles behind, tiny nervous swallow, subtle breathing, "
            "very slight handheld feel, cinematic, no large movement"
        ),
    },
    {
        "shot": "SHOT03",
        "slug": "kenji-checking",
        "characters": ["kenji"],
        "duration_s": 4,
        "summary": "ラベルを一本ずつ確認する焦り（手元クロース）",
        "prompt": (
            "Cinematic close-up of a Japanese man in his mid-20s, short neat black hair, clean-shaven, in "
            "a white dress shirt with rolled sleeves and black waistcoat, his finger tracing along the "
            "small paper name tags of kept whisky bottles on a shelf, eyes darting nervously, a faint "
            "sweat on his forehead, growing anxiety, inside an upscale whisky bar at night, dark wood, "
            "brass, warm bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color "
            "grade, warm amber tungsten key light, low-key moody lighting, shallow depth of field, subtle "
            "film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, "
            "professional cinematography, 8k"
        ),
        "motion": (
            "his finger slides across the bottle name tags one by one, eyes flicking left and right with "
            "rising worry, subtle nervous breathing, tiny handheld camera sway to build tension, cinematic, "
            "small realistic movements only"
        ),
    },
    {
        "shot": "SHOT04",
        "slug": "manami-glance",
        "characters": ["manami"],
        "duration_s": 3,
        "summary": "マナミがチラッと時間を見る",
        "prompt": (
            "Cinematic close-up of an elegant Japanese woman in her early 30s, wavy dark-brown hair, "
            "wine-red silk blouse, seated at a bar counter, glancing down at her wristwatch with a subtle "
            "patient look, not annoyed, refined, inside an upscale whisky bar at night, warm amber "
            "lighting, brass fixtures, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic "
            "film color grade, warm amber tungsten key light, low-key moody lighting, shallow depth of "
            "field, subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 "
            "composition, professional cinematography, 8k"
        ),
        "motion": (
            "she subtly lowers her eyes to check the time then looks back up toward the bar, a small "
            "patient breath, very gentle movement, warm candle flicker, cinematic, minimal motion"
        ),
    },
    {
        "shot": "SHOT05",
        "slug": "takashi-concern",
        "characters": ["takashi", "kenji"],  # 主役=takashi、奥にケンジをボケ
        "duration_s": 3,
        "summary": "タカシが気づいて小声で気遣う（奥にケンジ）",
        "prompt": (
            "Cinematic shot of a distinguished Japanese man in his late 40s, short salt-and-pepper hair, a "
            "well-groomed short grey beard, wearing a black shirt and dark sommelier apron, standing a "
            "little apart behind the bar, glancing with a slightly furrowed concerned brow toward a young "
            "bartender blurred in the background, inside an upscale whisky bar at night, warm amber "
            "lighting, brass, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color "
            "grade, warm amber tungsten key light, low-key moody lighting, shallow depth of field, subtle "
            "film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, "
            "professional cinematography, 8k"
        ),
        "motion": (
            "the veteran manager notices, brow furrows slightly with concern, he leans in a touch and "
            "speaks quietly, very subtle head turn toward the younger staff, cinematic, small realistic "
            "movement"
        ),
    },
    {
        "shot": "SHOT06",
        "slug": "kenji-idea",
        "characters": ["kenji"],
        "duration_s": 3,
        "summary": "ひらめいてスマホを取り出す",
        "prompt": (
            "Cinematic close-up of a Japanese man in his mid-20s, short neat black hair, white dress shirt "
            "and black waistcoat, a sudden spark of realization on his face, reaching into his apron pocket "
            "to pull out a smartphone, inside an upscale whisky bar at night, warm amber lighting starting "
            "to mix with a faint cool phone-screen glow on his face, brass, bottle bokeh, shot on ARRI "
            "Alexa, 35mm anamorphic lens, cinematic film color grade, shallow depth of field, subtle film "
            "grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional "
            "cinematography, 8k"
        ),
        "motion": (
            "his eyes light up with an idea, he quickly pulls a smartphone from his pocket and raises it, a "
            "faint cool glow begins to touch his face, decisive small movement, cinematic, natural motion"
        ),
    },
    {
        "shot": "SHOT07",
        "slug": "kenji-scan",
        "characters": ["kenji"],
        "duration_s": 3,
        "summary": "★ヒーローショット AR発見（スマホ画面はFCPXでUI合成／余白を残す）",
        "prompt": (
            "Cinematic over-the-shoulder shot of a Japanese man in his mid-20s, white dress shirt and "
            "black waistcoat, holding up a smartphone toward a wall of kept whisky bottles, his face lit "
            "brighter now with a cool mint-cyan glow from the screen mixing with warm amber, an expression "
            "of relief and delight beginning, the bottle shelf in front sharp and inviting, inside an "
            "upscale whisky bar at night, brass, bottle bokeh, shot on ARRI Alexa, 35mm anamorphic lens, "
            "cinematic film color grade, brighter uplifting lighting, shallow depth of field, subtle film "
            "grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional "
            "cinematography, 8k"
        ),
        "motion": (
            "he holds the phone steady toward the shelf, his face brightens into relief and a small smile, "
            "the lighting subtly lifts from dark to bright, a gentle push-in toward the target bottle, "
            "cinematic, smooth minimal motion, leave clean space on the phone screen for a UI overlay"
        ),
    },
    {
        "shot": "SHOT08",
        "slug": "kenji-serve",
        "characters": ["kenji"],
        "duration_s": 4,
        "summary": "ボトルを取りカウンターへ提供（自信）",
        "prompt": (
            "Cinematic medium shot of a Japanese man in his mid-20s, white dress shirt and black waistcoat "
            "and bartender apron, confidently taking a specific whisky bottle from the shelf and setting it "
            "down on the polished bar counter in front of a customer, self-assured posture, inside an "
            "upscale whisky bar at night, warm and now brighter inviting lighting, brass, bottle bokeh, "
            "shot on ARRI Alexa, 35mm anamorphic lens, cinematic film color grade, shallow depth of field, "
            "subtle film grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, "
            "professional cinematography, 8k"
        ),
        "motion": (
            "he decisively takes the bottle, turns and places it gently on the counter with a confident "
            "motion, a slight professional nod, warmer brighter light, cinematic, smooth natural movement"
        ),
    },
    {
        "shot": "SHOT09",
        "slug": "manami-thanks",
        "characters": ["manami", "takashi"],  # 主役=manami、奥にタカシのうなずき
        "duration_s": 4,
        "summary": "マナミの笑顔／奥でタカシのうなずき（オチ）",
        "prompt": (
            "Cinematic close-up of an elegant Japanese woman in her early 30s, wavy dark-brown hair, "
            "wine-red silk blouse, seated at the bar, looking up with a genuine warm delighted smile, and "
            "softly out of focus in the background a distinguished late-40s Japanese man with "
            "salt-and-pepper hair and grey beard in a black shirt nodding with quiet satisfaction, inside "
            "an upscale whisky bar at night, warm bright happy lighting, brass, bottle bokeh, shot on ARRI "
            "Alexa, 35mm anamorphic lens, cinematic film color grade, shallow depth of field, subtle film "
            "grain, photorealistic, ultra detailed skin texture, vertical 9:16 composition, professional "
            "cinematography, 8k"
        ),
        "motion": (
            "the woman looks up and breaks into a warm genuine smile, in the soft background the veteran "
            "manager gives a small satisfied nod, gentle warm ambience, cinematic, natural "
            "micro-expressions, minimal camera motion"
        ),
    },
]


def build_job_graph() -> list[dict]:
    """全ジョブ（base 3 + still 9 + clip 9 = 21）をフラットな辞書リストで返す。

    各ジョブは manifest.py がステータス等を付与する前の「不変な設計データ」。
    """
    jobs: list[dict] = []

    # Stage 1: 基準顔
    for name, c in CHARACTERS.items():
        jobs.append({
            "id": f"base_{name}",
            "kind": "base_face",
            "stage": 1,
            "character": name,
            "characters": [name],
            "shot": None,
            "label": c["label"],
            "prompt": c["prompt"],
            "negative": NEG_BASE,
            "aspect_ratio": ASPECT,
            "duration_s": None,
            "output": f"base_{name}.png",
            "depends_on": [],
            "reference_images": [],  # T2I なので参照なし（ここで顔が決まる）
        })

    # Stage 2: 状況静止画（基準顔を編集して配置）
    for s in SHOTS:
        primary = s["characters"][0]
        refs = [f"base_{c}.png" for c in s["characters"]]
        jobs.append({
            "id": f"still_{s['shot']}",
            "kind": "still",
            "stage": 2,
            "character": primary,
            "characters": s["characters"],
            "shot": s["shot"],
            "label": s["summary"],
            "prompt": s["prompt"],
            "negative": NEG_SCENE,
            "aspect_ratio": ASPECT,
            "duration_s": None,
            "output": f"still_{s['shot']}.png",
            "depends_on": [f"base_{c}" for c in s["characters"]],
            "reference_images": refs,  # 一貫性の要：基準顔を参照として渡す
        })

    # Stage 3: I2V クリップ
    for s in SHOTS:
        refs = [f"base_{c}.png" for c in s["characters"]]
        jobs.append({
            "id": f"clip_{s['shot']}",
            "kind": "clip",
            "stage": 3,
            "character": s["characters"][0],
            "characters": s["characters"],
            "shot": s["shot"],
            "label": s["summary"],
            "prompt": s["motion"],           # I2V は動作プロンプト
            "negative": NEG_SCENE,
            "aspect_ratio": ASPECT,
            "duration_s": s["duration_s"],
            "output": f"{s['shot']}_{s['slug']}.mp4",
            "depends_on": [f"still_{s['shot']}"],
            # 静止画 + 基準顔シートを I2V に渡して identity を再アンカー
            "reference_images": [f"still_{s['shot']}.png"] + refs,
        })

    return jobs


# 期待される最終成果物の枚数（QA 用の完了条件）
EXPECTED = {"base_face": 3, "still": 9, "clip": 9}
