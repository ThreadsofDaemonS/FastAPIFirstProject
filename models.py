from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

# Correctly define Base for async models
class Base(AsyncAttrs, DeclarativeBase):
    """Base class for async SQLAlchemy models."""
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    age: Mapped[int] = mapped_column(Integer)

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    body: Mapped[str] = mapped_column(String)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    # Define relationship with User
    author: Mapped[User] = relationship("User", lazy="joined")  # Use `joined` for eager loading
