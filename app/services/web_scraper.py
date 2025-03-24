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
from playwright.async_api import async_playwright

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

class WebScraperService:
    def __init__(self):
        self.browser = None
        self.context = None
    
    async def setup(self):
        """Initialize the browser."""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()

    async def close(self):
        """Clean up resources."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

    async def find_property_managers(self, 
                                   location: str, 
                                   properties_range: str,
                                   max_leads: int = 25) -> List[Dict]:
        """Find property managers based on criteria."""
        if not self.browser:
            await self.setup()

        leads = []
        search_queries = [
            f"property manager {location}",
            f"residential property management company {location}",
            f"apartment property manager {location}"
        ]

        for query in search_queries:
            if len(leads) >= max_leads:
                break

            # Search Google
            google_results = await self._search_google(query)
            
            # Search LinkedIn
            linkedin_results = await self._search_linkedin(query)
            
            # Combine and deduplicate results
            all_results = google_results + linkedin_results
            unique_results = self._deduplicate_leads(all_results)
            
            # Filter by properties range
            filtered_results = self._filter_by_properties(unique_results, properties_range)
            
            leads.extend(filtered_results)
            
            # Respect rate limits
            await asyncio.sleep(2)

        # Trim to max_leads
        return leads[:max_leads]

    async def _search_google(self, query: str) -> List[Dict]:
        """Search Google for property management companies."""
        page = await self.context.new_page()
        results = []
        
        try:
            # Search Google
            await page.goto(f'https://www.google.com/search?q={query}')
            await page.wait_for_load_state('networkidle')
            
            # Extract business listings and organic results
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Process Google Business listings
            business_results = soup.find_all('div', class_='VkpGBb')
            for result in business_results:
                name = result.find('div', class_='dbg0pd')
                if name:
                    name = name.text.strip()
                    website = self._extract_website(result)
                    phone = self._extract_phone(result)
                    
                    results.append({
                        'name': name,
                        'company': name,
                        'source': 'google',
                        'website': website,
                        'phone': phone,
                        'location': self._extract_location(result)
                    })
            
        except Exception as e:
            logger.error(f"Error in Google search: {str(e)}")
        finally:
            await page.close()
        
        return results

    async def _search_linkedin(self, query: str) -> List[Dict]:
        """Search LinkedIn for property managers."""
        page = await self.context.new_page()
        results = []
        
        try:
            # Search LinkedIn
            await page.goto('https://www.linkedin.com/search/results/people/')
            await page.fill('input[aria-label="Search"]', query)
            await page.press('input[aria-label="Search"]', 'Enter')
            await page.wait_for_load_state('networkidle')
            
            # Extract profiles
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            profiles = soup.find_all('li', class_='reusable-search__result-container')
            for profile in profiles:
                name = profile.find('span', class_='actor-name')
                title = profile.find('div', class_='entity-result__primary-subtitle')
                
                if name and title:
                    results.append({
                        'name': name.text.strip(),
                        'title': title.text.strip(),
                        'source': 'linkedin',
                        'linkedin_url': self._extract_linkedin_url(profile),
                        'company': self._extract_company(profile)
                    })
                    
        except Exception as e:
            logger.error(f"Error in LinkedIn search: {str(e)}")
        finally:
            await page.close()
            
        return results

    def _extract_website(self, element) -> Optional[str]:
        """Extract website URL from Google result."""
        website_elem = element.find('a', href=True)
        return website_elem['href'] if website_elem else None

    def _extract_phone(self, element) -> Optional[str]:
        """Extract phone number from result."""
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        text = element.get_text()
        match = re.search(phone_pattern, text)
        return match.group(0) if match else None

    def _extract_location(self, element) -> Optional[str]:
        """Extract location from result."""
        location_elem = element.find('div', class_='address')
        return location_elem.text.strip() if location_elem else None

    def _extract_linkedin_url(self, element) -> Optional[str]:
        """Extract LinkedIn profile URL."""
        link = element.find('a', href=True)
        return link['href'] if link else None

    def _extract_company(self, element) -> Optional[str]:
        """Extract company name from LinkedIn result."""
        company_elem = element.find('div', class_='entity-result__secondary-subtitle')
        return company_elem.text.strip() if company_elem else None

    def _deduplicate_leads(self, leads: List[Dict]) -> List[Dict]:
        """Remove duplicate leads based on name and company."""
        seen = set()
        unique_leads = []
        
        for lead in leads:
            key = f"{lead.get('name', '')}-{lead.get('company', '')}"
            if key not in seen:
                seen.add(key)
                unique_leads.append(lead)
        
        return unique_leads

    def _filter_by_properties(self, leads: List[Dict], properties_range: str) -> List[Dict]:
        """Filter leads by property count range."""
        def parse_range(range_str: str) -> tuple:
            if range_str == "1-7":
                return (1, 7)
            elif range_str == "8-15":
                return (8, 15)
            elif range_str == "15-24":
                return (15, 24)
            else:  # "25+"
                return (25, float('inf'))
        
        min_props, max_props = parse_range(properties_range)
        
        filtered_leads = []
        for lead in leads:
            # Try to find property count in title or description
            properties_count = self._estimate_properties_count(lead)
            if min_props <= properties_count <= max_props:
                lead['properties'] = properties_count
                filtered_leads.append(lead)
        
        return filtered_leads

    def _estimate_properties_count(self, lead: Dict) -> int:
        """Estimate number of properties managed based on available information."""
        # This is a simplified estimation - you might want to enhance this
        title = lead.get('title', '').lower()
        company = lead.get('company', '').lower()
        
        if 'small portfolio' in title or 'small portfolio' in company:
            return 5
        elif 'medium portfolio' in title or 'medium portfolio' in company:
            return 15
        elif 'large portfolio' in title or 'large portfolio' in company:
            return 30
        else:
            return 10  # Default assumption 