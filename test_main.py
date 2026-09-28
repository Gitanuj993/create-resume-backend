"""
API Gateway Interface
"""
import io

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from models import ResumeData

app = FastAPI(title="Resume Generator API")

# MVP: wide open CORS so any frontend can call this during development.
# Tighten allow_origins to your actual frontend domain before going live.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

env = Environment(loader=FileSystemLoader("templates")) # **


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/generate-resume")
async def generate_resume(data: ResumeData):
    try:
        template = env.get_template("resume.html")
        html_content = template.render(**data.model_dump())
        pdf_bytes = HTML(string=html_content).write_pdf()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {e}")

    safe_name = data.full_name.replace(" ", "_")
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={safe_name}_resume.pdf"},
    )

