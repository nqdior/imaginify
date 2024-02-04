import discord
import requests
import os, io, base64
from discord.ext import commands
from discord.commands import slash_command, Option
from dotenv import load_dotenv

load_dotenv()
engine_id = "stable-diffusion-v1-6"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")

if api_key is None:
    raise Exception("Missing Stability API key.")

class IMAGINE(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Imagine command
    @slash_command()
    async def imagine(self, ctx, 
                      prompt: Option(str, "prompt"), 
                      # add option
                      seed: Option(int, "seed", required=False)
                      ):

        # waiting start
        await ctx.defer()

        # API request
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 4,
                "steps": 30,
                "seed": seed,
            },
        )
        # response check
        if response.status_code != 200:
            embed = discord.Embed(
                color=discord.Color.red(),
                description="Non-200 response: " + str(response.text)
            )
            await ctx.respond(embed=embed)

        # response create
        data = response.json()
        files  = []
        for i, image in enumerate(data["artifacts"]):
            buf = image["base64"]
            file = discord.File(io.BytesIO(base64.b64decode(buf)), filename=f"{i}.png")
            files.append(file)
        embed = discord.Embed(
            color=discord.Color.blurple(),
            description="画像生成が完了しました。"
        )
        
        # files send & waiting end
        await ctx.respond(embed=embed, files=files)

def setup(bot: discord.Bot):
    bot.add_cog(IMAGINE(bot))
