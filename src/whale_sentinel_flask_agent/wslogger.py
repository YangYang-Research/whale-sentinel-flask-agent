import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()

LOG_MAX_SIZE = os.getenv("LOG_MAX_SIZE", 10000000)  # in bytes
LOG_MAX_BACKUPS = os.getenv("LOG_MAX_BACKUPS", 3)  # number of backup files
AGENT_NAME = os.getenv("WS_AGENT_NAME")

class CustomFormatter(logging.Formatter):
    def formatLevel(self, record):
        # Convert levelname to lowercase
        record.levelname = record.levelname.lower()
        return super().format(record)
    
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        return dt.isoformat()
    
def create_log_directory():
    import os
    log_dir = '/var/log/whale-sentinel/ws-agents'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        os.chmod(log_dir, 0o755)

def setup_logging():
    wslogger = logging.getLogger('wslogger')
    wslogger.setLevel(logging.INFO)
    formatter = CustomFormatter(json.dumps({'level': '%(levelname)s', 'msg': '%(message)s', 'time': '%(asctime)s'}))
    handler = RotatingFileHandler(f'/var/log/whale-sentinel/ws-agents/{AGENT_NAME}.log', maxBytes=int(LOG_MAX_SIZE), backupCount=int(LOG_MAX_BACKUPS))
    handler.setFormatter(formatter)
    wslogger.addHandler(handler)

# setup logging for script
create_log_directory()
setup_logging()
wslogger = logging.getLogger('wslogger')