from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import SHSResult, Recommendation, CareerSuggestion
from app.services.ml_service import ml_service

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

@router.post("/{result_id}")
def get_recommendation(
    result_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.query(SHSResult).filter(
        SHSResult.id == result_id, SHSResult.user_id == user_id
    ).first()
    if not result:
        raise HTTPException(404, "Result not found")

    prediction = ml_service.predict(result.__dict__)

    rec = Recommendation(
        user_id=user_id,
        result_id=result_id,
        recommended_programme=prediction["recommended_programme"],
        model_version=prediction["model_version"],
        confidence_score=prediction["confidence"],
        eligible=prediction["eligible"],
    )
    db.add(rec); db.flush()
    for career in prediction["careers"]:
        db.add(CareerSuggestion(
            recommendation_id=rec.id,
            career_title=career["title"],
            industry=career["industry"]
        ))
    db.commit()
    return prediction

@router.get("/history")
def history(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Recommendation).filter(Recommendation.user_id == user_id).all()