from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()


from pydantic import BaseModel



class User(BaseModel):
    id: int
    name: str
    age: int

users = [
    {"id": 1, "name": "John Doe", "age": 30},
    {"id": 2, "name": "Cat", "age": 25},
    {"id": 3, "name": "Dog", "age": 54},
]


class Post(BaseModel):
    id: int
    title: str
    content: str
    author: User

posts = [
    Post(id=1, title="First Post", content="This is First Post", author=users[0] ),
    Post(id=2, title="Second Post", content="This is Second Post", author=users[1] ),
    Post(id=3, title="Third Post", content="This is Third Post", author=users[2] )
]



@app.get('/items')
async def read_items() -> list[Post]:
    return posts

@app.get("/items/{item_id}", response_model=Post)
async def read_item(item_id: int) -> Post:
    for post in posts:
        if post.id == item_id:
            return post

    raise HTTPException(status_code=404, detail="Post not found")

@app.get("/search")
async def search(post_id: int | None = None) -> Post | dict:
    if post_id:
        for post in posts:
            if post.id == post_id:
                return post
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"error": None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)