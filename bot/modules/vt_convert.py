import os
import time
import asyncio
from typing import Dict, Optional, List
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.config import Config
from bot.helpers.utils import utils

class VTConverter:
    """Video Tools Converter System"""
    
    def __init__(self):
        self.active_sessions = {}
        self.output_dir = os.path.join(Config.DOWNLOAD_DIR, 'vt_output')
        os.makedirs(self.output_dir, exist_ok=True)
        self.session_timeout = 600  # 10 minutes
        
    async def show_vt_panel(
        self,
        client: Client,
        message: Message,
        file_path: str,
        file_info: Dict = None
    ):
        """Show Video Tools panel"""
        try:
            panel_id = f"vt_{message.from_user.id}_{int(time.time())}"
            
            self.active_sessions[panel_id] = {
                'file_path': file_path,
                'file_info': file_info or {},
                'user_id': message.from_user.id,
                'created_at': time.time(),
                'active': True
            }
            
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            panel_text = f"""
🎬 **Video Tools Panel**

📁 **File:** {file_name}
💾 **Size:** {self.format_size(file_size)}
⏱ **Time Left: 600.0 sec**

Select an option:
"""
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Encode", callback_data=f"vt_encode_{panel_id}"),
                    InlineKeyboardButton("Convert", callback_data=f"vt_convert_{panel_id}")
                ],
                [
                    InlineKeyboardButton("Multi-Resolution", callback_data=f"vt_multi_{panel_id}"),
                    InlineKeyboardButton("Video + Video", callback_data=f"vt_vidvid_{panel_id}")
                ],
                [
                    InlineKeyboardButton("Video + Audio", callback_data=f"vt_vidaud_{panel_id}"),
                    InlineKeyboardButton("Video + Subtitle", callback_data=f"vt_vidsub_{panel_id}")
                ],
                [
                    InlineKeyboardButton("Video+Audio+Sub", callback_data=f"vt_vas_{panel_id}"),
                    InlineKeyboardButton("IntroSub", callback_data=f"vt_introsub_{panel_id}")
                ],
                [
                    InlineKeyboardButton("HardSub", callback_data=f"vt_hardsub_{panel_id}"),
                    InlineKeyboardButton("Remove Subs", callback_data=f"vt_remsub_{panel_id}")
                ],
                [
                    InlineKeyboardButton("Remove Audio", callback_data=f"vt_remaud_{panel_id}"),
                    InlineKeyboardButton("Remove Streams", callback_data=f"vt_remstream_{panel_id}")
                ],
                [
                    InlineKeyboardButton("Strip Metadata", callback_data=f"vt_strip_{panel_id}"),
                    InlineKeyboardButton("Extract Subs/Audio", callback_data=f"vt_extract_{panel_id}")
                ],
                [
                    InlineKeyboardButton("Swap Audio", callback_data=f"vt_swapaud_{panel_id}"),
                    InlineKeyboardButton("Watermark", callback_data=f"vt_water_{panel_id}")
                ],
                [
                    InlineKeyboardButton("Convert Audio", callback_data=f"vt_convaud_{panel_id}"),
                    InlineKeyboardButton("Aspect Ratio", callback_data=f"vt_aspect_{panel_id}")
                ],
                [
                    InlineKeyboardButton("X Cancel", callback_data=f"vt_cancel_{panel_id}")
                ]
            ])
            
            await message.reply_text(
                panel_text,
                reply_markup=keyboard,
                parse_mode="markdown"
            )
            
            # Start timeout countdown
            asyncio.create_task(self.panel_timeout(panel_id))
            
        except Exception as e:
            await message.reply_text(f"❌ **Error:** {str(e)}")
            
    async def panel_timeout(self, panel_id: str):
        """Panel timeout countdown"""
        await asyncio.sleep(self.session_timeout)
        if panel_id in self.active_sessions:
            self.active_sessions[panel_id]['active'] = False
            del self.active_sessions[panel_id]
            
    async def process_vt_action(
        self,
        client: Client,
        callback_query: CallbackQuery,
        action: str,
        panel_id: str
    ):
        """Process VT action"""
        if panel_id not in self.active_sessions:
            await callback_query.answer("Panel expired!", show_alert=True)
            return
            
        session = self.active_sessions[panel_id]
        file_path = session['file_path']
        
        await callback_query.answer(f"Processing {action}...")
        status_msg = await callback_query.message.reply_text(f"🔄 **Processing {action}...**")
        
        output_path = os.path.join(
            self.output_dir,
            f"{os.path.splitext(os.path.basename(file_path))[0]}_{action}.mp4"
        )
        
        # FFmpeg commands
        commands = {
            'encode': f"ffmpeg -i '{file_path}' -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k '{output_path}'",
            'convert': f"ffmpeg -i '{file_path}' -c:v libx264 -c:a aac '{output_path}'",
            'hardsub': f"ffmpeg -i '{file_path}' -vf subtitles='{file_path}' '{output_path}'",
            'strip': f"ffmpeg -i '{file_path}' -map_metadata -1 -c copy '{output_path}'",
            'remaud': f"ffmpeg -i '{file_path}' -an -c:v copy '{output_path}'",
            'water': f"ffmpeg -i '{file_path}' -vf drawtext=text='ZxZone':fontsize=24:fontcolor=white:x=10:y=10 '{output_path}'",
            'convaud': f"ffmpeg -i '{file_path}' -vn -c:a aac -b:a 192k '{os.path.splitext(output_path)[0]}.m4a'",
            'aspect': f"ffmpeg -i '{file_path}' -vf scale=1280:720 '{output_path}'",
        }
        
        command = commands.get(action)
        
        if not command:
            await status_msg.edit_text(f"❌ **Unknown action:** {action}")
            return
            
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.wait()
            
            final_path = output_path if os.path.exists(output_path) else f"{os.path.splitext(output_path)[0]}.m4a"
            
            if os.path.exists(final_path):
                await status_msg.edit_text("📤 **Uploading processed file...**")
                
                from bot.modules.uploader import uploader
                success, msg = await uploader.upload_to_telegram(
                    client, final_path, callback_query.message.chat.id,
                    caption=f"✅ Processed: {action}",
                    user_id=callback_query.from_user.id
                )
                
                if success:
                    await status_msg.edit_text("✅ **Processing complete!**")
                else:
                    await status_msg.edit_text(f"❌ **Upload failed:** {msg}")
                    
                os.remove(final_path)
            else:
                await status_msg.edit_text("❌ **Processing failed!**")
                
        except Exception as e:
            await status_msg.edit_text(f"❌ **Error:** {str(e)}")
            
    def format_size(self, size: int) -> str:
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

vt_converter = VTConverter()

# Command handler
@Client.on_message(filters.command("vt") & filters.private)
async def vt_command(client: Client, message: Message):
    """Video tools command"""
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "📝 **Usage:**\n"
            "/vt - Reply to video file\n"
            "/leech <url> -vt - Leech with VT panel",
            parse_mode="markdown"
        )
        return
        
    if message.reply_to_message:
        if not message.reply_to_message.video and not message.reply_to_message.document:
            await message.reply_text("❌ **Reply to a video file!**")
            return
            
        status_msg = await message.reply_text("📥 **Downloading video...**")
        
        try:
            file_path = await message.reply_to_message.download()
            await status_msg.delete()
            await vt_converter.show_vt_panel(client, message, file_path)
        except Exception as e:
            await status_msg.edit_text(f"❌ **Error:** {str(e)}")
    else:
        url = message.command[1]
        # Download then show panel
        status_msg = await message.reply_text("📥 **Downloading video...**")
        
        try:
            from bot.modules.downloader import downloader
            file_path = os.path.join(Config.DOWNLOAD_DIR, f"vt_{utils.generate_task_id()}.mp4")
            
            result = await downloader.download_file(url, file_path)
            
            if result['success']:
                await status_msg.delete()
                await vt_converter.show_vt_panel(client, message, result['file'])
            else:
                await status_msg.edit_text(f"❌ **Download failed:** {result['error']}")
        except Exception as e:
            await status_msg.edit_text(f"❌ **Error:** {str(e)}")

# Callback handler
@Client.on_callback_query(filters.regex("^vt_"))
async def vt_callback(client: Client, callback_query: CallbackQuery):
    """Handle VT callbacks"""
    data = callback_query.data
    parts = data.split('_')
    
    if len(parts) >= 3:
        action = parts[1]
        panel_id = '_'.join(parts[2:])
        
        if action == 'cancel':
            if panel_id in vt_converter.active_sessions:
                del vt_converter.active_sessions[panel_id]
            await callback_query.message.delete()
            await callback_query.answer("Panel cancelled!")
            return
            
        await vt_converter.process_vt_action(client, callback_query, action, panel_id)
    else:
        await callback_query.answer("Invalid callback!")
