import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Config
from bot.helpers.utils import utils
from bot.helpers.notification import notification
from bot.modules.downloader import downloader
from bot.modules.rclone import rclone_manager
from bot.database.users import users_db
from bot.database.tasks import tasks_db

@Client.on_message(filters.command("mirror") & filters.private)
async def mirror_command(client: Client, message: Message):
    """Mirror command"""
    user = message.from_user
    
    if await users_db.is_banned(user.id):
        await message.reply_text("❌ **You are banned!**")
        return
    
    if len(message.command) < 2:
        await message.reply_text(
            "📝 **Usage:** /mirror <url>",
            parse_mode="markdown"
        )
        return
    
    url = message.command[1]
    task_id = utils.generate_task_id()
    
    await notification.send_processing_notification(
        client, user.id, user.username, "Mirror"
    )
    
    status_msg = await message.reply_text(
        f"📥 **Mirror Started**\n\n"
        f"🔖 Task ID: `{task_id}`\n"
        f"⏳ Downloading..."
    )
    
    await tasks_db.add_task(task_id, user.id, 'mirror', url)
    
    try:
        file_path = os.path.join(Config.DOWNLOAD_DIR, f"mirror_{task_id}")
        result = await downloader.download_with_retry(url, file_path)
        
        if not result['success']:
            await status_msg.edit_text(f"❌ **Download failed:** {result['error']}")
            return
            
        # Upload to cloud
        await status_msg.edit_text("☁️ **Uploading to cloud...**")
        upload_result = await rclone_manager.upload_file(result['file'])
        
        if upload_result['success']:
            await status_msg.edit_text("✅ **Mirror Complete!**")
            await tasks_db.update_task_status(task_id, 'completed')
            await notification.send_completion_notification(
                client, user.id, user.username, 1, 0
            )
        else:
            await status_msg.edit_text(f"❌ **Upload failed:** {upload_result['error']}")
            
        if os.path.exists(result['file']):
            os.remove(result['file'])
            
    except Exception as e:
        await status_msg.edit_text(f"❌ **Error:** {str(e)}")
