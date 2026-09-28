from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.schemas.resume import ResumeRequest
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resume",tags=["Resume"])

@router.post(
  "/generate",
  response_class=FileResponse,
  responses={
    200: {
      "description": "Generated resume PDF",
      "content": {
        "application/pdf": {
          "schema": {"type": "string", "format": "binary"}
        }
      },
    }
  },
)
async def create_resume(data:ResumeRequest) :
  pdf_path = ResumeService().generate_resume(data)
  return FileResponse(
    path=pdf_path,
    media_type="application/pdf",
    filename=Path(pdf_path).name
  )
