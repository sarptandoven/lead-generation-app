import pytest
import asyncio
from web_scraper import WebScraper, Lead

@pytest.fixture
async def scraper():
    scraper = WebScraper()
    yield scraper
    await scraper.close()

@pytest.mark.asyncio
async def test_scrape_sources_empty_sources(scraper):
    leads = await scraper.scrape_sources([], "test query")
    assert isinstance(leads, list)
    assert len(leads) == 0

@pytest.mark.asyncio
async def test_scrape_linkedin(scraper):
    leads = await scraper.scrape_linkedin("test query")
    assert isinstance(leads, list)
    # LinkedIn scraping requires API access, so it should return empty list
    assert len(leads) == 0

@pytest.mark.asyncio
async def test_scrape_custom_website(scraper):
    # Test with a known website structure
    leads = await scraper.scrape_custom_website("https://example.com")
    assert isinstance(leads, list)
    for lead in leads:
        assert isinstance(lead, Lead)
        assert hasattr(lead, 'firstName')
        assert hasattr(lead, 'lastName')
        assert hasattr(lead, 'email')
        assert hasattr(lead, 'phone')
        assert hasattr(lead, 'location')
        assert hasattr(lead, 'source')

@pytest.mark.asyncio
async def test_scrape_sources_with_invalid_source(scraper):
    leads = await scraper.scrape_sources(["invalid_source"], "test query")
    assert isinstance(leads, list)
    assert len(leads) == 0

if __name__ == '__main__':
    pytest.main(['-v', __file__]) 