from sqlalchemy.orm import Session
import models
from database import SessionLocal

def insert_dummy_posts():
    db: Session = SessionLocal()

    if db.query(models.Post).count() == 0:  # 중복 방지
        sample_posts = [
            models.Post(title="첫 번째 글", content="내용입니다."),
            models.Post(title="FastAPI 연습", content="SQLAlchemy 테스트"),
            models.Post(title="더미 데이터", content="이건 테스트 글입니다.")
        ]
        for p in sample_posts:
            db.add(p)
        db.commit()
    db.close()
