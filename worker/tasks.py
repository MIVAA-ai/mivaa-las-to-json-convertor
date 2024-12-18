from . import app
from scanners.scanner import Scanner
from utils.SerialiseJson import JsonSerializable
import json
from pathlib import Path
import hashlib

def calculate_checksum(filepath, algorithm="sha256"):
    """
    Calculate the checksum of a file using the specified algorithm.
    """
    hash_func = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

@app.task
def convert_las_to_json_task(filepath, output_folder):
    """
    Task to convert a LAS file to JSONWellLogFormat.
    """
    try:
        # Normalize paths
        filepath = Path(filepath).resolve()
        output_folder = Path(output_folder).resolve()

        # Calculate file checksum
        print(f"Calculating checksum for {filepath}...")
        file_checksum = calculate_checksum(filepath)

        # Parse the LAS file
        print(f"Scanning LAS file: {filepath}...")
        scanner = Scanner(filepath)
        normalised_json = scanner.scan()

        # Ensure json_data is a dict/list
        print(f"Serializing scanned data from {filepath}...")
        json_data = JsonSerializable.to_json(normalised_json)

        # Check if json_data is already serialized, if so, load it back
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        # Save JSON to file
        filename = filepath.stem + ".json"
        output_path = output_folder / filename
        print(f"Saving JSON data to {output_path}...")

        with open(output_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        # Prepare result metadata
        result = {
            "status": "SUCCESS",
            "file_name": filepath.name,
            "file_checksum": file_checksum,
            "output_file": str(output_path),
            "message": f"File processed successfully: {filepath}"
        }

        print(f"Task completed successfully: {result}")


        return result

    except Exception as e:
        result = {
            "status": "ERROR",
            "file_name": filepath.name if 'filepath' in locals() else None,
            "error_message": str(e)
        }
        print(f"Error processing LAS file: {e}")
        return result