from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from pydantic import BaseModel
import uvicorn
from typing import Annotated
from sqlalchemy.orm import Session

from models import User, Post, Base
from database import session_local, engine
from schemas import PostCreate, UserCreate, PostResponse, User as DbUser

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

@app.get("/posts/", response_model=list[PostResponse])
async def get_posts(db: Session = Depends(get_db)) -> list[PostResponse]:
    return db.query(Post).all()


# @app.get("/items")
# async def get_items() -> list[Post]:
#     return [Post(**post) for post in posts]
#
# @app.post("/items/add")
# async def add_item(post: PostCreate) -> Post:
#     author = next((user for user in users if user['id'] == post.author_id), None)
#     if not author:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     new_post_id = len(posts) + 1
#     new_post = {"id": new_post_id, "title": post.title, "body": post.body, "author": author}
#     posts.append(new_post)
#
#     return Post(**new_post)
#
# @app.post("/user/add")
# async def add_user(user: Annotated[UserCreate, Body(..., example={
#     "name": "John Doe",
#     "age": 30
# })]) -> User:
#     new_user_id = len(users) + 1
#     new_user = {"id": new_user_id, "name": user.name, "age": user.age}
#     users.append(new_user)
#
#     return User(**new_user)
#
#
# @app.get("/items/{item_id}")
# async def get_item(item_id: Annotated[int, Path(..., title='The post ID is specified here', ge=1, lt=100)]) -> Post:
#     for post in posts:
#         if post["id"] == item_id:
#             return Post(**post)
#
#     raise HTTPException(status_code=404, detail="Item not found")
#
# @app.get("/search")
# async def search(post_id: Annotated[
#     int | None, Query(title="ID of post to search", ge=1, lt=100)
# ]) -> Post | dict:
#     if post_id:
#         for post in posts:
#             if post["id"] == post_id:
#                 return {"data": Post(**post)}
#         raise HTTPException(status_code=404, detail="Post not found")
#     else:
#         return {"error": None}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)