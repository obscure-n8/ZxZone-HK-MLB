from typing import List
from bot.config import Config
from bot.database.users import users_db

class PermissionSystem:
    """Permission management"""
    
    def __init__(self):
        self.levels = {
            'owner': 5,
            'sudo': 4,
            'admin': 3,
            'premium': 2,
            'user': 1,
            'banned': 0
        }
        
    async def get_user_level(self, user_id: int) -> str:
        if user_id == Config.OWNER_ID:
            return 'owner'
            
        if user_id in Config.SUDO_USERS if hasattr(Config, 'SUDO_USERS') else []:
            return 'sudo'
            
        user = await users_db.get_user(user_id)
        if not user:
            return 'user'
            
        if user.get('is_banned'):
            return 'banned'
        if user.get('is_admin'):
            return 'admin'
        if user.get('is_premium'):
            return 'premium'
            
        return 'user'
        
    async def is_admin(self, user_id: int) -> bool:
        level = await self.get_user_level(user_id)
        return level in ['owner', 'sudo', 'admin']
        
    async def is_sudo(self, user_id: int) -> bool:
        level = await self.get_user_level(user_id)
        return level in ['owner', 'sudo']
        
    async def is_owner(self, user_id: int) -> bool:
        return user_id == Config.OWNER_ID

permission_system = PermissionSystem()
