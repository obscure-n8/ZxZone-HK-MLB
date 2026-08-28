import os
import re
import time
import string
import random
import asyncio
from typing import Optional, Tuple

class Utils:
    @staticmethod
    def generate_task_id(length: int = 8) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def clean_filename(filename: str) -> str:
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = ' '.join(filename.split())
        if len(filename) > 150:
            name, ext = os.path.splitext(filename)
            filename = name[:147] + ext
        return filename
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        return os.path.splitext(filename)[1].lower()
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url))
    
    @staticmethod
    def is_magnet_link(url: str) -> bool:
        return url.startswith('magnet:')
    
    @staticmethod
    def human_readable_size(size: float) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    @staticmethod
    async def run_command(command: str) -> Tuple[int, str, str]:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()

utils = Utils()
