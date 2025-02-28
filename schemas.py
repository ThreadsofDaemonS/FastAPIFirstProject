from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str
    age: int

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass


class PostBase(BaseModel):
    title: str
    body: str
    author_id: int

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author: User


    class Config:
        from_attributes = True

