import time
import psutil
from typing import Dict, Optional, List
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import Config
from bot.helpers.progress import progress_helper

class StatusView:
    """Bot task status view with pagination"""
    
    def __init__(self):
        self.active_tasks = {}
        self.page_size = 3  # 3 tasks per page
        self.max_pages = 4  # Max 4 pages
        self.max_tasks = 12  # Total 12 tasks
        
    def get_pagination_keyboard(self, task_id: str, page: int = 1, total_pages: int = 1) -> InlineKeyboardMarkup:
        """Get pagination keyboard"""
        buttons = []
        
        # Refresh and Cancel row
        buttons.append([
            InlineKeyboardButton("♻️ Refresh", callback_data=f"refresh_{task_id}_{page}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{task_id}")
        ])
        
        # Pagination row
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{task_id}_{page-1}"))
        else:
            nav_buttons.append(InlineKeyboardButton("|||", callback_data="noop"))
            
        nav_buttons.append(InlineKeyboardButton(f"📄 {page}/{total_pages}", callback_data="noop"))
        
        if page < total_pages:
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_{task_id}_{page+1}"))
        else:
            nav_buttons.append(InlineKeyboardButton("|||", callback_data="noop"))
            
        buttons.append(nav_buttons)
        
        return InlineKeyboardMarkup(buttons)
        
    async def create_multi_task_status(
        self,
        task_id: str,
        tasks: List[Dict],
        page: int = 1
    ) -> tuple:
        """Create multi-task status view with pagination"""
        
        total_tasks = len(tasks)
        total_pages = min(self.max_pages, (total_tasks + self.page_size - 1) // self.page_size)
        page = max(1, min(page, total_pages))
        
        start_idx = (page - 1) * self.page_size
        end_idx = min(start_idx + self.page_size, total_tasks)
        page_tasks = tasks[start_idx:end_idx]
        
        system = progress_helper.get_system_stats()
        
        status_text = f"""
**{Config.BOT_USERNAME}**
┌ **ZxZone-HK-MLB**
└ `/leech1 {task_id}`

▍ **Powered By Zonexus Hub** ❞

📊 **Active Tasks:** {total_tasks}/12
📄 **Page:** {page}/{total_pages}

"""
        
        for i, task in enumerate(page_tasks, start_idx + 1):
            percentage = task.get('percentage', 0)
            progress_bar = progress_helper.get_progress_bar(percentage)
            
            status_text += f"""
{i}. `{task.get('file_name', 'Unknown')}`
┌ **Task By {task.get('user_name', 'User')}**
│ {progress_bar} {percentage:.1f}%
│ **Status** : {task.get('status', 'Processing')}
│ **Total** : {task.get('total_size_str', '0 B')} | **Done** : {task.get('done_size_str', '0 B')}
│ **Speed** : {task.get('speed_str', '0 B/s')} | **ETA** : {task.get('eta_str', '0s')}
│ **Mode** : `#{task.get('mode', 'Leech')}`
> **Stop** : `/c_{task.get('task_id', '')}`

"""
        
        status_text += f"""
⬢ **BOT STATS**
┌ **CPU** : {system['cpu']}% | **RAM** : {system['ram']}%
└ **FREE** : {system['free_disk']}
"""
        
        keyboard = self.get_pagination_keyboard(task_id, page, total_pages)
        return status_text, keyboard

status_view = StatusView()
