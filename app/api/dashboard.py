from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..models.database import SessionLocal, Incident
from .proxy import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def get_dashboard(request: Request, db: Session = Depends(get_db)):
    incidents = db.query(Incident).order_by(Incident.timestamp.desc()).limit(100).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "incidents": incidents})

@router.get("/api/incidents")
async def get_incidents_api(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.timestamp.desc()).limit(100).all()
