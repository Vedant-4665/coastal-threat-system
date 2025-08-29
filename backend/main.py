from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from db.models import create_tables
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Coastal Threat Alert System",
    description="AI-powered coastal threat detection and alerting system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    print("🚀 Starting Coastal Threat Alert System...")
    create_tables()
    print("✅ Database tables created")
    print("✅ Services initialized")
    print("✅ Ready to receive requests")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down Coastal Threat Alert System...")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
