from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from ..models.database import get_db
from ..models.system import System
from ..schemas.system import SystemCreate, SystemUpdate, SystemInDB
from ..core.dependencies import get_current_user

router = APIRouter()

# Public endpoints
@router.get("/", response_model=List[SystemInDB])
async def get_systems(db: Session = Depends(get_db)):
    systems = db.query(System).filter(System.is_active == True).order_by(System.order).all()
    return systems

@router.get("/{slug}", response_model=SystemInDB)
async def get_system(slug: str, db: Session = Depends(get_db)):
    system = db.query(System).filter(System.slug == slug, System.is_active == True).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return system

# Admin endpoints
@router.post("/", response_model=SystemInDB, status_code=status.HTTP_201_CREATED)
async def create_system(
    system: SystemCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_system = System(
        name=system.name,
        slug=system.slug,
        title=system.title,
        description=system.description,
        key_features=json.dumps(system.key_features),
        learn_more_url=system.learn_more_url,
        icon=system.icon,
        order=system.order,
        is_active=system.is_active
    )
    db.add(db_system)
    db.commit()
    db.refresh(db_system)
    return db_system

@router.put("/{system_id}", response_model=SystemInDB)
async def update_system(
    system_id: int,
    system_update: SystemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_system = db.query(System).filter(System.id == system_id).first()
    if not db_system:
        raise HTTPException(status_code=404, detail="System not found")
    
    update_data = system_update.dict(exclude_unset=True)
    if "key_features" in update_data and update_data["key_features"] is not None:
        update_data["key_features"] = json.dumps(update_data["key_features"])
    
    for field, value in update_data.items():
        setattr(db_system, field, value)
    
    db.commit()
    db.refresh(db_system)
    return db_system

@router.delete("/{system_id}")
async def delete_system(
    system_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_system = db.query(System).filter(System.id == system_id).first()
    if not db_system:
        raise HTTPException(status_code=404, detail="System not found")
    
    db.delete(db_system)
    db.commit()
    return {"message": "System deleted successfully"}