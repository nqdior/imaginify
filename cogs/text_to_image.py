import discord
import requests
import os, io, base64
from discord.ui import Button, View
from discord.ext import commands
from discord.commands import slash_command, Option
from dotenv import load_dotenv
from .common.options import model_options, sampler_options, aspect_ratio_options, style_preset_options, clip_guidance_preset_options

# 環境変数の読み込みと検証
load_dotenv()
API_HOST = os.getenv('API_HOST', 'https://api.stability.ai')
API_KEY = os.getenv("STABILITY_API_KEY")
if not API_KEY:
    raise EnvironmentError("Missing Stability API key.")

class IMAGINE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ### Imagineコマンドの実装
    @slash_command(name="imagine", description="Stable Diffusionを使用して画像を生成します。")
    async def imagine(self, ctx, 
                      prompt: Option(str, "画像生成に使用するプロンプトを入力してください。(英語のみ)", required=True),
                      negative_prompt: Option(str, "画像生成に使用するネガティブプロンプトを入力してください。(英語のみ)", required=False, default=""),
                      cfg_scale: Option(float, "プロンプトの強制力を、0.0～35.0の範囲で入力してください。デフォルト値は7です。(値が大きいほど、プロンプトに厳密に従います)", required=False, min_value=0.0, max_value=35.0),
                      clip_guidance_preset: Option(str, "画像生成に使用するガイダンスのプリセットを、選択肢から選んでください。デフォルト値は指定なしです。", choices=list(clip_guidance_preset_options.keys()), required=False, default="NONE"),
                      aspect: Option(str, "生成する画像のサイズを、選択肢から選んでください。デフォルト値は1:1です。", choices=list(aspect_ratio_options.keys()), required=False, default="square 1:1"),
                      style: Option(str, "生成する画像のスタイルを、選択肢から選んでください。デフォルト値は指定なしです。", choices=list(style_preset_options.keys()), required=False ,default="None"),
                      sampler: Option(str, "拡散プロセスにどのサンプラーを使用するか、選択肢から選んでください。指定が無ければ最適なサンプラーが自動選択されます。", choices=list(sampler_options.keys()), required=False),
                      seed: Option(int, "ランダムノイズシードを0～4294967295の範囲で入力してください。空欄の場合は自動採番されます。", required=False, min_value=0, max_value=4294967295),
                      model: Option(str, "画像生成に使用するStable Diffusionモデルの種類を、選択肢から選んでください。", choices=list(model_options.keys()), required=False, default="Stable Diffusion XL 1.0")
                      ):
        
        # ユーザーの入力を検証                  
        await ctx.defer()

        # 画像生成のリクエストJSONを作成
        width, height = aspect_ratio_options[aspect]
        json_data = {
            "text_prompts": [{"text": prompt, "weight": 1}] + ([{"text": negative_prompt, "weight": -1}] if negative_prompt else []),
            "height": height,
            "width": width,
            "samples": 4,
            "steps": 10,
            **({"cfg_scale": cfg_scale} if style != "None" else {}),
            **({"clip_guidance_preset": clip_guidance_preset}),
            **({"sampler": sampler} if sampler != "None" else {}),
            **({"style_preset": style_preset_options[style]} if style != "None" else {}),
            **({"seed": seed} if seed else {}),
        }

        # 画像生成のリクエストを送信
        response = requests.post(f"{API_HOST}/v1/generation/{model_options[model]}/text-to-image", headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, json=json_data)

        # 画像生成のリクエストが成功したかどうかを検証
        if response.status_code != 200:
            embed=discord.Embed(
                color=discord.Color.red(), 
                description="不適切なプロンプトが検出されたため、実行を中断しました。",
            )
            embed.set_footer(text=f"プロンプトは英語で入力してください。\nまた、NSFWコンテンツを生成することは禁止されています。")

            # エラーの場合、エラーメッセージを送信して終了
            await ctx.respond(embed=embed)
            return
        
        # 画像生成の結果を取得
        files = []
        seeds = ""
        nsfw_content_count = 0
        view = discord.ui.View()
        for i, image in enumerate(response.json().get("artifacts", [])):
            
            # NSFWコンテンツが検出された場合、画像を除外
            if "SUCCESS" != image.get("finishReason") :
                nsfw_content_count += 1
                continue

            files.append(discord.File(io.BytesIO(base64.b64decode(image["base64"])), filename=f"image{i}.png"))
            seeds += f"  - image{i+1}: `{image['seed']}`\n"

            button = discord.ui.Button(label=f"upscale {i+1}", custom_id=f"{i+1}")
            view.add_item(button)
        
        # 画像生成に使用された情報を構成
        embed = discord.Embed(
                description=
                    f"**{ctx.author.mention}'s Imagine**\n\n" +
                    f"- model: `{model}`\n" +
                    f"- prompt: `{prompt}`\n" +
                    (f"- negative: `{negative_prompt}`\n" if negative_prompt else "") +
                    f"- aspect: `{aspect}({width}:{height})`\n" +
                    (f"- cfg_scale: `{cfg_scale}`\n" if cfg_scale else "") +
                    (f"- clip_guidance_preset: `{clip_guidance_preset}`\n" if clip_guidance_preset != "NONE" else "") +
                    (f"- sampler: `{sampler}`\n" if sampler else "") +
                    (f"- style_preset: `{style}`\n" if style != "None" else "") +
                    f"- seed:\n{seeds}" +
                    # NSFWコンテンツが存在した場合、検出結果を追記
                    (f"\n\nNSFWコンテンツが検出されたため、{nsfw_content_count}枚の画像が除外されています。" if nsfw_content_count !=0 else ""),
                color=discord.Color.blurple() 
            )
            
        # 画像生成の結果を送信
        embed.set_thumbnail(url="https://images.squarespace-cdn.com/content/v1/646b4513dbebfb2c0adc2b52/1684751740466-5T0GG85P7CVA04C4SKKB/StabilityAi_Logo_White-19.png")
        embed.set_footer(text=f"created by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed, files=files, view=view)


        ### upscalerボタンのコールバックを実装
        async def button_callback(interaction: discord.Interaction):
            await interaction.response.defer()

            # ボタンが押されたときの処理
            original_message = interaction.message
            custom_id = int(interaction.data["custom_id"]) - 1

            # 画像をダウンロードしてバイナリデータを取得
            attachment_url = original_message.attachments[custom_id].url
            response = requests.get(attachment_url)

            # 画像のダウンロード失敗時のエラー処理
            if response.status_code != 200:
                embed=discord.Embed(
                    color=discord.Color.red(), 
                    description="システムエラーが発生したため、実行を中断しました。",
                )
                embed.set_footer(text=f"時間を置いて再度お試しください。")
                await interaction.followup.send(embed=embed)
                return
            
            # 画像のダウンロード成功時の処理
            image_data = response.content

            # 画像をアップスケール
            engine_id = "esrgan-v1-x2plus" # esrgan-v1-x2plus
            response = requests.post(
                f"{API_HOST}/v1/generation/{engine_id}/image-to-image/upscale",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                },
                files={
                    "image": image_data
                }
            )
            # アップスケールの結果を解析
            files = []
            for i, image in enumerate(response.json().get("artifacts", [])):
                files.append(discord.File(io.BytesIO(base64.b64decode(image["base64"])), filename=f"image{i}.png"))

            # 画像生成に使用された情報を構成
            embed = discord.Embed(
                description=
                    f"**{ctx.author.mention}'s UpScale**\n\n" +
                    f"- model: `{engine_id}`\n",
                color=discord.Color.blurple() 
            )
            
            # 画像生成の結果を送信
            embed.set_thumbnail(url="https://images.squarespace-cdn.com/content/v1/646b4513dbebfb2c0adc2b52/1684751740466-5T0GG85P7CVA04C4SKKB/StabilityAi_Logo_White-19.png")
            embed.set_footer(text=f"created by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            await interaction.followup.send(embed=embed, files=files)

        for item in view.children:
            if isinstance(item, Button):
                item.callback = button_callback

def setup(bot):
    bot.add_cog(IMAGINE(bot))