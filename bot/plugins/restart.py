import os
import sys
import time
import asyncio
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import Config
from bot.helpers.permissions import permission_system
from bot.database.settings import settings_db

class RestartManager:
    def __init__(self):
        self.restarting = False
        self.last_restart = 0
        
    async def restart_bot(self, client: Client, message: Message):
        """Restart bot"""
        user = message.from_user
        
        if not await permission_system.is_admin(user.id):
            await message.reply_text("❌ **Admin only!**")
            return
            
        if self.restarting:
            await message.reply_text("⚠️ **Restart already in progress!**")
            return
            
        self.restarting = True
        self.last_restart = time.time()
        
        status_msg = await message.reply_text(
            "🔄 **Restarting bot...**\n\n"
            "⏳ Please wait..."
        )
        
        try:
            # Save state
            await settings_db.update_setting('last_restart', time.time())
            await settings_db.update_setting('restart_by', user.id)
            
            await status_msg.edit_text(
                "🔄 **Restarting bot...**\n\n"
                "✅ State saved\n"
                "🔄 Executing restart..."
            )
            
            await asyncio.sleep(2)
            
            # Restart based on environment
            if Config.IS_HEROKU:
                # Heroku: Use heroku restart
                app_name = os.getenv('HEROKU_APP_NAME', '')
                if app_name:
                    command = f"heroku ps:restart --app {app_name}"
                    process = await asyncio.create_subprocess_shell(
                        command,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    await process.wait()
                else:
                    # Exit and let Heroku restart
                    os._exit(0)
            else:
                # VPS/Local: Use os.execv
                os.execv(sys.executable, [sys.executable, "-m", "bot"])
                
        except Exception as e:
            self.restarting = False
            await status_msg.edit_text(f"❌ **Restart failed:** {str(e)}")
            
    async def shutdown_bot(self, client: Client, message: Message):
        """Shutdown bot"""
        user = message.from_user
        
        if not await permission_system.is_admin(user.id):
            await message.reply_text("❌ **Admin only!**")
            return
            
        status_msg = await message.reply_text("🛑 **Shutting down...**")
        
        try:
            await settings_db.update_setting('last_shutdown', time.time())
            await settings_db.update_setting('shutdown_by', user.id)
            
            await status_msg.edit_text("🛑 **Shutting down...**\n\n✅ State saved")
            
            await asyncio.sleep(2)
            await client.stop()
            os._exit(0)
            
        except Exception as e:
            await status_msg.edit_text(f"❌ **Shutdown failed:** {str(e)}")
            
    async def ping_bot(self, client: Client, message: Message):
        """Ping bot"""
        start_time = time.time()
        
        msg = await message.reply_text("🏓 **Pinging...**")
        
        end_time = time.time()
        ping_time = (end_time - start_time) * 1000
        
        await msg.edit_text(
            f"🏓 **Pong!**\n\n"
            f"⚡ Response Time: {ping_time:.2f}ms\n"
            f"📱 Bot: @{Config.BOT_USERNAME}\n"
            f"✅ Status: Online",
            parse_mode="markdown"
        )
        
    async def sysinfo(self, client: Client, message: Message):
        """System information"""
        user = message.from_user
        
        if not await permission_system.is_admin(user.id):
            await message.reply_text("❌ **Admin only!**")
            return
            
        import psutil
        import platform
        
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        uptime = time.time() - psutil.boot_time()
        
        info_text = f"""
🖥 **System Information**

💻 **OS:** {platform.system()} {platform.release()}
🐍 **Python:** {sys.version.split()[0]}

⚡ **CPU:** {cpu}%
💾 **RAM:** {memory.percent}%
💿 **Disk:** {disk.percent}%

⏰ **Uptime:** {int(uptime // 3600)}h {int((uptime % 3600) // 60)}m

📱 **Bot:** @{Config.BOT_USERNAME}
🌍 **Environment:** {'Heroku' if Config.IS_HEROKU else 'Local'}
"""
        
        await message.reply_text(info_text, parse_mode="markdown")

restart_manager = RestartManager()

@Client.on_message(filters.command("restart") & filters.private)
async def restart_command(client: Client, message: Message):
    """Restart command"""
    await restart_manager.restart_bot(client, message)

@Client.on_message(filters.command("shutdown") & filters.private)
async def shutdown_command(client: Client, message: Message):
    """Shutdown command"""
    await restart_manager.shutdown_bot(client, message)

@Client.on_message(filters.command("ping") & filters.private)
async def ping_command(client: Client, message: Message):
    """Ping command"""
    await restart_manager.ping_bot(client, message)

@Client.on_message(filters.command("sysinfo") & filters.private)
async def sysinfo_command(client: Client, message: Message):
    """System info command"""
    await restart_manager.sysinfo(client, message)
