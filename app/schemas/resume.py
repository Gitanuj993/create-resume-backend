from pydantic import BaseModel


class Contact(BaseModel):
    email: str
    phone: str
    location: str


class SocialLinks(BaseModel):
    linkedin: str
    github: str
    portfolio: str


class Skills(BaseModel):
    languages: list[str]
    frameworks: list[str]
    databases: list[str]
    tools: list[str]


class Experience(BaseModel):
    company: str
    role: str
    location: str
    start_date: str
    end_date: str
    description: list[str]


class Project(BaseModel):
    name: str
    description: str
    technologies: list[str]
    link: str


class Achievement(BaseModel):
    title: str
    description: str
    date: str


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: str
    grade: str


class ResumeRequest(BaseModel):
    full_name: str
    contact: Contact
    social_links: SocialLinks
    summary: str
    skills: Skills
    experience: list[Experience]
    projects: list[Project]
    achievements: list[Achievement]
    education: list[Education]
    section_order: list[str]
