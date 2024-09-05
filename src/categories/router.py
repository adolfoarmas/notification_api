from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .schemas import CategoryCreate, Category as CategorySchema
from .crud import create_category as crud_create_category, read_categories as crud_read_categories, read_category as crud_read_category, delete_category as crud_delete_category
from src.database import get_db

router = APIRouter()

@router.post("/categories/", response_model=CategoryCreate)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return crud_create_category(category, db)

@router.get("/categories/", response_model=List[CategorySchema])
def read_categories(db: Session = Depends(get_db)):
    return crud_read_categories(db)

@router.get("/categories/{category_id}", response_model=CategorySchema)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud_read_category(category_id, db)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted_category = crud_delete_category(category_id, db)
    if deleted_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return None
