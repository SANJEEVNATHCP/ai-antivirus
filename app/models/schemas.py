from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class IncidentBase(BaseModel):
    direction: str
    input_text: str
    risk_score: float
    risk_level: str
    detected_threats: List[str]
    action_taken: str
    extra_info: Optional[Dict[str, Any]] = None

class IncidentCreate(IncidentBase):
    pass

class Incident(IncidentBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# OpenAI Schemas (Simplified)
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: Optional[bool] = False

# Ollama Schemas (Simplified)
class OllamaGenerateRequest(BaseModel):
    model: str
    prompt: str
    stream: Optional[bool] = False

class OllamaChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: Optional[bool] = False
