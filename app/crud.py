from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Hashing context

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()  # Query by ID

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)  # Hash password
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)  # Add to session
    db.commit()  # Commit transaction
    db.refresh(db_user)  # Refresh with DB values
    return db_user