from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from difflib import SequenceMatcher
import re

from database import get_db
from models.chat_models import ChatScript, UnansweredQuestion, PageContext
from schemas.chat_schemas import (
    ChatQuery, ChatResponse, ScriptCreate, ScriptUpdate,
    UnansweredCreate, PageContextCreate
)
from core.dependencies import get_current_user

router = APIRouter(prefix="/api/chat", tags=["chat"])

def similarity(a: str, b: str) -> float:
    """Calculate string similarity for fuzzy matching"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

@router.post("/query", response_model=ChatResponse)
async def query_chat(
    query: ChatQuery,
    db: Session = Depends(get_db)
):
    """Main chat endpoint - finds best match or stores unanswered question"""

    # Get all scripts
    scripts = db.query(ChatScript).filter(
        ChatScript.requires_approval == False
    ).all()

    best_match = None
    best_score = 0.0
    threshold = 0.7

    # Fuzzy matching against all questions
    for script in scripts:
        score = similarity(query.question, script.question_pattern)
        if score > best_score:
            best_score = score
            best_match = script

    # If good match found
    if best_match and best_score >= threshold:
        best_match.usage_count += 1
        db.commit()

        return ChatResponse(
            answer=best_match.answer,
            confidence=best_score,
            source="database",
            script_id=best_match.id,
            suggestions=[]
        )

    # No good match - store as unanswered
    unanswered = UnansweredQuestion(
        question=query.question,
        user_session=query.session_id,
        page_url=query.page_url
    )
    db.add(unanswered)
    db.commit()

    # Return helpful fallback with suggestions
    suggestions = get_similar_questions(db, query.question, limit=3)

    return ChatResponse(
        answer="I'm not sure about that yet, but I'm learning! I've noted your question.",
        confidence=0.0,
        source="learning",
        suggestions=suggestions
    )

def get_similar_questions(db: Session, question: str, limit: int = 3):
    """Find similar questions for suggestions"""
    scripts = db.query(ChatScript).all()
    scored = [(s, similarity(question, s.question_pattern)) for s in scripts]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [{"question": s.question_pattern, "id": s.id} for s, _ in scored[:limit]]

@router.post("/scripts", response_model=dict)
async def create_script(
    script: ScriptCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Add new Q&A to the vault (admin only)"""

    # Check for duplicates
    existing = db.query(ChatScript).filter(
        ChatScript.question_pattern == script.question_pattern
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Question pattern already exists")

    new_script = ChatScript(
        question_pattern=script.question_pattern,
        answer=script.answer,
        category=script.category,
        page_context=script.page_context,
        is_learned=script.is_learned,
        requires_approval=script.requires_approval
    )
    db.add(new_script)
    db.commit()
    db.refresh(new_script)

    return {"id": new_script.id, "message": "Script added successfully"}

@router.get("/scripts", response_model=List[dict])
async def list_scripts(
    category: Optional[str] = None,
    is_learned: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all chat scripts with filters"""
    query = db.query(ChatScript)

    if category:
        query = query.filter(ChatScript.category == category)
    if is_learned is not None:
        query = query.filter(ChatScript.is_learned == is_learned)

    scripts = query.order_by(ChatScript.usage_count.desc()).all()

    return [{
        "id": s.id,
        "question": s.question_pattern,
        "answer": s.answer[:100] + "..." if len(s.answer) > 100 else s.answer,
        "category": s.category,
        "usage_count": s.usage_count,
        "is_learned": s.is_learned,
        "requires_approval": s.requires_approval,
        "confidence": s.confidence_score
    } for s in scripts]

@router.put("/scripts/{script_id}")
async def update_script(
    script_id: int,
    update: ScriptUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a script (admin only)"""
    script = db.query(ChatScript).filter(ChatScript.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")

    for field, value in update.dict(exclude_unset=True).items():
        setattr(script, field, value)

    db.commit()
    return {"message": "Script updated"}

@router.get("/unanswered", response_model=List[dict])
async def list_unanswered(
    resolved: Optional[bool] = False,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List unanswered questions for admin review"""
    questions = db.query(UnansweredQuestion).filter(
        UnansweredQuestion.is_resolved == resolved
    ).order_by(UnansweredQuestion.created_at.desc()).all()

    return [{
        "id": q.id,
        "question": q.question,
        "page_url": q.page_url,
        "suggested_answer": q.suggested_answer,
        "created_at": q.created_at.isoformat(),
        "admin_notes": q.admin_notes
    } for q in questions]

@router.post("/unanswered/{question_id}/resolve")
async def resolve_question(
    question_id: int,
    resolution: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Convert unanswered question to learned script"""
    question = db.query(UnansweredQuestion).filter(
        UnansweredQuestion.id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Create new script from resolution
    new_script = ChatScript(
        question_pattern=resolution.get("question_pattern", question.question),
        answer=resolution["answer"],
        category=resolution.get("category", "learned"),
        is_learned=True,
        requires_approval=False,
        page_context=question.page_url or "global"
    )
    db.add(new_script)

    # Mark as resolved
    question.is_resolved = True
    question.admin_notes = resolution.get("notes", "")

    db.commit()

    return {
        "message": "Question resolved and added to knowledge base",
        "script_id": new_script.id
    }

@router.post("/page-context")
async def set_page_context(
    context: PageContextCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Set context for a specific page"""
    existing = db.query(PageContext).filter(
        PageContext.page_route == context.page_route
    ).first()

    if existing:
        for field, value in context.dict().items():
            setattr(existing, field, value)
    else:
        new_context = PageContext(**context.dict())
        db.add(new_context)

    db.commit()
    return {"message": "Page context updated"}

@router.get("/page-context/{page_route}")
async def get_page_context(page_route: str, db: Session = Depends(get_db)):
    """Get context for a specific page"""
    context = db.query(PageContext).filter(
        PageContext.page_route == page_route
    ).first()

    if not context:
        return {"description": "", "key_topics": [], "design_notes": ""}

    return {
        "page_name": context.page_name,
        "description": context.description,
        "key_topics": context.key_topics,
        "design_notes": context.design_notes
    }

@router.get("/stats")
async def get_chat_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get learning statistics"""
    total_scripts = db.query(ChatScript).count()
    learned_scripts = db.query(ChatScript).filter(ChatScript.is_learned == True).count()
    unanswered = db.query(UnansweredQuestion).filter(
        UnansweredQuestion.is_resolved == False
    ).count()
    total_queries = db.query(ChatScript).with_entities(
        func.sum(ChatScript.usage_count)
    ).scalar() or 0

    return {
        "total_scripts": total_scripts,
        "learned_scripts": learned_scripts,
        "pending_questions": unanswered,
        "total_queries_answered": total_queries,
        "learning_rate": learned_scripts / total_scripts if total_scripts > 0 else 0
    }