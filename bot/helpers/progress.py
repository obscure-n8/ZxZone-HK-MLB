import time
import psutil
import humanize

class Progress:
    def __init__(self):
        self.last_update_time = 0
        
    def get_progress_bar(self, percentage: float) -> str:
        blocks = int(percentage / 10)
        return f"[{'●' * blocks}{'o' * (10 - blocks)}]"
    
    def format_size(self, size: float) -> str:
        return humanize.naturalsize(size)
    
    def format_speed(self, speed: float) -> str:
        return f"{humanize.naturalsize(speed)}/s"
    
    def format_eta(self, seconds: float) -> str:
        if seconds <= 0:
            return "0s"
        return time.strftime("%Hh%Mm%Ss", time.gmtime(seconds))
    
    def get_system_stats(self) -> dict:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/')
        free_disk = humanize.naturalsize(disk.free)
        
        return {
            'cpu': cpu,
            'ram': ram,
            'free_disk': free_disk
        }

progress_helper = Progress()
