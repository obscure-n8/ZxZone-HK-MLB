import time
import psutil
from typing import Dict, Optional
from bot.config import Config
from bot.helpers.progress import progress_helper

class StatusView:
    """Bot task status view system"""
    
    def __init__(self):
        self.active_tasks = {}
        self.task_history = []
        
    async def create_status_view(
        self,
        task_id: str,
        file_name: str,
        total_size: int,
        user_name: str,
        mode: str = "Leech"
    ) -> str:
        """Create status view message"""
        
        status_text = f"""
**{Config.BOT_USERNAME}**
┌ **ZxZone-HK-MLB**
└ `/leech1 {task_id}`

▍ **Powered By Zonexus Hub** ❞

1. `{file_name}`
┌ **Task By {user_name}**
│ [oooooooooo] 0.0%
│ **Status** : Starting
│ **Total** : {progress_helper.format_size(total_size)} | **Done** : 0 B
│ **Speed** : 0 B/s | **ETA** : 0s
│ **Engine** : Aria2 v1.37.0 | **Mode** : `#{mode}`
> **Stop** : `/c_{task_id}`

⬢ **BOT STATS**
┌ **CPU** : 0% | **RAM** : 0%
└ **FREE** : 0 B
"""
        return status_text
        
    async def update_status_view(
        self,
        task_id: str,
        file_name: str,
        total_size: int,
        downloaded: int,
        user_name: str,
        mode: str = "Leech",
        status: str = "Downloading"
    ) -> str:
        """Update status view with progress"""
        
        percentage = (downloaded / total_size) * 100 if total_size > 0 else 0
        speed = downloaded / 2  # Example calculation
        eta = (total_size - downloaded) / speed if speed > 0 else 0
        
        progress_bar = progress_helper.get_progress_bar(percentage)
        system = progress_helper.get_system_stats()
        
        status_text = f"""
**{Config.BOT_USERNAME}**
┌ **ZxZone-HK-MLB**
└ `/leech1 {task_id}`

▍ **Powered By Zonexus Hub** ❞

1. `{file_name}`
┌ **Task By {user_name}**
│ {progress_bar} {percentage:.1f}%
│ **Status** : {status}
│ **Total** : {progress_helper.format_size(total_size)} | **Done** : {progress_helper.format_size(downloaded)}
│ **Speed** : {progress_helper.format_speed(speed)} | **ETA** : {progress_helper.format_eta(eta)}
│ **Engine** : Aria2 v1.37.0 | **Mode** : `#{mode}`
> **Stop** : `/c_{task_id}`

⬢ **BOT STATS**
┌ **CPU** : {system['cpu']}% | **RAM** : {system['ram']}%
└ **FREE** : {system['free_disk']}
"""
        return status_text
        
    async def create_upload_status(
        self,
        task_id: str,
        file_name: str,
        total_size: int,
        uploaded: int,
        user_name: str
    ) -> str:
        """Create upload status view"""
        
        percentage = (uploaded / total_size) * 100 if total_size > 0 else 0
        progress_bar = progress_helper.get_progress_bar(percentage)
        system = progress_helper.get_system_stats()
        
        status_text = f"""
**{Config.BOT_USERNAME}**
┌ **ZxZone-HK-MLB**
└ `/leech1 {task_id}`

▍ **Powered By Zonexus Hub** ❞

1. `{file_name}`
┌ **Task By {user_name}**
│ {progress_bar} {percentage:.1f}%
│ **Status** : Uploading
│ **Total** : {progress_helper.format_size(total_size)} | **Done** : {progress_helper.format_size(uploaded)}
│ **Engine** : Aria2 v1.37.0 | **Mode** : `#Leech`
> **Stop** : `/c_{task_id}`

⬢ **BOT STATS**
┌ **CPU** : {system['cpu']}% | **RAM** : {system['ram']}%
└ **FREE** : {system['free_disk']}
"""
        return status_text
        
    async def create_complete_status(
        self,
        task_id: str,
        file_name: str,
        file_size: int,
        user_name: str,
        mode: str = "Leech"
    ) -> str:
        """Create completion status view"""
        
        status_text = f"""
**{Config.BOT_USERNAME}**
┌ **ZxZone-HK-MLB**
└ `/leech1 {task_id}`

▍ **Powered By Zonexus Hub** ❞

1. `{file_name}`
┌ **Task By {user_name}**
│ [●●●●●●●●●●] 100.0%
│ **Status** : Completed
│ **Total** : {progress_helper.format_size(file_size)} | **Done** : {progress_helper.format_size(file_size)}
│ **Engine** : Aria2 v1.37.0 | **Mode** : `#{mode}`

✅ **Task Completed Successfully!**

⬢ **BOT STATS**
┌ **CPU** : {psutil.cpu_percent()}% | **RAM** : {psutil.virtual_memory().percent}%
└ **FREE** : {progress_helper.format_size(psutil.disk_usage('/').free)}
"""
        return status_text

status_view = StatusView()
