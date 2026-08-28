import asyncio
import logging
import threading
from pyrogram import Client, idle
from bot.config import Config
from bot.core.stealth_manager import stealth_manager

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Main bot function"""
    Config.validate_config()
    Config.ensure_dirs()
    
    logger.info("=" * 50)
    logger.info("ZxZone-HK-MLB Bot Starting...")
    
    # Start stealth protection
    await stealth_manager.start_all()
    
    # Start web server
    if Config.IS_HEROKU:
        from web_server import start_web_server
        web_thread = threading.Thread(target=start_web_server, daemon=True)
        web_thread.start()
        logger.info("Web server started")
    
    # Create bot client
    bot = Client(
        "ZxZone-HK-MLB",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        plugins=dict(root="bot/plugins"),
        workers=50
    )
    
    try:
        await bot.start()
        logger.info("Bot started successfully!")
        logger.info(f"Bot: @{Config.BOT_USERNAME}")
        
        await idle()
        
    except Exception as e:
        logger.error(f"Bot failed: {e}")
        
    finally:
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
