import logging
import asyncio
from pyrogram import Client as bot, idle
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
LOGGER.info("⚡ Live log streaming to Telegram")

# Plugin system
plugins = dict(root="plugins")

# Initialize bot
bot = bot(
    name="HerokuBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=plugins,
    workers=10,
    sleep_threshold=120,
)

async def main():
    await bot.start()
    me = await bot.get_me()
    LOGGER.info(f"✅ Bot Started as @{me.username}")
    await idle()
    await bot.stop()
    LOGGER.info("🛑 Bot Stopped")

if __name__ == "__main__":
    asyncio.run(main())
