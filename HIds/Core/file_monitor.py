import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

WATCH_DIR = r"C:\Users\KIIT0001\OneDrive\Pictures"  # Update as needed
LOG_FILE = r"C:\Study\MajorProject\IDS\HIds\logs\file_changes.log"
SNAPSHOT_FILE = r"C:\Study\MajorProject\IDS\HIds\logs\snapshot.json"

class FileChangeLogger(FileSystemEventHandler):
    def _init_(self):
        super()._init_()

    def log_change(self, action, path):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"{timestamp} - {action}: {path}"
        print(message)
        with open(LOG_FILE, 'a') as log:
            log.write(message + "\n")

    def on_created(self, event):
        self.log_change("CREATED", event.src_path)

    def on_deleted(self, event):
        self.log_change("DELETED", event.src_path)

    def on_modified(self, event):
        self.log_change("MODIFIED", event.src_path)

    def on_moved(self, event):
        self.log_change("MOVED", f"{event.src_path} -> {event.dest_path}")

def get_current_snapshot(directory):
    snapshot = {}
    for root, _, files in os.walk(directory):
        for f in files:
            full_path = os.path.join(root, f)
            try:
                snapshot[full_path] = os.path.getmtime(full_path)
            except FileNotFoundError:
                continue
    return snapshot

def compare_snapshots(old, new):
    changes = []
    old_files = set(old.keys())
    new_files = set(new.keys())

    added = new_files - old_files
    removed = old_files - new_files
    modified = {f for f in old_files & new_files if old[f] != new[f]}

    for f in added:
        changes.append(("ADDED", f))
    for f in removed:
        changes.append(("REMOVED", f))
    for f in modified:
        changes.append(("MODIFIED", f))

    return changes

def save_snapshot(snapshot):
    with open(SNAPSHOT_FILE, 'w') as f:
        json.dump(snapshot, f)

def load_previous_snapshot():
    if os.path.exists(SNAPSHOT_FILE):
        try:
            with open(SNAPSHOT_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("[!] Warning: snapshot.json is empty or corrupted. Starting fresh.")
            return {}
    return {}


if __name__ == "__main__":
    print(f"[*] Starting to monitor: {WATCH_DIR}")

    # Compare snapshots before starting live monitoring
    prev_snapshot = load_previous_snapshot()
    curr_snapshot = get_current_snapshot(WATCH_DIR)
    changes = compare_snapshots(prev_snapshot, curr_snapshot)

    if changes:
        print("[*] Detected changes since last run:")
        with open(LOG_FILE, 'a') as log:
            for action, file in changes:
                log_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {action}: {file}"
                print(log_msg)
                log.write(log_msg + "\n")
    else:
        print("[*] No changes since last run.")

    # Save current snapshot
    save_snapshot(curr_snapshot)

    # Start real-time monitoring
    event_handler = FileChangeLogger()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=True)
    observer.start()
    print("Xxx")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[!] Monitoring stopped.")

    observer.join()