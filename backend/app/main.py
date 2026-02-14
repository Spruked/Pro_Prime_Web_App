from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api import auth, systems, social, pages, chat
from .models.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(systems.router, prefix="/api/systems", tags=["systems"])
app.include_router(social.router, prefix="/api/social", tags=["social"])
app.include_router(pages.router, prefix="/api/pages", tags=["pages"])
app.include_router(chat.router, tags=["chat"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Pro Prime Series Systems API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}