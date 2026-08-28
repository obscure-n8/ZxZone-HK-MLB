import os
import asyncio
from typing import Dict, Optional
from bot.config import Config

class RcloneManager:
    def __init__(self):
        self.config_path = Config.RCLONE_CONFIG
        self.remote = Config.RCLONE_REMOTE
        
    async def check_remote(self) -> bool:
        """Check if rclone is configured"""
        if not os.path.exists(self.config_path):
            return False
        return os.path.getsize(self.config_path) > 0
        
    async def upload_file(self, file_path: str, destination: str = "") -> Dict:
        """Upload file to cloud"""
        try:
            if not await self.check_remote():
                return {'success': False, 'error': 'Rclone not configured'}
                
            dest = f"{self.remote}:{destination}" if destination else f"{self.remote}:"
            
            command = f"rclone copy '{file_path}' '{dest}' --progress"
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.wait()
            
            if process.returncode == 0:
                return {'success': True}
            else:
                return {'success': False, 'error': 'Upload failed'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def list_remotes(self) -> list:
        """List rclone remotes"""
        try:
            process = await asyncio.create_subprocess_shell(
                "rclone listremotes",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return [r.strip() for r in stdout.decode().split('\n') if r.strip()]
        except:
            return []

rclone_manager = RcloneManager()
