from fastapi import FastAPI
from routers import rules, rulesets, events
from database import engine
from models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(rules.router)
app.include_router(rulesets.router)
app.include_router(events.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Fraud Rules Management API"}