# スラッシュコマンドのオプション説明
IMAGINE_DESCRIPTION = "Stable Diffusionを使用して画像を生成します。"
ATTACHMENT_OPTION_DESC = "画像生成に使用する画像を添付してください。"
PROMPT_OPTION_DESC = "画像生成に使用するプロンプトを入力してください。(英語のみ)"
NEGATIVE_PROMPT_OPTION_DESC = "画像生成に使用するネガティブプロンプトを入力してください。(英語のみ)"
IMAGE_STRENGTH_OPTION_DESC = "画像の強制力を、0.00～1.00の範囲で入力してください。デフォルト値は0.35です。(値が大きいほど、画像に厳密に従います)"
CFG_SCALE_OPTION_DESC = "プロンプトの強制力を、0.0～35.0の範囲で入力してください。デフォルト値は7です。(値が大きいほど、プロンプトに厳密に従います)"
CLIP_GUIDANCE_PRESET_OPTION_DESC = "画像生成に使用するガイダンスのプリセットを、選択肢から選んでください。デフォルト値は指定なしです。"
ASPECT_OPTION_DESC = "生成する画像のサイズを、選択肢から選んでください。デフォルト値は1:1です。"
STYLE_OPTION_DESC = "生成する画像のスタイルを、選択肢から選んでください。デフォルト値は指定なしです。"
SAMPLER_OPTION_DESC = "拡散プロセスにどのサンプラーを使用するか、選択肢から選んでください。指定が無ければ最適なサンプラーが自動選択されます。"
SEED_OPTION_DESC = "ランダムノイズシードを0～4294967295の範囲で入力してください。空欄の場合は自動採番されます。"
MODEL_OPTION_DESC = "画像生成に使用するStable Diffusionモデルの種類を、選択肢から選んでください。"

# エラーメッセージ
ERROR_PROMPT_DETECTED = "不適切なプロンプトが検出されたため、実行を中断しました。"
ERROR_SYSTEM = "システムエラーが発生したため、実行を中断しました。"
ERROR_RETRY = "時間を置いて再度お試しください。"
ERROR_NSFW = "NSFWコンテンツが検出されたため、{}枚の画像が除外されています。"

# フッターメッセージ
FOOTER_PROMPT_ENGLISH = "プロンプトは英語で入力してください。\nまた、NSFWコンテンツを生成することは禁止されています。"
STABILITY_AI_LOGO_URL = "https://images.squarespace-cdn.com/content/v1/646b4513dbebfb2c0adc2b52/1684751740466-5T0GG85P7CVA04C4SKKB/StabilityAi_Logo_White-19.png"