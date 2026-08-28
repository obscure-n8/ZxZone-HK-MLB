from pyrogram import Client
from bot.config import Config

class Notification:
    """User notification system"""
    
    def __init__(self):
        self.processing_messages = {}
        
    async def send_completion_notification(
        self,
        client: Client,
        user_id: int,
        username: str,
        files_sent: int,
        files_failed: int,
        group_chat_id: int = None
    ):
        """Send completion notification to DM and Group"""
        
        mention = f"@{username}" if username else f"User {user_id}"
        
        # Message for DM
        dm_text = f"""
✅ **Files Sent in Your DM!**

👤 **User:** {mention}

📊 **Results:**
• ✅ Sent: {files_sent} files
• ❌ Failed: {files_failed} files

**Powered By Zonexus Hub** ❞
"""
        
        # Send to DM
        try:
            await client.send_message(user_id, dm_text, parse_mode="markdown")
        except:
            pass
            
        # Send to Group (if bot is in group)
        if group_chat_id:
            group_text = f"""
📦 **File Leech Completed!**

👤 **User:** {mention}

✅ **Files Sent:** {files_sent}
❌ **Failed:** {files_failed}

📥 **Check your DM for files!**

**Powered By Zonexus Hub** ❞
"""
            try:
                await client.send_message(
                    group_chat_id,
                    group_text,
                    parse_mode="markdown"
                )
            except:
                pass
                
    async def send_processing_notification(
        self,
        client: Client,
        user_id: int,
        username: str,
        task_type: str,
        group_chat_id: int = None
    ):
        """Send processing notification"""
        
        mention = f"@{username}" if username else f"User {user_id}"
        
        dm_text = f"""
🔄 **Your Files Processing Going On!**

👤 **User:** {mention}
📥 **Type:** {task_type}
⏳ **Status:** Processing...

**Powered By Zonexus Hub** ❞
"""
        
        try:
            msg = await client.send_message(user_id, dm_text, parse_mode="markdown")
            self.processing_messages[user_id] = msg.id
        except:
            pass
            
        if group_chat_id:
            group_text = f"""
🔄 **Processing Started!**

👤 **User:** {mention}
📥 **Type:** {task_type}

**Powered By Zonexus Hub** ❞
"""
            try:
                await client.send_message(group_chat_id, group_text, parse_mode="markdown")
            except:
                pass
                
    async def clear_processing_message(self, client: Client, user_id: int):
        """Clear processing message"""
        if user_id in self.processing_messages:
            try:
                await client.delete_messages(user_id, self.processing_messages[user_id])
                del self.processing_messages[user_id]
            except:
                pass

notification = Notification()
