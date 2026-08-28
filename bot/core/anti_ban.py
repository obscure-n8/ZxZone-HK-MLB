import os
import time
import random
import asyncio
from typing import Dict

class AntiBan:
    """Anti-ban protection system"""
    
    def __init__(self):
        self.is_heroku = 'DYNO' in os.environ
        self.request_interval = (3, 8)  # Random 3-8 seconds
        self.max_requests_per_minute = 20
        self.request_count = 0
        self.last_reset = time.time()
        
    async def check_rate_limit(self) -> bool:
        """Check if rate limit exceeded"""
        current_time = time.time()
        
        if current_time - self.last_reset > 60:
            self.request_count = 0
            self.last_reset = current_time
            
        if self.request_count >= self.max_requests_per_minute:
            await asyncio.sleep(random.uniform(*self.request_interval))
            self.request_count = 0
            self.last_reset = current_time
            
        self.request_count += 1
        return True
        
    async def random_delay(self):
        """Random delay between operations"""
        await asyncio.sleep(random.uniform(*self.request_interval))
        
    async def hide_heroku_headers(self):
        """Hide Heroku-specific headers"""
        os.environ.pop('HEROKU_SLUG_COMMIT', None)
        os.environ.pop('HEROKU_RELEASE_VERSION', None)
        os.environ.pop('HEROKU_APP_ID', None)
        
    def get_status(self) -> Dict:
        return {
            'active': self.is_heroku,
            'request_count': self.request_count,
            'interval': self.request_interval
        }

anti_ban = AntiBan()
