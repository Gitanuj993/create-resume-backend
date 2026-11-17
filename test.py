from app.schemas.resume import ResumeRequest
from app.services.resume_service import ResumeService

"""
  PUT THE EXACT NESTED JSON
  THAT YOUR ResumeRequest ACCEPTS HERE
"""
resume_data = {
  
        }


resume = ResumeRequest(**resume_data)

service = ResumeService()

pdf_path = service.generate_resume(resume)

print("PDF generated:", pdf_path)