#!/bin/bash
# PV音声 再生成スクリプト（Irodori / 方式B＝同一caption+seed直生成）
# 実行: cd ~/Irodori-TTS && bash <このスクリプト>
# 出力: ~/Irodori-TTS/pv_voices/final3/*.wav（納品は別途 -3dB/48k/24bit 変換して voice-exports/ へ）
# 詳細・provenance: bottlePV videogen/audio/VOICES.md
set -u
cd "$HOME/Irodori-TTS" || { echo "Irodori-TTS が無い"; exit 1; }
export PYTORCH_ENABLE_MPS_FALLBACK=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
OUT=pv_voices/final3; mkdir -p "$OUT"

KCAP="少し高めで若々しい、20代前半の男性の声。まだ硬さの残る初々しさがあり、緊張するとわずかに上ずる。息を多めに含み、早口になりがちだが、根は明るく素直で一生懸命。作りこんだ演技ではなく等身大の自然な話し方で、ほんの少しかすれた生っぽさがある。目の前の相手に真っ直ぐ応えるように話す。"
MCAP="落ち着いた30代の女性の声。中〜やや低めのピッチで、上品でありながら気取らない。ゆったりと余裕があり、ささやくような息づかいをわずかに含む。あたたかく親密で、たった一人にそっと語りかけるような近い距離感。作為のない自然体で、少しハスキーな陰影と大人の落ち着いた色気がにじむ。"
TCAP="低く落ち着いた40代後半の男性の声。渋みと深みがありながら輪郭は明瞭で聞き取りやすい。長く現場に立ってきた余裕と包容力があり、抑えたトーンでゆっくり気遣うように話す。威圧感は一切なく、あたたかく諭すような柔らかさ。ざらついた息をわずかに含む生身の質感。"
NCAP="ブランドナレーション向けの女性の声。落ち着いてクリアで信頼感がある。上質で温かく、少し低めのしっとりした響き。押し付けず丁寧に語りかける、洗練された大人のトーン。作りすぎない自然な息づかいを含む。"
TR="silenceremove=start_periods=1:start_threshold=-50dB:detection=peak,areverse,silenceremove=start_periods=1:start_threshold=-50dB:detection=peak,areverse"

gen() { # caption seed ds text out
  echo ">> $5"
  uv run --no-sync python infer.py --hf-checkpoint Aratako/Irodori-TTS-600M-v3-VoiceDesign --no-ref \
    --model-device mps --model-precision fp32 --codec-device mps \
    --num-steps 40 --t-schedule-mode sway --sway-coeff -1.0 \
    --seed "$2" --duration-scale "$3" --caption "$1" --text "$4" \
    --output-wav "$OUT/$5.wav" >"$OUT/$5.log" 2>&1 || { echo "   FAIL"; return; }
  ffmpeg -y -i "$OUT/$5.wav" -af "$TR" "$OUT/$5.t.wav" >/dev/null 2>&1 && mv "$OUT/$5.t.wav" "$OUT/$5.wav"
}

gen "$MCAP" 9030679349209590968 0.72 "いつものボトル、お願いできる？やまざきの…"        VO_S1_manami_01
gen "$KCAP" 7733634242191095402 0.8  "あ、はい！少々お待ちください！"                    VO_S1_kenji_01
gen "$KCAP" 7733634242191095402 0.8  "え、どれだっけ…先週も探したのに"                   NA_S2_kenji_01
gen "$TCAP" 1185207036886487931 0.9  "ケンジ、大丈夫か？"                                 VO_S2_takashi_01
gen "$KCAP" 7733634242191095402 0.85 "あった！"                                           VO_S3_kenji_01
gen "$KCAP" 7733634242191095402 0.85 "お待たせしました、やまざきです"                     VO_S4_kenji_01
gen "$MCAP" 9030679349209590968 0.9  "早いね、ケンジ君。頼りになる"                       VO_S4_manami_01
gen "$NCAP" 1959243235121053001 0.85 "ボトルスキャナー。探す時間を、おもてなしの時間に。" NA_S5_narrator_01
echo "DONE -> $OUT"
