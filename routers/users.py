from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, models
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# 회원가입
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # username 중복체크
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    # user 생성
    new_user = crud.create_user(db, user)
    return new_user

@router.get("/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
