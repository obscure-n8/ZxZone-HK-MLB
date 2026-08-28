import os
import random
import asyncio
from typing import Dict
from bot.core.stealth import stealth
from bot.core.anti_ban import anti_ban
from bot.core.rotator import rotator
from bot.core.keep_alive_stealth import stealth_keep_alive

class StealthManager:
    """Complete stealth management system"""
    
    def __init__(self):
        self.is_heroku = 'DYNO' in os.environ
        self.components = {
            'stealth': stealth,
            'anti_ban': anti_ban,
            'rotator': rotator,
            'keep_alive': stealth_keep_alive
        }
        
    async def start_all(self):
        """Start all stealth components"""
        if not self.is_heroku:
            return
            
        await stealth.hide_bot_activity()
        await anti_ban.hide_heroku_headers()
        await rotator.randomize_startup()
        await stealth_keep_alive.start()
        
        asyncio.create_task(rotator.rotate_process())
        
    async def get_stealth_report(self) -> Dict:
        """Get stealth system report"""
        return {
            'stealth': stealth.get_stealth_status(),
            'anti_ban': anti_ban.get_status(),
            'rotator': rotator.get_status(),
            'keep_alive': stealth_keep_alive.get_status()
        }

stealth_manager = StealthManager()
