from datetime import datetime
from bot.database.db import db

class TaskDB:
    def __init__(self):
        self.collection = db.tasks
        
    async def add_task(self, task_id: str, user_id: int, task_type: str, url: str = ""):
        await self.collection.insert_one({
            'task_id': task_id,
            'user_id': user_id,
            'task_type': task_type,
            'url': url,
            'status': 'queued',
            'progress': 0,
            'created_at': datetime.now(),
            'completed_at': None,
            'file_name': '',
            'file_size': 0
        })
        
    async def update_task_status(self, task_id: str, status: str):
        update = {'status': status}
        if status in ['completed', 'failed', 'cancelled']:
            update['completed_at'] = datetime.now()
            
        await self.collection.update_one(
            {'task_id': task_id},
            {'$set': update}
        )
        
    async def update_task_progress(self, task_id: str, progress: float):
        await self.collection.update_one(
            {'task_id': task_id},
            {'$set': {'progress': progress}}
        )
        
    async def get_task(self, task_id: str):
        return await self.collection.find_one({'task_id': task_id})
        
    async def get_user_tasks(self, user_id: int, limit: int = 10):
        tasks = []
        cursor = self.collection.find({'user_id': user_id}).sort('created_at', -1).limit(limit)
        async for task in cursor:
            tasks.append(task)
        return tasks
        
    async def get_task_stats(self) -> dict:
        total = await self.collection.count_documents({})
        completed = await self.collection.count_documents({'status': 'completed'})
        failed = await self.collection.count_documents({'status': 'failed'})
        active = await self.collection.count_documents({'status': {'$in': ['queued', 'downloading', 'uploading']}})
        
        return {
            'total': total,
            'completed': completed,
            'failed': failed,
            'active': active
        }

tasks_db = TaskDB()
