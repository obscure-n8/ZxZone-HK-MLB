import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def safe_get_env(key: str, default: str = "") -> str:
    value = os.getenv(key, default)
    return value.strip() if value else default

def safe_get_int(key: str, default: int = 0) -> int:
    try:
        return int(safe_get_env(key, str(default)))
    except:
        return default

class Config:
    # Required
    BOT_TOKEN = safe_get_env("BOT_TOKEN", "")
    API_ID = safe_get_int("API_ID", 0)
    API_HASH = safe_get_env("API_HASH", "")
    OWNER_ID = safe_get_int("OWNER_ID", 0)
    DATABASE_URL = safe_get_env("DATABASE_URL", "")
    
    # Bot Info
    BOT_USERNAME = safe_get_env("BOT_USERNAME", "ZxZoneHKMLB_Bot")
    AUTHOR_NAME = safe_get_env("AUTHOR_NAME", "ZxZone Hub")
    
    # Links
    UPDATE_CHANNEL = safe_get_env("UPDATE_CHANNEL", "https://t.me/zxzoneupdates")
    REPO_LINK = safe_get_env("REPO_LINK", "https://github.com/obscure-n8/ZxZone-HK-MLB")
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DOWNLOAD_DIR = str(BASE_DIR / "downloads")
    ENCODE_DIR = str(BASE_DIR / "encode")
    THUMB_DIR = str(BASE_DIR / "thumbnails")
    CONFIG_DIR = str(BASE_DIR / "config")
    SESSION_DIR = str(BASE_DIR / "sessions")
    
    # Heroku Optimized Limits
    BOT_MAX_TASKS = safe_get_int("MAX_TOTAL_TASKS", 25)
    USER_MAX_TASKS = safe_get_int("MAX_TASKS_PER_USER", 3)
    QUEUE_LIMIT = safe_get_int("QUEUE_LIMIT", 10)
    
    # Upload
    DEFAULT_UPLOAD_MODE = safe_get_env("DEFAULT_UPLOAD_MODE", "document")
    LEECH_SPLIT_SIZE = safe_get_int("LEECH_SPLIT_SIZE", 2 * 1024 * 1024 * 1024)
    
    # Aria2
    ARIA2_HOST = safe_get_env("ARIA2_HOST", "http://localhost")
    ARIA2_PORT = safe_get_int("ARIA2_PORT", 6800)
    ARIA2_SECRET = safe_get_env("ARIA2_SECRET", "")
    
    # Rclone
    RCLONE_CONFIG = safe_get_env("RCLONE_CONFIG_PATH", str(BASE_DIR / "config" / "rclone.conf"))
    RCLONE_REMOTE = safe_get_env("RCLONE_REMOTE", "gdrive")
    
    # Heroku
    PORT = safe_get_int("PORT", 8080)
    APP_URL = safe_get_env("APP_URL", "")
    IS_HEROKU = 'DYNO' in os.environ
    
    @classmethod
    def validate_config(cls):
        errors = []
        if not cls.BOT_TOKEN:
            errors.append("BOT_TOKEN is missing!")
        if not cls.API_ID:
            errors.append("API_ID is missing!")
        if not cls.API_HASH:
            errors.append("API_HASH is missing!")
        if not cls.OWNER_ID:
            errors.append("OWNER_ID is missing!")
        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL is missing!")
        if errors:
            raise ValueError("\n".join(errors))
        return True
    
    @classmethod
    def ensure_dirs(cls):
        dirs = [
            cls.DOWNLOAD_DIR, cls.ENCODE_DIR, cls.THUMB_DIR,
            cls.CONFIG_DIR, cls.SESSION_DIR,
            os.path.join(cls.DOWNLOAD_DIR, "temp"),
            os.path.join(cls.DOWNLOAD_DIR, "queue"),
            os.path.join(cls.THUMB_DIR, "users"),
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
