import os
import logging

# Define log directory and file
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "hids_logs.log")

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Get the logger instance
logger = logging.getLogger("HIDS_Logger")

# Remove any existing handlers (fixes "Bad file descriptor" issue)
if logger.hasHandlers():
    logger.handlers.clear()

# Set logging level
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler(LOG_FILE, mode="a")
file_handler.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Logger initialized successfully.")
