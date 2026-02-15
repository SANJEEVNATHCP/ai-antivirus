from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from ..services.scanner import scanner_service
from ..services.proxy_service import proxy_service
from ..models.database import SessionLocal, Incident
from ..models import schemas
from typing import Any, Dict

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_incident(db: Session, text: str, direction: str, scan_result: Dict[str, Any], metadata: Dict[str, Any] = None):
    incident = Incident(
        direction=direction,
        input_text=text,
        risk_score=scan_result["risk_score"],
        risk_level=scan_result["risk_level"],
        detected_threats=scan_result["threats"],
        action_taken=scan_result["action"],
        extra_info=metadata
    )
    db.add(incident)
    db.commit()

@router.post("/v1/chat/completions")
async def openai_proxy(request: schemas.ChatCompletionRequest, db: Session = Depends(get_db)):
    # Combine messages for scanning
    full_text = " ".join([m.content for m in request.messages])
    
    # Scan
    scan_result = scanner_service.scan_text(full_text)
    
    # Log incident
    log_incident(db, full_text, "INBOUND", scan_result, {"model": request.model, "type": "openai"})

    if scan_result["action"] == "BLOCK":
        raise HTTPException(status_code=403, detail={
            "error": "Safety violation detected",
            "threats": scan_result["threats"],
            "risk_score": scan_result["risk_score"]
        })

    # Forward to OpenAI
    return await proxy_service.forward_to_openai("/chat/completions", "POST", request.dict())

@router.post("/api/generate")
async def ollama_generate_proxy(request: schemas.OllamaGenerateRequest, db: Session = Depends(get_db)):
    # Scan
    scan_result = scanner_service.scan_text(request.prompt)
    
    # Log incident
    log_incident(db, request.prompt, "INBOUND", scan_result, {"model": request.model, "type": "ollama_generate"})

    if scan_result["action"] == "BLOCK":
        raise HTTPException(status_code=403, detail={
            "error": "Safety violation detected",
            "threats": scan_result["threats"],
            "risk_score": scan_result["risk_score"]
        })

    # Forward to Ollama
    return await proxy_service.forward_to_ollama("/api/generate", "POST", request.dict())

@router.post("/api/chat")
async def ollama_chat_proxy(request: schemas.OllamaChatRequest, db: Session = Depends(get_db)):
    # Combine messages
    full_text = " ".join([m.content for m in request.messages])
    
    # Scan
    scan_result = scanner_service.scan_text(full_text)
    
    # Log incident
    log_incident(db, full_text, "INBOUND", scan_result, {"model": request.model, "type": "ollama_chat"})

    if scan_result["action"] == "BLOCK":
        raise HTTPException(status_code=403, detail={
            "error": "Safety violation detected",
            "threats": scan_result["threats"],
            "risk_score": scan_result["risk_score"]
        })

    # Forward to Ollama
    return await proxy_service.forward_to_ollama("/api/chat", "POST", request.dict())
