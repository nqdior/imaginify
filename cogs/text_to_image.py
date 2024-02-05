import discord
import requests
import os, io, base64, random
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

class ImageGenerationOptions:
    def __init__(self, 
                 prompt: str,
                 negative_prompt: str = "",
                 cfg_scale: float = 7.0,
                 clip_guidance_preset: str = "NONE",
                 aspect: str = "square 1:1",
                 style: str = "None",
                 sampler: str = None,
                 seed: int = None,
                 model: str = "Stable Diffusion XL 1.0"):
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.cfg_scale = cfg_scale
        self.clip_guidance_preset = clip_guidance_preset
        self.aspect = aspect
        self.style = style
        self.sampler = sampler
        self.seed = seed
        self.model = model

    def to_dict(self):
        return {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "cfg_scale": self.cfg_scale,
            "clip_guidance_preset": self.clip_guidance_preset,
            "aspect": self.aspect,
            "style": self.style,
            "sampler": self.sampler,
            "seed": self.seed,
            "model": self.model
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class IMAGINE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                                          
        await ctx.defer()
        width, height = aspect_ratio_options[aspect]
        json_data = {
            "text_prompts": [{"text": prompt, "weight": 1}] + ([{"text": negative_prompt, "weight": -1}] if negative_prompt else []),
            "height": height,
            "width": width,
            "samples": 4,
            "steps": 40,
            **({"cfg_scale": cfg_scale} if style != "None" else {}),
            **({"clip_guidance_preset": clip_guidance_preset}),
            **({"sampler": sampler} if sampler != "None" else {}),
            **({"style_preset": style_preset_options[style]} if style != "None" else {}),
            **({"seed": seed} if seed else {}),
        }
        response = requests.post(f"{API_HOST}/v1/generation/{model_options[model]}/text-to-image", headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, json=json_data)

        if response.status_code != 200:
            await ctx.respond(embed=discord.Embed(color=discord.Color.red(), description="Error: " + response.text))
            return

        data = response.json()
        files = []
        seeds = ""
        for i, image in enumerate(data.get("artifacts", [])):
            files.append(discord.File(io.BytesIO(base64.b64decode(image["base64"])), filename=f"image{i}.png"))
            seeds += f"  - image{i+1}: `{image['seed']}`\n"
        embed = discord.Embed(
            # 投稿者のアイコンを表示
                    description=
                        f"{ctx.author.mention}'s Imagine\n\n" +
                        f"- model: `{model}`\n" +
                        f"- prompt: `{prompt}`\n" +
                        (f"- negative: `{negative_prompt}`\n" if negative_prompt else "") +
                        f"- aspect: `{aspect}({width}:{height})`\n" +
                        (f"- cfg_scale: `{cfg_scale}`\n" if cfg_scale else "") +
                        (f"- clip_guidance_preset: `{clip_guidance_preset}`\n" if clip_guidance_preset != "NONE" else "") +
                        (f"- sampler: `{sampler}`\n" if sampler else "") +
                        (f"- style_preset: `{style}`\n" if style != "None" else "") +
                        f"- seed:\n{seeds}\n",
                    color=discord.Color.blurple() 
                )
        embed.set_author(name=f"{ctx.author.name}" ,icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed, files=files)

def setup(bot):
    bot.add_cog(IMAGINE(bot))