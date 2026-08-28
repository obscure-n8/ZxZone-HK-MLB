from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import Config
from bot.helpers.permissions import permission_system

@Client.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    """Help command"""
    user = message.from_user
    
    is_admin = await permission_system.is_admin(user.id)
    is_sudo = await permission_system.is_sudo(user.id)
    is_owner = await permission_system.is_owner(user.id)
    
    help_text = f"""
📚 **Help Menu**

**Download Commands:**
• /leech <url> - Leech to Telegram
• /mirror <url> - Mirror to cloud
• /ytdl <url> - YouTube download
• /qbleech <urls> - Batch leech
• /qbmirror <urls> - Batch mirror

**User Commands:**
• /usetting - User settings
• /thumb - Set thumbnail
• /stats - Your statistics
• /mysession - Session status

**Status:**
• /status - Bot status
• /ping - Ping bot
"""
    
    if is_admin:
        help_text += """
**Admin Commands:**
• /bsetting - Bot settings
• /restart - Restart bot
• /cancelalltask - Cancel all tasks
• /logs - View logs
"""
    
    if is_sudo:
        help_text += """
**Sudo Commands:**
• /addsudo <id> - Add sudo
• /removesudo <id> - Remove sudo
• /broadcast - Broadcast
"""
    
    if is_owner:
        help_text += """
**Owner Commands:**
• /owner - Owner panel
• /backup - Create backup
• /update - Update bot
"""
    
    help_text += f"""
**Powered By ZxZone Hub** ❞
"""
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📦 Repo", url=Config.REPO_LINK),
            InlineKeyboardButton("📢 Channel", url=Config.UPDATE_CHANNEL)
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="start")
        ]
    ])
    
    await message.reply_text(help_text, reply_markup=keyboard, parse_mode="markdown")
