"""API Main - FastAPI app initialization"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router

# Create FastAPI app
app = FastAPI(
    title="OncoReconcile AI",
    description="Human-Governed AI Agent System for Precision Oncology Semantic Interoperability",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "OncoReconcile AI",
        "version": "0.1.0",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "reconcile": "/reconcile (POST)",
            "review_queue": "/review-queue (GET)",
            "docs": "/docs",
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
