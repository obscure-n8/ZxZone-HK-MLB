import time
import asyncio
from typing import Dict, Optional, Any

class SmartCache:
    """Smart caching for Heroku performance"""
    
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300
        self.max_cache_size = 100
        self.hit_count = 0
        self.miss_count = 0
        
    async def get(self, key: str, fetch_func=None) -> Optional[Any]:
        if key in self.cache:
            cached = self.cache[key]
            if time.time() - cached['time'] < self.cache_timeout:
                self.hit_count += 1
                return cached['data']
                
        if fetch_func:
            data = await fetch_func()
            await self.set(key, data)
            self.miss_count += 1
            return data
            
        return None
        
    async def set(self, key: str, data: Any):
        if len(self.cache) >= self.max_cache_size:
            await self.cleanup()
            
        self.cache[key] = {
            'data': data,
            'time': time.time()
        }
        
    async def cleanup(self):
        current_time = time.time()
        for key in list(self.cache.keys()):
            if current_time - self.cache[key]['time'] > self.cache_timeout:
                del self.cache[key]
                
    async def clear(self):
        self.cache.clear()
        
    def get_stats(self) -> Dict:
        return {
            'size': len(self.cache),
            'hits': self.hit_count,
            'misses': self.miss_count
        }

smart_cache = SmartCache()
