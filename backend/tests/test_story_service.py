import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
from models.story import Story, StoryMetrics
from services.story_service import StoryService

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
    """Test story creation through service."""
    story = StoryService.create_story(
        db=db_session,
        title="Test Story",
        description="Test Description",
        url="https://test.com",
        source="Test Source",
        interesting_score=0.8,
        published_at=datetime.utcnow()
    )
    
    assert story.title == "Test Story"
    assert story.interesting_score == 0.8
    assert story.source == "Test Source"

def test_get_stories_with_filtering(db_session):
    """Test story retrieval with filtering."""
    # Create test stories with different scores
    stories = [
        StoryService.create_story(
            db=db_session,
            title=f"Test Story {i}",
            description=f"Test Description {i}",
            url=f"https://test{i}.com",
            source="Test Source",
            interesting_score=score,
            published_at=datetime.utcnow()
        )
        for i, score in enumerate([0.3, 0.5, 0.7, 0.9])
    ]
    
    # Test filtering by min_score
    filtered_stories = StoryService.get_stories(db_session, min_score=0.6)
    assert len(filtered_stories) == 2
    assert all(s.interesting_score >= 0.6 for s in filtered_stories)

def test_get_story_by_url(db_session):
    """Test retrieving story by URL."""
    url = "https://test.com"
    StoryService.create_story(
        db=db_session,
        title="Test Story",
        description="Test Description",
        url=url,
        source="Test Source",
        interesting_score=0.8,
        published_at=datetime.utcnow()
    )
    
    story = StoryService.get_story_by_url(db_session, url)
    assert story is not None
    assert story.url == url

def test_update_story_score(db_session):
    """Test updating story's interesting score."""
    story = StoryService.create_story(
        db=db_session,
        title="Test Story",
        description="Test Description",
        url="https://test.com",
        source="Test Source",
        interesting_score=0.5,
        published_at=datetime.utcnow()
    )
    
    updated_story = StoryService.update_story_score(db_session, story.id, 0.9)
    assert updated_story.interesting_score == 0.9

def test_story_metrics_operations(db_session):
    """Test creating and updating story metrics."""
    # Create a story first
    story = StoryService.create_story(
        db=db_session,
        title="Test Story",
        description="Test Description",
        url="https://test.com",
        source="Test Source",
        interesting_score=0.8,
        published_at=datetime.utcnow()
    )
    
    # Create metrics
    metrics = StoryService.create_story_metrics(db_session, story.id)
    assert metrics.story_id == story.id
    assert metrics.email_opens == 0
    
    # Update metrics
    updated_metrics = StoryService.update_story_metrics(
        db_session,
        story_id=story.id,
        email_opens=10,
        link_clicks=5,
        time_spent=120.5,
        feedback_score=4.5
    )
    
    assert updated_metrics.email_opens == 10
    assert updated_metrics.link_clicks == 5
    assert updated_metrics.time_spent == 120.5
    assert updated_metrics.feedback_score == 4.5

def test_pagination(db_session):
    """Test story pagination."""
    # Create multiple stories
    for i in range(15):
        StoryService.create_story(
            db=db_session,
            title=f"Test Story {i}",
            description=f"Test Description {i}",
            url=f"https://test{i}.com",
            source="Test Source",
            interesting_score=0.8,
            published_at=datetime.utcnow()
        )
    
    # Test first page
    first_page = StoryService.get_stories(db_session, skip=0, limit=10)
    assert len(first_page) == 10
    
    # Test second page
    second_page = StoryService.get_stories(db_session, skip=10, limit=10)
    assert len(second_page) == 5
    
    # Ensure no overlap between pages
    first_page_urls = {story.url for story in first_page}
    second_page_urls = {story.url for story in second_page}
    assert not first_page_urls.intersection(second_page_urls)