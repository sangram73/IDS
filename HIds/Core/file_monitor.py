import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.logger import logger  # Import the logger

# Define the directory to monitor (Modify as per your system)
MONITOR_DIR = "C:/Users/KIIT0001/Desktop/Lab Test"

# Ensure directory exists
if not os.path.exists(MONITOR_DIR):
    os.makedirs(MONITOR_DIR)

class FileMonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        logger.info(f"📝 File modified: {event.src_path}")

    def on_created(self, event):
        if event.is_directory:
            return
        logger.info(f"📂 File created: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        logger.warning(f"❌ File deleted: {event.src_path}")

# Setup observer
observer = Observer()
event_handler = FileMonitorHandler()
observer.schedule(event_handler, MONITOR_DIR, recursive=True)

# Start monitoring
logger.info(f"🔍 Monitoring started on: {MONITOR_DIR}")

try:
    observer.start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    logger.info("🛑 Monitoring stopped.")

observer.join()
