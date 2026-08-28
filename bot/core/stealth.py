import os
import random
import asyncio
from typing import Dict

class StealthMode:
    """Heroku detection evasion system"""
    
    def __init__(self):
        self.is_heroku = 'DYNO' in os.environ
        self.stealth_enabled = True
        self.process_names = [
            'worker', 'web', 'bot', 'app', 'service',
            'background', 'daemon', 'scheduler', 'runner'
        ]
        
    def get_stealth_name(self) -> str:
        """Get random process name to avoid detection"""
        return random.choice(self.process_names)
        
    async def hide_bot_activity(self):
        """Hide bot activity from Heroku detection"""
        if not self.is_heroku:
            return
            
        # Set environment variables to avoid detection
        os.environ['HEROKU_APP_NAME'] = ''
        os.environ['DYNO'] = ''
        os.environ['PORT'] = '8080'
        
        # Random sleep to avoid pattern detection
        await asyncio.sleep(random.randint(1, 5))
        
    async def randomize_requests(self):
        """Randomize request intervals"""
        if not self.stealth_enabled:
            return
            
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
    def get_stealth_status(self) -> Dict:
        return {
            'enabled': self.stealth_enabled,
            'is_heroku': self.is_heroku,
            'process_name': self.get_stealth_name()
        }

stealth = StealthMode()
