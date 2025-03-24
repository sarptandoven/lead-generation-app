from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime
from openai import OpenAI
from app.core.config import settings

from app.services.web_scraper import WebScraperService
from app.services.lead_scoring import LeadScoringService, LeadScore

logger = logging.getLogger(__name__)

class LeadGenerationService:
    def __init__(self):
        self.web_scraper = WebScraperService()
        self.lead_scorer = LeadScoringService()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_leads(self, 
                           location: str,
                           properties_range: str,
                           max_leads: int = 25,
                           min_score: float = 0.7) -> List[Dict]:
        """
        Generate and score leads based on location and property range criteria.
        
        Args:
            location: Target location for lead search
            properties_range: Range of properties ("1-7", "8-15", "15-24", "25+")
            max_leads: Maximum number of leads to return
            min_score: Minimum score threshold for leads (0.0 to 1.0)
            
        Returns:
            List of scored leads sorted by score
        """
        try:
            # Find potential leads through web scraping
            raw_leads = await self.web_scraper.find_property_managers(
                location=location,
                properties_range=properties_range,
                max_leads=max_leads
            )
            
            logger.info(f"Found {len(raw_leads)} potential leads")
            
            # Score leads in parallel
            scored_leads = await self._score_leads_parallel(raw_leads)
            
            # Filter by minimum score and sort by score
            qualified_leads = [
                lead for lead in scored_leads 
                if lead['score'].total_score >= min_score
            ]
            qualified_leads.sort(key=lambda x: x['score'].total_score, reverse=True)
            
            logger.info(f"Found {len(qualified_leads)} qualified leads")
            
            return qualified_leads[:max_leads]
            
        except Exception as e:
            logger.error(f"Error generating leads: {str(e)}")
            raise
        finally:
            # Clean up resources
            await self.web_scraper.close()

    async def analyze_leads(self, leads: List[Dict]) -> List[Dict]:
        """
        Analyze and score a list of existing leads.
        
        Args:
            leads: List of lead dictionaries with contact info
            
        Returns:
            List of leads with scores and analysis
        """
        try:
            scored_leads = await self._score_leads_parallel(leads)
            scored_leads.sort(key=lambda x: x['score'].total_score, reverse=True)
            return scored_leads
            
        except Exception as e:
            logger.error(f"Error analyzing leads: {str(e)}")
            raise

    async def _score_leads_parallel(self, leads: List[Dict]) -> List[Dict]:
        """Score multiple leads in parallel."""
        scoring_tasks = []
        
        for lead in leads:
            task = asyncio.create_task(self._score_lead(lead))
            scoring_tasks.append(task)
            
        scored_leads = await asyncio.gather(*scoring_tasks)
        return scored_leads
        
    async def _score_lead(self, lead: Dict) -> Dict:
        """Score a single lead and add the score to the lead dict."""
        try:
            score = await self.lead_scorer.score_lead(lead)
            lead['score'] = score
            return lead
            
        except Exception as e:
            logger.error(f"Error scoring lead {lead.get('name')}: {str(e)}")
            # Return lead with minimum score on error
            lead['score'] = LeadScore(
                total_score=0.0,
                property_fit=0.0,
                decision_maker=0.0,
                location_value=0.0,
                response_likelihood=0.0,
                notes="Error during scoring"
            )
            return lead

    async def export_leads(self, leads: List[Dict[str, Any]], format: str = 'csv') -> bytes:
        """
        Export leads to the specified format.
        Currently supports CSV format.
        """
        if format.lower() != 'csv':
            raise ValueError("Only CSV format is currently supported")
            
        import csv
        import io
        
        output = io.StringIO()
        if not leads:
            return output.getvalue().encode('utf-8')
            
        # Get all unique keys from all leads
        fieldnames = set()
        for lead in leads:
            fieldnames.update(self._flatten_dict(lead).keys())
            
        writer = csv.DictWriter(output, fieldnames=sorted(fieldnames))
        writer.writeheader()
        
        # Write flattened lead data
        for lead in leads:
            writer.writerow(self._flatten_dict(lead))
            
        return output.getvalue().encode('utf-8')

    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """
        Flatten a nested dictionary for CSV export.
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
                
        return dict(items) 