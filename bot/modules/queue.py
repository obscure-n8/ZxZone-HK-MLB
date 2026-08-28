import asyncio
from typing import Dict, Optional
from bot.config import Config

class TaskQueue:
    def __init__(self):
        self.queue = asyncio.Queue(maxsize=Config.QUEUE_LIMIT)
        self.active_tasks = {}
        self.waiting_tasks = []
        
    async def add_task(self, task_id: str, task_data: Dict) -> bool:
        """Add task to queue"""
        if len(self.active_tasks) >= Config.BOT_MAX_TASKS:
            return False
            
        task_data['task_id'] = task_id
        task_data['status'] = 'queued'
        self.waiting_tasks.append(task_data)
        
        await self.process_queue()
        return True
        
    async def process_queue(self):
        """Process queue"""
        while len(self.active_tasks) < Config.BOT_MAX_TASKS and self.waiting_tasks:
            task = self.waiting_tasks.pop(0)
            task['status'] = 'active'
            self.active_tasks[task['task_id']] = task
            asyncio.create_task(self.execute_task(task))
            
    async def execute_task(self, task: Dict):
        """Execute task"""
        task_id = task['task_id']
        
        try:
            if task['type'] == 'leech':
                await self.process_leech(task)
            elif task['type'] == 'mirror':
                await self.process_mirror(task)
                
            task['status'] = 'completed'
            
        except Exception as e:
            task['status'] = 'failed'
            task['error'] = str(e)
            
        finally:
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
            await self.process_queue()
            
    async def process_leech(self, task: Dict):
        """Process leech task"""
        from bot.modules.downloader import downloader
        from bot.modules.uploader import uploader
        
        result = await downloader.download_file(task['url'], task.get('file_path', ''))
        if result['success']:
            await uploader.upload_to_telegram(
                task['client'], result['file'], task['chat_id'],
                user_id=task['user_id']
            )
            
    async def process_mirror(self, task: Dict):
        """Process mirror task"""
        from bot.modules.downloader import downloader
        from bot.modules.rclone import rclone_manager
        
        result = await downloader.download_file(task['url'], task.get('file_path', ''))
        if result['success']:
            await rclone_manager.upload_file(result['file'])
            
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel task"""
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
            await self.process_queue()
            return True
            
        for task in self.waiting_tasks:
            if task['task_id'] == task_id:
                self.waiting_tasks.remove(task)
                return True
                
        return False
        
    def get_queue_status(self) -> Dict:
        """Get queue status"""
        return {
            'active': len(self.active_tasks),
            'waiting': len(self.waiting_tasks),
            'total': len(self.active_tasks) + len(self.waiting_tasks),
            'max': Config.BOT_MAX_TASKS
        }

task_queue = TaskQueue()
