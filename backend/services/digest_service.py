from datetime import datetime, timedelta
from typing import List
import os
from sqlalchemy.orm import Session
from models.story import Story
from .story_service import StoryService

class DigestService:
    @staticmethod
    def generate_daily_digest(db: Session, min_score: float = 0.7, limit: int = 10) -> str:
        """Generate a markdown digest of top stories."""
        stories = StoryService.get_stories(
            db=db,
            min_score=min_score,
            limit=limit,
            skip=0
        )
        
        return DigestService._create_markdown(stories)
    
    @staticmethod
    def save_daily_digest(content: str, directory: str = "digests") -> str:
        """Save digest to a markdown file."""
        # Create digests directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Generate filename with date
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{directory}/digest-{today}.md"
        
        # Write content to file
        with open(filename, "w") as f:
            f.write(content)
        
        return filename
    
    @staticmethod
    def _create_markdown(stories: List[Story]) -> str:
        """Convert stories to markdown format."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Start with header
        lines = [
            f"# AI News Digest - {today}",
            "",
            "Today's top stories about artificial intelligence and machine learning.",
            "",
            "## Top Stories",
            ""
        ]
        
        # Add each story
        for idx, story in enumerate(stories, 1):
            # Format published date
            pub_date = story.published_at.strftime("%Y-%m-%d %H:%M")
            
            # Add story details
            lines.extend([
                f"### {idx}. {story.title}",
                "",
                f"**Source:** {story.source}  ",
                f"**Published:** {pub_date}  ",
                f"**Interest Score:** {story.interesting_score:.2f}",
                "",
                f"{story.description or 'No description available.'}" if story.description else "",
                "",
                f"[Read more]({story.url})",
                "",
                "---",
                ""
            ])
        
        # Add footer
        lines.extend([
            "## About This Digest",
            "",
            "This digest is automatically generated based on story relevance and interest scores. ",
            "Stories are selected based on their potential impact on business AI integration decisions.",
            "",
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ])
        
        return "\n".join(lines)