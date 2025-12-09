from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud
from auth_utils import get_current_user
from database import get_db
import models

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

@router.get("/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    
    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
