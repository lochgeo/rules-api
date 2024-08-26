from pydantic import BaseModel
from typing import List, Optional
import datetime

class ConditionBase(BaseModel):
    field: str
    operator: str
    value: str

class ConditionCreate(ConditionBase):
    pass

class Condition(ConditionBase):
    id: int
    rule_id: int

    class Config:
        orm_mode = True

class ActionBase(BaseModel):
    type: str
    parameters: dict

class ActionCreate(ActionBase):
    pass

class Action(ActionBase):
    id: int
    rule_id: int

    class Config:
        orm_mode = True

class RuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class RuleCreate(RuleBase):
    conditions: List[ConditionCreate]
    actions: List[ActionCreate]
    ruleset_id: int

class Rule(RuleBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    ruleset_id: int
    conditions: List[Condition]
    actions: List[Action]

    class Config:
        orm_mode = True

class RuleSetBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class RuleSetCreate(RuleSetBase):
    pass

class RuleSet(RuleSetBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    rules: List[Rule]

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    type: str
    data: dict

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True