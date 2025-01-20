from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from api import news
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from models.database import get_db
from models.story import Story as DBStory
from services.story_service import StoryService
from api import digest

# Load environment variables first thing
load_dotenv()
print("Environment loaded. NEWS_API_KEY present:", bool(os.getenv("NEWS_API_KEY")))

app = FastAPI(title="AI News Aggregator")

# Enable CORS for development
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(digest.router, prefix="/api/digest", tags=["digest"])
app.include_router(news.router, prefix="/api", tags=["news"])


@app.get("/")
async def root():
    return {"message": "AI News Aggregator API", "status": "running"}


if __name__ == "__main__":
    import uvicorn
    print("Starting server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")