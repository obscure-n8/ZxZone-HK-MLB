import os
import time
import asyncio
import aiohttp
import aiofiles
from typing import Dict, Optional, Callable
from bot.config import Config
from bot.core.stream_processor import stream_processor
from bot.core.speed_booster import speed_booster

class DownloadManager:
    def __init__(self):
        self.active_downloads = {}
        self.download_queue = asyncio.Queue()
        
    async def download_file(
        self,
        url: str,
        file_path: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """Download file with progress"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Get optimal settings
            settings = await speed_booster.optimize_download(url)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return {'success': False, 'error': f'HTTP {response.status}'}
                        
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0
                    start_time = time.time()
                    
                    async with aiofiles.open(file_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(settings['chunk_size']):
                            await f.write(chunk)
                            downloaded += len(chunk)
                            
                            if progress_callback:
                                await progress_callback(
                                    downloaded=downloaded,
                                    total=total_size,
                                    start_time=start_time
                                )
                                
            return {
                'success': True,
                'file': file_path,
                'size': downloaded
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def download_m3u8(self, url: str, file_path: str) -> Dict:
        """Download M3U8 stream"""
        return await stream_processor.stream_m3u8(url, file_path)
        
    async def download_with_retry(
        self,
        url: str,
        file_path: str,
        max_retries: int = 3,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """Download with retry"""
        for attempt in range(max_retries):
            result = await self.download_file(url, file_path, progress_callback)
            if result['success']:
                return result
            await asyncio.sleep(2 ** attempt)
            
        return {'success': False, 'error': 'Max retries exceeded'}
        
    async def cancel_download(self, task_id: str) -> bool:
        """Cancel download"""
        if task_id in self.active_downloads:
            self.active_downloads[task_id]['cancelled'] = True
            return True
        return False
        
    def get_active_count(self) -> int:
        return len(self.active_downloads)

downloader = DownloadManager()
