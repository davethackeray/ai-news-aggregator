#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from models.database import get_db, engine
from services.digest_service import DigestService

def generate_daily_digest(db: Session):
    """Generate and save the daily digest."""
    print(f"Generating digest for {datetime.now().strftime('%Y-%m-%d')}...")
    
    try:
        # Generate digest content
        content = DigestService.generate_daily_digest(
            db=db,
            min_score=0.7,  # Only include high-scoring stories
            limit=10        # Top 10 stories
        )
        
        # Save to file
        digest_dir = os.path.join(os.path.dirname(__file__), "..", "digests")
        filename = DigestService.save_daily_digest(content, digest_dir)
        
        print(f"Successfully generated digest: {filename}")
        
        # Preview the first few lines
        print("\nPreview:")
        with open(filename, 'r') as f:
            preview = "\n".join(f.readlines()[:10])
            print(preview)
            
    except Exception as e:
        print(f"Error generating digest: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Get database session
    db = next(get_db())
    try:
        generate_daily_digest(db)
    finally:
        db.close()