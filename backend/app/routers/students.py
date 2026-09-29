from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import SHSResult
from app.schemas.student import SHSResultCreate

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/results", status_code=201)
def submit_results(
    body: SHSResultCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = SHSResult(user_id=user_id, **body.model_dump())
    db.add(result); db.commit(); db.refresh(result)
    return {"result_id": result.id, "message": "Results submitted"}

@router.get("/results")
def get_my_results(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(SHSResult).filter(SHSResult.user_id == user_id).all()