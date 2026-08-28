import os
import asyncio
import aiohttp
from typing import Dict

class KeepAlive:
    """24/7 keep alive system for Heroku"""
    
    def __init__(self):
        self.is_heroku = 'DYNO' in os.environ
        self.app_url = os.getenv('APP_URL', '')
        self.last_ping = 0
        self.ping_interval = 300  # 5 minutes
        
    async def start(self):
        """Start keep alive"""
        if not self.is_heroku:
            return
            
        if not self.app_url:
            app_name = os.getenv('HEROKU_APP_NAME', '')
            if app_name:
                self.app_url = f"https://{app_name}.herokuapp.com"
                
        if self.app_url:
            asyncio.create_task(self._keep_alive_loop())
            
    async def _keep_alive_loop(self):
        """Keep alive loop"""
        while True:
            try:
                await self.ping_self()
                await asyncio.sleep(self.ping_interval)
            except:
                await asyncio.sleep(60)
                
    async def ping_self(self):
        """Ping own app"""
        if not self.app_url:
            return
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.app_url, timeout=10) as response:
                    self.last_ping = asyncio.get_event_loop().time()
        except:
            pass
            
    def get_status(self) -> Dict:
        """Get keep alive status"""
        return {
            'active': self.is_heroku,
            'app_url': self.app_url,
            'last_ping': self.last_ping
        }

keep_alive = KeepAlive()
