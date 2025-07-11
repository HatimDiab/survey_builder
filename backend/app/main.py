from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api.survey import router as survey_router
from .db.connection import engine
from .db.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Clean up resources if needed
    pass

app = FastAPI(
    title="Survey Builder API", 
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(survey_router)

@app.get("/")
async def root():
    return {"message": "Survey Builder API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
