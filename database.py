from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://root:Ghda74661!@localhost:3306/fastapi_db"
    ) #로컬 파일 DB

engine =  create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True
)

# DB 세션 형성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 모델의 기반이 되는 Base 클래스
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()