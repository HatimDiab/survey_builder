from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Survey Builder API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Survey Builder API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/save-progress")
async def save_progress(data: dict):
    # TODO: Implement save logic
    return {"status": "success", "message": "Progress saved"}

@app.post("/api/export")
async def export_survey(data: dict):
    # TODO: Implement export logic
    return {"status": "success", "message": "Survey exported successfully"}
