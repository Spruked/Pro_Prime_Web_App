from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SocialLinkBase(BaseModel):
    platform: str
    url: str
    icon: Optional[str] = None
    is_active: bool = True
    order: int = 0

class SocialLinkCreate(SocialLinkBase):
    pass

class SocialLinkUpdate(BaseModel):
    platform: Optional[str] = None
    url: Optional[str] = None
    icon: Optional[str] = None
    is_active: Optional[bool] = None
    order: Optional[int] = None

class SocialLinkInDB(SocialLinkBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True