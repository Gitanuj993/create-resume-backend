from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


class PDFService:

    def __init__(self, output_dir: str = "generated_resumes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.styles = self._create_styles()

    # =========================================================
    # MAIN PDF GENERATOR
    # =========================================================

    def generate_resume(
        self,
        resume_data: dict,
        filename: str,
    ) -> str:

        output_path = self.output_dir / filename

        document = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
        )

        story = []

        sections = [
            ("personal", self._add_personal_section),
            ("summary", self._add_summary),
            ("education", self._add_education),
            ("experience", self._add_experience),
            ("projects", self._add_projects),
            ("skills", self._add_skills),
            ("certifications", self._add_certifications),
            ("achievements", self._add_achievements),
        ]

        for section_name, renderer in sections:

            data = resume_data.get(section_name)

            if data:
                renderer(story, data)

        document.build(story)

        return str(output_path)

    # =========================================================
    # STYLES
    # =========================================================

    def _create_styles(self):

        base_styles = getSampleStyleSheet()

        return {
            "name": ParagraphStyle(
                "ResumeName",
                parent=base_styles["Title"],
                fontName="Helvetica-Bold",
                fontSize=20,
                leading=24,
                alignment=TA_CENTER,
                spaceAfter=5,
            ),

            "contact": ParagraphStyle(
                "Contact",
                parent=base_styles["Normal"],
                fontName="Helvetica",
                fontSize=9,
                leading=12,
                alignment=TA_CENTER,
                textColor=colors.grey,
                spaceAfter=10,
            ),

            "section": ParagraphStyle(
                "Section",
                parent=base_styles["Heading2"],
                fontName="Helvetica-Bold",
                fontSize=11,
                leading=14,
                spaceBefore=8,
                spaceAfter=5,
            ),

            "heading": ParagraphStyle(
                "Heading",
                parent=base_styles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=10,
                leading=13,
            ),

            "normal": ParagraphStyle(
                "NormalResume",
                parent=base_styles["Normal"],
                fontName="Helvetica",
                fontSize=9,
                leading=13,
                spaceAfter=3,
            ),

            "small": ParagraphStyle(
                "SmallResume",
                parent=base_styles["Normal"],
                fontName="Helvetica",
                fontSize=8,
                leading=11,
            ),
        }

    # =========================================================
    # PERSONAL
    # =========================================================

    def _add_personal_section(
        self,
        story: list,
        personal: dict,
    ):

        name = personal.get("name")

        if name:
            story.append(
                Paragraph(
                    self._escape(name),
                    self.styles["name"],
                )
            )

        contact_items = []

        for field in [
            "email",
            "phone",
            "location",
        ]:

            value = personal.get(field)

            if value:
                contact_items.append(
                    self._escape(str(value))
                )

        if contact_items:
            story.append(
                Paragraph(
                    " | ".join(contact_items),
                    self.styles["contact"],
                )
            )

    # =========================================================
    # SUMMARY
    # =========================================================

    def _add_summary(
        self,
        story: list,
        summary,
    ):

        self._add_section_title(
            story,
            "Professional Summary",
        )

        text = (
            summary.get("text")
            if isinstance(summary, dict)
            else summary
        )

        if text:
            story.append(
                Paragraph(
                    self._escape(str(text)),
                    self.styles["normal"],
                )
            )

    # =========================================================
    # EDUCATION
    # =========================================================

    def _add_education(
        self,
        story: list,
        education: list,
    ):

        self._add_section_title(
            story,
            "Education",
        )

        for item in education:

            degree = item.get("degree")
            field_of_study = item.get("field_of_study")
            institution = item.get("institution")

            program = self._join_non_empty(
                [degree, field_of_study],
                " in ",
            )
            title = self._join_non_empty(
                [program, institution],
                " | ",
            )

            if title:
                story.append(
                    Paragraph(
                        self._escape(title),
                        self.styles["heading"],
                    )
                )

            date_text = self._format_date_range(
                item.get("start_date"),
                item.get("end_date"),
            )

            if date_text:
                story.append(
                    Paragraph(
                        self._escape(date_text),
                        self.styles["small"],
                    )
                )

            grade = item.get("grade")

            if grade:
                story.append(
                    Paragraph(
                        self._escape(f"Grade: {grade}"),
                        self.styles["small"],
                    )
                )

            story.append(Spacer(1, 3))

    # =========================================================
    # EXPERIENCE
    # =========================================================

    def _add_experience(
        self,
        story: list,
        experience: list,
    ):

        self._add_section_title(
            story,
            "Experience",
        )

        for item in experience:

            title = self._join_non_empty(
                [
                    item.get("role"),
                    item.get("company"),
                ],
                " | ",
            )

            if title:
                story.append(
                    Paragraph(
                        self._escape(title),
                        self.styles["heading"],
                    )
                )

            date_text = self._format_date_range(
                item.get("start_date"),
                item.get("end_date"),
            )

            if date_text:
                story.append(
                    Paragraph(
                        self._escape(date_text),
                        self.styles["small"],
                    )
                )

            self._add_bullet_list(
                story,
                item.get("responsibilities", []),
            )

            story.append(Spacer(1, 3))

    # =========================================================
    # PROJECTS
    # =========================================================

    def _add_projects(
        self,
        story: list,
        projects: list,
    ):

        self._add_section_title(
            story,
            "Projects",
        )

        for project in projects:

            name = project.get("name")

            if name:
                story.append(
                    Paragraph(
                        self._escape(name),
                        self.styles["heading"],
                    )
                )

            description = project.get("description")

            if description:
                story.append(
                    Paragraph(
                        self._escape(str(description)),
                        self.styles["normal"],
                    )
                )

            technologies = project.get("technologies")

            if technologies:
                tech_text = ", ".join(
                    str(technology)
                    for technology in technologies
                )

                story.append(
                    Paragraph(
                        f"<b>Technologies:</b> "
                        f"{self._escape(tech_text)}",
                        self.styles["normal"],
                    )
                )

            self._add_bullet_list(
                story,
                project.get("highlights", []),
            )

            story.append(Spacer(1, 3))

    # =========================================================
    # SKILLS
    # =========================================================

    def _add_skills(
        self,
        story: list,
        skills,
    ):

        self._add_section_title(
            story,
            "Skills",
        )

        if isinstance(skills, dict):

            for category, values in skills.items():

                if isinstance(values, list):
                    value_text = ", ".join(
                        str(value)
                        for value in values
                    )
                else:
                    value_text = str(values)

                story.append(
                    Paragraph(
                        f"<b>{self._escape(str(category))}:</b> "
                        f"{self._escape(value_text)}",
                        self.styles["normal"],
                    )
                )

        elif isinstance(skills, list):

            skill_text = ", ".join(
                str(skill)
                for skill in skills
            )

            story.append(
                Paragraph(
                    self._escape(skill_text),
                    self.styles["normal"],
                )
            )

    # =========================================================
    # CERTIFICATIONS
    # =========================================================

    def _add_certifications(
        self,
        story: list,
        certifications: list,
    ):

        self._add_section_title(
            story,
            "Certifications",
        )

        for certification in certifications:

            if isinstance(certification, dict):

                name = certification.get("name")
                issuer = certification.get("issuer")

                text = self._join_non_empty(
                    [name, issuer],
                    " | ",
                )

            else:
                text = str(certification)

            if text:
                story.append(
                    Paragraph(
                        f"• {self._escape(text)}",
                        self.styles["normal"],
                    )
                )

    # =========================================================
    # ACHIEVEMENTS
    # =========================================================

    def _add_achievements(
        self,
        story: list,
        achievements: list,
    ):

        self._add_section_title(
            story,
            "Achievements",
        )

        for achievement in achievements:

            if isinstance(achievement, dict):
                title = achievement.get("title") or achievement.get("text")
                description = achievement.get("description")
                date = achievement.get("date")

                if title:
                    story.append(
                        Paragraph(
                            self._escape(str(title)),
                            self.styles["heading"],
                        )
                    )

                if description:
                    story.append(
                        Paragraph(
                            self._escape(str(description)),
                            self.styles["normal"],
                        )
                    )

                if date:
                    story.append(
                        Paragraph(
                            self._escape(str(date)),
                            self.styles["small"],
                        )
                    )

            elif achievement:
                story.append(
                    Paragraph(
                        f"• {self._escape(str(achievement))}",
                        self.styles["normal"],
                    )
                )

            story.append(Spacer(1, 3))

    # =========================================================
    # HELPERS
    # =========================================================

    def _add_section_title(
        self,
        story: list,
        title: str,
    ):

        story.append(
            Paragraph(
                self._escape(title),
                self.styles["section"],
            )
        )

        line = Table(
            [[""]],
            colWidths=[174 * mm],
            rowHeights=[0.5],
        )

        line.setStyle(
            TableStyle(
                [
                    (
                        "LINEBELOW",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.black,
                    ),
                ]
            )
        )

        story.append(line)
        story.append(Spacer(1, 4))

    def _add_bullet_list(
        self,
        story: list,
        items: list,
    ):

        for item in items:

            text = (
                item.get("text")
                if isinstance(item, dict)
                else str(item)
            )

            if text:
                story.append(
                    Paragraph(
                        f"• {self._escape(text)}",
                        self.styles["normal"],
                    )
                )

    @staticmethod
    def _join_non_empty(
        values: list,
        separator: str,
    ) -> str:

        return separator.join(
            str(value)
            for value in values
            if value
        )

    @staticmethod
    def _format_date_range(
        start_date,
        end_date,
    ) -> str:

        if start_date and end_date:
            return f"{start_date} - {end_date}"

        if start_date:
            return f"{start_date} - Present"

        if end_date:
            return str(end_date)

        return ""

    @staticmethod
    def _escape(value: str) -> str:

        return (
            value
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
