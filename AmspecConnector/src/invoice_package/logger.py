import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get log levels and file paths from .env
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
LOG_FILE_INFO = os.getenv("LOG_FILE_INFO", "logs/info.log")
LOG_FILE_ERROR = os.getenv("LOG_FILE_ERROR", "logs/error.log")
LOG_FILE_DEBUG = os.getenv("LOG_FILE_DEBUG", "logs/debug.log")

# Ensure logs directory exists
os.makedirs(os.path.dirname(LOG_FILE_INFO), exist_ok=True)

# Create log formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL, logging.DEBUG))

# Console Handler (for real-time logging)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Info Log File Handler
info_handler = RotatingFileHandler(LOG_FILE_INFO, maxBytes=5*1024*1024, backupCount=5)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)
logger.addHandler(info_handler)

# Error Log File Handler
error_handler = RotatingFileHandler(LOG_FILE_ERROR, maxBytes=5*1024*1024, backupCount=5)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

# Debug Log File Handler
debug_handler = RotatingFileHandler(LOG_FILE_DEBUG, maxBytes=5*1024*1024, backupCount=5)
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)
logger.addHandler(debug_handler)

