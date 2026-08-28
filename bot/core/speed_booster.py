import os
import asyncio
from typing import Dict, Optional

class SpeedBooster:
    """Speed optimization for Heroku"""
    
    def __init__(self):
        self.is_heroku = 'DYNO' in os.environ
        self.optimal_settings = self.get_optimal_settings()
        
    def get_optimal_settings(self) -> Dict:
        if self.is_heroku:
            return {
                'chunk_size': 256 * 1024,
                'connections': 8,
                'split': 8,
                'buffer_size': 1024 * 1024,
                'timeout': 120,
                'max_workers': 50,
                'queue_limit': 10
            }
        else:
            return {
                'chunk_size': 1024 * 1024,
                'connections': 16,
                'split': 16,
                'buffer_size': 4 * 1024 * 1024,
                'timeout': 300,
                'max_workers': 100,
                'queue_limit': 25
            }
            
    async def optimize_download(self, url: str) -> Dict:
        settings = self.optimal_settings.copy()
        
        if 'm3u8' in url.lower():
            settings['chunk_size'] = 512 * 1024
            settings['connections'] = 5
        elif 'mega' in url.lower():
            settings['chunk_size'] = 1024 * 1024
            settings['connections'] = 4
        elif 'drive.google' in url.lower():
            settings['chunk_size'] = 512 * 1024
            settings['connections'] = 4
            
        return settings
        
    async def get_speed_limit(self, user_id: Optional[int] = None) -> int:
        if not user_id:
            return 10
            
        try:
            from bot.database.users import users_db
            user = await users_db.get_user(user_id)
            has_session = user.get('has_session', False) if user else False
            is_premium = user.get('is_premium', False) if user else False
            
            if has_session and is_premium:
                return 20
            elif has_session or is_premium:
                return 15
            else:
                return 10
        except:
            return 10
            
    def get_status(self) -> Dict:
        return {
            'active': self.is_heroku,
            'settings': self.optimal_settings
        }

speed_booster = SpeedBooster()
