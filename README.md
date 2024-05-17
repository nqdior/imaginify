
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

## License
Shield: [![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
