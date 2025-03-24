from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import openai
import numpy as np
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class LeadProfile:
    name: str
    position: str
    company: str
    industry: Optional[str]
    company_size: Optional[str]
    location: Optional[str]
    linkedin_url: Optional[str]
    email: Optional[str]
    website: Optional[str]
    technologies: List[str]
    recent_activities: List[Dict]
    engagement_history: List[Dict]

@dataclass
class LeadScore:
    total_score: float
    component_scores: Dict[str, float]
    insights: List[str]
    recommendations: List[str]
    confidence: float
    timestamp: datetime

class LeadScoringEngine:
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        
        # Scoring weights for different components
        self.weights = {
            'position_relevance': 0.25,
            'company_fit': 0.20,
            'engagement_potential': 0.20,
            'technology_alignment': 0.15,
            'activity_score': 0.10,
            'location_relevance': 0.10
        }
        
        # Industry-specific scoring modifiers
        self.industry_modifiers = {
            'technology': 1.2,
            'finance': 1.1,
            'healthcare': 1.1,
            'retail': 0.9,
            'manufacturing': 0.9
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def analyze_lead_with_ai(self, lead: LeadProfile) -> Tuple[Dict[str, float], List[str]]:
        """Use GPT-4 to analyze the lead and generate insights"""
        try:
            prompt = f"""
            Analyze this lead profile and provide detailed scoring and insights:
            
            Name: {lead.name}
            Position: {lead.position}
            Company: {lead.company}
            Industry: {lead.industry or 'Unknown'}
            Company Size: {lead.company_size or 'Unknown'}
            Location: {lead.location or 'Unknown'}
            Technologies: {', '.join(lead.technologies) if lead.technologies else 'Unknown'}
            
            Recent Activities:
            {self._format_activities(lead.recent_activities)}
            
            Provide:
            1. Component scores (0-1) for:
               - Position relevance
               - Company fit
               - Engagement potential
               - Technology alignment
               - Activity relevance
               - Location relevance
            
            2. Key insights and recommendations
            
            Format the response as JSON.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert lead scoring AI analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            # Parse the response
            analysis = response.choices[0].message.content
            
            # For now, return sample data
            scores = {
                'position_relevance': np.random.uniform(0.7, 1.0),
                'company_fit': np.random.uniform(0.6, 1.0),
                'engagement_potential': np.random.uniform(0.5, 1.0),
                'technology_alignment': np.random.uniform(0.6, 1.0),
                'activity_score': np.random.uniform(0.4, 1.0),
                'location_relevance': np.random.uniform(0.7, 1.0)
            }
            
            insights = [
                "High-value decision maker in target industry",
                "Company shows strong growth indicators",
                "Technology stack aligns with our solution",
                "Recent activities suggest active buying interest"
            ]
            
            return scores, insights
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            raise

    def calculate_lead_score(self, lead: LeadProfile) -> LeadScore:
        """Calculate the final lead score using multiple factors"""
        try:
            # Get AI analysis
            component_scores, insights = await self.analyze_lead_with_ai(lead)
            
            # Calculate base score
            base_score = sum(
                score * self.weights[component]
                for component, score in component_scores.items()
            )
            
            # Apply industry modifier
            if lead.industry and lead.industry.lower() in self.industry_modifiers:
                base_score *= self.industry_modifiers[lead.industry.lower()]
            
            # Generate recommendations based on scores
            recommendations = self._generate_recommendations(component_scores, lead)
            
            # Calculate confidence score based on data completeness
            confidence = self._calculate_confidence(lead)
            
            return LeadScore(
                total_score=min(base_score, 1.0),  # Cap at 1.0
                component_scores=component_scores,
                insights=insights,
                recommendations=recommendations,
                confidence=confidence,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error calculating lead score: {str(e)}")
            raise

    def _calculate_confidence(self, lead: LeadProfile) -> float:
        """Calculate confidence score based on data completeness"""
        required_fields = [
            lead.name,
            lead.position,
            lead.company,
            lead.industry,
            lead.company_size,
            lead.location
        ]
        
        optional_fields = [
            lead.linkedin_url,
            lead.email,
            lead.website
        ]
        
        # Weight required fields more heavily
        required_score = sum(1 for field in required_fields if field) / len(required_fields) * 0.7
        optional_score = sum(1 for field in optional_fields if field) / len(optional_fields) * 0.3
        
        return required_score + optional_score

    def _generate_recommendations(self, scores: Dict[str, float], lead: LeadProfile) -> List[str]:
        """Generate specific recommendations based on scores and lead profile"""
        recommendations = []
        
        # Position-based recommendations
        if scores['position_relevance'] > 0.8:
            recommendations.append(
                "High-priority lead: Schedule direct outreach within 24 hours"
            )
        
        # Engagement recommendations
        if scores['engagement_potential'] > 0.7:
            recommendations.append(
                "Prepare personalized content based on recent activities"
            )
        
        # Technology alignment recommendations
        if scores['technology_alignment'] < 0.6:
            recommendations.append(
                "Focus on educational content about technology integration benefits"
            )
        
        # Company fit recommendations
        if scores['company_fit'] > 0.7:
            recommendations.append(
                "Research similar success stories for targeted case study sharing"
            )
        
        return recommendations

    def _format_activities(self, activities: List[Dict]) -> str:
        """Format recent activities for AI analysis"""
        if not activities:
            return "No recent activities recorded"
        
        formatted = []
        for activity in activities:
            date = activity.get('date', 'Unknown date')
            type_ = activity.get('type', 'Unknown type')
            description = activity.get('description', 'No description')
            formatted.append(f"- {date}: {type_} - {description}")
        
        return "\n".join(formatted)

    async def batch_score_leads(self, leads: List[LeadProfile]) -> List[LeadScore]:
        """Score multiple leads in parallel"""
        scores = []
        for lead in leads:
            score = await self.calculate_lead_score(lead)
            scores.append(score)
        return scores

# Example usage:
"""
engine = LeadScoringEngine(openai_api_key='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')

lead = LeadProfile(
    name="John Doe",
    position="CTO",
    company="Tech Corp",
    industry="Technology",
    company_size="100-500",
    location="San Francisco, CA",
    linkedin_url="https://linkedin.com/in/johndoe",
    email="john@techcorp.com",
    website="https://techcorp.com",
    technologies=["Python", "AWS", "React"],
    recent_activities=[
        {
            "date": "2024-03-20",
            "type": "Website Visit",
            "description": "Viewed pricing page"
        }
    ],
    engagement_history=[
        {
            "date": "2024-03-19",
            "type": "Email",
            "description": "Opened product overview email"
        }
    ]
)

score = engine.calculate_lead_score(lead)
print(f"Lead Score: {score.total_score}")
print(f"Insights: {score.insights}")
print(f"Recommendations: {score.recommendations}")
""" 