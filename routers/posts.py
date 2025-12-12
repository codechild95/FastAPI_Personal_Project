from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import schemas, crud
from auth_utils import get_current_user
from database import get_db
import models
from sqlalchemy import text   

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

# 전체 게시글(JSON, 작성자 정보 포함X)
@router.get("/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

# Front HTML 함수 정의
@router.get("/list-author")
def list_posts_with_authors(request: Request, db: Session = Depends(get_db)):
    posts = crud.get_posts_with_author_rows(db)
    return templates.TemplateResponse(
        "posts_with_authors.html",
        {
            "request": request,
            "posts": posts
        }
    )
#SQL 연습용 API 추가
@router.get("/raw/all")
def get_posts_raw(db: Session = Depends(get_db)):
    sql = text("SELECT * FROM posts")
    result = db.execute(sql)
    return [dict(r._mapping) for r in result.fetchall()]

# 현재 로그인한 유저가 쓴 글만 보기
@router.get("/me", response_model=list[schemas.Post])
def read_my_post(current_user: models.User = Depends(get_current_user), 
                 db: Session=Depends(get_db)):
    return crud.get_posts_by_users(db, current_user.id)



# 로그인한 유저가 글 작성 (user_id 채우기)
@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    
    new_post = crud.create_post(db, post, user_id=current_user.id)
    return new_post

# JOIN + relationship 사용: 작성자 정보까지 리턴
@router.get("/with-authors/all", response_model=list[schemas.PostWithAuthor])
def read_posts_with_authors(db: Session = Depends(get_db)):
    posts = crud.get_posts_with_authors(db)
    return posts # Post.author 에 User 객체가 달려있음

# 특정 유저가 쓴 글만 보기
@router.get("/by-user/{user_id}", response_model=list[schemas.Post])
def read_posts_By_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_posts_by_users(db, user_id)

# JOIN SQL API 추가
@router.get("/raw/with_author")
def get_posts_with_author_row(db: Session = Depends(get_db)):
    sql = text("""
               SELECT posts.id, posts.title, posts.content, users.username
               FROM posts
               JOIN users ON posts.user_id = users.id
               """)
    result = db.execute(sql)
    return [dict(row._mapping) for row in result.fetchall()]

# 단일 게시글 조회
@router.get("/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post