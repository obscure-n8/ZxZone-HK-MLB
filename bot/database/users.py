from datetime import datetime
from bot.database.db import db

class UserDB:
    def __init__(self):
        self.collection = db.users
        
    async def add_user(self, user_id: int, username: str = "", first_name: str = ""):
        user = await self.get_user(user_id)
        if not user:
            await self.collection.insert_one({
                'user_id': user_id,
                'username': username,
                'first_name': first_name,
                'joined_at': datetime.now(),
                'total_tasks': 0,
                'total_downloads': 0,
                'is_banned': False,
                'is_premium': False,
                'is_admin': False,
                'has_session': False,
                'settings': {}
            })
        else:
            await self.collection.update_one(
                {'user_id': user_id},
                {'$set': {
                    'username': username,
                    'first_name': first_name,
                    'last_seen': datetime.now()
                }}
            )
            
    async def get_user(self, user_id: int):
        return await self.collection.find_one({'user_id': user_id})
        
    async def update_user(self, user_id: int, data: dict):
        await self.collection.update_one(
            {'user_id': user_id},
            {'$set': data}
        )
        
    async def increment_tasks(self, user_id: int):
        await self.collection.update_one(
            {'user_id': user_id},
            {'$inc': {'total_tasks': 1}}
        )
        
    async def increment_downloads(self, user_id: int):
        await self.collection.update_one(
            {'user_id': user_id},
            {'$inc': {'total_downloads': 1}}
        )
        
    async def ban_user(self, user_id: int):
        await self.update_user(user_id, {'is_banned': True})
        
    async def unban_user(self, user_id: int):
        await self.update_user(user_id, {'is_banned': False})
        
    async def is_banned(self, user_id: int) -> bool:
        user = await self.get_user(user_id)
        return user.get('is_banned', False) if user else False
        
    async def get_total_users(self) -> int:
        return await self.collection.count_documents({})
        
    async def get_user_settings(self, user_id: int) -> dict:
        user = await self.get_user(user_id)
        return user.get('settings', {}) if user else {}
        
    async def update_user_settings(self, user_id: int, settings: dict):
        await self.collection.update_one(
            {'user_id': user_id},
            {'$set': {'settings': settings}}
        )

users_db = UserDB()
