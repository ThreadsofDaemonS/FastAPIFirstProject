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
    body: str
    author: User

posts = [
    {"id": 1, "title": "Foo", "body": "A very long description", "author": users[0]},
    {"id": 2, "title": "Foo", "body": "A very long description", "author": users[1]},
    {"id": 3, "title": "Foo", "body": "A very long description", "author": users[2]}
]



@app.get("/items")
async def get_items() -> list[Post]:
    return [Post(**post) for post in posts]

@app.get("/items/{item_id}")
async def get_item(item_id: int) -> Post:
    for post in posts:
        if post["id"] == item_id:
            return Post(**post)

    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/search")
async def search(post_id: int | None = None) -> Post | dict:
    if post_id:
        for post in posts:
            if post["id"] == post_id:
                return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"error": None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)