import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Config
from bot.helpers.utils import utils
from bot.helpers.notification import notification
from bot.helpers.status import status_view
from bot.modules.downloader import downloader
from bot.modules.uploader import uploader
from bot.database.users import users_db
from bot.database.tasks import tasks_db

@Client.on_message(filters.command("leech") & filters.private)
async def leech_command(client: Client, message: Message):
    """Leech command"""
    user = message.from_user
    
    if await users_db.is_banned(user.id):
        await message.reply_text("❌ **You are banned!**")
        return
    
    if len(message.command) < 2:
        await message.reply_text(
            "📝 **Usage:** /leech <url>\n\n"
            "Supported: Direct, Torrent, M3U8, Mega, Gofile, Drive",
            parse_mode="markdown"
        )
        return
    
    url = message.command[1]
    task_id = utils.generate_task_id()
    
    # Send processing notification
    await notification.send_processing_notification(
        client, user.id, user.username, "Leech"
    )
    
    # Create status view
    status_text, keyboard = await status_view.create_status_view(
        task_id, "Downloading...", 0, user.first_name
    )
    
    status_msg = await message.reply_text(
        status_text,
        reply_markup=keyboard,
        parse_mode="markdown"
    )
    
    await tasks_db.add_task(task_id, user.id, 'leech', url)
    await users_db.increment_tasks(user.id)
    
    try:
        # Download
        file_path = os.path.join(Config.DOWNLOAD_DIR, f"leech_{task_id}")
        
        result = await downloader.download_with_retry(
            url,
            file_path,
            progress_callback=lambda downloaded, total, start_time: update_status(
                status_msg, task_id, downloaded, total, start_time, user.first_name
            )
        )
        
        if not result['success']:
            await status_msg.edit_text(f"❌ **Download failed:** {result['error']}")
            await tasks_db.update_task_status(task_id, 'failed')
            return
            
        # Upload
        success, msg = await uploader.upload_to_telegram(
            client, result['file'], message.chat.id,
            caption=f"📁 {os.path.basename(result['file'])}",
            user_id=user.id
        )
        
        if success:
            await status_msg.edit_text(
                f"✅ **Leech Complete!**\n\n"
                f"📁 File: {os.path.basename(result['file'])}",
                parse_mode="markdown"
            )
            await tasks_db.update_task_status(task_id, 'completed')
            await users_db.increment_downloads(user.id)
            
            # Send completion notification
            await notification.send_completion_notification(
                client, user.id, user.username, 1, 0
            )
        else:
            await status_msg.edit_text(f"❌ **Upload failed:** {msg}")
            
        # Clean up
        if os.path.exists(result['file']):
            os.remove(result['file'])
            
    except Exception as e:
        await status_msg.edit_text(f"❌ **Error:** {str(e)}")
        await tasks_db.update_task_status(task_id, 'failed')

async def update_status(status_msg, task_id, downloaded, total, start_time, user_name):
    """Update status view"""
    from bot.helpers.status import status_view
    
    status_text, keyboard = await status_view.update_status_view(
        task_id, "Downloading...", total, downloaded, start_time, user_name
    )
    
    try:
        await status_msg.edit_text(status_text, reply_markup=keyboard, parse_mode="markdown")
    except:
        pass
