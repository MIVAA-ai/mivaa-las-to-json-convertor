import os
import csv
from .celeryconfig import csv_path
from . import app

# Global set of headers to ensure consistent column order
global_headers = set()

def update_csv(result, json_data=None):
    """
    Update the CSV file dynamically based on the result and json_data.
    :param result: Metadata about the LAS to JSON conversion.
    :param json_data: Full JSON data structure including headers, parameters, curves, and data (optional).
    """
    global global_headers

    # Extract dynamic headers from JSON data
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

    # Add curve names to the result
    result["Curve Names"] = ", ".join(curve_names) if curve_names else "None"

    # Merge headers and dynamically update the global header set
    row = {**result, **header}
    global_headers.update(row.keys())

    # Write to CSV
    write_to_csv(row)


def write_to_csv(row):
    """
    Write a single row to the CSV file, ensuring consistent column order.
    """
    global global_headers

    # Ensure the CSV file exists and write the header
    file_exists = os.path.exists(csv_path)

    with open(csv_path, mode="a", newline="", encoding="utf-8") as csv_file:
        # Sort headers alphabetically for consistent order
        sorted_headers = sorted(global_headers)

        writer = csv.DictWriter(csv_file, fieldnames=sorted_headers)

        if not file_exists:
            writer.writeheader()  # Write header if the file is new

        # Align the row with the current global headers
        aligned_row = {header: row.get(header, None) for header in sorted_headers}
        writer.writerow(aligned_row)

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
