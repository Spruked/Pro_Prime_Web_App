from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import json

class SystemBase(BaseModel):
    name: str
    title: str
    description: str
    key_features: List[str] = Field(default_factory=list)
    learn_more_url: str = "#"
    icon: Optional[str] = None
    order: int = 0
    is_active: bool = True

class SystemCreate(SystemBase):
    slug: str

class SystemUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    key_features: Optional[List[str]] = None
    learn_more_url: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None

class SystemInDB(SystemBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
    @property
    def key_features_list(self) -> List[str]:
        if isinstance(self.key_features, str):
            return json.loads(self.key_features)
        return self.key_features or []