from pydantic import BaseModel

# POST (게시글)
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int

    class Config:
        orm_mode = True


# ----User----
class UserBase(BaseModel):
    username: str

# User Create (회원가입)
class UserCreate(UserBase):
    password: str

# User Response
class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# ----Login----
class LoginRequest(UserBase):
    password: str

