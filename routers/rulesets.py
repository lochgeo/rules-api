from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import models
from schemas import schemas

router = APIRouter()

@router.post("/rulesets/", response_model=schemas.RuleSet)
def create_ruleset(ruleset: schemas.RuleSetCreate, db: Session = Depends(get_db)):
    db_ruleset = models.RuleSet(**ruleset.dict())
    db.add(db_ruleset)
    db.commit()
    db.refresh(db_ruleset)
    return db_ruleset

@router.get("/rulesets/", response_model=List[schemas.RuleSet])
def read_rulesets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rulesets = db.query(models.RuleSet).offset(skip).limit(limit).all()
    return rulesets

@router.get("/rulesets/{ruleset_id}", response_model=schemas.RuleSet)
def read_ruleset(ruleset_id: int, db: Session = Depends(get_db)):
    ruleset = db.query(models.RuleSet).filter(models.RuleSet.id == ruleset_id).first()
    if ruleset is None:
        raise HTTPException(status_code=404, detail="RuleSet not found")
    return ruleset

@router.put("/rulesets/{ruleset_id}", response_model=schemas.RuleSet)
def update_ruleset(ruleset_id: int, ruleset: schemas.RuleSetCreate, db: Session = Depends(get_db)):
    db_ruleset = db.query(models.RuleSet).filter(models.RuleSet.id == ruleset_id).first()
    if db_ruleset is None:
        raise HTTPException(status_code=404, detail="RuleSet not found")

    for key, value in ruleset.dict().items():
        setattr(db_ruleset, key, value)

    db.commit()
    db.refresh(db_ruleset)
    return db_ruleset

@router.delete("/rulesets/{ruleset_id}", response_model=schemas.RuleSet)
def delete_ruleset(ruleset_id: int, db: Session = Depends(get_db)):
    ruleset = db.query(models.RuleSet).filter(models.RuleSet.id == ruleset_id).first()
    if ruleset is None:
        raise HTTPException(status_code=404, detail="RuleSet not found")
    db.delete(ruleset)
    db.commit()
    return ruleset