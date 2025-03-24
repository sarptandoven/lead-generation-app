"""Tests for the web scraper module."""

import pytest
from web_scraper import WebScraper, Lead

@pytest.fixture
async def web_scraper_fixture():
    """Create a WebScraper instance for testing."""
    scraper = WebScraper()
    yield scraper
    await scraper.close()

@pytest.mark.asyncio
async def test_scrape_sources_empty_sources(web_scraper_fixture):
    """Test scraping with empty sources list."""
    leads = await web_scraper_fixture.scrape_sources(sources=[])
    assert isinstance(leads, list)
    assert len(leads) == 0

@pytest.mark.asyncio
async def test_scrape_linkedin(web_scraper_fixture):
    """Test LinkedIn scraping with test query."""
    leads = await web_scraper_fixture.scrape_linkedin(query="test", location="test")
    assert isinstance(leads, list)
    assert len(leads) == 0  # Expect empty list without API access

@pytest.mark.asyncio
async def test_scrape_custom_website(web_scraper_fixture):
    """Test scraping from a known website structure."""
    leads = await web_scraper_fixture.scrape_custom_website("https://example.com")
    assert isinstance(leads, list)
    for lead in leads:
        assert isinstance(lead, Lead)
        assert hasattr(lead, "first_name")
        assert hasattr(lead, "last_name")
        assert hasattr(lead, "email")
        assert hasattr(lead, "phone")
        assert hasattr(lead, "location")
        assert hasattr(lead, "source")

@pytest.mark.asyncio
async def test_scrape_sources_with_invalid_source(web_scraper_fixture):
    """Test scraping with an invalid source."""
    leads = await web_scraper_fixture.scrape_sources(sources=["invalid_source"])
    assert isinstance(leads, list)
    assert len(leads) == 0

if __name__ == "__main__":
    pytest.main(["-v"]) 