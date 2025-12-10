from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # User(1): Post(N)
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    # 테이블 이름은 "users"이므로 ForeignKey("user.id")
    user_id = Column(Integer, ForeignKey("users.id"))

    # Post -> User
    author = relationship("User", back_populates="posts")
