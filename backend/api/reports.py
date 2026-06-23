from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional, List
from ..services.report_service import ReportService

router = APIRouter(prefix="/api/reports")

@router.post("/submit")
async def submit_report(
    location: str = Form(...),
    description: Optional[str] = Form(""),
    file: Optional[UploadFile] = File(None)
):
    """
    Ingests a citizen report, saves the evidence, analyzes the text, and stores the record.
    """
    try:
        record = ReportService.submit_report(location=location, description=description, file=file)
        return {"success": True, "report": record}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_report_history():
    """
    Retrieves all stored citizen reports.
    """
    return ReportService.get_all_reports()
