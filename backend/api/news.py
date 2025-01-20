from fastapi import APIRouter, Depends, Query
from models.news_item import NewsItem
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from models.database import get_db
from models.news_item import NewsItem
from services.story_service import StoryService

router = APIRouter()

@router.get("/news", response_model=List[NewsItem])
async def get_news(
    skip: int = Query(0, description="Number of stories to skip"),
    limit: int = Query(10, description="Number of stories to return"),
    min_score: float = Query(0.0, description="Minimum interesting score"),
    db: Session = Depends(get_db)
):
    try:
        # First try to get stories from database
        stories = StoryService.get_stories(db, skip=skip, limit=limit, min_score=min_score)
        
        # If we don't have enough stories, fetch more from the API
        if len(stories) < limit:
            # Initialize NewsAPI client
            api_key = os.getenv("NEWS_API_KEY")
            if not api_key:
                print("ERROR: NEWS_API_KEY not found in environment variables")
                return JSONResponse(
                    status_code=500,
                    content={"error": "NEWS_API_KEY not found in environment variables"}
                )
                
            print(f"Initializing NewsAPI client with key: {api_key[:4]}...")
            newsapi = NewsApiClient(api_key=api_key)
            
            # Fetch AI-related news
            print("Fetching news from NewsAPI...")
            news = newsapi.get_everything(
                q='artificial intelligence OR machine learning',
                language='en',
                sort_by='relevancy',
                page_size=limit
            )
            
            print(f"Received {len(news['articles'])} articles")
            
            # Store new articles in database
            for article in news['articles']:
                # Check if article already exists
                existing_story = StoryService.get_story_by_url(db, article['url'])
                if not existing_story:
                    # Calculate initial interesting score based on relevancy and freshness
                    hours_old = (datetime.utcnow() - datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')).total_seconds() / 3600
                    freshness_score = max(0, 1 - (hours_old / 72))  # Decay over 72 hours
                    initial_score = 0.7 + (freshness_score * 0.3)  # Base score 0.7 plus freshness bonus
                    
                    # Create new story
                    story = StoryService.create_story(
                        db=db,
                        title=article['title'],
                        description=article['description'],
                        url=article['url'],
                        source=article['source']['name'],
                        interesting_score=initial_score,
                        published_at=datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                    )
                    
                    # Initialize metrics
                    StoryService.create_story_metrics(db, story.id)
            
            # Get updated list of stories
            stories = StoryService.get_stories(db, skip=skip, limit=limit, min_score=min_score)
        
        print(f"Returning {len(stories)} processed articles")
        return [
            NewsItem(
                title=story.title,
                description=story.description,
                url=story.url,
                source=story.source,
                interesting_score=story.interesting_score,
                published_at=story.published_at,
                created_at=story.created_at
            ) for story in stories
        ]
        
    except Exception as e:
        print(f"ERROR in /api/news endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Error fetching news: {str(e)}"}
        )