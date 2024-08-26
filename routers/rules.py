from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import models
from schemas import schemas

router = APIRouter()

@router.post("/rules/", response_model=schemas.Rule)
def create_rule(rule: schemas.RuleCreate, ruleset_id: int, db: Session = Depends(get_db)):
    # First, check if the ruleset exists
    db_ruleset = db.query(models.RuleSet).filter(models.RuleSet.id == ruleset_id).first()
    if db_ruleset is None:
        raise HTTPException(status_code=404, detail="RuleSet not found")

    # Create the rule
    db_rule = models.Rule(name=rule.name, description=rule.description, is_active=rule.is_active, ruleset_id=ruleset_id)
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)

    # Add conditions
    for condition in rule.conditions:
        db_condition = models.Condition(**condition.dict(), rule_id=db_rule.id)
        db.add(db_condition)

    # Add actions
    for action in rule.actions:
        db_action = models.Action(**action.dict(), rule_id=db_rule.id)
        db.add(db_action)

    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.get("/rules/", response_model=List[schemas.Rule])
def read_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rules = db.query(models.Rule).offset(skip).limit(limit).all()
    return rules

@router.get("/rules/{rule_id}", response_model=schemas.Rule)
def read_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(models.Rule).filter(models.Rule.id == rule_id).first()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule

@router.put("/rules/{rule_id}", response_model=schemas.Rule)
def update_rule(rule_id: int, rule: schemas.RuleCreate, db: Session = Depends(get_db)):
    db_rule = db.query(models.Rule).filter(models.Rule.id == rule_id).first()
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")

    for key, value in rule.dict().items():
        setattr(db_rule, key, value)

    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.delete("/rules/{rule_id}", response_model=schemas.Rule)
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(models.Rule).filter(models.Rule.id == rule_id).first()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(rule)
    db.commit()
    return rule