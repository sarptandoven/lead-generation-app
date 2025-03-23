import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any
import random
import time
from fake_useragent import UserAgent
from ..core.config import settings

logger = logging.getLogger(__name__)

class AirbnbScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = None
        self.base_url = "https://www.airbnb.com"
        self.headers = {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
        }

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
        Scrape property managers from Airbnb based on provided parameters.
        """
        leads = []
        try:
            await self.setup_session()
            
            # Get initial search results
            search_url = self._construct_search_url(parameters)
            async with self.session.get(search_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch search results: {response.status}")
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Get total number of pages
                total_pages = self._get_total_pages(soup)
                
                # Scrape each page
                for page in range(1, total_pages + 1):
                    logger.info(f"Scraping page {page} of {total_pages}")
                    
                    if page > 1:
                        page_url = self._construct_search_url(parameters, page)
                        async with self.session.get(page_url) as page_response:
                            if page_response.status != 200:
                                continue
                            html = await page_response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract property listings
                    listings = soup.find_all('div', {'itemprop': 'itemListElement'})
                    
                    for listing in listings:
                        lead = await self._parse_listing(listing)
                        if lead:
                            leads.append(lead)
                    
                    # Add delay between pages
                    self._random_delay()
            
            return leads
            
        except Exception as e:
            logger.error(f"Error scraping Airbnb leads: {str(e)}")
            raise
        finally:
            await self.close_session()

    def _construct_search_url(self, parameters: Dict[str, Any], page: int = 1) -> str:
        """Construct Airbnb search URL."""
        base_url = f"{self.base_url}/s/{parameters.get('location', 'United-States')}/homes"
        
        # Add search parameters
        params = {
            "adults": "1",
            "children": "0",
            "infants": "0",
            "checkin": parameters.get("checkin", ""),
            "checkout": parameters.get("checkout", ""),
            "page": str(page),
            "tab": "all",
            "price_min": parameters.get("price_min", ""),
            "price_max": parameters.get("price_max", ""),
            "room_types[]": "Entire home/apt",
            "property_type_id[]": "1",  # House
            "amenities[]": "4",  # Kitchen
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items() if v])
        return f"{base_url}?{query_string}"

    def _get_total_pages(self, soup: BeautifulSoup) -> int:
        """Get total number of pages from pagination."""
        try:
            pagination = soup.find('nav', {'aria-label': 'Pagination'})
            if not pagination:
                return 1
            
            pages = pagination.find_all('button')
            if not pages:
                return 1
            
            last_page = pages[-1].text
            return int(last_page) if last_page.isdigit() else 1
        except:
            return 1

    async def _parse_listing(self, listing) -> Dict[str, Any]:
        """Parse individual listing into lead data."""
        try:
            # Get listing details
            title = listing.find('meta', {'itemprop': 'name'})['content']
            price = listing.find('span', {'class': '_tyxjp1'}).text
            rating = listing.find('span', {'class': 'r1g2bVn'}).text
            
            # Get host information
            host_link = listing.find('a', {'class': '_1n81at5'})
            if not host_link:
                return None
                
            host_url = f"{self.base_url}{host_link['href']}"
            
            # Fetch host profile
            async with self.session.get(host_url) as response:
                if response.status != 200:
                    return None
                    
                host_html = await response.text()
                host_soup = BeautifulSoup(host_html, 'html.parser')
                
                host_name = host_soup.find('h1', {'class': '_1n81at5'}).text
                host_location = host_soup.find('div', {'class': '_1n81at5'}).text
                
                # Get host's other listings
                listings_count = host_soup.find('div', {'class': '_1n81at5'}).text
                listings_count = int(''.join(filter(str.isdigit, listings_count)))
                
                return {
                    "name": host_name,
                    "title": "Property Manager",
                    "company": f"Airbnb Host ({listings_count} properties)",
                    "location": host_location,
                    "source": "airbnb",
                    "property_count": listings_count,
                    "average_rating": float(rating.split()[0]),
                    "profile_url": host_url
                }
                
        except Exception as e:
            logger.error(f"Error parsing listing: {str(e)}")
            return None

    async def get_host_details(self, host_url: str) -> Dict[str, Any]:
        """Get detailed information about a host."""
        try:
            async with self.session.get(host_url) as response:
                if response.status != 200:
                    return None
                    
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract host details
                name = soup.find('h1', {'class': '_1n81at5'}).text
                location = soup.find('div', {'class': '_1n81at5'}).text
                response_rate = soup.find('div', {'class': '_1n81at5'}).text
                response_time = soup.find('div', {'class': '_1n81at5'}).text
                
                # Get all listings
                listings = []
                listings_section = soup.find('div', {'class': '_1n81at5'})
                if listings_section:
                    for listing in listings_section.find_all('div', {'class': '_1n81at5'}):
                        listing_data = {
                            "title": listing.find('div', {'class': '_1n81at5'}).text,
                            "price": listing.find('span', {'class': '_tyxjp1'}).text,
                            "rating": listing.find('span', {'class': 'r1g2bVn'}).text
                        }
                        listings.append(listing_data)
                
                return {
                    "name": name,
                    "location": location,
                    "response_rate": response_rate,
                    "response_time": response_time,
                    "listings": listings
                }
                
        except Exception as e:
            logger.error(f"Error getting host details: {str(e)}")
            return None 