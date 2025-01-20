from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    url = Column(String, index=True)
    source = Column(String, index=True)
    interesting_score = Column(Float, index=True)
    published_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    used_in_email = Column(Boolean, default=False)
    content = Column(String)  # Added content attribute

    metrics = relationship("StoryMetrics", back_populates="story")

class StoryMetrics(Base):
    __tablename__ = "story_metrics"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"))
    email_opens = Column(Integer, default=0)
    link_clicks = Column(Integer, default=0)
    time_spent = Column(Float, default=0.0)
    feedback_score = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow)

    story = relationship("Story", back_populates="metrics")