from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PageBase(BaseModel):
    name: str
    title: str
    content: str
    meta_description: Optional[str] = None
    is_published: bool = True

class PageCreate(PageBase):
    pass

class PageUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    meta_description: Optional[str] = None
    is_published: Optional[bool] = None

class PageInDB(PageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True