from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello, World!"}

@app.get("/contacts")
async def get_contacts() -> list[dict[str, str]]:
    contacts = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]
    return contacts

@app.get('/items')
async def read_items() -> list[dict]:
    return posts


from pydantic import BaseModel

class Post(BaseModel):
    id: int
    title: str
    content: str

posts = [
    Post(id=1, title="First Post", content="This is First Post"),
    Post(id=2, title="Second Post", content="This is Second Post"),
    Post(id=3, title="Third Post", content="This is Third Post")
]

@app.get("/items/{item_id}", response_model=Post)
async def read_item(item_id: int):
    for post in posts:
        if post.id == item_id:
            return post

    raise HTTPException(status_code=404, detail="Post not found")

@app.get("/search")
async def search(post_id: int | None = None):
    if post_id:
        for post in posts:
            if post.id == post_id:
                return post
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"error": "No post_id provided"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)