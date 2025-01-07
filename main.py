from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from pydantic import BaseModel

app = FastAPI()




class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int



class User(BaseModel):
    id: int
    name: str
    age: int

class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User

users = [
    {"id": 1, "name": "John Doe", "age": 30},
    {"id": 2, "name": "Mike", "age": 25},
    {"id": 3, "name": "Alice", "age": 44}
]



posts = [
    {"id": 1, "title": "Foo", "body": "A very long description", "author": users[0]},
    {"id": 2, "title": "Foo", "body": "A very long description", "author": users[1]},
    {"id": 3, "title": "Foo", "body": "A very long description", "author": users[2]}
]



@app.get("/items")
async def get_items() -> list[Post]:
    return [Post(**post) for post in posts]

@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next((user for user in users if user['id'] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")

    new_post_id = len(posts) + 1
    new_post = {"id": new_post_id, "title": post.title, "body": post.body, "author": author}
    posts.append(new_post)

    return Post(**new_post)


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