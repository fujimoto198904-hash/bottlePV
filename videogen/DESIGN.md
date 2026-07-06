# DESIGN ― videogen アーキテクチャ意思決定記録

Bottle Scanner PV の映像クリップ生成システムの設計判断を、実データ調査（2026-07）に基づいて記録する。

---

## 1. Irodori は音声専用（(a)却下の技術的理由）

`~/Irodori-TTS` は日本語TTS `Aratako/Irodori-TTS-600M-v3-VoiceDesign`。中核は
`TextToLatentRFDiT` = **音声コーデック潜在（DACVAE 32次元）上のRectified-Flow拡散Transformer**。
入出力テンソル・トークナイザ・損失がすべて音声コーデック形。空間2D/3D潜在もピクセルVAEも
時間フレームモデルも無い。**映像化＝別モデルクラスをゼロ学習**する話で、Apple Silicon/MPSでは
学習も実用推論も非現実的。→ Irodori本体の改造(a)からは何も得られない。

**再利用するのはモデルでなく“tsuki”オーケストレーション設計**（`tsuki_narrate.py` /
`tsuki_noise.py` / `tsuki_watcher/watcher.py`）。これがこの `videogen/` の設計元。

---

## 2. ハーネス対応表（Irodori → videogen）

| Irodori（音声） | videogen（映像） | 実装 |
|---|---|---|
| `script.txt`（1行=1セグメント） | ジョブグラフ（3顔+9静止画+9クリップ） | `pipeline/jobs.py` |
| `manifest.jsonl` | `manifest.json` | `pipeline/manifest.py` |
| `derived_seed(id)`（id sha1で決定的） | 同方式の `derived_seed` | `manifest.py` |
| `text_hash`/`voice_hash` キャッシュ | `job_hash`（prompt/参照/尺/aspect） | `manifest.py` |
| `generate`（TTS推論） | Web UI操作 or API呼び出しでT2I/編集/I2V | バックエンド（下記§4） |
| `tsuki_noise.py`（波形ノイズ検知→再生成） | **顔一貫性ガード**（顔埋め込みcosine→再生成） | `pipeline/faceguard.py` |
| `stitch`前のSR/長さ検証 | 9:16/尺の機械検証 | `pipeline/validate.py` |
| 完成物だけアトミック納品(Drive) | approvedクリップをアトミック納品(domoai-exports) | `pipeline/deliver.py` |
| watcher（フォルダ監視・直列FIFO） | （将来）manifest監視で自動投入 | 未実装（土台では手動 `next`） |

位相はそのまま、`generate` 段だけ差し替えたのが本システム。

---

## 3. 一貫性戦略（本件の成否）

調査の一致点：**どの動画モデルも別々の生成をまたいで顔を覚えていない**。よって
同一人物性は **③I2Vでなく①②の静止画段で解く**。

1. 各キャラの基準顔を **凍結**（`base_*.png`、`job_hash`でバージョンピン、手承認）
2. 各ショットの静止画は基準顔を**参照として渡して編集**（「顔をImage1と同一に保て」）
3. **静止画を人手承認してからアニメ化**（静止画は安く作り直せる最後の完全制御点）
4. I2Vには静止画＋基準顔シートを渡し identity を再アンカー
5. **顔ガード**（`faceguard.py`）が静止画とクリップ代表フレームを基準顔とcosine比較、
   閾値割れは別seed/テイクで再生成 → ダメなら `needs_review` で人手へ

manifest の `reference_images` が各ジョブに「どの基準顔を参照に渡すか」を保持している。

**難所（リスク）**：極端なポーズ/照明での顔ドリフト、衣装/小物のドリフト（顔より崩れやすい）、
**2キャラ同居フレーム（SHOT05, SHOT09）が最難**。→ 多めに作って選別、衣装/セットも参照に。

---

## 4. 生成バックエンド（差し替え可能な(c)）

ハーネスはバックエンド非依存。現在の選択と、実データ調査で判明した代替を記録する。

### 4.1 採用：Chrome操作（Web UI）
ログイン済みChromeでWeb UIを操作。API課金なし。手順は
[chrome_control/PLAYBOOK.md](chrome_control/PLAYBOOK.md)。
- **DomoAIのWeb UIはT2I＋Nano Banana Pro画像編集＋image2videoを持つ**ので、
  ①②③を1ツールで回せる（＝既存ブリーフの流れと一致）。
- **既知のトレードオフ**：DomoAIのToSはbot自動化・スクレイピングを明文で禁止（BANリスク）。
  SPA/キュー/Cloudflareで自動化は不安定。半自動（人が最終操作、Claudeが下書き/整理）推奨。

### 4.2 代替（API化する場合の推奨スタック）※将来 `pipeline/backends/` に実装
API鍵を用意すれば、ハーネスの `generate` 段をAPI呼び出しに替えるだけで移行できる。
2026-07時点の調査結論：

| 段 | 推奨 | 補欠 | 実費目安 |
|---|---|---|---|
| ①T2I 基準顔 | Nano Banana Pro (Gemini 3 Pro Image) | Seedream 4.5 / Flux Kontext | ~$0.13/枚 |
| ②編集 配置 | Nano Banana Pro 多画像編集 | Seedream 4.5（新環境配置が強い） | ~$0.04/枚 |
| ③I2V | Kling O1 Reference-to-Video (fal、参照最大7・9:16) | Hailuo S2V / Luma Ray3 / Veo3.1 Fast | ~$0.112/秒 |
| 基盤 | **fal.ai** 単一鍵（上記を網羅） | Replicate（Luma/Runway用） | 従量・月額なし |

- 全体一発 **~$15–25**（再生成込みでも$30未満）。従量課金。
- Runway Gen-4 References は一貫性が理論上最良だが公式RESTが2026-01からEnterprise限定 →
  当てにせずReplicate経由の補欠扱い。
- **キャラは全員AI創作の架空人物**なのでNano Banana/VeoのGoogle系も使用可
  （実在人物の写実生成は各社が拒否するため、架空なら制約なし）。
  → 実写の実在人物顔をベースにする場合はGoogle系不可、Seedream/Kling系に限定。

### 4.3 バックエンド差し替え点
`manifest.json` の各ジョブは backend 非依存の設計データ（prompt/negative/参照/尺/aspect/出力名）を
持つ。API化は「pending ジョブを読む → API submit/poll → output/ に保存 → status更新」の
アダプタを1個足すだけ。検証・顔ガード・納品・命名は共通のまま。

---

## 5. リスクと緩和

| リスク | 緩和 |
|---|---|
| 別生成間の顔ドリフト（最重要） | 静止画段で顔固定＋人手承認、顔ガード再生成、衣装/セットも参照に |
| 2キャラ同居（S05/S09） | 多めに生成し選別。API化時はKling/Vidu多参照へ |
| I2Vの非決定性（DomoAIはseed非公開） | 再生成ガードが主機能。seed対応ツールでは決定的seedを固定 |
| アスペクト事故（Veo16:9強制/Domo既定1:1） | `validate` で1080×1920/9:16を必ず確認。UIは9:16明示 |
| DomoAI ToS（自動化禁止・BAN） | Web UI自動化は半自動運用。完全自動化を望むなら公式API/他社APIへ |
| ベンダ変動（Runway Enterprise化・モデル改名） | manifestにツール/モデルを記録、代替を温存 |
| 固定5s/10s最小尺 | FCPXで3–5sにトリム（納品前提） |

---

## 6. ブランチ運用

- 本システムは `main` から切った `claude/videogen-chrome-pipeline` に自己完結で追加。
- **既存の `claude/pv-assets-subtitles-altversions`（PR #1）には一切触れない。**
- 生成物（`base_*.png`/`still_*.png`/`SHOT*.mp4`）は最終的に PR #1 側の
  `bottle-scanner-video/domoai-exports/` へ。`deliver --dest` でそのパスを指す。
