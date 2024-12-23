import os
import csv
from .celeryconfig import csv_path
from . import app


def update_csv(result, json_data=None):
    """
    Update the CSV file dynamically based on the result and json_data.
    :param result: Metadata about the LAS to JSON conversion.
    :param json_data: Full JSON data structure including headers, parameters, curves, and data (optional).
    """
    # Initialize fields
    header = {}
    curve_names = []

    if json_data:
        if isinstance(json_data, list) and len(json_data) > 0:
            header = json_data[0].get("header", {})
            curves = json_data[0].get("curves", [])
            curve_names = [curve.get("name", "Unknown") for curve in curves]
        else:
            print(f"Unexpected json_data format: {type(json_data)}")
            header = {}
            curve_names = []

    # Ensure curve names are added to the result
    result["Curve Names"] = ", ".join(curve_names) if curve_names else "None"

    # Combine static fields from result and dynamic fields from the header
    dynamic_fieldnames = list(header.keys())
    fieldnames = list(result.keys()) + dynamic_fieldnames  # Merge result and header keys

    # Ensure the CSV file exists and write the header
    file_exists = os.path.exists(csv_path)
    with open(csv_path, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        # Prepare the row by combining result and header
        row = {**result, **header}

        # Write the row to the CSV
        writer.writerow(row)


@app.task(bind=True)
def handle_task_completion(self, result, json_data=None, initial_task_id=None):
    """
    Handle the completion of a task by updating the CSV file.
    This function is chained to run after `convert_las_to_json_task`.
    """
    try:
        # Ensure result is a dictionary
        if not isinstance(result, dict):
            raise ValueError(f"Expected result to be a dict, got {type(result).__name__}")

        # Combine initial task ID with the current task ID
        combined_task_ids = f"{initial_task_id}, {self.request.id}"
        result["task_id"] = combined_task_ids

        # Update the CSV file
        update_csv(result, json_data)
        print(f"CSV updated with task result: {result}")

        # Return a meaningful status
        return f"CSV updated for file: {result['file_name']}"
    except Exception as e:
        print(f"Error updating CSV: {e}")
        return f"Error updating CSV for file: {result.get('file_name', 'Unknown')}"
