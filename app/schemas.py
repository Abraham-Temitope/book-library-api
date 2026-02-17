from pydantic import BaseModel

class UserCreate(BaseModel):  # Input for creating user
    username: str
    password: str

class User(BaseModel):  # Output user (no password)
    id: int
    username: str

    class Config:  # Allows ORM mode
        from_attributes = True

class BookCreate(BaseModel):  # Input for book
    title: str
    author: str

class Book(BaseModel):  # Output book
    id: int
    title: str
    author: str
    owner_id: int

    class Config:
        from_attributes = True