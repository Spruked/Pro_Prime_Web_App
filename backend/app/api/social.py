from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models.database import get_db
from ..models.social import SocialLink
from ..schemas.social import SocialLinkCreate, SocialLinkUpdate, SocialLinkInDB
from ..core.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[SocialLinkInDB])
async def get_social_links(db: Session = Depends(get_db)):
    links = db.query(SocialLink).filter(SocialLink.is_active == True).order_by(SocialLink.order).all()
    return links

@router.post("/", response_model=SocialLinkInDB, status_code=status.HTTP_201_CREATED)
async def create_social_link(
    link: SocialLinkCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_link = SocialLink(**link.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

@router.put("/{link_id}", response_model=SocialLinkInDB)
async def update_social_link(
    link_id: int,
    link_update: SocialLinkUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_link = db.query(SocialLink).filter(SocialLink.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Social link not found")
    
    update_data = link_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_link, field, value)
    
    db.commit()
    db.refresh(db_link)
    return db_link

@router.delete("/{link_id}")
async def delete_social_link(
    link_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_link = db.query(SocialLink).filter(SocialLink.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Social link not found")
    
    db.delete(db_link)
    db.commit()
    return {"message": "Social link deleted successfully"}