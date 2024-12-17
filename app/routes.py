from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Request
from worker.tasks import convert_las_to_json_task
from fastapi.responses import RedirectResponse

router = APIRouter()

# In-memory file statuses
file_status = {}

@router.get("/")
async def index():
    """Root route placeholder."""
    return {"message": "Welcome to the FastAPI Well Log File Processor!"}

@router.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Upload a file and trigger background processing.
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file selected")

        # Access directories from app state
        UPLOAD_FOLDER = request.app.state.UPLOAD_FOLDER
        PROCESSED_FOLDER = request.app.state.PROCESSED_FOLDER

        # Save file to UPLOAD_FOLDER
        filepath = UPLOAD_FOLDER / file.filename
        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())


        # Trigger Celery task for background processing
        result = convert_las_to_json_task.delay(str(filepath), str(PROCESSED_FOLDER))
        file_status[file.filename] = {"status": "Processing", "task_id": result.id}
        print(f"Task submitted: {result.id}")

        # Redirect to success route
        return RedirectResponse(url="/success", status_code=303)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/success/")
async def upload_success():
    """
    Success route placeholder.
    """
    return {"message": "File uploaded successfully and processing started."}


@router.get("/status/")
async def get_file_status():
    """
    Check the status of uploaded files.
    """
    return file_status
