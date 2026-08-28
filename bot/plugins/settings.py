from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import Config
from bot.database.users import users_db

@Client.on_message(filters.command("usetting") & filters.private)
async def usetting_command(client: Client, message: Message):
    """User settings command"""
    user = message.from_user
    
    user_settings = await users_db.get_user_settings(user.id)
    
    settings_text = f"""
⚙️ **User Settings**

👤 **User:** {user.first_name}

**Leech Settings:**
• Split Size: 2GB (Default) / 4GB (Session)
• Upload Mode: {user_settings.get('upload_mode', 'document')}

**General Settings:**
• Thumbnail: {'✅ Set' if user_settings.get('thumbnail') else '❌ Not set'}
• Session: {'✅ Active' if user_settings.get('has_session') else '❌ Not set'}

Select a category:
"""
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📥 Leech Settings", callback_data="uset_leech"),
            InlineKeyboardButton("⚙️ General", callback_data="uset_general")
        ],
        [
            InlineKeyboardButton("🔒 Private Files", callback_data="uset_private")
        ],
        [
            InlineKeyboardButton("❌ Close", callback_data="uset_close")
        ]
    ])
    
    await message.reply_text(settings_text, reply_markup=keyboard, parse_mode="markdown")

@Client.on_message(filters.command("bsetting") & filters.private)
async def bsetting_command(client: Client, message: Message):
    """Bot settings command - admin only"""
    user = message.from_user
    
    from bot.helpers.permissions import permission_system
    if not await permission_system.is_admin(user.id):
        await message.reply_text("❌ **Admin only!**")
        return
    
    settings_text = f"""
🔧 **Bot Settings**

Select a category:
"""
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚙️ Config Variables", callback_data="bset_config"),
            InlineKeyboardButton("📥 Aria2 Settings", callback_data="bset_aria2")
        ],
        [
            InlineKeyboardButton("🔒 Private Files", callback_data="bset_private"),
            InlineKeyboardButton("📡 JD Account", callback_data="bset_jd")
        ],
        [
            InlineKeyboardButton("❌ Close", callback_data="bset_close")
        ]
    ])
    
    await message.reply_text(settings_text, reply_markup=keyboard, parse_mode="markdown")
