from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth_utils import create_access_token, get_current_user
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

@router.post("/login")
def login(login_req: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, login_req.username)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    if not crud.verify_password(login_req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # JWT 발급
    token = create_access_token({"sub":user.username, "user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def read_me(current_user: models.User = Depends(get_current_user)):
    return {
        "message": "This is your profile",
        "id": current_user.id,
        "username": current_user.username
    }