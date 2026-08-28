import os
import asyncio
from typing import Dict
from PIL import Image, ImageEnhance
from bot.config import Config

class HDThumbnailGenerator:
    """1080p HD Thumbnail auto generation"""
    
    def __init__(self):
        self.thumb_dir = os.path.join(Config.THUMB_DIR, 'auto_hd')
        os.makedirs(self.thumb_dir, exist_ok=True)
        self.enabled = True
        self.width = 1920
        self.height = 1080
        
    async def generate_1080p_thumbnail(
        self,
        video_path: str,
        timestamp: str = '00:00:02'
    ) -> Dict:
        """Generate 1080p HD thumbnail"""
        try:
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            thumb_path = os.path.join(self.thumb_dir, f"{video_name}_1080p.jpg")
            
            command = (
                f"ffmpeg -i '{video_path}' "
                f"-ss {timestamp} "
                f"-vframes 1 "
                f"-vf 'scale=1920:1080:force_original_aspect_ratio=decrease,"
                f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2' "
                f"-q:v 2 "
                f"'{thumb_path}'"
            )
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.wait()
            
            if os.path.exists(thumb_path):
                await self.enhance_thumbnail(thumb_path)
                return {
                    'success': True,
                    'thumbnail': thumb_path,
                    'width': self.width,
                    'height': self.height
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
        return {'success': False}
        
    async def enhance_thumbnail(self, thumb_path: str):
        """Enhance thumbnail quality"""
        try:
            with Image.open(thumb_path) as img:
                img = img.convert('RGB')
                
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.3)
                
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.15)
                
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.15)
                
                img.save(thumb_path, 'JPEG', quality=100, optimize=True)
        except:
            pass
            
    def get_status(self) -> Dict:
        return {
            'enabled': self.enabled,
            'quality': '1080p',
            'width': self.width,
            'height': self.height
        }

hd_thumbnail = HDThumbnailGenerator()
