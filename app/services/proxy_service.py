import httpx
from typing import Any, Dict, Optional
from ..core.config import settings

class ProxyService:
    async def forward_to_ollama(self, path: str, method: str, body: Dict[str, Any]) -> Any:
        url = f"{settings.OLLAMA_BASE_URL}{path}"
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                json=body,
                timeout=None # LLMs can take time
            )
            return response.json()

    async def forward_to_openai(self, path: str, method: str, body: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Any:
        url = f"{settings.OPENAI_BASE_URL}{path}"
        
        # Merge headers, ensuring we have the API key
        request_headers = headers.copy() if headers else {}
        if "Authorization" not in request_headers and settings.OPENAI_API_KEY:
            request_headers["Authorization"] = f"Bearer {settings.OPENAI_API_KEY}"
            
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                json=body,
                headers=request_headers,
                timeout=None
            )
            return response.json()

proxy_service = ProxyService()
