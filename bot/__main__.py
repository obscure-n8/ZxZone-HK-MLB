import asyncio
import logging
import threading
from pyrogram import Client, idle
from bot.config import Config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Main bot function"""
    # Validate config
    Config.validate_config()
    
    # Create directories
    Config.ensure_dirs()
    
    logger.info("=" * 50)
    logger.info("ZxZone-HK-MLB Bot Starting...")
    logger.info(f"Environment: {'Heroku' if Config.IS_HEROKU else 'Local'}")
    logger.info("=" * 50)
    
    # Start web server in background (Heroku keep alive)
    if Config.IS_HEROKU:
        from web_server import start_web_server
        web_thread = threading.Thread(target=start_web_server, daemon=True)
        web_thread.start()
        logger.info("Web server started for keep alive")
    
    # Create bot client
    bot = Client(
        "ZxZone-HK-MLB",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        plugins=dict(root="bot/plugins"),
        workers=50 if Config.IS_HEROKU else 100
    )
    
    try:
        await bot.start()
        logger.info("Bot started successfully!")
        logger.info(f"Bot: @{Config.BOT_USERNAME}")
        logger.info(f"Owner: {Config.OWNER_ID}")
        
        await idle()
        
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")
        
    finally:
        await bot.stop()
        logger.info("Bot stopped!")

if __name__ == "__main__":
    asyncio.run(main())
