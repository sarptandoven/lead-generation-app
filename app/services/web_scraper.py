"""web scraping module specialized for property management leads."""

from typing import Dict, List, Optional
import logging
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential
from ratelimit import limits, sleep_and_retry
from dataclasses import dataclass
from linkedin_api import Linkedin
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Lead:
    """data class for property management leads."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    portfolio_size: Optional[int] = None
    property_types: Optional[List[str]] = None
    experience_years: Optional[int] = None
    source: str = "unknown"
    score: Optional[float] = None
    analysis: Optional[Dict] = None

class WebScraper:
    """web scraper specialized for property management leads."""

    def __init__(self, linkedin_username: Optional[str] = None, linkedin_password: Optional[str] = None):
        """initialize the web scraper with necessary configurations."""
        self.user_agent = UserAgent()
        self.session = None
        self.rate_limit = 100  # increased rate limit
        self.max_retries = 5   # increased retries
        self.linkedin_api = None
        if linkedin_username and linkedin_password:
            self.linkedin_api = Linkedin(linkedin_username, linkedin_password)
        
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
            'community manager'
        ]
        
        self.company_keywords = [
            'properties',
            'realty',
            'real estate',
            'property management',
            'asset management',
            'facilities'
        ]

    async def __aenter__(self):
        """setup async context."""
        self.session = aiohttp.ClientSession(
            headers={'User-Agent': self.user_agent.random},
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """cleanup async context."""
        if self.session:
            await self.session.close()

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
    @sleep_and_retry
    @limits(calls=100, period=60)
    async def fetch_page(self, url: str) -> str:
        """fetch webpage content with improved rate limiting and retries."""
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            logger.error(f"error fetching page {url}: {str(e)}")
            raise

    async def scrape_linkedin(self, query: str, location: Optional[str] = None, limit: int = 50) -> List[Lead]:
        """scrape property management leads from linkedin with enhanced filtering."""
        leads = []
        if not self.linkedin_api:
            logger.error("linkedin api credentials not provided")
            return leads

        try:
            # Search for property management professionals
            search_params = {
                'keywords': ' OR '.join(self.property_management_keywords),
                'location': location if location else 'United States',
                'limit': limit * 2  # fetch more to filter down to quality leads
            }
            
            results = self.linkedin_api.search_people(**search_params)
            
            for result in results:
                # Enhanced filtering for quality leads
                if not self._is_quality_property_manager(result):
                    continue
                    
                profile = self.linkedin_api.get_profile(result['public_id'])
                
                # Extract years of experience
                experience_years = self._calculate_experience_years(profile.get('experience', []))
                
                # Extract portfolio size and property types
                portfolio_info = self._extract_portfolio_info(profile)
                
                lead = Lead(
                    first_name=profile.get('first_name'),
                    last_name=profile.get('last_name'),
                    position=profile.get('headline'),
                    company=profile.get('company'),
                    location=profile.get('location'),
                    experience_years=experience_years,
                    portfolio_size=portfolio_info['size'],
                    property_types=portfolio_info['types'],
                    source='linkedin'
                )
                
                if self._meets_quality_threshold(lead):
                    leads.append(lead)
                
                if len(leads) >= limit:
                    break
                    
                await asyncio.sleep(1)  # Respect rate limits
                
        except Exception as e:
            logger.error(f"error scraping linkedin: {str(e)}")
            
        return leads

    def _is_quality_property_manager(self, profile: Dict) -> bool:
        """verify if the profile matches our property manager criteria."""
        if not profile.get('headline'):
            return False
            
        headline = profile['headline'].lower()
        
        # Must have property management related terms
        if not any(keyword in headline for keyword in self.property_management_keywords):
            return False
            
        # Prefer decision makers
        leadership_terms = ['director', 'head', 'chief', 'vp', 'president', 'owner']
        is_leader = any(term in headline for term in leadership_terms)
        
        # Prefer those with company names indicating property management
        company = profile.get('company', '').lower()
        is_property_company = any(keyword in company for keyword in self.company_keywords)
        
        return is_leader or is_property_company

    def _calculate_experience_years(self, experience: List[Dict]) -> int:
        """calculate total years of relevant property management experience."""
        total_years = 0
        for role in experience:
            if any(keyword in role.get('title', '').lower() for keyword in self.property_management_keywords):
                # Calculate duration of each relevant role
                start_year = int(role.get('starts_at', {}).get('year', 0))
                end_year = int(role.get('ends_at', {}).get('year', 2024))
                total_years += end_year - start_year
        return total_years

    def _extract_portfolio_info(self, profile: Dict) -> Dict:
        """extract information about portfolio size and property types."""
        info = {'size': 0, 'types': []}
        
        # Look for portfolio information in about section and experience
        text_to_analyze = profile.get('about', '') + ' ' + \
                         ' '.join(str(exp.get('description', '')) for exp in profile.get('experience', []))
        
        # Extract portfolio size
        size_patterns = [
            r'(\d+)\s*properties',
            r'(\d+)\s*units',
            r'portfolio of (\d+)',
            r'managing (\d+)'
        ]
        
        for pattern in size_patterns:
            matches = re.findall(pattern, text_to_analyze, re.IGNORECASE)
            if matches:
                info['size'] = max([int(num) for num in matches])
                break
        
        # Extract property types
        property_types = [
            'residential',
            'commercial',
            'industrial',
            'retail',
            'multi-family',
            'single-family',
            'office',
            'mixed-use'
        ]
        
        info['types'] = [pt for pt in property_types if pt in text_to_analyze.lower()]
        
        return info

    def _meets_quality_threshold(self, lead: Lead) -> bool:
        """determine if a lead meets our quality standards."""
        if not lead.position or not lead.company:
            return False
            
        # Must be in property management
        if not any(keyword in lead.position.lower() for keyword in self.property_management_keywords):
            return False
            
        # Prefer experienced professionals
        if lead.experience_years and lead.experience_years < 2:
            return False
            
        # Prefer those managing larger portfolios
        if lead.portfolio_size and lead.portfolio_size < 10:
            return False
            
        return True

    async def scrape_sources(self, sources: List[str], query: str, location: Optional[str] = None, limit: int = 50) -> List[Lead]:
        """scrape leads from multiple sources with enhanced filtering."""
        all_leads = []
        tasks = []
        
        for source in sources:
            if source.lower() == 'linkedin':
                task = self.scrape_linkedin(query, location, limit)
                tasks.append(task)
            else:
                # Add other specialized property management sources here
                pass
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, list):
                    all_leads.extend(result)
                else:
                    logger.error(f"error in scraping task: {str(result)}")

        # Sort leads by portfolio size and experience
        all_leads.sort(key=lambda x: (x.portfolio_size or 0, x.experience_years or 0), reverse=True)
        
        return all_leads[:limit] if limit else all_leads 