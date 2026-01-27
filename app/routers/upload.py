from fastapi import APIRouter, UploadFile, File
from app.services.excel_loader import load_excel

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/excel")
async def upload_excel(file: UploadFile = File(...)):
    await load_excel(file)
    return {"status": "uploaded"}
