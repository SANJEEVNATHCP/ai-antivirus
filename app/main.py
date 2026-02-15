from fastapi import FastAPI
from .api import proxy, dashboard
from .models.database import init_db
from .core.config import settings

app = FastAPI(title="AI Safety Agent")

# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Include routers
app.include_router(proxy.router, tags=["proxy"])
app.include_router(dashboard.router, tags=["dashboard"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.APP_ENV}
