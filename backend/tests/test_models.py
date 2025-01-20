import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
from models.story import Story, StoryMetrics

# Test database URL
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ainews_test"

@pytest.fixture
def db_session():
    """Create a clean database session for testing."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

def test_create_story(db_session):
    """Test story creation and retrieval."""
    story = Story(
        title="Test Story",
        description="Test Description",
        url="https://test.com",
        source="Test Source",
        interesting_score=0.8,
        published_at=datetime.utcnow()
    )
    
    db_session.add(story)
    db_session.commit()
    
    stored_story = db_session.query(Story).first()
    assert stored_story.title == "Test Story"
    assert stored_story.interesting_score == 0.8

def test_story_metrics_relationship(db_session):
    """Test relationship between Story and StoryMetrics."""
    story = Story(
        title="Test Story",
        description="Test Description",
        url="https://test.com",
        source="Test Source",
        interesting_score=0.8,
        published_at=datetime.utcnow()
    )
    db_session.add(story)
    db_session.commit()
    
    metrics = StoryMetrics(
        story_id=story.id,
        email_opens=10,
        link_clicks=5,
        time_spent=120.5,
        feedback_score=4.5
    )
    db_session.add(metrics)
    db_session.commit()
    
    # Test relationship from Story to StoryMetrics
    assert story.metrics.email_opens == 10
    assert story.metrics.link_clicks == 5
    
    # Test relationship from StoryMetrics to Story
    assert metrics.story.title == "Test Story"