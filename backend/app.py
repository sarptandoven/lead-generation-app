from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import jwt
import os
from functools import wraps
import openai
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from dataclasses import dataclass
import logging
from concurrent.futures import ThreadPoolExecutor
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_scraper import WebScraper
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
OPENAI_API_KEY = os.getenv('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')
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize the web scraper with LinkedIn API key from environment variables
scraper = WebScraper(linkedin_api_key=os.getenv('LINKEDIN_API_KEY'))

@dataclass
class LeadScore:
    relevance: float
    engagement: float
    potential: float
    total: float

class LeadGenerator:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
    
    def setup_driver(self):
        return webdriver.Chrome(options=self.chrome_options)
    
    def scrape_linkedin_profile(self, url: str) -> Dict[str, Any]:
        driver = self.setup_driver()
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'profile-info'))
            )
            
            # Extract profile information
            name = driver.find_element(By.CLASS_NAME, 'profile-name').text
            position = driver.find_element(By.CLASS_NAME, 'profile-position').text
            company = driver.find_element(By.CLASS_NAME, 'profile-company').text
            
            return {
                'name': name,
                'position': position,
                'company': company,
                'url': url
            }
        finally:
            driver.quit()
    
    def analyze_profile(self, profile_data: Dict[str, Any]) -> LeadScore:
        # Use OpenAI to analyze the profile
        prompt = f"""
        Analyze this professional profile and provide scores for:
        - Relevance to target market
        - Engagement potential
        - Business opportunity
        
        Profile:
        Name: {profile_data['name']}
        Position: {profile_data['position']}
        Company: {profile_data['company']}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert lead qualification AI."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse the response and generate scores
        analysis = response.choices[0].message.content
        
        # Generate scores (this would be more sophisticated in production)
        relevance = random.uniform(0.6, 1.0)
        engagement = random.uniform(0.5, 1.0)
        potential = random.uniform(0.4, 1.0)
        total = (relevance + engagement + potential) / 3
        
        return LeadScore(
            relevance=relevance,
            engagement=engagement,
            potential=potential,
            total=total
        )

lead_generator = LeadGenerator()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/api/leads/generate', methods=['POST'])
@token_required
def generate_leads():
    data = request.json
    
    try:
        # Extract configuration
        industry = data.get('industry')
        target_market = data.get('targetMarket')
        company_size = data.get('companySize')
        location = data.get('location')
        keywords = data.get('keywords', [])
        
        # Use OpenAI to generate search strategies
        prompt = f"""
        Generate LinkedIn search strategies for finding leads with these criteria:
        Industry: {industry}
        Target Market: {target_market}
        Company Size: {company_size}
        Location: {location}
        Keywords: {', '.join(keywords)}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert lead generation strategist."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Process the strategies and generate leads
        strategies = response.choices[0].message.content
        
        # Simulate lead generation (in production, this would actually scrape LinkedIn)
        generated_leads = []
        for _ in range(5):
            lead = {
                'id': f"lead_{random.randint(1000, 9999)}",
                'name': f"Lead {random.randint(1, 100)}",
                'company': f"Company {random.randint(1, 50)}",
                'position': "CEO" if random.random() > 0.5 else "CTO",
                'score': random.uniform(0.5, 1.0),
                'status': 'new',
                'source': 'linkedin',
                'lastActivity': datetime.now().isoformat()
            }
            generated_leads.append(lead)
        
        return jsonify({
            'leads': generated_leads,
            'strategies': strategies
        })
    
    except Exception as e:
        logger.error(f"Error generating leads: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<lead_id>/insights', methods=['GET'])
@token_required
def get_lead_insights(lead_id):
    try:
        # In production, fetch actual lead data from database
        lead_data = {
            'name': f"Lead {lead_id}",
            'company': f"Company {random.randint(1, 50)}",
            'position': "CEO" if random.random() > 0.5 else "CTO"
        }
        
        # Generate insights using OpenAI
        prompt = f"""
        Analyze this lead and provide business insights:
        Name: {lead_data['name']}
        Company: {lead_data['company']}
        Position: {lead_data['position']}
        
        Provide:
        1. Potential value
        2. Engagement strategy
        3. Risk factors
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert business analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        
        insights = response.choices[0].message.content
        
        return jsonify({
            'lead_id': lead_id,
            'insights': insights,
            'scores': {
                'potential_value': random.uniform(0.6, 1.0),
                'engagement_likelihood': random.uniform(0.5, 1.0),
                'risk_level': random.uniform(0.1, 0.5)
            }
        })
    
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
@token_required
def get_analytics():
    timeframe = request.args.get('timeframe', '7d')
    
    try:
        # Generate sample analytics data
        dates = pd.date_range(end=datetime.now(), periods=int(timeframe[:-1]), freq='D')
        
        analytics_data = {
            'leadsBySource': {
                'linkedin': random.randint(50, 200),
                'website': random.randint(20, 100),
                'referral': random.randint(10, 50)
            },
            'conversionRates': {
                'overall': random.uniform(0.1, 0.3),
                'linkedin': random.uniform(0.15, 0.35),
                'website': random.uniform(0.05, 0.25)
            },
            'qualityScores': {
                'average': random.uniform(0.6, 0.8),
                'median': random.uniform(0.5, 0.7)
            },
            'trends': [
                {
                    'date': date.strftime('%Y-%m-%d'),
                    'leads': random.randint(5, 20),
                    'conversions': random.randint(1, 5)
                }
                for date in dates
            ]
        }
        
        return jsonify(analytics_data)
    
    except Exception as e:
        logger.error(f"Error generating analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/scrape/company', methods=['POST'])
@token_required
def scrape_company():
    url = request.json.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Fetch and parse the company website
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract company information
        company_data = {
            'name': soup.title.string if soup.title else None,
            'description': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else None,
            'technologies': [],  # In production, implement technology stack detection
            'social_links': []  # In production, implement social media link detection
        }
        
        return jsonify(company_data)
    
    except Exception as e:
        logger.error(f"Error scraping company data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/scrape', methods=['POST'])
async def scrape_data():
    try:
        data = request.get_json()
        sources = data.get('sources', [])
        search_query = data.get('query', '')
        location = data.get('location')
        
        if not sources or not search_query:
            return jsonify({
                'error': 'Missing required parameters: sources and query'
            }), 400
            
        # Run the scraping operation
        leads = await scraper.scrape_multiple_sources(
            sources=sources,
            search_query=search_query,
            location=location
        )
        
        # Export to CSV if leads were found
        csv_path = None
        if leads:
            filename = f"leads_{search_query.replace(' ', '_')}_{len(leads)}.csv"
            csv_path = scraper.export_to_csv(leads, filename)
        
        return jsonify({
            'success': True,
            'leads': [vars(lead) for lead in leads],
            'total_found': len(leads),
            'csv_path': csv_path
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/export/csv', methods=['POST'])
def export_to_csv():
    try:
        data = request.get_json()
        leads = data.get('leads', [])
        
        if not leads:
            return jsonify({
                'error': 'No leads provided for export'
            }), 400
            
        filename = f"leads_export_{len(leads)}.csv"
        csv_path = scraper.export_to_csv(leads, filename)
        
        return jsonify({
            'success': True,
            'csv_path': csv_path
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.teardown_appcontext
def cleanup(error):
    """Clean up resources when the application shuts down."""
    scraper.cleanup()

if __name__ == '__main__':
    app.run(debug=True, port=5000) 