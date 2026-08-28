import time
import psutil
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Config

@Client.on_message(filters.command("ping") & filters.private)
async def ping_command(client: Client, message: Message):
    """Ping command - test bot speed"""
    
    # Start time
    start_time = time.time()
    
    # Send initial message
    ping_msg = await message.reply_text(
        "🏓 **Pinging...**",
        parse_mode="markdown"
    )
    
    # Calculate ping
    end_time = time.time()
    ping_ms = (end_time - start_time) * 1000
    
    # Get system stats
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    
    # Calculate bot speed
    bot_speed = self.calculate_speed(ping_ms)
    
    # Edit with result
    await ping_msg.edit_text(
        f"""
🏓 **Pong!**

⚡ **Ping:** {ping_ms:.2f}ms
📱 **Bot:** @{Config.BOT_USERNAME}

📊 **System:**
• CPU: {cpu}%
• RAM: {ram}%

🚀 **Speed:** {bot_speed}

✅ **Status:** {'Online' if ping_ms < 500 else 'Slow'}

**Powered By ZxZone Hub** ❞
""",
        parse_mode="markdown"
    )

def calculate_speed(ping_ms: float) -> str:
    """Calculate bot speed based on ping"""
    if ping_ms < 100:
        return "Very Fast ⚡⚡⚡"
    elif ping_ms < 200:
        return "Fast ⚡⚡"
    elif ping_ms < 400:
        return "Normal ⚡"
    else:
        return "Slow 🐢"
