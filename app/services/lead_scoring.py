"""Lead scoring module for evaluating and analyzing leads."""

from typing import Dict, List, Optional, Any
import logging
from openai import OpenAI
from dataclasses import dataclass
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LeadScore:
    relevance: float  # How well the lead matches target criteria
    engagement: float  # Level of engagement/activity
    potential: float  # Potential value as a client
    total: float  # Overall score

class LeadScoringService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
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

    async def score_lead(self, lead_data: Dict[str, Any]) -> LeadScore:
        """
        Score a lead based on various criteria using OpenAI's GPT model for analysis.
        """
        try:
            # Get detailed analysis first
            analysis = await self.analyze_lead(lead_data)
            
            # Calculate component scores
            role_score = self._calculate_role_relevance(lead_data)
            portfolio_score = self._calculate_portfolio_size(lead_data)
            authority_score = self._calculate_decision_authority(lead_data)
            location_score = self._calculate_location_value(lead_data)
            
            # Calculate weighted scores
            relevance = (role_score * self.scoring_criteria['role_relevance'] +
                        location_score * self.scoring_criteria['location_value'])
            
            engagement = portfolio_score * self.scoring_criteria['portfolio_size']
            
            potential = (authority_score * self.scoring_criteria['decision_authority'] +
                        portfolio_score * self.scoring_criteria['portfolio_size'])
            
            # Normalize scores to 0-1 range
            total = (relevance + engagement + potential) / 3
            
            return LeadScore(
                relevance=relevance,
                engagement=engagement,
                potential=potential,
                total=total
            )
        except Exception as e:
            logger.error(f"Error scoring lead: {str(e)}")
            return LeadScore(
                relevance=0.5,
                engagement=0.5,
                potential=0.5,
                total=0.5
            )

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