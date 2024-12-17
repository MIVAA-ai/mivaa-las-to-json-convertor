from . import app
from scanners.scanner import Scanner
from utils.SerialiseJson import JsonSerializable
import json
from pathlib import Path

@app.task
def convert_las_to_json_task(filepath, output_folder):
    """
    Task to convert a LAS file to JSONWellLogFormat.
    """
    try:
        # Normalize paths
        filepath = Path(filepath).resolve()
        output_folder = Path(output_folder).resolve()

        scanner = Scanner(filepath)
        normalised_json = scanner.scan()

        # Ensure json_data is a dict/list
        json_data = JsonSerializable.to_json(normalised_json)

        # Check if json_data is already serialized, if so, load it back
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        # Save JSON to file
        filename = filepath.stem + ".json"
        output_path = output_folder / filename

        with open(output_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        print(f"File processed successfully: {filepath}")
        return f"File processed: {output_path}"

    except Exception as e:
        print(f"Error processing LAS file: {e}")
        return f"Error: {e}"