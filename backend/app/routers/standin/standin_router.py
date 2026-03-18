from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from threading import Thread
import shutil

from app.core.standin.pipeline import run_pipeline
from app.core.standin.job_manager import create_job, get_job

router = APIRouter( prefix="/standin", tags=["standin"] )

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    job_id = create_job()

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    Thread(
        target=run_pipeline,
        args=(file_path, job_id),
        daemon=True
    ).start()

    return {
        "job_id": job_id
    }


@router.get("/status/{job_id}")
def status(job_id: str):

    job = get_job(job_id)

    if not job:
        return {"error": "Job não encontrado"}

    return job