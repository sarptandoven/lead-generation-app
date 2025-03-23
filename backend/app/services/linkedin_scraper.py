from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
import logging
from typing import List, Dict, Any
from ..core.config import settings
import os

logger = logging.getLogger(__name__)

class LinkedInScraper:
    def __init__(self):
        self.username = settings.LINKEDIN_USERNAME
        self.password = settings.LINKEDIN_PASSWORD
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        """Initialize the Chrome WebDriver with appropriate options."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Add proxy if configured
        if settings.PROXY_LIST:
            proxy = random.choice(settings.PROXY_LIST.split(','))
            options.add_argument(f'--proxy-server={proxy}')

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    async def login(self):
        """Log in to LinkedIn Sales Navigator."""
        try:
            self.driver.get("https://www.linkedin.com/sales/login")
            
            # Wait for iframe and switch to it
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            self.driver.switch_to.frame(iframe)
            
            # Enter credentials
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(self.username)
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            # Click login button
            login_button = self.driver.find_element(By.CLASS_NAME, "login__form_action_container")
            login_button.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "search-results__pagination"))
            )
            
            return True
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return False

    def _random_delay(self):
        """Add random delay between actions to avoid detection."""
        time.sleep(random.uniform(1, 3))

    def _scroll_page(self):
        """Scroll the page gradually to load all content."""
        total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
        for i in range(0, total_height, 100):
            self.driver.execute_script(f"window.scrollTo(0, {i});")
            self._random_delay()

    async def scrape_leads(self, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Scrape leads from LinkedIn Sales Navigator based on provided parameters.
        """
        leads = []
        try:
            if not await self.login():
                raise Exception("Failed to log in to LinkedIn")

            # Construct search URL based on parameters
            search_url = self._construct_search_url(parameters)
            self.driver.get(search_url)
            
            # Wait for results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "search-results__result-item"))
            )
            
            # Get total number of pages
            total_pages = self._get_total_pages()
            
            # Scrape each page
            for page in range(1, total_pages + 1):
                logger.info(f"Scraping page {page} of {total_pages}")
                
                # Scroll to load all results
                self._scroll_page()
                
                # Parse results
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                results = soup.find_all('div', class_='search-results__result-item')
                
                for result in results:
                    lead = self._parse_result(result)
                    if lead:
                        leads.append(lead)
                
                # Add delay between pages
                self._random_delay()
                
                # Go to next page if not the last page
                if page < total_pages:
                    next_page_url = self._construct_search_url(parameters, page + 1)
                    self.driver.get(next_page_url)
                    self._random_delay()
            
            return leads
            
        except Exception as e:
            logger.error(f"Error scraping leads: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()

    def _construct_search_url(self, parameters: Dict[str, Any], page: int = 1) -> str:
        """Construct LinkedIn Sales Navigator search URL."""
        base_url = "https://www.linkedin.com/sales/search/people"
        
        # Add search parameters
        params = {
            "companySize": "E,F,G,H,I",  # Enterprise companies
            "functionIncluded": "12",  # Property Management
            "geoIncluded": "101165590",  # United States
            "industryIncluded": parameters.get("industry", ""),
            "page": str(page),
            "spotlight": "RECENT_POSITION_CHANGE"
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"

    def _get_total_pages(self) -> int:
        """Get total number of pages from pagination."""
        try:
            pagination = self.driver.find_elements(By.CSS_SELECTOR, ".search-results__pagination-list li")
            if not pagination:
                return 1
            
            last_page = pagination[-1].text
            if "..." in last_page:
                return int(last_page.split()[1])
            return int(last_page)
        except:
            return 1

    def _parse_result(self, result) -> Dict[str, Any]:
        """Parse individual search result into lead data."""
        try:
            name = result.find('div', class_='result-lockup__name').text.strip()
            title = result.find('div', class_='result-lockup__highlight-keyword').text.strip()
            company = result.find('div', class_='result-lockup__position-company').text.strip()
            location = result.find('div', class_='result-lockup__misc-list').text.strip()
            
            return {
                "name": name,
                "title": title,
                "company": company,
                "location": location,
                "source": "linkedin"
            }
        except Exception as e:
            logger.error(f"Error parsing result: {str(e)}")
            return None 