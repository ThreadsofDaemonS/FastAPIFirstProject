from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, Post
from database import get_db, engine, Base
from schemas import PostCreate, UserCreate, PostResponse, User as DbUser
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import joinedload
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from decouple import config


app = FastAPI()

origins = config("CORS_ORIGINS", default="http://localhost:8080").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def init_db():
    """Асинхронная инициализация базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    """Событие запуска приложения"""
    await init_db()


@app.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)) -> PostResponse:
    # Проверяем, существует ли автор
    result = await db.execute(
        select(User).filter(User.id == post.author_id)
    )
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Создаём пост
    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)

    # Загружаем связанного автора перед возвратом
    await db.refresh(db_post, attribute_names=["author"])
    return db_post


@app.get("/posts/", response_model=list[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)) -> list[PostResponse]:
    result = await db.execute(select(Post).options(joinedload(Post.author)))
    posts = result.scalars().all()
    return posts


@app.get("/users/{name}", response_model=DbUser)
async def get_user(name: str, db: AsyncSession = Depends(get_db)) -> DbUser:
    result = await db.execute(
        select(User).filter(User.name == name)
    )
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
