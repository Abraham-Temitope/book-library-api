from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session
from app import models, schemas, crud, database, auth
app = FastAPI()  # Create app instance
@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Library API!"}

@app.get("/users/me", response_model=schemas.User)  # Get current user endpoint
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

models.Base.metadata.create_all(bind=database.engine)  # Create tables

@app.post("/users/", response_model=schemas.User)  # Create user endpoint
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username taken")
    return crud.create_user(db=db, user=user)

@app.post("/token")  # Login for token
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
    ):
    user = crud.authenticate_user(db, form_data.username, form_data.password)  # Add this func to crud
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
@app.post("/books/", response_model=schemas.Book)  # Create book endpoint
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    db_book = models.Book(**book.dict(), owner_id=current_user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book