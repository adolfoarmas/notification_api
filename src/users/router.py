from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schemas import UserCreate, User as UserSchema
from .crud import create_user as crud_create_user, read_users as crud_read_users, read_user as crud_read_user, update_user as crud_update_user, delete_user as crud_delete_user
from src.database import get_db

router = APIRouter()

@router.post("/users/", response_model=UserSchema)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_create_user(user, db)

@router.get("/users/", response_model=List[UserSchema])
def read_users(db: Session = Depends(get_db)):
    return crud_read_users(db)

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_read_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated_user = crud_update_user(user_id, user, db)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = crud_delete_user(user_id, db)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
