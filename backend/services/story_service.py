from datetime import datetime
from sqlalchemy.orm import Session
import sys
import os

# Add the backend directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.story import Story, StoryMetrics
from typing import List, Optional

class StoryService:
    @staticmethod
    def create_story(db: Session,
                    title: str,
                    description: Optional[str],
                    url: str,
                    source: str,
                    interesting_score: float,
                    published_at: datetime) -> Story:
        """Create a new story in the database."""
        story = Story(
            title=title,
            description=description,
            url=url,
            source=source,
            interesting_score=interesting_score,
            published_at=published_at
        )
        db.add(story)
        db.commit()
        db.refresh(story)
        return story

    @staticmethod
    def get_stories(db: Session,
                   skip: int = 0,
                   limit: int = 10,
                   min_score: float = 0.0) -> List[Story]:
        """Get stories from the database with optional filtering."""
        return db.query(Story)\
                .filter(Story.interesting_score >= min_score)\
                .order_by(Story.published_at.desc())\
                .offset(skip)\
                .limit(limit)\
                .all()

    @staticmethod
    def get_story_by_url(db: Session, url: str) -> Optional[Story]:
        """Get a story by its URL to avoid duplicates."""
        return db.query(Story).filter(Story.url == url).first()

    @staticmethod
    def update_story_score(db: Session, story_id: int, new_score: float) -> Optional[Story]:
        """Update the interesting score of a story."""
        story = db.query(Story).filter(Story.id == story_id).first()
        if story:
            story.interesting_score = new_score
            db.commit()
            db.refresh(story)
        return story

    @staticmethod
    def create_story_metrics(db: Session, story_id: int) -> StoryMetrics:
        """Initialize metrics for a story."""
        metrics = StoryMetrics(story_id=story_id)
        db.add(metrics)
        db.commit()
        db.refresh(metrics)
        return metrics

    @staticmethod
    def update_story_metrics(db: Session,
                           story_id: int,
                           email_opens: Optional[int] = None,
                           link_clicks: Optional[int] = None,
                           time_spent: Optional[float] = None,
                           feedback_score: Optional[float] = None) -> Optional[StoryMetrics]:
        """Update metrics for a story."""
        metrics = db.query(StoryMetrics).filter(StoryMetrics.story_id == story_id).first()
        
        if metrics:
            if email_opens is not None:
                metrics.email_opens = email_opens
            if link_clicks is not None:
                metrics.link_clicks = link_clicks
            if time_spent is not None:
                metrics.time_spent = time_spent
            if feedback_score is not None:
                metrics.feedback_score = feedback_score
            
            db.commit()
            db.refresh(metrics)
            
        return metrics

    @staticmethod
    def calculate_interesting_score(story: Story) -> float:
        """Calculate story interest score based on multiple factors."""
        content_score = analyze_content_relevance(story.content)
        engagement_score = get_historical_engagement(story.source)
        freshness_score = calculate_freshness_score(story.published_at)
        source_credibility_score = get_source_credibility(story.source)
        podcast_engagement_score = get_podcast_engagement(story.id)  # New factor
        return weighted_average([content_score, engagement_score, freshness_score, source_credibility_score, podcast_engagement_score])

def get_podcast_engagement(story_id: int) -> float:
    """Fetch podcast engagement data for a story."""
    # Placeholder logic for fetching podcast engagement data
    # This should be replaced with actual logic to fetch data from the podcast analytics system
    return 0.8  # Example score

def weighted_average(scores: List[float]) -> float:
    """Calculate the weighted average of the given scores."""
    # Placeholder logic for weighted average calculation
    # This should be replaced with actual logic for weighted average
    return sum(scores) / len(scores)

def analyze_content_relevance(content: str) -> float:
    """Analyze the content relevance of a story."""
    # Placeholder logic for content relevance analysis
    return 0.7

def get_historical_engagement(source: str) -> float:
    """Get historical engagement for a source."""
    # Placeholder logic for historical engagement
    return 0.6

def calculate_freshness_score(published_at: datetime) -> float:
    """Calculate the freshness score of a story."""
    # Placeholder logic for freshness score calculation
    return 0.9

def get_source_credibility(source: str) -> float:
    """Get the credibility score of a source."""
    # Placeholder logic for source credibility
    return 0.85