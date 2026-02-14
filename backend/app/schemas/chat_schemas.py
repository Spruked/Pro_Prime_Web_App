from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatQuery(BaseModel):
    question: str
    session_id: Optional[str] = None
    page_url: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    confidence: float
    source: str
    script_id: Optional[int] = None
    suggestions: List[dict] = []

class ScriptCreate(BaseModel):
    question_pattern: str
    answer: str
    category: str = "general"
    page_context: str = "global"
    is_learned: bool = False
    requires_approval: bool = False

class ScriptUpdate(BaseModel):
    question_pattern: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    confidence_score: Optional[float] = None
    requires_approval: Optional[bool] = None

class UnansweredCreate(BaseModel):
    question: str
    user_session: Optional[str] = None
    page_url: Optional[str] = None

class PageContextCreate(BaseModel):
    page_route: str
    page_name: Optional[str] = None
    description: Optional[str] = None
    key_topics: Optional[List[str]] = None
    design_notes: Optional[str] = None