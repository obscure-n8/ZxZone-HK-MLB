import os
import re
import asyncio
import aiohttp
import aiofiles
from typing import Dict, Optional
from bot.config import Config

class SpecialDownloader:
    """Special downloader for cloud services"""
    
    def __init__(self):
        self.download_dir = Config.DOWNLOAD_DIR
        
    async def detect_and_download(self, url: str, file_path: str) -> Dict:
        """Detect link type and download"""
        
        # Google Drive
        if 'drive.google.com' in url:
            return await self.download_gdrive(url, file_path)
            
        # Gofile
        elif 'gofile.io' in url:
            return await self.download_gofile(url, file_path)
            
        # Pixeldrain
        elif 'pixeldrain.com' in url:
            return await self.download_pixeldrain(url, file_path)
            
        # Mega
        elif 'mega.nz' in url:
            return await self.download_mega(url, file_path)
            
        # YouTube
        elif 'youtube.com' in url or 'youtu.be' in url:
            return await self.download_youtube(url, file_path)
            
        # M3U8
        elif '.m3u8' in url:
            return await self.download_m3u8(url, file_path)
            
        # Direct link
        else:
            return await self.download_direct(url, file_path)
            
    async def download_gdrive(self, url: str, file_path: str) -> Dict:
        """Download from Google Drive"""
        try:
            # Extract file ID
            file_id = self.extract_gdrive_id(url)
            
            if not file_id:
                return {'success': False, 'error': 'Invalid Drive link'}
                
            direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(direct_url) as response:
                    if response.status == 200:
                        async with aiofiles.open(file_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(1024 * 1024):
                                await f.write(chunk)
                                
                        return {'success': True, 'file': file_path}
                        
            return {'success': False, 'error': 'Drive download failed'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def extract_gdrive_id(self, url: str) -> Optional[str]:
        """Extract Google Drive file ID"""
        patterns = [
            r'/file/d/([^/]+)',
            r'id=([^&]+)',
            r'/open\?id=([^&]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
                
        return None
        
    async def download_gofile(self, url: str, file_path: str) -> Dict:
        """Download from Gofile"""
        try:
            import requests
            
            # Get server
            server_response = requests.get('https://api.gofile.io/getServer')
            server = server_response.json()['data']['server']
            
            # Get file info
            file_id = url.split('/')[-1]
            info_response = requests.get(f'https://{server}.gofile.io/getContent?contentId={file_id}')
            data = info_response.json()['data']
            
            if 'children' in data:
                for fid, file_info in data['children'].items():
                    download_link = file_info['link']
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.get(download_link) as response:
                            async with aiofiles.open(file_path, 'wb') as f:
                                async for chunk in response.content.iter_chunked(1024 * 1024):
                                    await f.write(chunk)
                                    
                    return {'success': True, 'file': file_path}
                    
            return {'success': False, 'error': 'Gofile download failed'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def download_pixeldrain(self, url: str, file_path: str) -> Dict:
        """Download from Pixeldrain"""
        try:
            file_id = url.split('/')[-1]
            direct_url = f"https://pixeldrain.com/api/file/{file_id}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(direct_url) as response:
                    if response.status == 200:
                        async with aiofiles.open(file_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(1024 * 1024):
                                await f.write(chunk)
                                
                        return {'success': True, 'file': file_path}
                        
            return {'success': False, 'error': 'Pixeldrain download failed'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def download_mega(self, url: str, file_path: str) -> Dict:
        """Download from Mega"""
        try:
            from mega import Mega
            
            mega = Mega()
            m = mega.login()
            
            file_info = m.download_url(url, os.path.dirname(file_path))
            
            if file_info:
                return {'success': True, 'file': os.path.join(os.path.dirname(file_path), file_info)}
                
            return {'success': False, 'error': 'Mega download failed'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def download_youtube(self, url: str, file_path: str) -> Dict:
        """Download from YouTube"""
        try:
            import yt_dlp
            
            ydl_opts = {
                'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.splitext(file_path)[0] + '.%(ext)s',
                'quiet': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                actual_path = ydl.prepare_filename(info)
                
                return {'success': True, 'file': actual_path}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def download_m3u8(self, url: str, file_path: str) -> Dict:
        """Download M3U8 stream"""
        from bot.core.stream_processor import stream_processor
        return await stream_processor.stream_m3u8(url, file_path)
        
    async def download_direct(self, url: str, file_path: str) -> Dict:
        """Download direct link"""
        from bot.modules.downloader import downloader
        return await downloader.download_file(url, file_path)

special_downloader = SpecialDownloader()
