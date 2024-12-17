from fastapi import FastAPI
from app.routes import router
from pathlib import Path

def create_app():
    """
    FastAPI application factory function.
    """
    # Initialize FastAPI app
    app = FastAPI(title="Well Log File Processor", version="1.0.0")

    # Configuration: Directories for uploads and processing
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.state.UPLOAD_FOLDER = BASE_DIR / "uploads"
    app.state.PROCESSED_FOLDER = BASE_DIR / "processed"

    # Ensure directories exist
    app.state.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    app.state.PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

    # Include routes
    app.include_router(router)

    return app