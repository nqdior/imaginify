from fastapi import FastAPI
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

app = FastAPI()

# Discord Botの起動
@app.on_event("startup")
async def startup_event():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    token = os.getenv("DISCORD_BOT_TOKEN")
    await bot.start(token)

# Discord Botの終了
@app.on_event("shutdown")
async def shutdown_event():
    await bot.close()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)