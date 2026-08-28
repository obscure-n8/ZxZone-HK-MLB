import os
import asyncio
import aiohttp
import aiofiles
from typing import Dict, Optional, Callable

class StreamProcessor:
    """Stream processing without disk cache"""
    
    def __init__(self):
        self.chunk_size = 256 * 1024  # 256KB for Heroku
        
    async def stream_download(
        self,
        url: str,
        file_path: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """Stream download with minimal memory"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return {'success': False, 'error': f'HTTP {response.status}'}
                        
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0
                    
                    async with aiofiles.open(file_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(self.chunk_size):
                            await f.write(chunk)
                            downloaded += len(chunk)
                            
                            if progress_callback and total_size > 0:
                                await progress_callback(downloaded, total_size)
                                
            return {'success': True, 'file': file_path, 'size': downloaded}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def stream_m3u8(self, url: str, file_path: str) -> Dict:
        """Stream M3U8 with concurrent fragments"""
        try:
            command = f"yt-dlp --concurrent-fragments 3 --no-part --no-cache-dir '{url}' -o '{file_path}'"
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.wait()
            
            if os.path.exists(file_path):
                return {'success': True, 'file': file_path}
                
        except:
            pass
            
        return {'success': False}

stream_processor = StreamProcessor()
