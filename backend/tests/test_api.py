import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from main import app
from models.database import Base, get_db
from services.story_service import StoryService

# Test database URL
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ainews_test"

# Create test engine
engine = create_engine(TEST_DATABASE_URL)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Test database dependency override."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def test_db():
    """Create test database tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client(test_db):
    """Create test client with clean database."""
    return TestClient(app)

@pytest.fixture
def db_session(test_db):
    """Create database session for test data setup."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_read_root(test_client):
    """Test root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI News Aggregator API", "status": "running"}

def test_get_news_empty_db(test_client):
    """Test getting news with empty database."""
    response = test_client.get("/api/news")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_get_news_with_data(test_client, db_session):
    """Test getting news with existing stories."""
    # Create test stories
    for i in range(5):
        StoryService.create_story(
            db=db_session,
            title=f"Test Story {i}",
            description=f"Description {i}",
            url=f"https://test{i}.com",
            source="Test Source",
            interesting_score=0.5 + (i * 0.1),
            published_at=datetime.utcnow() - timedelta(hours=i)
        )
    
    # Test default pagination
    response = test_client.get("/api/news")
    assert response.status_code == 200
    assert len(response.json()) == 5
    
    # Test pagination parameters
    response = test_client.get("/api/news?skip=2&limit=2")
    assert response.status_code == 200
    stories = response.json()
    assert len(stories) == 2
    
    # Test minimum score filter
    response = test_client.get("/api/news?min_score=0.7")
    assert response.status_code == 200
    stories = response.json()
    assert len(stories) == 3  # Stories with scores 0.7, 0.8, 0.9

def test_get_news_validation(test_client):
    """Test input validation for news endpoint."""
    # Test invalid skip parameter
    response = test_client.get("/api/news?skip=-1")
    assert response.status_code == 422
    
    # Test invalid limit parameter
    response = test_client.get("/api/news?limit=0")
    assert response.status_code == 422
    
    # Test invalid score parameter
    response = test_client.get("/api/news?min_score=-0.1")
    assert response.status_code == 422

def test_news_response_structure(test_client, db_session):
    """Test the structure of returned news items."""
    # Create a test story
    story = StoryService.create_story(
        db=db_session,
        title="Test Story",
        description="Test Description",
        url="https://test.com",
        source="Test Source",
        interesting_score=0.8,
        published_at=datetime.utcnow()
    )
    
    response = test_client.get("/api/news")
    assert response.status_code == 200
    stories = response.json()
    assert len(stories) == 1
    
    story_data = stories[0]
    assert "title" in story_data
    assert "description" in story_data
    assert "url" in story_data
    assert "source" in story_data
    assert "interesting_score" in story_data
    assert "published_at" in story_data
    
    assert story_data["title"] == "Test Story"
    assert story_data["interesting_score"] == 0.8

def test_error_handling(test_client, monkeypatch):
    """Test API error handling."""
    # Simulate database error
    def mock_get_stories(*args, **kwargs):
        raise Exception("Database error")
    
    monkeypatch.setattr(StoryService, "get_stories", mock_get_stories)
    
    response = test_client.get("/api/news")
    assert response.status_code == 500
    assert "error" in response.json()