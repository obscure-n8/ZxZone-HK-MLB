import os
import gc
import asyncio
import psutil
from typing import Dict
from bot.config import Config

class HerokuOptimizer:
    """Heroku memory optimizer"""
    
    def __init__(self):
        self.is_heroku = 'DYNO' in os.environ
        self.memory_threshold = 400  # MB
        
    async def apply_optimizations(self):
        """Apply Heroku optimizations"""
        if not self.is_heroku:
            return
            
        # Optimize for free dyno (512MB)
        Config.BOT_MAX_TASKS = min(Config.BOT_MAX_TASKS, 15)
        Config.USER_MAX_TASKS = min(Config.USER_MAX_TASKS, 2)
        Config.QUEUE_LIMIT = min(Config.QUEUE_LIMIT, 5)
        
        # Start background optimization
        asyncio.create_task(self._optimization_loop())
        
    async def _optimization_loop(self):
        """Background optimization loop"""
        while True:
            try:
                memory_usage = self.get_memory_usage()
                
                if memory_usage > self.memory_threshold:
                    gc.collect()
                    
                    import functools
                    for obj in gc.get_objects():
                        if isinstance(obj, functools._lru_cache_wrapper):
                            obj.cache_clear()
                            
                await asyncio.sleep(300)
                
            except:
                await asyncio.sleep(60)
                
    def get_memory_usage(self) -> float:
        """Get memory usage in MB"""
        process = psutil.Process()
        return process.memory_info().rss / (1024 * 1024)
        
    def get_status(self) -> Dict:
        """Get optimizer status"""
        return {
            'active': self.is_heroku,
            'memory': self.get_memory_usage()
        }

heroku_optimizer = HerokuOptimizer()
