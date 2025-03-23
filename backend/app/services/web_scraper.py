import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any
import random
import time
from fake_useragent import UserAgent
from ..core.config import settings
import re
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = None
        self.headers = {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
        }
        self.property_manager_keywords = [
            "property manager",
            "property management",
            "real estate manager",
            "property owner",
            "landlord",
            "property administrator",
            "property supervisor",
            "property director",
            "property coordinator",
            "property specialist"
        ]
        self.excluded_domains = [
            "linkedin.com",
            "airbnb.com",
            "facebook.com",
            "twitter.com",
            "instagram.com"
        ]

    async def setup_session(self):
        """Initialize aiohttp session with proxy if configured."""
        if settings.PROXY_LIST:
            proxy = random.choice(settings.PROXY_LIST.split(','))
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                proxy=f"http://{proxy}"
            )
        else:
            self.session = aiohttp.ClientSession(headers=self.headers)

    async def close_session(self):
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()

    def _random_delay(self):
        """Add random delay between requests."""
        time.sleep(random.uniform(2, 5))

    async def scrape_leads(self, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Scrape property managers from various web sources based on provided parameters.
        """
        leads = []
        try:
            await self.setup_session()
            
            # Get search results from multiple sources
            search_queries = self._generate_search_queries(parameters)
            
            for query in search_queries:
                # Google search
                google_results = await self._scrape_google(query)
                
                # Process each result
                for url in google_results:
                    try:
                        page_leads = await self._process_webpage(url)
                        leads.extend(page_leads)
                    except Exception as e:
                        logger.error(f"Error processing webpage {url}: {str(e)}")
                        continue
                    
                    self._random_delay()
            
            return leads
            
        except Exception as e:
            logger.error(f"Error scraping web leads: {str(e)}")
            raise
        finally:
            await self.close_session()

    def _generate_search_queries(self, parameters: Dict[str, Any]) -> List[str]:
        """Generate search queries based on parameters."""
        location = parameters.get("location", "")
        queries = []
        
        # Generate queries with different keyword combinations
        for keyword in self.property_manager_keywords:
            if location:
                queries.append(f"{keyword} {location}")
            else:
                queries.append(keyword)
        
        # Add industry-specific queries
        industries = parameters.get("industries", [])
        for industry in industries:
            for keyword in self.property_manager_keywords:
                if location:
                    queries.append(f"{keyword} {industry} {location}")
                else:
                    queries.append(f"{keyword} {industry}")
        
        return queries

    async def _scrape_google(self, query: str) -> List[str]:
        """Scrape Google search results."""
        try:
            search_url = f"https://www.google.com/search?q={query}"
            async with self.session.get(search_url) as response:
                if response.status != 200:
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract search result URLs
                urls = []
                for result in soup.find_all('div', {'class': 'g'}):
                    link = result.find('a')
                    if link and 'href' in link.attrs:
                        url = link['href']
                        if not any(domain in url for domain in self.excluded_domains):
                            urls.append(url)
                
                return urls[:10]  # Limit to top 10 results
                
        except Exception as e:
            logger.error(f"Error scraping Google results: {str(e)}")
            return []

    async def _process_webpage(self, url: str) -> List[Dict[str, Any]]:
        """Process a webpage to extract property manager information."""
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                leads = []
                
                # Extract contact information
                contact_info = self._extract_contact_info(soup)
                
                # Extract property manager information
                manager_info = self._extract_manager_info(soup)
                
                # Combine information
                for manager in manager_info:
                    lead = {
                        "name": manager.get("name", ""),
                        "title": manager.get("title", "Property Manager"),
                        "company": manager.get("company", ""),
                        "location": contact_info.get("location", ""),
                        "email": contact_info.get("email", ""),
                        "phone": contact_info.get("phone", ""),
                        "source": "web",
                        "source_url": url
                    }
                    leads.append(lead)
                
                return leads
                
        except Exception as e:
            logger.error(f"Error processing webpage {url}: {str(e)}")
            return []

    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract contact information from webpage."""
        contact_info = {}
        
        # Extract email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, soup.get_text())
        if emails:
            contact_info["email"] = emails[0]
        
        # Extract phone numbers
        phone_pattern = r'\+?1?\d{9,15}'
        phones = re.findall(phone_pattern, soup.get_text())
        if phones:
            contact_info["phone"] = phones[0]
        
        # Extract location
        location_patterns = [
            r'\d+\s+[A-Za-z\s,]+(?:Avenue|Lane|Road|Boulevard|Drive|Street|Ave|Ln|Rd|Blvd|Dr|St)\.?',
            r'[A-Za-z\s]+,\s*[A-Z]{2}',
            r'[A-Za-z\s]+,\s*[A-Za-z\s]+,\s*[A-Z]{2}'
        ]
        
        for pattern in location_patterns:
            locations = re.findall(pattern, soup.get_text())
            if locations:
                contact_info["location"] = locations[0]
                break
        
        return contact_info

    def _extract_manager_info(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract property manager information from webpage."""
        managers = []
        
        # Look for property manager information in various formats
        for keyword in self.property_manager_keywords:
            # Find text containing property manager keywords
            manager_elements = soup.find_all(
                lambda tag: tag.name in ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
                and keyword.lower() in tag.get_text().lower()
            )
            
            for element in manager_elements:
                # Extract name (assuming it's before the keyword)
                text = element.get_text()
                name_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+' + keyword, text)
                
                if name_match:
                    name = name_match.group(1)
                    
                    # Look for company name
                    company = ""
                    company_element = element.find_next(['p', 'div', 'span'])
                    if company_element:
                        company = company_element.get_text().strip()
                    
                    managers.append({
                        "name": name,
                        "company": company
                    })
        
        return managers

    async def verify_contact_info(self, email: str, phone: str) -> Dict[str, bool]:
        """Verify contact information using external services."""
        verification = {
            "email_valid": False,
            "phone_valid": False
        }
        
        # Email verification
        if email and settings.EMAIL_VERIFICATION_API_KEY:
            try:
                async with self.session.get(
                    f"https://api.email-validator.net/api/verify?EmailAddress={email}&APIKey={settings.EMAIL_VERIFICATION_API_KEY}"
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        verification["email_valid"] = result.get("status", 0) == 200
            except Exception as e:
                logger.error(f"Error verifying email: {str(e)}")
        
        # Phone verification (implement with your preferred service)
        if phone:
            # Add phone verification logic here
            verification["phone_valid"] = True
        
        return verification 