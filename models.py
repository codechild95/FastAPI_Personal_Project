from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

    # User(1): Post(N)
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    # 테이블 이름은 "users"이므로 ForeignKey("users.id")
    user_id = Column(Integer, ForeignKey("users.id"))

    # Post -> User
    author = relationship("User", back_populates="posts")
