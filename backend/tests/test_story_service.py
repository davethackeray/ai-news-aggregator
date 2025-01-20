import unittest
from unittest.mock import patch
from datetime import datetime
import sys
import os

# Add the backend directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.services.story_service import StoryService
from backend.models.story import Story

class TestStoryService(unittest.TestCase):
    def setUp(self):
        self.story = Story(
            id=1,
            title="Test Story",
            description="This is a test story",
            url="http://example.com/test-story",
            source="Example Source",
            interesting_score=0.0,
            published_at=datetime.now()
        )

    @patch('backend.services.story_service.get_podcast_engagement', return_value=0.8)
    @patch('backend.services.story_service.analyze_content_relevance', return_value=0.7)
    @patch('backend.services.story_service.get_historical_engagement', return_value=0.6)
    @patch('backend.services.story_service.calculate_freshness_score', return_value=0.9)
    @patch('backend.services.story_service.get_source_credibility', return_value=0.85)
    @patch('backend.services.story_service.weighted_average', return_value=0.8)
    def test_calculate_interesting_score(self, mock_weighted_average, mock_source_credibility, mock_freshness_score, mock_historical_engagement, mock_content_relevance, mock_podcast_engagement):
        score = StoryService.calculate_interesting_score(self.story)
        self.assertEqual(score, 0.8)
        mock_podcast_engagement.assert_called_once_with(self.story.id)
        mock_content_relevance.assert_called_once_with(self.story.content)
        mock_historical_engagement.assert_called_once_with(self.story.source)
        mock_freshness_score.assert_called_once_with(self.story.published_at)
        mock_source_credibility.assert_called_once_with(self.story.source)
        mock_weighted_average.assert_called_once_with([0.7, 0.6, 0.9, 0.85, 0.8])

if __name__ == '__main__':
    unittest.main()