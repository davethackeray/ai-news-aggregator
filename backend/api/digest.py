from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from services.digest_service import DigestService
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()

class DigestResponse(BaseModel):
    content: str
    generated_at: datetime
    story_count: int
    min_score: float

@router.get("/generate", response_model=DigestResponse)
async def generate_digest(
    min_score: float = 0.7,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Generate a markdown digest of top AI stories."""
    try:
        content = DigestService.generate_daily_digest(
            db=db,
            min_score=min_score,
            limit=limit
        )
        
        # Count actual stories in digest (by counting ### prefixes)
        story_count = content.count("### ")
        
        return DigestResponse(
            content=content,
            generated_at=datetime.utcnow(),
            story_count=story_count,
            min_score=min_score
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating digest: {str(e)}"
        )