import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.config import Config
from bot.helpers.permissions import permission_system
from bot.database.settings import settings_db

class BSettingsComplete:
    def __init__(self):
        # 15 Pages Config Variables
        self.config_pages = {
            1: ['LEECH_LIMIT', 'DIRECT_LIMIT', 'MEGA_LIMIT'],
            2: ['JD_LIMIT', 'TORRENT_LIMIT', 'YTDLP_LIMIT'],
            3: ['YT_DL_LIMIT', 'PLAYLIST_LIMIT', 'CLONE_LIMIT'],
            4: ['VT_ENABLED', 'VT_CONVERT', 'VT_ENCODE'],
            5: ['AUTHORIZED_CHATS', 'SUDO_USERS', 'OWNER_ID'],
            6: ['QUEUE_DOWNLOAD', 'QUEUE_UPLOAD', 'QUEUE_ALL'],
            7: ['MAX_CONCURRENT_DOWNLOADS', 'MAX_CONCURRENT_UPLOADS'],
            8: ['MAX_TORRENT_SIZE', 'DEFAULT_SPLIT_SIZE'],
            9: ['SESSION_SPLIT_SIZE', 'DEFAULT_UPLOAD_SPEED'],
            10: ['SESSION_UPLOAD_SPEED', 'BOT_MAX_TASKS'],
            11: ['USER_MAX_TASKS', 'USER_TIME_INTERVAL'],
            12: ['DISABLE_TORRENTS', 'DISABLE_LEECH', 'DISABLE_MIRROR'],
            13: ['DISABLE_YTDLP', 'DISABLE_MEGA', 'DISABLE_JD'],
            14: ['FORCE_SUB_IDS', 'MEDIA_STORE', 'DELETE_LINKS'],
            15: ['TIMEZONE', 'BOT_PM', 'SET_COMMANDS']
        }
        
        # 5 Pages Aria2 Settings
        self.aria2_pages = {
            1: ['DOWNLOAD_PATH', 'MAX_CONNECTIONS', 'SPLIT'],
            2: ['SPEED_LIMIT', 'DOWNLOAD_SPEED_LIMIT', 'UPLOAD_SPEED_LIMIT'],
            3: ['RETRY_COUNT', 'TIMEOUT', 'MAX_TRIES'],
            4: ['FILE_ALLOCATION', 'CHECK_CERTIFICATE', 'CONTINUE_DOWNLOAD'],
            5: ['MIN_SPLIT_SIZE', 'MAX_OVERALL_DOWNLOAD_LIMIT']
        }
        
        # Private Files
        self.private_files = [
            'cookies.txt',
            'token.pickle',
            'rclone.conf',
            'shortner.txt',
            'accounts.zip',
            'credentials.json',
            'client_secrets.json',
            'gofile_api.txt',
            'pixeldrain_api.txt'
        ]
        
    async def show_main_menu(self, callback_query: CallbackQuery):
        """Show main bsetting menu"""
        user_id = callback_query.from_user.id
        
        if not await permission_system.is_admin(user_id):
            await callback_query.answer("Admin only!", show_alert=True)
            return
            
        text = f"""
🔧 **Bot Settings Panel**

👑 **Admin Panel**

Select a category:
"""
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚙️ Config Variables", callback_data="bset_config_1"),
                InlineKeyboardButton("📥 Aria2 Settings", callback_data="bset_aria2_1")
            ],
            [
                InlineKeyboardButton("🔒 Private Files", callback_data="bset_private"),
                InlineKeyboardButton("📡 JD Account", callback_data="bset_jd")
            ],
            [
                InlineKeyboardButton("❌ Close", callback_data="bset_close")
            ]
        ])
        
        await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="markdown")
        
    async def show_config_page(self, callback_query: CallbackQuery, page: int):
        """Show config variables page"""
        variables = self.config_pages.get(page, [])
        
        text = f"""
⚙️ **Config Variables** (Page {page}/15)

"""
        for var in variables:
            value = getattr(Config, var, 'N/A')
            text += f"• **{var}:** {value}\n"
            
        text += "\nClick variable to edit:"
        
        buttons = []
        for var in variables:
            buttons.append([
                InlineKeyboardButton(f"✏️ {var}", callback_data=f"bset_edit_{var}")
            ])
            
        # Navigation
        nav = []
        if page > 1:
            nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"bset_config_{page-1}"))
        if page < 15:
            nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"bset_config_{page+1}"))
        buttons.append(nav)
        
        # Page numbers
        page_nav = []
        for i in range(1, 16):
            page_nav.append(InlineKeyboardButton(str(i), callback_data=f"bset_config_{i}"))
        buttons.append(page_nav)
        
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="bset_main")])
        
        keyboard = InlineKeyboardMarkup(buttons)
        await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="markdown")
        
    async def show_aria2_page(self, callback_query: CallbackQuery, page: int):
        """Show Aria2 settings page"""
        variables = self.aria2_pages.get(page, [])
        
        text = f"""
📥 **Aria2 Settings** (Page {page}/5)

"""
        for var in variables:
            value = getattr(Config, var, 'N/A')
            text += f"• **{var}:** {value}\n"
            
        text += "\nClick to edit:"
        
        buttons = []
        for var in variables:
            buttons.append([
                InlineKeyboardButton(f"✏️ {var}", callback_data=f"bset_aria2_edit_{var}")
            ])
            
        nav = []
        if page > 1:
            nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"bset_aria2_{page-1}"))
        if page < 5:
            nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"bset_aria2_{page+1}"))
        buttons.append(nav)
        
        page_nav = []
        for i in range(1, 6):
            page_nav.append(InlineKeyboardButton(str(i), callback_data=f"bset_aria2_{i}"))
        buttons.append(page_nav)
        
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="bset_main")])
        
        keyboard = InlineKeyboardMarkup(buttons)
        await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="markdown")
        
    async def show_private_files(self, callback_query: CallbackQuery):
        """Show private files management"""
        text = f"""
🔒 **Private Files**

Upload configuration files:

"""
        for file in self.private_files:
            file_path = os.path.join(Config.CONFIG_DIR, file)
            status = '✅' if os.path.exists(file_path) else '❌'
            text += f"{status} • {file}\n"
            
        text += """
**Commands:**
/upload <filename> - Upload file
/delete <filename> - Delete file
"""
        
        buttons = []
        for i in range(0, len(self.private_files), 2):
            row = []
            for file in self.private_files[i:i+2]:
                row.append(InlineKeyboardButton(
                    f"{file}",
                    callback_data=f"bset_priv_{file.split('.')[0]}"
                ))
            buttons.append(row)
            
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="bset_main")])
        
        keyboard = InlineKeyboardMarkup(buttons)
        await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="markdown")
        
    async def show_jd_account(self, callback_query: CallbackQuery):
        """Show JD Account management"""
        settings = await settings_db.get_settings()
        jd_email = settings.get('jd_email', '')
        jd_password = settings.get('jd_password', '')
        
        text = f"""
📡 **JD Account**

• Email: {'✅ Set' if jd_email else '❌ Not Set'}
• Password: {'✅ Set' if jd_password else '❌ Not Set'}

**Commands:**
/setjdemail <email> - Set email
/setjdpass <password> - Set password
"""
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📧 Set Email", callback_data="bset_jd_email"),
                InlineKeyboardButton("🔑 Set Password", callback_data="bset_jd_pass")
            ],
            [
                InlineKeyboardButton("💾 Save", callback_data="bset_jd_save"),
                InlineKeyboardButton("🗑 Delete", callback_data="bset_jd_delete")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="bset_main")
            ]
        ])
        
        await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="markdown")

bsettings_complete = BSettingsComplete()

@Client.on_message(filters.command("bsetting") & filters.private)
async def bsetting_command(client: Client, message: Message):
    """Bot settings command"""
    await bsettings_complete.show_main_menu(message)

@Client.on_callback_query(filters.regex("^bset_"))
async def bsetting_callback(client: Client, callback_query: CallbackQuery):
    """Handle bsetting callbacks"""
    data = callback_query.data
    
    if data == "bset_main":
        await bsettings_complete.show_main_menu(callback_query)
    elif data.startswith("bset_config_"):
        page = int(data.split("_")[2])
        await bsettings_complete.show_config_page(callback_query, page)
    elif data.startswith("bset_aria2_"):
        page = int(data.split("_")[2])
        await bsettings_complete.show_aria2_page(callback_query, page)
    elif data == "bset_private":
        await bsettings_complete.show_private_files(callback_query)
    elif data == "bset_jd":
        await bsettings_complete.show_jd_account(callback_query)
    elif data == "bset_close":
        await callback_query.message.delete()
    elif data.startswith("bset_edit_"):
        var = data.replace("bset_edit_", "")
        await callback_query.answer(f"Send: /setvar {var} <value>", show_alert=True)
    elif data.startswith("bset_aria2_edit_"):
        var = data.replace("bset_aria2_edit_", "")
        await callback_query.answer(f"Send: /setaria2 {var} <value>", show_alert=True)
    elif data.startswith("bset_priv_"):
        file_name = data.replace("bset_priv_", "")
        await callback_query.answer(f"Reply with file: /upload {file_name}", show_alert=True)
    elif data == "bset_jd_email":
        await callback_query.answer("Send: /setjdemail <email>", show_alert=True)
    elif data == "bset_jd_pass":
        await callback_query.answer("Send: /setjdpass <password>", show_alert=True)
    elif data == "bset_jd_save":
        await callback_query.answer("JD account saved!", show_alert=True)
    elif data == "bset_jd_delete":
        await callback_query.answer("JD account deleted!", show_alert=True)
        
    await callback_query.answer()
