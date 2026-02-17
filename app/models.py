from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):  # User table
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    books = relationship("Book", back_populates="owner")  # One-to-many with books

class Book(Base):  # Book table
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to user
    owner = relationship("User", back_populates="books")  # Relationship