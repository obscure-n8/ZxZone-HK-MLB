from bot.database.db import db

class SettingsDB:
    def __init__(self):
        self.collection = db.settings
        
    async def get_settings(self, key: str = "bot_settings") -> dict:
        """Get bot settings"""
        settings = await self.collection.find_one({'key': key})
        return settings.get('data', {}) if settings else {}
        
    async def update_settings(self, data: dict, key: str = "bot_settings"):
        """Update bot settings"""
        await self.collection.update_one(
            {'key': key},
            {'$set': {'data': data}},
            upsert=True
        )
        
    async def get_setting(self, setting_key: str, default=None):
        """Get specific setting"""
        settings = await self.get_settings()
        return settings.get(setting_key, default)
        
    async def update_setting(self, setting_key: str, value):
        """Update specific setting"""
        settings = await self.get_settings()
        settings[setting_key] = value
        await self.update_settings(settings)
        
    async def set_default_settings(self):
        """Set default settings"""
        default = {
            'max_tasks_per_user': 3,
            'max_total_tasks': 25,
            'default_upload_mode': 'document',
            'force_subscribe': False,
            'maintenance_mode': False,
        }
        await self.update_settings(default)
        
    async def toggle_maintenance(self, status: bool = None) -> bool:
        """Toggle maintenance mode"""
        current = await self.get_setting('maintenance_mode', False)
        new_status = status if status is not None else not current
        await self.update_setting('maintenance_mode', new_status)
        return new_status

# Create instance
settings_db = SettingsDB()
