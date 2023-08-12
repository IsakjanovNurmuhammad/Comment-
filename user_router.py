from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from db import get_db
from models import User
from schemas import UserSchema, UserCreate

router = APIRouter()

@router.post("/users/", response_model=UserSchema)
async def create_user(user: UserCreate,db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@router.get("/users/", response_model=list[UserSchema])
async def get_users(db=Depends(get_db)):
    users = db.query(User).all()
    return users



@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

