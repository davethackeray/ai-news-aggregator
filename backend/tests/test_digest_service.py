import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import shutil
from models.database import Base
from models.story import Story
from services.digest_service import DigestService
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

@pytest.fixture
def test_stories(db_session):
    """Create test stories in the database."""
    stories = []
    for i in range(3):
        story = StoryService.create_story(
            db=db_session,
            title=f"Test Story {i}",
            description=f"Description for story {i}",
            url=f"https://test{i}.com",
            source=f"Source {i}",
            interesting_score=0.8 + (i * 0.1),
            published_at=datetime.utcnow()
        )
        stories.append(story)
    return stories

@pytest.fixture
def test_digest_dir():
    """Create and clean up a test digest directory."""
    test_dir = "test_digests"
    os.makedirs(test_dir, exist_ok=True)
    yield test_dir
    shutil.rmtree(test_dir)

def test_generate_daily_digest(db_session, test_stories):
    """Test markdown digest generation."""
    markdown = DigestService.generate_daily_digest(db_session)
    
    # Check basic structure
    assert "# AI News Digest" in markdown
    assert "## Top Stories" in markdown
    assert "## About This Digest" in markdown
    
    # Check all stories are included
    for story in test_stories:
        assert story.title in markdown
        assert story.description in markdown
        assert story.source in markdown
        assert story.url in markdown
        assert f"{story.interesting_score:.2f}" in markdown

def test_save_daily_digest(test_digest_dir):
    """Test saving digest to file."""
    content = "# Test Digest\n\nTest content"
    filename = DigestService.save_daily_digest(content, test_digest_dir)
    
    # Check file exists
    assert os.path.exists(filename)
    
    # Check content was saved correctly
    with open(filename, 'r') as f:
        saved_content = f.read()
    assert saved_content == content

def test_digest_file_naming(test_digest_dir):
    """Test digest file naming convention."""
    content = "Test content"
    filename = DigestService.save_daily_digest(content, test_digest_dir)
    
    # Check filename format
    today = datetime.now().strftime("%Y-%m-%d")
    expected_filename = f"{test_digest_dir}/digest-{today}.md"
    assert filename == expected_filename

def test_markdown_formatting(db_session, test_stories):
    """Test specific markdown formatting elements."""
    markdown = DigestService.generate_daily_digest(db_session)
    
    # Check headers
    assert "###" in markdown  # Story titles
    assert "**Source:**" in markdown  # Bold text
    assert "[Read more]" in markdown  # Links
    assert "---" in markdown  # Separators
    
    # Check interest score formatting
    for story in test_stories:
        score_text = f"**Interest Score:** {story.interesting_score:.2f}"
        assert score_text in markdown

def test_empty_digest(db_session):
    """Test digest generation with no stories."""
    markdown = DigestService.generate_daily_digest(db_session, min_score=0.99)
    
    # Should still have basic structure
    assert "# AI News Digest" in markdown
    assert "## Top Stories" in markdown
    assert "## About This Digest" in markdown
    
    # But no story content
    assert "### 1." not in markdown

def test_digest_with_missing_description(db_session):
    """Test handling of stories with missing descriptions."""
    # Create a story without description
    StoryService.create_story(
        db=db_session,
        title="No Description Story",
        description=None,
        url="https://test.com",
        source="Test Source",
        interesting_score=0.9,
        published_at=datetime.utcnow()
    )
    
    markdown = DigestService.generate_daily_digest(db_session)
    
    # Should include the story but handle missing description
    assert "No Description Story" in markdown
    assert "No description available." in markdown