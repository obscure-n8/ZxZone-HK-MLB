import os
import asyncio
from typing import Dict, Optional, Callable
from pyrogram import Client
from bot.config import Config
from bot.helpers.thumbnail import hd_thumbnail

class UploadManager:
    def __init__(self):
        self.active_uploads = {}
        
    async def get_split_size(self, user_id: Optional[int] = None) -> int:
        """Get split size based on user"""
        if not user_id:
            return 2 * 1024 * 1024 * 1024  # 2GB
            
        try:
            from bot.database.users import users_db
            user = await users_db.get_user(user_id)
            has_session = user.get('has_session', False) if user else False
            is_premium = user.get('is_premium', False) if user else False
            
            if has_session and is_premium:
                return 4 * 1024 * 1024 * 1024  # 4GB
            elif has_session or is_premium:
                return 3 * 1024 * 1024 * 1024  # 3GB
            else:
                return 2 * 1024 * 1024 * 1024  # 2GB
        except:
            return 2 * 1024 * 1024 * 1024
            
    async def upload_to_telegram(
        self,
        client: Client,
        file_path: str,
        chat_id: int,
        caption: str = "",
        user_id: Optional[int] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """Upload file to Telegram with 1080p HD thumbnail"""
        try:
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            
            # Generate 1080p HD thumbnail for videos
            thumbnail = None
            if file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm')):
                if hd_thumbnail.enabled:
                    result = await hd_thumbnail.generate_1080p_thumbnail(file_path)
                    if result['success']:
                        thumbnail = result['thumbnail']
                        
            # Check split size
            split_size = await self.get_split_size(user_id)
            
            if file_size > split_size:
                return await self.split_and_upload(
                    client, file_path, chat_id, caption, split_size, thumbnail, user_id
                )
            else:
                await self.direct_upload(
                    client, file_path, chat_id, caption, thumbnail
                )
                
            # Clean up thumbnail
            if thumbnail and os.path.exists(thumbnail):
                os.remove(thumbnail)
                
            return {'success': True, 'message': 'Upload successful'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def split_and_upload(
        self,
        client: Client,
        file_path: str,
        chat_id: int,
        caption: str,
        split_size: int,
        thumbnail: Optional[str],
        user_id: Optional[int]
    ) -> Dict:
        """Split and upload large file"""
        try:
            file_size = os.path.getsize(file_path)
            num_parts = (file_size + split_size - 1) // split_size
            
            for i in range(num_parts):
                part_path = f"{file_path}.part{i+1:03d}"
                
                with open(file_path, 'rb') as source, open(part_path, 'wb') as target:
                    remaining = min(split_size, file_size - (i * split_size))
                    while remaining > 0:
                        chunk = source.read(min(1024 * 1024, remaining))
                        if not chunk:
                            break
                        target.write(chunk)
                        remaining -= len(chunk)
                        
                part_caption = f"{caption}\n\nPart {i+1}/{num_parts}"
                await self.direct_upload(client, part_path, chat_id, part_caption, thumbnail if i == 0 else None)
                os.remove(part_path)
                
            return {'success': True, 'message': f'Uploaded in {num_parts} parts'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def direct_upload(
        self,
        client: Client,
        file_path: str,
        chat_id: int,
        caption: str,
        thumbnail: Optional[str]
    ):
        """Direct upload without splitting"""
        if file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm')):
            await client.send_video(
                chat_id,
                file_path,
                caption=caption,
                thumb=thumbnail,
                supports_streaming=True
            )
        elif file_path.lower().endswith(('.mp3', '.m4a', '.wav', '.ogg')):
            await client.send_audio(chat_id, file_path, caption=caption, thumb=thumbnail)
        else:
            await client.send_document(chat_id, file_path, caption=caption, thumb=thumbnail)

uploader = UploadManager()
