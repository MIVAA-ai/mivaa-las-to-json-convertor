from flask import Blueprint, render_template, request, redirect, url_for, current_app
import os
from worker.tasks import convert_las_to_json_task

main = Blueprint("main", __name__)

# In-memory store for file statuses
file_status = {}

@main.route("/")
def index():
    """Serve the SPA template."""
    return render_template("index.html")

# @main.route("/", methods=["GET", "POST"])
# def upload_file():
#     if request.method == "POST":
#         if "file" not in request.files:
#             return "No file part", 400
#
#         file = request.files["file"]
#         if file.filename == "":
#             return "No selected file", 400
#
#         # Save file to uploads folder
#         filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
#         file.save(filepath)
#
#         result = convert_las_to_json_task.delay(filepath, current_app.config["PROCESSED_FOLDER"])
#         print(f"Task submitted: {result.id}")
#         return redirect(url_for(".success"))
#
#     return render_template("upload.html")
#
# @main.route("/success")
# def success():
#     return render_template("success.html")