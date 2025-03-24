from typing import List, Dict, Any, Optional
import asyncio
import logging
from datetime import datetime
from openai import OpenAI
from app.core.config import settings

from app.services.web_scraper import WebScraper
from app.services.lead_scoring import LeadScoringService, LeadScore

logger = logging.getLogger(__name__)

class LeadGenerationService:
    def __init__(self):
        self.web_scraper = WebScraper()
        self.lead_scorer = LeadScoringService()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_leads(self, search_criteria: Dict[str, Any], max_leads: int = 10) -> List[Dict[str, Any]]:
        """
        Generate leads based on search criteria using web scraping and lead scoring.
        """
        try:
            # Scrape raw lead data
            raw_leads = await self.web_scraper.scrape_leads(
                keywords=search_criteria.get('keywords', []),
                location=search_criteria.get('location'),
                max_results=max_leads
            )
            
            # Process and score the leads
            processed_leads = await self._process_leads(raw_leads)
            
            # Sort leads by total score in descending order
            sorted_leads = sorted(
                processed_leads,
                key=lambda x: x.get('score', {}).get('total', 0),
                reverse=True
            )
            
            return sorted_leads[:max_leads]
            
        except Exception as e:
            logger.error(f"Error generating leads: {str(e)}")
            return []

    async def _process_leads(self, raw_leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process and score multiple leads concurrently.
        """
        tasks = []
        for lead in raw_leads:
            tasks.append(self._process_single_lead(lead))
            
        # Process leads concurrently
        processed_leads = await asyncio.gather(*tasks)
        
        # Filter out None values (failed processing)
        return [lead for lead in processed_leads if lead is not None]

    async def _process_single_lead(self, lead_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process and score a single lead.
        """
        try:
            # Score the lead
            score = await self.lead_scorer.score_lead(lead_data)
            
            # Enrich lead data with score and metadata
            enriched_lead = {
                **lead_data,
                'score': {
                    'relevance': round(score.relevance * 100, 2),
                    'engagement': round(score.engagement * 100, 2),
                    'potential': round(score.potential * 100, 2),
                    'total': round(score.total * 100, 2)
                },
                'metadata': {
                    'processed_at': datetime.utcnow().isoformat(),
                    'source': lead_data.get('source', 'web_scraper')
                }
            }
            
            return enriched_lead
            
        except Exception as e:
            logger.error(f"Error processing lead: {str(e)}")
            return None

    async def analyze_leads(self, leads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze a batch of leads using GPT to provide insights.
        """
        try:
            prompt = self._create_analysis_prompt(leads)
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a lead analysis expert specializing in property management professionals."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                'analysis': response.choices[0].message.content,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing leads: {str(e)}")
            return {
                'analysis': "Error analyzing leads",
                'timestamp': datetime.utcnow().isoformat()
            }

    def _create_analysis_prompt(self, leads: List[Dict[str, Any]]) -> str:
        """
        Create a prompt for batch lead analysis.
        """
        prompt_parts = [
            f"Analyze the following {len(leads)} property management leads:\n"
        ]
        
        for i, lead in enumerate(leads, 1):
            prompt_parts.extend([
                f"\nLead {i}:",
                f"Name: {lead.get('name', 'N/A')}",
                f"Title: {lead.get('title', 'N/A')}",
                f"Company: {lead.get('company', 'N/A')}",
                f"Location: {lead.get('location', 'N/A')}",
                f"Score: {lead.get('score', {}).get('total', 0)}/100"
            ])
        
        prompt_parts.extend([
            "\nProvide insights on:",
            "1. Overall quality of the lead set",
            "2. Common patterns or trends",
            "3. Recommended prioritization strategy",
            "4. Potential engagement approaches"
        ])
        
        return "\n".join(prompt_parts)

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