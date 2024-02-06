import discord
import requests
import os, io, base64
from discord.ext import commands
from discord.commands import slash_command, Option
from dotenv import load_dotenv
from .common.options import model_options, sampler_options, aspect_ratio_options, style_preset_options, clip_guidance_preset_options
from .common.messages import *

load_dotenv()
API_HOST = os.getenv('API_HOST', 'https://api.stability.ai')
API_KEY = os.getenv("STABILITY_API_KEY")
if not API_KEY:
    raise EnvironmentError("Missing Stability API key.")

class IMAGINE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="imagine", description=IMAGINE_DESCRIPTION)
    async def imagine(self, ctx,
                      prompt: Option(str, PROMPT_OPTION_DESC, required=True),
                      negative_prompt: Option(str, NEGATIVE_PROMPT_OPTION_DESC, required=False, default=""),
                      cfg_scale: Option(float, CFG_SCALE_OPTION_DESC, required=False, min_value=0.0, max_value=35.0),
                      clip_guidance_preset: Option(str, CLIP_GUIDANCE_PRESET_OPTION_DESC, choices=list(clip_guidance_preset_options.keys()), required=False, default="NONE"),
                      aspect: Option(str, ASPECT_OPTION_DESC, choices=list(aspect_ratio_options.keys()), required=False, default="square 1:1"),
                      style: Option(str, STYLE_OPTION_DESC, choices=list(style_preset_options.keys()), required=False, default="None"),
                      sampler: Option(str, SAMPLER_OPTION_DESC, choices=list(sampler_options.keys()), required=False),
                      seed: Option(int, SEED_OPTION_DESC, required=False, min_value=0, max_value=4294967295),
                      model: Option(str, MODEL_OPTION_DESC, choices=list(model_options.keys()), required=False, default="Stable Diffusion XL 1.0")
                      ):
                   
        await ctx.defer()

        width, height = aspect_ratio_options[aspect]
        json_data = {
            "text_prompts": [{"text": prompt, "weight": 1}] + ([{"text": negative_prompt, "weight": -1}] if negative_prompt else []),
            "height": height,
            "width": width,
            "samples": 4,
            "steps": 50,
            **({"cfg_scale": cfg_scale} if cfg_scale else {}),
            **({"clip_guidance_preset": clip_guidance_preset}),
            **({"sampler": sampler} if sampler else {}),
            **({"style_preset": style_preset_options[style]} if style != "None" else {}),
            **({"seed": seed} if seed else {}),
        }

        response = requests.post(f"{API_HOST}/v1/generation/{model_options[model]}/text-to-image", headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, json=json_data)

        if response.status_code != 200:
            embed=discord.Embed(
                color=discord.Color.red(), 
                description=ERROR_PROMPT_DETECTED,
            )
            embed.set_footer(text=FOOTER_PROMPT_ENGLISH)
            await ctx.respond(embed=embed)
            return
        
        files = []
        seeds = ""
        nsfw_content_count = 0
        view = discord.ui.View()
        for i, image in enumerate(response.json().get("artifacts", [])):
            
            if "SUCCESS" != image.get("finishReason") :
                nsfw_content_count += 1
                continue

            files.append(discord.File(io.BytesIO(base64.b64decode(image["base64"])), filename=f"image{i+1}.png"))
            seeds += f"  - image{i+1}: `{image['seed']}`\n"

            button = discord.ui.Button(label=f"upscale {i+1}", custom_id=f"{i+1}")
            view.add_item(button)

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
                    (f"\n\n") +
                    (ERROR_NSFW.format(nsfw_content_count) if nsfw_content_count !=0 else ""),
                color=discord.Color.blurple() 
                )
            

        embed.set_thumbnail(url=STABILITY_AI_LOGO_URL)
        embed.set_footer(text=f"created by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed, files=files, view=view)


        async def button_callback(interaction: discord.Interaction):
            await interaction.response.defer()

            original_message = interaction.message
            custom_id = int(interaction.data["custom_id"]) - 1

            # BUG: NSFW画像が含まれている場合、indexが正しく指定できずエラーが発生する
            attachment_url = original_message.attachments[custom_id].url
            response = requests.get(attachment_url)

            if response.status_code != 200:
                embed=discord.Embed(
                    color=discord.Color.red(), 
                    description=ERROR_SYSTEM,
                )
                embed.set_footer(text=ERROR_RETRY)
                await interaction.followup.send(embed=embed)
                return  
            image_data = response.content

            engine_id = "esrgan-v1-x2plus"
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

            files = []
            for i, image in enumerate(response.json().get("artifacts", [])):
                files.append(discord.File(io.BytesIO(base64.b64decode(image["base64"])), filename=f"image{i+1}.png"))

            embed = discord.Embed(
                description=
                    f"**{ctx.author.mention}'s UpScale**\n",
                color=discord.Color.blurple() 
            )

            embed.set_thumbnail(url=STABILITY_AI_LOGO_URL)
            embed.set_footer(text=f"created by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
            await interaction.followup.send(embed=embed, files=files)

        for item in view.children:
            if isinstance(item, discord.ui.Button):
                item.callback = button_callback

def setup(bot):
    bot.add_cog(IMAGINE(bot))