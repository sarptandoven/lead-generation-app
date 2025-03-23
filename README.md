# AI-Powered Lead Generation System

A production-ready lead generation system that combines multiple data sources and AI-powered analysis to identify and qualify property management leads.

## Features

- LinkedIn Lead Scraping
- Airbnb Property Manager Scraping
- General Web Scraping for Property Managers
- AI-Powered Lead Scoring
- Contact Enrichment
- Email Verification
- Modern React Frontend
- FastAPI Backend
- PostgreSQL Database
- Rate Limiting & Proxy Support
- Export Functionality

## Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Chrome/Chromium browser
- OpenAI API key
- LinkedIn Sales Navigator account

## Required API Keys and Credentials

1. **LinkedIn Credentials**
   - LinkedIn Sales Navigator username and password
   - Location: `backend/.env` file

2. **OpenAI API Key**
   - Required for AI-powered lead scoring and enrichment
   - Location: `backend/.env` file

3. **Database Credentials**
   - PostgreSQL connection string
   - Location: `backend/.env` file

4. **Application Secret Key**
   - Used for JWT token generation
   - Location: `backend/.env` file

5. **Optional: Email Verification API**
   - For verifying contact information
   - Location: `backend/.env` file

## Installation

### Backend Setup

1. Create and activate a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Initialize the database:
```bash
alembic upgrade head
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your backend API URL
```

## Running the Application

### Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Usage

1. Log in to the application
2. Select your lead generation source (LinkedIn, Airbnb, or Web)
3. Configure search parameters
4. Start the scraping process
5. View and export leads in the dashboard

## Rate Limiting and Best Practices

- The system includes built-in rate limiting to prevent API blocks
- Use proxy servers for large-scale scraping
- Respect robots.txt and website terms of service
- Implement appropriate delays between requests

## Security Considerations

- All credentials are stored in environment variables
- JWT-based authentication
- Rate limiting to prevent abuse
- Input validation and sanitization
- HTTPS encryption

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Style

```bash
# Backend
cd backend
black .
isort .
flake8

# Frontend
cd frontend
npm run lint
```

## Deployment

1. Set up a production PostgreSQL database
2. Configure production environment variables
3. Build the frontend:
```bash
cd frontend
npm run build
```
4. Deploy using your preferred hosting service (e.g., Heroku, AWS, GCP)

## Support

For support, please create an issue in the GitHub repository or contact the development team.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
