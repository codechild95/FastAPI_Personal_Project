from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine
from pydantic import BaseModel

app = FastAPI()

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
    