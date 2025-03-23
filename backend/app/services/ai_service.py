from openai import AsyncOpenAI
from typing import Dict, Any, Optional
import json
from ..core.config import settings

class AIService:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.scoring_prompt = """
        Analyze the following lead information and provide a score from 0-100 based on their potential as a property management lead.
        Consider:
        1. Title relevance to property management
        2. Company size and type
        3. Location
        4. Decision-making authority
        5. Industry relevance
        
        Lead Information:
        {lead_info}
        
        Provide a JSON response with:
        1. score (0-100)
        2. reasoning
        3. suggested approach
        """
        
        self.enrichment_prompt = """
        Based on the following lead information, suggest additional data points and insights that would be valuable for property management sales.
        
        Lead Information:
        {lead_info}
        
        Provide a JSON response with:
        1. suggested questions
        2. pain points to address
        3. value propositions
        4. potential objections
        """

    async def score_lead(self, lead_data: Dict[str, Any]) -> float:
        """Score a lead based on their potential as a property management prospect."""
        lead_info = json.dumps(lead_data, indent=2)
        prompt = self.scoring_prompt.format(lead_info=lead_info)
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a lead scoring expert for property management software."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result["score"]

    async def enrich_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich lead data with AI-generated insights."""
        lead_info = json.dumps(lead_data, indent=2)
        prompt = self.enrichment_prompt.format(lead_info=lead_info)
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a sales strategy expert for property management software."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        enrichment_data = json.loads(response.choices[0].message.content)
        
        # Add enrichment data to lead data
        lead_data.update({
            "ai_insights": enrichment_data,
            "score": await self.score_lead(lead_data)
        })
        
        return lead_data

    async def generate_personalized_email(self, lead_data: Dict[str, Any]) -> str:
        """Generate a personalized email for the lead."""
        prompt = f"""
        Create a personalized email for the following lead, focusing on property management solutions.
        The email should be professional, engaging, and highlight relevant value propositions.
        
        Lead Information:
        {json.dumps(lead_data, indent=2)}
        
        Include:
        1. Personalized greeting
        2. Relevant pain points
        3. Value proposition
        4. Clear call to action
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional sales copywriter."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

    async def analyze_conversation(self, conversation_history: list, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a conversation with a lead and provide insights."""
        prompt = f"""
        Analyze the following conversation with a lead and provide insights on:
        1. Key points discussed
        2. Pain points identified
        3. Objections raised
        4. Next steps recommended
        
        Lead Information:
        {json.dumps(lead_data, indent=2)}
        
        Conversation History:
        {json.dumps(conversation_history, indent=2)}
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a sales conversation analyst."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content) 