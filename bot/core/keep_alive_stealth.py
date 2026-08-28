import os
import random
import asyncio
import aiohttp
from typing import Dict

class StealthKeepAlive:
    """Stealth keep alive system"""
    
    def __init__(self):
        self.is_heroku = 'DYNO' in os.environ
        self.app_url = os.getenv('APP_URL', '')
        self.ping_interval = (240, 360)  # Random 4-6 minutes
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Mozilla/5.0 (X11; Linux x86_64)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)'
        ]
        
    async def start(self):
        """Start stealth keep alive"""
        if not self.is_heroku:
            return
            
        if not self.app_url:
            app_name = os.getenv('HEROKU_APP_NAME', '')
            if app_name:
                self.app_url = f"https://{app_name}.herokuapp.com"
                
        asyncio.create_task(self._stealth_loop())
        
    async def _stealth_loop(self):
        """Stealth ping loop"""
        while True:
            try:
                # Random user agent
                headers = {
                    'User-Agent': random.choice(self.user_agents)
                }
                
                # Random ping
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        self.app_url,
                        headers=headers,
                        timeout=random.randint(5, 10)
                    ) as response:
                        pass
                        
                # Random sleep
                await asyncio.sleep(random.uniform(*self.ping_interval))
                
            except:
                await asyncio.sleep(60)
                
    def get_status(self) -> Dict:
        return {
            'active': self.is_heroku,
            'interval': self.ping_interval,
            'agents': len(self.user_agents)
        }

stealth_keep_alive = StealthKeepAlive()
