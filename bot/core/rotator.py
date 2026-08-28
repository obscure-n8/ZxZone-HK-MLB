import os
import time
import random
import asyncio
from typing import Dict

class ProcessRotator:
    """Process rotation to avoid detection"""
    
    def __init__(self):
        self.is_heroku = 'DYNO' in os.environ
        self.rotation_interval = 1800  # 30 minutes
        self.process_patterns = [
            'python3 -m bot',
            'python3 bot.py',
            'python3 app.py',
            'python3 worker.py'
        ]
        
    async def rotate_process(self):
        """Rotate process pattern"""
        while True:
            try:
                if self.is_heroku:
                    # Random sleep to avoid pattern
                    await asyncio.sleep(random.randint(1500, 2100))
                    
                    # Clear logs to avoid detection
                    os.system('clear')
                    
            except:
                pass
                
    async def randomize_startup(self):
        """Randomize startup time"""
        if self.is_heroku:
            delay = random.randint(10, 60)
            await asyncio.sleep(delay)
            
    def get_current_pattern(self) -> str:
        return random.choice(self.process_patterns)
        
    def get_status(self) -> Dict:
        return {
            'active': self.is_heroku,
            'interval': self.rotation_interval,
            'pattern': self.get_current_pattern()
        }

rotator = ProcessRotator()
