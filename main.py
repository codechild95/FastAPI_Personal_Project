from fastapi import FastAPI, HTTPException, Depends, Request
from database import SessionLocal, engine


from sqlalchemy.orm import Session
import models
import schemas

from routers import posts # router 불러옴
from routers import users
from pydantic import BaseModel
from dummy_data import insert_dummy_posts

# Post 모델(models.Post)이 실제 DB(test.db) 안에 posts 테이블로 생성
models.Base.metadata.create_all(bind=engine)
insert_dummy_posts()

app = FastAPI()

app.include_router(posts.router) # router 불러오기
app.include_router(users.router) 
                   
# DB 세션 가져오기 / 실무 백엔드는 DB 세션을 항상 열고 닫아야함 -> 자동으로 해주는 코드
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST - 글 생성
@app.post("/posts", response_model=schemas.Post) # Method: Post, URL: /posts, 응답 타입: schemas.Post
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)): # 요청 Body 타입:schemas.PostCreate, db: DB 세션이 자동 주입
    # CRUD 로직
    db_post = models.Post(title=post.title, content=post.content) # DB 모델(Post 모델) 인스턴스 생성
    db.add(db_post) # INSERT 준비
    db.commit() # 실제 DB에 저장
    db.refresh(db_post) # 새로 생성된 id값 불러오기
    return db_post
    # POST는 글이 DB에 새롭게 생성되는 동작

# GET 전체
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.get("/posts", response_model=list[schemas.Post]) # DB에서 Post테이블 전체 데이터 SELECT, 리스트 형태로 반환
def read_posts(db: Session = Depends(get_db)): 
    return db.query(models.Post).all() # FastAPI가 자동으로 JSON으로 반환

# GET 단일
@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first() # 하나 가져오기
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# PUT 수정
@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post

# DELETE 삭제
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    return {"message": "Deleted"}
