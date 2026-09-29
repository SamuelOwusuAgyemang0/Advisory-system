from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True, index=True)
    full_name     = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role          = Column(String(20), default="student")
    created_at    = Column(DateTime, server_default=func.now())
    results         = relationship("SHSResult", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")

class SHSResult(Base):
    __tablename__ = "shs_results"
    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id"), nullable=False)
    shs_program      = Column(String(50))
    elective_1       = Column(String(50))
    elective_1_grade = Column(String(3))
    elective_2       = Column(String(50))
    elective_2_grade = Column(String(3))
    elective_3       = Column(String(50))
    elective_3_grade = Column(String(3))
    interest         = Column(String(50))
    core_math_grade  = Column(String(3))
    english_grade    = Column(String(3))
    science_grade    = Column(String(3))
    social_grade     = Column(String(3))
    submitted_at     = Column(DateTime, server_default=func.now())
    user             = relationship("User", back_populates="results")
    recommendation   = relationship("Recommendation", back_populates="result", uselist=False)
class Recommendation(Base):
    __tablename__ = "recommendations"
    id                    = Column(Integer, primary_key=True, index=True)
    user_id               = Column(Integer, ForeignKey("users.id"), nullable=False)
    result_id             = Column(Integer, ForeignKey("shs_results.id"), nullable=False)
    recommended_programme = Column(String(100))
    model_version         = Column(String(10))
    confidence_score      = Column(Float)
    eligible              = Column(Boolean, default=False)
    generated_at          = Column(DateTime, server_default=func.now())
    user    = relationship("User", back_populates="recommendations")
    result  = relationship("SHSResult", back_populates="recommendation")
    careers = relationship("CareerSuggestion", back_populates="recommendation")

class CareerSuggestion(Base):
    __tablename__ = "career_suggestions"
    id                = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=False)
    career_title      = Column(String(100))
    career_description= Column(String(255))
    industry          = Column(String(50))
    recommendation    = relationship("Recommendation", back_populates="careers")