from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging

from web_scraper import WebScraper
from lead_scoring import LeadScoringEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Lead Generation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    sources: List[str]
    query: str
    location: Optional[str] = None

class Lead(BaseModel):
    firstName: str
    lastName: str
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    source: str
    qualityScore: float

class ScrapeResponse(BaseModel):
    leads: List[Lead]
    totalFound: int

@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape_leads(request: ScrapeRequest):
    try:
        scraper = WebScraper()
        scoring_engine = LeadScoringEngine()
        
        # Scrape leads
        raw_leads = await scraper.scrape_sources(
            sources=request.sources,
            query=request.query,
            location=request.location
        )
        
        # Score and filter leads
        scored_leads = []
        for lead in raw_leads:
            score = scoring_engine.analyze_lead(lead)
            if score.qualityScore >= 0.4:  # Only include leads with decent quality
                scored_leads.append(Lead(
                    firstName=lead.firstName,
                    lastName=lead.lastName,
                    email=lead.email,
                    phone=lead.phone,
                    location=lead.location,
                    source=lead.source,
                    qualityScore=score.qualityScore
                ))
        
        return ScrapeResponse(
            leads=scored_leads,
            totalFound=len(scored_leads)
        )
        
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export/csv")
async def export_to_csv(leads: List[Lead]):
    try:
        import pandas as pd
        import os
        from datetime import datetime
        
        # Convert leads to DataFrame
        df = pd.DataFrame([lead.dict() for lead in leads])
        
        # Create exports directory if it doesn't exist
        os.makedirs("exports", exist_ok=True)
        
        # Generate filename with timestamp
        filename = f"exports/leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Export to CSV
        df.to_csv(filename, index=False)
        
        return {"message": "Leads exported successfully", "filename": filename}
        
    except Exception as e:
        logger.error(f"Error during export: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
