from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import random
from datetime import datetime
import logging
# from web_scraper import WebScraper  # Commented out for now

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Lead Generation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data
mock_role_categories = [
    {
        "id": "management",
        "name": "Management",
        "roles": ["Property Manager", "Asset Manager", "Portfolio Manager"],
        "description": "Management level positions in property management"
    },
    {
        "id": "operations",
        "name": "Operations",
        "roles": ["Maintenance Technician", "Leasing Agent", "Property Administrator"],
        "description": "Operational roles in property management"
    }
]

mock_popular_roles = [
    "Property Manager",
    "Asset Manager",
    "Maintenance Technician",
    "Leasing Agent",
    "Property Accountant"
]

class ScrapeRequest(BaseModel):
    sources: List[str]
    query: str
    location: Optional[str] = None

class Lead(BaseModel):
    firstName: str
    lastName: str
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    source: str
    qualityScore: float

class ScrapeResponse(BaseModel):
    leads: List[Lead]
    totalFound: int

# API Routes
@app.get("/")
async def root():
    return {"message": "Lead Generation API"}

@app.post("/api/sources/{source_id}/configure")
async def configure_source(source_id: str, config: Dict[str, Any]):
    return {
        "id": random.randint(1000, 9999),
        "sourceId": source_id,
        "status": "configured",
        "credentials": config.get("credentials", {}),
        "rateLimits": {
            "maxRequests": 1000,
            "period": "1h"
        }
    }

@app.post("/api/sources/{source_id}/test")
async def test_source_connection(source_id: str):
    # Simulate connection test
    success = source_id != "invalid"
    return {
        "success": success,
        "error": "Invalid credentials" if not success else None
    }

@app.get("/api/leads/search")
async def search_leads(
    sources: str,
    location: Optional[str] = None,
    roles: Optional[str] = None,
    limit: int = 10
):
    sources_list = sources.split(",")
    roles_list = roles.split(",") if roles else []
    
    # Generate mock leads
    leads = []
    for i in range(limit):
        lead = {
            "id": f"lead_{i}",
            "source": random.choice(sources_list),
            "companyName": f"Company {i}",
            "industry": "Real Estate",
            "location": location or "San Francisco, CA",
            "size": random.choice(["1-10", "11-50", "51-200"]),
            "revenue": f"${random.randint(1, 10)}M",
            "founded": str(random.randint(1990, 2020)),
            "description": "Property management company",
            "website": f"https://company{i}.com",
            "contacts": [
                {
                    "name": f"Contact {i}",
                    "title": random.choice(roles_list) if roles_list else "Property Manager",
                    "email": f"contact{i}@company{i}.com",
                    "phone": f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
                }
            ],
            "lastUpdated": datetime.now().isoformat(),
            "confidence": random.uniform(0.7, 1.0)
        }
        leads.append(lead)
    
    return {
        "leads": leads,
        "total": len(leads)
    }

@app.get("/api/sources/{source_id}/stats")
async def get_source_stats(source_id: str):
    return {
        "totalLeads": random.randint(100, 1000),
        "lastSync": datetime.now().isoformat(),
        "requestsRemaining": random.randint(500, 1000),
        "requestsLimit": 1000
    }

@app.post("/api/sources/{source_id}/sync")
async def sync_source(source_id: str):
    return {
        "status": "success",
        "message": f"Successfully synced {source_id}"
    }

@app.get("/api/sources/{source_id}/filters")
async def get_source_filters(source_id: str):
    return {
        "locations": ["San Francisco, CA", "New York, NY", "Chicago, IL"],
        "industries": ["Real Estate", "Property Management", "Construction"],
        "companySizes": ["1-10", "11-50", "51-200", "201-500", "501+"]
    }

@app.get("/api/roles/categories")
async def get_role_categories():
    return mock_role_categories

@app.get("/api/roles/search")
async def search_roles(q: str):
    all_roles = [
        "Property Manager",
        "Asset Manager",
        "Maintenance Technician",
        "Leasing Agent",
        "Property Accountant",
        "Regional Manager",
        "Portfolio Manager",
        "Facilities Manager"
    ]
    return [role for role in all_roles if q.lower() in role.lower()]

@app.get("/api/roles/popular")
async def get_popular_roles():
    return mock_popular_roles

@app.get("/api/roles/stats")
async def get_role_stats(roles: str):
    roles_list = roles.split(",")
    return {
        "totalLeads": len(roles_list) * random.randint(50, 200),
        "averageSeniority": "Mid-Senior",
        "topIndustries": [
            {"industry": "Real Estate", "count": random.randint(100, 500)},
            {"industry": "Property Management", "count": random.randint(50, 300)},
            {"industry": "Construction", "count": random.randint(25, 150)}
        ],
        "roleDistribution": [
            {"role": role, "percentage": random.uniform(0.1, 0.5)}
            for role in roles_list
        ]
    }

@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape_leads(request: ScrapeRequest):
    # Mock response without web scraper dependency
    return ScrapeResponse(
        leads=[
            Lead(
                firstName="John",
                lastName="Doe",
                email="john@example.com",
                phone="+1-555-123-4567",
                location="San Francisco, CA",
                source="linkedin",
                qualityScore=0.85
            )
        ],
        totalFound=1
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
