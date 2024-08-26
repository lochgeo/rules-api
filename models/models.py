from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime

class RuleSet(Base):
    __tablename__ = "rulesets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    rules = relationship("Rule", back_populates="ruleset")

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    ruleset_id = Column(Integer, ForeignKey("rulesets.id"))

    ruleset = relationship("RuleSet", back_populates="rules")
    conditions = relationship("Condition", back_populates="rule")
    actions = relationship("Action", back_populates="rule")

class Condition(Base):
    __tablename__ = "conditions"

    id = Column(Integer, primary_key=True, index=True)
    field = Column(String)
    operator = Column(String)
    value = Column(String)
    rule_id = Column(Integer, ForeignKey("rules.id"))

    rule = relationship("Rule", back_populates="conditions")

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    parameters = Column(JSON)
    rule_id = Column(Integer, ForeignKey("rules.id"))

    rule = relationship("Rule", back_populates="actions")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    data = Column(JSON)