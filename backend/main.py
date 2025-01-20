from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from fastapi.responses import JSONResponse

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

class NewsItem(BaseModel):
    title: str
    description: str | None
    url: str
    source: str
    interesting_score: float

@app.get("/")
async def root():
    return {"message": "AI News Aggregator API", "status": "running"}

@app.get("/api/news", response_model=List[NewsItem])
async def get_news():
    try:
        # Initialize NewsAPI client
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            print("ERROR: NEWS_API_KEY not found in environment variables")
            return JSONResponse(
                status_code=500,
                content={"error": "NEWS_API_KEY not found in environment variables"}
            )
            
        print(f"Initializing NewsAPI client with key: {api_key[:4]}...")  # Only print first 4 chars for security
        newsapi = NewsApiClient(api_key=api_key)
        
        # Fetch AI-related news
        print("Fetching news from NewsAPI...")
        news = newsapi.get_everything(
            q='artificial intelligence OR machine learning',
            language='en',
            sort_by='relevancy',
            page_size=10
        )
        
        print(f"Received {len(news['articles'])} articles")
        
        # Transform and return news items
        articles = [
            NewsItem(
                title=article['title'],
                description=article['description'],
                url=article['url'],
                source=article['source']['name'],
                interesting_score=0.5  # Placeholder score
            )
            for article in news['articles']
        ]
        
        print(f"Returning {len(articles)} processed articles")
        return articles
        
    except Exception as e:
        print(f"ERROR in /api/news endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Error fetching news: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    print("Starting server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")