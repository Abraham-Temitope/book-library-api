from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from . import crud, models, schemas, database, auth

app = FastAPI()  # Create app instance
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