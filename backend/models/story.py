from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    interesting_score = Column(Float, nullable=False)
    published_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    used_in_email = Column(Boolean, default=False)

    # Relationship with metrics
    metrics = relationship("StoryMetrics", back_populates="story", uselist=False)

class StoryMetrics(Base):
    __tablename__ = "story_metrics"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"))
    email_opens = Column(Integer, default=0)
    link_clicks = Column(Integer, default=0)
    time_spent = Column(Float)
    feedback_score = Column(Float)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship with story
    story = relationship("Story", back_populates="metrics")