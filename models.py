from sqlalchemy import Column, Integer, String
from database import Base

class Post(Base):
    __tablename__ = "posts" # 테이블 이름

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)