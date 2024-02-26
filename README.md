
# Stability AI Japan - FastAPI Discord Bot XL
In this repository, you can find the source code for a Discord Bot implemented using FastAPI. This bot utilizes [Pycord](https://github.com/Pycord-Development/pycord), a Python library built upon [discord.py](https://github.com/Rapptz/discord.py) for accessing the Discord API. FastAPI enhances the bot by providing a web interface for management and operations.

## Setup
1. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications/).
2. Create an `.env` file to store your bot token and other environment variables:
```
DISCORD_BOT_TOKEN="your_bot_token_here"
STABILITY_API_KEY="your_api_key_here"
```
3. Install the required Python packages from the `requirements.txt` file:
```
python -m pip install -r requirements.txt
```

4. Start the FastAPI application:
```
uvicorn main:app --reload
```
This command will start the FastAPI server with live reloading enabled, making development more efficient. Ensure your `main.py` file is configured to initialize and run your FastAPI app.
