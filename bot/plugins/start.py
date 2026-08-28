from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bot.config import Config
from bot.database.users import users_db

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    user = message.from_user
    
    # Add user to database
    await users_db.add_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or ""
    )
    
    # Create buttons
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📦 Repo", url=Config.REPO_LINK),
            InlineKeyboardButton("📢 Channel", url=Config.UPDATE_CHANNEL)
        ],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")
        ],
        [
            InlineKeyboardButton("📊 My Stats", callback_data="my_stats")
        ]
    ])
    
    welcome_text = f"""
**{Config.BOT_USERNAME}**

**Powered By ZxZone Hub** ❞

👋 Welcome **{user.first_name}**!

I'm **Heroku Optimized Mirror/Leech Bot**

**Features:**
• Direct Link Download
• Torrent/Magnet Support
• YouTube/YT-DLP
• Google Drive/Mega
• M3U8 Stream Download
• Video Tools
• 1080p HD Thumbnail

**Commands:**
• /leech - Leech to Telegram
• /mirror - Mirror to Cloud
• /ytdl - YouTube Download
• /settings - Bot Settings
• /help - Help Menu
"""
    
    await message.reply_text(
        welcome_text,
        reply_markup=keyboard,
        parse_mode="markdown"
    )

@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(client: Client, callback_query):
    """Handle help callback"""
    from bot.plugins.help import help_command
    await help_command(client, callback_query.message)
    await callback_query.answer()

@Client.on_callback_query(filters.regex("^start$"))
async def start_callback(client: Client, callback_query):
    """Handle start callback"""
    await start_command(client, callback_query.message)
    await callback_query.answer()
