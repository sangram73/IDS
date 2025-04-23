import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from alert_manager import show_alert, show_warning


class FileSystemMonitor:
    def __init__(self, watch_dir, log_file, snapshot_file):
        self.watch_dir = watch_dir
        self.log_file = log_file
        self.snapshot_file = snapshot_file
        self.event_handler = self.FileChangeLogger(self)
        self.observer = Observer()
        self.StopfileScan = False  # Flag to control sniffing


    class FileChangeLogger(FileSystemEventHandler):
        def __init__(self, monitor):
            super().__init__()
            self.monitor = monitor

        def log_change(self, action, path):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"{timestamp} - {action}: {path}"
            print(message)
            with open(self.monitor.log_file, 'a') as log:
                log.write(message + "\n")

        def on_created(self, event):
            self.log_change("CREATED", event.src_path)

        def on_deleted(self, event):
            self.log_change("DELETED", event.src_path)

        def on_modified(self, event):
            self.log_change("MODIFIED", event.src_path)

        def on_moved(self, event):
            self.log_change("MOVED", f"{event.src_path} -> {event.dest_path}")

    def get_current_snapshot(self):
        snapshot = {}
        for root, _, files in os.walk(self.watch_dir):
            for f in files:
                full_path = os.path.join(root, f)
                try:
                    snapshot[full_path] = os.path.getmtime(full_path)
                except FileNotFoundError:
                    continue
        return snapshot

    def compare_snapshots(self, old, new):
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

        show_alert(changes)

    def save_snapshot(self, snapshot):
        with open(self.snapshot_file, 'w') as f:
            json.dump(snapshot, f)

    def load_previous_snapshot(self):
        if os.path.exists(self.snapshot_file):
            try:
                with open(self.snapshot_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("[!] Warning: snapshot.json is empty or corrupted. Starting fresh.")
                return {}
        return {}

    def start_monitoring(self):
        print(f"[*] Starting to monitor: {self.watch_dir}")

        prev_snapshot = self.load_previous_snapshot()
        curr_snapshot = self.get_current_snapshot()
        changes = self.compare_snapshots(prev_snapshot, curr_snapshot)

        if changes:
            print("[*] Detected changes since last run:")
            show_warning("A file change has been detected")

            with open(self.log_file, 'a') as log:
                for action, file in changes:
                    log_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {action}: {file}"
                    print(log_msg)
                    log.write(log_msg + "\n")
        else:
            print("[*] No changes since last run.")
            show_warning("No changes since last run.")
            FileSystemMonitor.stop(self)


        self.save_snapshot(curr_snapshot)

        self.observer.schedule(self.event_handler, path=self.watch_dir, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            self.observer.stop()
            print("\n[!] Monitoring stopped.")
        self.observer.join()


    def stop(self):
        print("\n[!] Monitoring stopped.")
        self.observer.stop()