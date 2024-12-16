"""Celery configuration using local filesystem."""

from pathlib import Path
import os

# Root directory for storing broker and backend data
_root = Path(__file__).parent.resolve().joinpath("data")
_backend_folder = _root.joinpath("results")
_backend_folder.mkdir(exist_ok=True, parents=True)

_folders = {
    "data_folder_in": _root.joinpath("in"),
    "data_folder_out": _root.joinpath("in"),  # Must be the same as 'data_folder_in'
    "processed_folder": _root.joinpath("processed"),
}

for folder in _folders.values():
    folder.mkdir(exist_ok=True)

# Celery configuration
broker_url = "filesystem://"
result_backend = f"file:///{os.path.normpath(_backend_folder).replace(os.sep, '/')}"
broker_transport_options = {k: str(v) for k, v in _folders.items()}
task_serializer = "json"
persist_results = True
result_serializer = "json"
accept_content = ["json"]
imports = ("worker.tasks",)  # Import the task module