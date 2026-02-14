from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.sql import func
from .database import Base

class ChatScript(Base):
    __tablename__ = "chat_scripts"

    id = Column(Integer, primary_key=True, index=True)
    question_pattern = Column(String(500), nullable=False, index=True)
    answer = Column(Text, nullable=False)
    category = Column(String(100), default="general")
    confidence_score = Column(Float, default=1.0)
    usage_count = Column(Integer, default=0)
    is_learned = Column(Boolean, default=False)
    requires_approval = Column(Boolean, default=False)
    page_context = Column(String(200), default="global")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UnansweredQuestion(Base):
    __tablename__ = "unanswered_questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    user_session = Column(String(100))
    page_url = Column(String(500))
    suggested_answer = Column(Text)
    is_resolved = Column(Boolean, default=False)
    admin_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PageContext(Base):
    __tablename__ = "page_contexts"

    id = Column(Integer, primary_key=True, index=True)
    page_route = Column(String(200), unique=True, index=True)
    page_name = Column(String(200))
    description = Column(Text)
    key_topics = Column(JSON, default=list)
    design_notes = Column(Text)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())