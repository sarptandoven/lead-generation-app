"""Lead scoring module for evaluating and analyzing leads."""

from typing import Dict, List, Optional, Any
import logging
import os
from openai import OpenAI
from pydantic import BaseModel
from dataclasses import dataclass
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeadScore(BaseModel):
    total: float
    property_fit: float
    decision_maker: float
    location_value: float
    response_likelihood: float
    notes: str

class LeadScoringService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.scoring_criteria = {
            'role_relevance': 0.35,  # how closely they match property management roles
            'portfolio_size': 0.25,  # estimated number of properties managed
            'decision_authority': 0.20,  # likelihood of being a decision maker
            'location_value': 0.20,  # property market value in their area
        }
        
        self.property_management_keywords = [
            'property manager',
            'property management',
            'real estate manager',
            'residential manager',
            'commercial property manager',
            'facility manager',
            'leasing manager',
            'asset manager',
            'portfolio manager',
            'building manager',
            'HOA manager',
            'community manager',
            'maintenance supervisor',
            'property operations',
            'real estate operations'
        ]

    def score_lead(self, lead: Dict[str, Any]) -> LeadScore:
        """Score a single lead based on various criteria."""
        # Create a detailed prompt for the AI
        prompt = self._create_scoring_prompt(lead)
        
        # Get AI analysis
        response = self.client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 for better analysis
            messages=[
                {"role": "system", "content": """You are an expert lead scoring system for property managers.
                Score leads based on these criteria:
                1. Property Fit (0-10): How well does their property portfolio match our target?
                2. Decision Maker Level (0-10): Are they the right person to talk to?
                3. Location Value (0-10): Is this a valuable market location?
                4. Response Likelihood (0-10): How likely are they to respond?
                
                Provide scores and brief explanations. Focus on property managers with:
                - Small to medium portfolio (1-25 properties)
                - Direct decision-making power
                - Active in growing markets
                - Signs of seeking efficiency improvements"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Parse the AI response
        return self._parse_scoring_response(response.choices[0].message.content)
    
    def _create_scoring_prompt(self, lead: Dict[str, Any]) -> str:
        return f"""Please analyze this property manager lead:
        Name: {lead.get('name', 'Unknown')}
        Company: {lead.get('company', 'Unknown')}
        Title: {lead.get('title', 'Unknown')}
        Properties Managed: {lead.get('properties', 'Unknown')}
        Location: {lead.get('location', 'Unknown')}
        LinkedIn Info: {lead.get('linkedin_info', 'None')}
        Recent Activity: {lead.get('recent_activity', 'None')}

        Score this lead and explain why. Format your response as:
        Property Fit: [score]
        Decision Maker: [score]
        Location Value: [score]
        Response Likelihood: [score]
        Notes: [brief explanation]"""

    def _parse_scoring_response(self, response: str) -> LeadScore:
        """Parse the AI response into a LeadScore object."""
        lines = response.strip().split('\n')
        scores = {}
        notes = ""
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                if key == 'notes':
                    notes = value.strip()
                else:
                    try:
                        scores[key] = float(value.strip().split()[0])
                    except (ValueError, IndexError):
                        scores[key] = 0.0
        
        total = sum([
            scores.get('property_fit', 0),
            scores.get('decision_maker', 0),
            scores.get('location_value', 0),
            scores.get('response_likelihood', 0)
        ]) / 4.0
        
        return LeadScore(
            total=total,
            property_fit=scores.get('property_fit', 0),
            decision_maker=scores.get('decision_maker', 0),
            location_value=scores.get('location_value', 0),
            response_likelihood=scores.get('response_likelihood', 0),
            notes=notes
        )

    def filter_top_leads(self, leads: List[Dict[str, Any]], threshold: float = 7.5) -> List[Dict[str, Any]]:
        """Filter and return only the highest-quality leads."""
        scored_leads = []
        for lead in leads:
            score = self.score_lead(lead)
            if score.total >= threshold:
                lead['score'] = score.dict()
                scored_leads.append(lead)
        
        # Sort by total score
        return sorted(scored_leads, key=lambda x: x['score']['total'], reverse=True)

    async def analyze_lead(self, lead_data: Dict) -> Dict:
        """Perform detailed analysis of a lead using GPT."""
        try:
            prompt = self._create_analysis_prompt(lead_data)
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": "You are a lead qualification expert specializing in property management professionals."
                },
                {
                    "role": "user",
                    "content": prompt
                }]
            )
            return self._parse_analysis_response(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error analyzing lead: {str(e)}")
            return {}

    def _create_analysis_prompt(self, lead_data: Dict) -> str:
        """Create a prompt for lead analysis."""
        return (
            f"Analyze this property management professional:\n"
            f"Name: {lead_data.get('name', '')}\n"
            f"Title: {lead_data.get('title', '')}\n"
            f"Company: {lead_data.get('company', '')}\n"
            f"Location: {lead_data.get('location', '')}\n\n"
            "Provide insights on:\n"
            "1. Role in property management decision-making\n"
            "2. Estimated portfolio size and type\n"
            "3. Market value of properties in their location\n"
            "4. Likelihood of being interested in property management solutions"
        )

    def _parse_analysis_response(self, response: str) -> Dict:
        """Parse the analysis response from OpenAI."""
        return {
            'analysis': response,
            'summary': response.split('\n')[0] if response else ''
        }

    def _calculate_role_relevance(self, lead_data: Dict) -> float:
        """Calculate role relevance score."""
        position = lead_data.get('title', '').lower()
        
        # Direct role match
        if any(keyword in position for keyword in self.property_management_keywords):
            return 1.0
            
        # Partial role match
        related_terms = ['real estate', 'property', 'facilities', 'operations', 'maintenance']
        if any(term in position for term in related_terms):
            return 0.7
            
        return 0.2

    def _calculate_portfolio_size(self, lead_data: Dict) -> float:
        """Estimate portfolio size score based on company information."""
        company = lead_data.get('company', '').lower()
        
        # Large property management companies
        if any(term in company for term in ['group', 'corporation', 'properties', 'management']):
            return 0.8
            
        # Medium-sized companies
        if any(term in company for term in ['realty', 'property']):
            return 0.6
            
        return 0.4

    def _calculate_decision_authority(self, lead_data: Dict) -> float:
        """Calculate decision-making authority score."""
        title = lead_data.get('title', '').lower()
        
        # High authority titles
        if any(term in title for term in ['owner', 'president', 'director', 'ceo', 'chief', 'vp', 'head']):
            return 1.0
            
        # Mid-level authority
        if any(term in title for term in ['manager', 'supervisor', 'lead']):
            return 0.7
            
        return 0.3

    def _calculate_location_value(self, lead_data: Dict) -> float:
        """Calculate location value score."""
        location = lead_data.get('location', '').lower()
        
        # High-value markets
        high_value_markets = ['new york', 'san francisco', 'los angeles', 'chicago', 'miami', 'boston']
        if any(market in location for market in high_value_markets):
            return 1.0
            
        # Mid-value markets
        mid_value_markets = ['denver', 'austin', 'seattle', 'portland', 'atlanta']
        if any(market in location for market in mid_value_markets):
            return 0.7
            
        return 0.5 