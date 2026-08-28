import os
import asyncio
from typing import Dict, Optional

class VideoTools:
    def __init__(self):
        self.output_dir = os.path.join(Config.DOWNLOAD_DIR, 'processed')
        os.makedirs(self.output_dir, exist_ok=True)
        
    async def convert(self, file_path: str, target_format: str = 'mp4') -> Dict:
        """Convert video format"""
        try:
            output_path = os.path.join(
                self.output_dir,
                f"{os.path.splitext(os.path.basename(file_path))[0]}.{target_format}"
            )
            
            command = f"ffmpeg -i '{file_path}' -c:v libx264 -c:a aac '{output_path}'"
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.wait()
            
            if os.path.exists(output_path):
                return {'success': True, 'file': output_path}
                
        except:
            pass
            
        return {'success': False}
        
    async def extract_audio(self, file_path: str) -> Dict:
        """Extract audio from video"""
        try:
            output_path = os.path.join(
                self.output_dir,
                f"{os.path.splitext(os.path.basename(file_path))[0]}.mp3"
            )
            
            command = f"ffmpeg -i '{file_path}' -vn -c:a libmp3lame '{output_path}'"
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.wait()
            
            if os.path.exists(output_path):
                return {'success': True, 'file': output_path}
                
        except:
            pass
            
        return {'success': False}
        
    async def compress(self, file_path: str, quality: str = 'medium') -> Dict:
        """Compress video"""
        try:
            quality_settings = {
                'low': '-crf 28 -preset fast',
                'medium': '-crf 23 -preset medium',
                'high': '-crf 18 -preset slow'
            }
            
            output_path = os.path.join(
                self.output_dir,
                f"{os.path.splitext(os.path.basename(file_path))[0]}_compressed.mp4"
            )
            
            command = f"ffmpeg -i '{file_path}' {quality_settings.get(quality)} '{output_path}'"
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.wait()
            
            if os.path.exists(output_path):
                return {'success': True, 'file': output_path}
                
        except:
            pass
            
        return {'success': False}

video_tools = VideoTools()
