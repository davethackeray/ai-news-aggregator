from datetime import datetime
from sqlalchemy.orm import Session
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
        return weighted_average([content_score, engagement_score, freshness_score, source_credibility_score])