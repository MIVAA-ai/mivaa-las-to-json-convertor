from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from worker.tasks import convert_las_to_json_task
from .crawlerconfig import CRAWLER_CONFIG
from pathlib import Path
import time
import os

class NewFileHandler(FileSystemEventHandler):
    """
    Event handler for detecting new .las files and triggering Celery tasks.
    """

    def on_created(self, event):
        # Check if the event is a file and ends with .las
        if event.is_directory or not event.src_path.endswith(".las"):
            return

        filepath = Path(event.src_path)
        print(f"New file detected: {filepath}")

        # Wait for the file to be fully copied
        if self._is_file_ready(filepath):
            print(f"File ready for processing: {filepath}")
            result = convert_las_to_json_task.delay(str(filepath), str(CRAWLER_CONFIG["PROCESSED_FOLDER"]))
            print(f"Task submitted for {filepath}, Task ID: {result.id}")
        else:
            print(f"File not ready: {filepath}")

    def _is_file_ready(self, filepath, timeout=30, check_interval=1):
        """
        Check if a file is fully copied by monitoring its size.
        :param filepath: Path of the file to check
        :param timeout: Total time (seconds) to wait for file to stabilize
        :param check_interval: Time interval (seconds) between size checks
        :return: True if the file is ready, False otherwise
        """
        last_size = -1
        elapsed_time = 0

        while elapsed_time < timeout:
            current_size = os.path.getsize(filepath)
            if current_size == last_size:
                return True  # File size stabilized, ready for processing
            last_size = current_size
            time.sleep(check_interval)
            elapsed_time += check_interval

        # Timeout reached, file still not stable
        print(f"Warning: File {filepath} not stabilized after {timeout} seconds.")
        return False

def watch_folder():
    """
    Monitor the uploads folder for new files.
    """
    upload_folder = CRAWLER_CONFIG["UPLOAD_FOLDER"]
    print(f"Watching folder: {upload_folder} for new .las files...")

    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(upload_folder), recursive=False)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
