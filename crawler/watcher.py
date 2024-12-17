from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from worker.tasks import convert_las_to_json_task
from .crawlerconfig import CRAWLER_CONFIG
from pathlib import Path
import time

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

        # Submit the file for processing via Celery
        result = convert_las_to_json_task.delay(str(filepath), str(CRAWLER_CONFIG["PROCESSED_FOLDER"]))
        print(f"Task submitted for {filepath}, Task ID: {result.id}")


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
