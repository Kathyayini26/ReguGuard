from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import audit_router, memory_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "ReguGuard is an AI-powered compliance agent that learns from historical audit findings, "
        "remediation outcomes, and auditor feedback using Vectorize Hindsight long-term memory."
    ),
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(audit_router)
app.include_router(memory_router)

@app.get("/", tags=["Health"])
async def root():
    """Service health and identity endpoint."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "memory_layer": "Vectorize Hindsight",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed healthcheck endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "hindsight_bank": settings.HINDSIGHT_BANK_ID
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
