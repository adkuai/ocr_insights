import os
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .collab_services import analyze_document

app = FastAPI(
    title="Hindi-English Document Intelligence",
    version="1.0.0"
)

# Enable CORS for frontend connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Define allowed extensions clearly
# Change this specific line inside app/main.py
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}


@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Validate the document by checking its file extension format directly
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, and PNG image files are supported in offline mode."
        )

    unique_name = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_name

    try:
        content = await file.read()
        if not content:
            return {
                "status": "no_content",
                "message": "The uploaded file is empty.",
                "data": None
            }

        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File size must be below 10 MB."
            )

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        # Process the clean image path locally via EasyOCR
        result = await analyze_document(str(file_path))

        if result is None:
            return {
                "status": "no_content",
                "message": "No meaningful information was detected.",
                "data": None
            }

        return {
            "status": "success",
            "message": "Document analyzed successfully.",
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )

    finally:
        # Guarantee file deletion from your local drive to prevent permission locks
        if file_path.exists():
            try:
                os.remove(file_path)
            except Exception:
                pass

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
