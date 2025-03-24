"""Lead scoring module for evaluating and analyzing leads."""

from typing import Dict, List, Optional
import logging
import os
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeadScoringEngine:
    """Engine for scoring and analyzing leads based on various criteria."""

    def __init__(self, api_key: str):
        """Initialize the scoring engine with OpenAI API key.

        Args:
            api_key: OpenAI API key for analysis
        """
        self.client = OpenAI(api_key=api_key)
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

    def analyze_lead(self, lead_data: Dict) -> Dict:
        """Perform detailed analysis of a lead using GPT."""
        try:
            prompt = self._create_analysis_prompt(lead_data)
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": "You are a lead qualification expert specializing in property management professionals. Focus on identifying decision-makers in property management who would benefit from comprehensive insurance solutions."
                },
                {
                    "role": "user",
                    "content": prompt
                }]
            )
            return self._parse_analysis_response(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"error analyzing lead: {str(e)}")
            return {}

    def score_lead(self, lead_data: Dict, analysis: Optional[Dict] = None) -> float:
        """Calculate overall lead score based on multiple criteria."""
        try:
            scores = {
                'role_relevance': self._calculate_role_relevance(lead_data),
                'portfolio_size': self._calculate_portfolio_size(lead_data),
                'decision_authority': self._calculate_decision_authority(lead_data),
                'location_value': self._calculate_location_value(lead_data)
            }
            
            total_score = sum(
                scores[criterion] * weight
                for criterion, weight in self.scoring_criteria.items()
            )
            
            return round(total_score * 100, 2)
        except Exception as e:
            logger.error(f"Error scoring lead: {str(e)}")
            return 0.0

    def _create_analysis_prompt(self, lead_data: Dict) -> str:
        """Create a prompt for lead analysis.

        Args:
            lead_data: Dictionary containing lead information

        Returns:
            String prompt for analysis
        """
        return (
            f"Analyze this property management professional:\n"
            f"Name: {lead_data.get('first_name', '')} {lead_data.get('last_name', '')}\n"
            f"Title: {lead_data.get('position', '')}\n"
            f"Company: {lead_data.get('company', '')}\n"
            f"Location: {lead_data.get('location', '')}\n"
            f"Experience: {lead_data.get('experience', '')}\n\n"
            "Provide insights on:\n"
            "1. Role in property management decision-making\n"
            "2. Estimated portfolio size and type (residential/commercial)\n"
            "3. Market value of properties in their location\n"
            "4. Likelihood of being interested in comprehensive insurance solutions\n"
            "5. Best approach for initial contact"
        )

    def _parse_analysis_response(self, response: str) -> Dict:
        """Parse the analysis response from OpenAI.

        Args:
            response: String response from OpenAI

        Returns:
            Dictionary containing parsed analysis
        """
        return {
            'analysis': response,
            'summary': response.split('\n')[0] if response else ''
        }

    def _calculate_role_relevance(self, lead_data: Dict) -> float:
        """Calculate role relevance score.

        Args:
            lead_data: Dictionary containing lead information

        Returns:
            Float score between 0 and 1
        """
        position = lead_data.get('position', '').lower()
        
        # Direct role match
        if any(keyword in position for keyword in self.property_management_keywords):
            return 1.0
            
        # Partial role match
        related_terms = ['real estate', 'property', 'facilities', 'operations', 'maintenance']
        if any(term in position for term in related_terms):
            return 0.7
            
        return 0.2

    def _calculate_portfolio_size(self, lead_data: Dict) -> float:
        """Calculate portfolio size score.

        Args:
            lead_data: Dictionary containing lead information

        Returns:
            Float score between 0 and 1
        """
        company = lead_data.get('company', '').lower()
        position = lead_data.get('position', '').lower()
        
        # Large property management companies
        if any(term in company for term in ['realty', 'properties', 'management group']):
            return 1.0
            
        # Individual property managers
        if 'manager' in position and 'property' in position:
            return 0.7
            
        return 0.4

    def _calculate_decision_authority(self, lead_data: Dict) -> float:
        """Calculate decision authority score.

        Args:
            lead_data: Dictionary containing lead information

        Returns:
            Float score between 0 and 1
        """
        position = lead_data.get('position', '').lower()
        
        leadership_terms = ['director', 'head', 'chief', 'vp', 'president', 'owner', 'founder']
        if any(term in position for term in leadership_terms):
            return 1.0
            
        management_terms = ['manager', 'supervisor', 'lead']
        if any(term in position for term in management_terms):
            return 0.8
            
        return 0.4

    def _calculate_location_value(self, lead_data: Dict) -> float:
        """Calculate location value score.

        Args:
            lead_data: Dictionary containing lead information

        Returns:
            Float score between 0 and 1
        """
        location = lead_data.get('location', '').lower()
        
        # High-value property markets
        premium_markets = ['new york', 'san francisco', 'los angeles', 'miami', 'seattle', 'boston', 'chicago']
        if any(market in location for market in premium_markets):
            return 1.0
            
        # Mid-tier markets
        mid_markets = ['austin', 'denver', 'portland', 'nashville', 'atlanta', 'dallas']
        if any(market in location for market in mid_markets):
            return 0.8
            
        return 0.6 if location else 0.3 