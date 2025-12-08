from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine
from routers import posts # router 불러옴
from pydantic import BaseModel
from dummy_data import insert_dummy_posts

# Post 모델(models.Post)이 실제 DB(test.db) 안에 posts 테이블로 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router) # router 불러오기

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


@app.get("/posts", response_model=list[schemas.Post]) # DB에서 Post테이블 전체 데이터 SELECT, 리스트 형태로 반환
def read_posts(db: Session = Depends(get_db)): 
    return db.query(models.Post).all() # FastAPI가 자동으로 JSON으로 반환

# post = db.query(model.Post).filter(models.Post.id == post_id).first()

class Post(BaseModel):
    title: str
    content: str

posts =[]
post_id_seq = 1

@app.post("/posts")
def create_post(post: Post):
    global post_id_seq
    new_post = {
        "id": post_id_seq,
        "title": post.title,
        "content": post.content
    }
    posts.append(new_post)
    post_id_seq += 1
    return new_post

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    for p in posts:
        if p["id"] == post_id:
            return p
    raise HTTPException(status_code=404, detail="Post not found")

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    for p in posts:
        if p["id"] == post_id:
            p["title"] = post.title
            p["content"] = post.content
            return p
    raise HTTPException(status_code=404, detail="Post not found")
    
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    for p in posts:
        if p["id"] == post_id:
            posts.remove(p)
            return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Post not found")
    