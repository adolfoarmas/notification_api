from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class UserCategoryBase(BaseModel):
    category_type: str
    category_id: int

class UserCategory(UserCategoryBase):
    user_id: int

    class Config:
        orm_mode = True
    
