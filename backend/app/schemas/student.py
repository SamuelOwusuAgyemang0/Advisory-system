import re
from typing import Literal, Optional, List
from pydantic import BaseModel, field_validator, EmailStr

GRADE_PATTERN = re.compile(r'^[A-F][1-9]$')

class StudentRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def strong_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class SHSResultCreate(BaseModel):
    shs_program: Literal[
        "General Arts", "General Science", "Business",
        "Home Economics", "Visual Arts", "Agricultural Science"
    ]
    elective_1: str
    elective_1_grade: str
    elective_2: str
    elective_2_grade: str
    elective_3: str
    elective_3_grade: str
    interest: str
    core_math_grade: str
    english_grade: str
    science_grade: str
    social_grade: str

    @field_validator(
        "core_math_grade","english_grade","science_grade","social_grade",
        "elective_1_grade","elective_2_grade","elective_3_grade"
    )
    @classmethod
    def validate_grade(cls, v):
        if not GRADE_PATTERN.match(v):
            raise ValueError(f"'{v}' is invalid. Grades must be A1 to F9.")
        return v

    @field_validator("elective_1","elective_2","elective_3")
    @classmethod
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Elective subject cannot be empty")
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RecommendationOut(BaseModel):
    eligible: bool
    confidence: float
    model_version: str
    recommended_programme: Optional[str]
    careers: List[dict]