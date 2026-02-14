from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models.database import get_db
from ..models.page import Page
from ..schemas.page import PageCreate, PageUpdate, PageInDB
from ..core.dependencies import get_current_user

router = APIRouter()

@router.get("/{page_name}", response_model=PageInDB)
async def get_page(page_name: str, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.name == page_name, Page.is_published == True).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.put("/{page_id}", response_model=PageInDB)
async def update_page(
    page_id: int,
    page_update: PageUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    update_data = page_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_page, field, value)
    
    db.commit()
    db.refresh(db_page)
    return db_page