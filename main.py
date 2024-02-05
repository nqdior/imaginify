import discord
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()

bot = discord.Bot(
    intents=intents,
    debug_guilds=[os.getenv("GUILD_ID")]  # hier server id einfügen
)

@bot.event
async def on_ready():
    print(f"{bot.user} ist online")

if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
