"""Web scraping module specialized for property management leads."""

from typing import Dict, List, Optional, Any
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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Lead:
    """Data class for property management leads."""
    name: str
    title: str
    company: str
    location: str
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_size: Optional[int] = None
    property_types: Optional[List[str]] = None
    experience_years: Optional[int] = None
    source: str = "web_scraper"
    metadata: Optional[Dict] = None

class WebScraper:
    """Web scraper specialized for property management leads."""

    def __init__(self):
        """Initialize the web scraper with necessary configurations."""
        self.user_agent = UserAgent()
        self.session = None
        self.rate_limit = 100
        self.max_retries = 5
        self.linkedin_api = None
        self.driver = None
        
        # Try to initialize LinkedIn API if credentials are available
        if hasattr(settings, 'LINKEDIN_USERNAME') and hasattr(settings, 'LINKEDIN_PASSWORD'):
            try:
                self.linkedin_api = Linkedin(settings.LINKEDIN_USERNAME, settings.LINKEDIN_PASSWORD)
                logger.info("LinkedIn API initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize LinkedIn API: {str(e)}")
        
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

    def setup_chrome_driver(self):
        """Set up Chrome driver for web scraping when needed."""
        if self.driver is None:
            try:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("Chrome driver initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Chrome driver: {str(e)}")
                raise

    async def __aenter__(self):
        """Set up async context."""
        self.session = aiohttp.ClientSession(
            headers={'User-Agent': self.user_agent.random},
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up async context."""
        if self.session:
            await self.session.close()
        if self.driver:
            self.driver.quit()
            self.driver = None

    async def scrape_leads(self, keywords: List[str], location: Optional[str] = None, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Main method to scrape leads from various sources.
        
        Args:
            keywords: List of keywords to search for
            location: Optional location to filter by
            max_results: Maximum number of leads to return
            
        Returns:
            List of leads in standardized format
        """
        try:
            async with self:
                leads = []
                
                # Try LinkedIn first if available
                if self.linkedin_api:
                    linkedin_leads = await self.scrape_linkedin(
                        query=' '.join(keywords),
                        location=location,
                        limit=max_results
                    )
                    leads.extend(self._convert_lead_to_dict(lead) for lead in linkedin_leads)
                
                # If we need more leads, try other sources
                if len(leads) < max_results:
                    remaining = max_results - len(leads)
                    other_leads = await self.scrape_other_sources(keywords, location, remaining)
                    leads.extend(other_leads)
                
                # Sort by completeness of profile and return top results
                sorted_leads = sorted(
                    leads,
                    key=lambda x: self._calculate_profile_completeness(x),
                    reverse=True
                )
                
                return sorted_leads[:max_results]
                
        except Exception as e:
            logger.error(f"Error scraping leads: {str(e)}")
            return []

    def _convert_lead_to_dict(self, lead: Lead) -> Dict[str, Any]:
        """Convert Lead object to dictionary format."""
        return {
            'name': lead.name,
            'title': lead.title,
            'company': lead.company,
            'location': lead.location,
            'email': lead.email,
            'phone': lead.phone,
            'linkedin_url': lead.linkedin_url,
            'metadata': {
                'portfolio_size': lead.portfolio_size,
                'property_types': lead.property_types,
                'experience_years': lead.experience_years,
                'source': lead.source,
                **({} if lead.metadata is None else lead.metadata)
            }
        }

    def _calculate_profile_completeness(self, lead: Dict[str, Any]) -> float:
        """Calculate a score for profile completeness."""
        score = 0.0
        required_fields = ['name', 'title', 'company', 'location']
        optional_fields = ['email', 'phone', 'linkedin_url']
        
        # Required fields contribute 60% of the score
        for field in required_fields:
            if lead.get(field):
                score += 0.6 / len(required_fields)
        
        # Optional fields contribute 40% of the score
        for field in optional_fields:
            if lead.get(field):
                score += 0.4 / len(optional_fields)
        
        # Metadata can boost the score by up to 20%
        metadata = lead.get('metadata', {})
        if metadata.get('portfolio_size'):
            score *= 1.1
        if metadata.get('property_types'):
            score *= 1.05
        if metadata.get('experience_years'):
            score *= 1.05
            
        return min(score, 1.0)  # Cap at 1.0

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
    @sleep_and_retry
    @limits(calls=100, period=60)
    async def fetch_page(self, url: str) -> str:
        """Fetch webpage content with improved rate limiting and retries."""
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            logger.error(f"Error fetching page {url}: {str(e)}")
            raise

    async def scrape_other_sources(self, keywords: List[str], location: Optional[str], limit: int) -> List[Dict[str, Any]]:
        """Scrape leads from other sources when LinkedIn is unavailable or insufficient."""
        # Implementation for other sources would go here
        # For now, return an empty list
        return []

    async def close(self):
        """Clean up resources."""
        if self.session:
            await self.session.close()
        if self.driver:
            self.driver.quit()
            self.driver = None

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
                    name=profile.get('first_name') + ' ' + profile.get('last_name'),
                    title=profile.get('headline'),
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
        if not lead.title or not lead.company:
            return False
            
        # Must be in property management
        if not any(keyword in lead.title.lower() for keyword in self.property_management_keywords):
            return False
            
        # Prefer experienced professionals
        if lead.experience_years and lead.experience_years < 2:
            return False
            
        # Prefer those managing larger portfolios
        if lead.portfolio_size and lead.portfolio_size < 10:
            return False
            
        return True 