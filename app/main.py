from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app import models, schemas, crud, database, auth

# Lifespan event for startup/shutdown (modern FastAPI way)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables if they don't exist (safe for RDS)
    print("Creating database tables if they don't exist...")
    database.Base.metadata.create_all(bind=database.engine)
    yield
    # Shutdown: You can add cleanup here if needed later
    print("Shutting down...")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Library API!"}

@app.get("/health")
def health_check():
    """Lightweight health check for ALB"""
    return {"status": "healthy"}

@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

# ==================== User Endpoints ====================
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(db=db, user=user)

@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ==================== Book Endpoints ====================
@app.post("/books/", response_model=schemas.Book)
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

# You can add more endpoints (GET books, etc.) here later