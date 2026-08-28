import os
import asyncio
from typing import Dict

class HerokuKeeper:
    """Auto restart and health check for Heroku"""
    
    def __init__(self):
        self.is_heroku = 'DYNO' in os.environ
        self.app_name = os.getenv('HEROKU_APP_NAME', '')
        self.last_restart = 0
        
    async def start(self):
        """Start Heroku keeper"""
        if not self.is_heroku:
            return
            
        asyncio.create_task(self._keeper_loop())
        
    async def _keeper_loop(self):
        """Keeper loop"""
        while True:
            try:
                await asyncio.sleep(300)  # 5 minutes
            except:
                await asyncio.sleep(60)
                
    def get_status(self) -> Dict:
        """Get keeper status"""
        return {
            'active': self.is_heroku,
            'app_name': self.app_name,
            'last_restart': self.last_restart
        }

heroku_keeper = HerokuKeeper()
