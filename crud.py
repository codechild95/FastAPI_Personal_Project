from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext
from sqlalchemy import text

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


## POST 관련 crud
def get_posts(db: Session):
    return db.query(models.Post).all()

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def create_post(db: Session, post: schemas.PostCreate, user_id: int | None = None):
    db_post = models.Post(title=post.title, content=post.content, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

## User 관련 crud (중복함수 정리)
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_posts_by_users(db: Session, user_id: int):
    return db.query(models.Post).filter(models.Post.user_id == user_id).all()

# JOIN + dict 결과 반환 함수 추가
def get_posts_with_author_rows(db: Session):
    sql = text("""
               SELECT posts.id, posts.title, posts.content, users.username
               FROM posts
               JOIN users ON posts.user_id = users.id
               """)
    result = db.execute(sql)

    # Row 객체 -> dict로 변환
    return [dict(row._mapping for row in result.fetchall())]