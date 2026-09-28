from app.schemas.resume import ResumeRequest
from services.pdf_service import PDFService


class ResumeService:

    def __init__(self):
        self.pdf_service = PDFService()

    def generate_resume(self, resume: ResumeRequest) -> str:
        """
        Generate a resume PDF from the validated nested resume data.

        Args:
            resume: Validated ResumeRequest containing the complete
                    nested resume structure.

        Returns:
            Path to the generated PDF file.
        """

        # Convert Pydantic model into a normal Python dictionary
        resume_data = resume.model_dump(exclude_none=True)

        # Use the user's name for the generated filename
        personal = resume_data.get("personal", {})
        name = personal.get("name", "resume")

        filename = self._create_filename(name)

        # Delegate PDF generation to PDFService
        pdf_path = self.pdf_service.generate_resume(
            resume_data=resume_data,
            filename=filename,
        )

        return pdf_path

    @staticmethod
    def _create_filename(name: str) -> str:
        """
        Convert the candidate's name into a safe PDF filename.
        """

        safe_name = "".join(
            character
            for character in name
            if character.isalnum() or character in (" ", "_", "-")
        )

        safe_name = safe_name.strip().replace(" ", "_")

        return f"{safe_name or 'resume'}.pdf"
