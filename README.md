# Lead Generation Application

A FastAPI-based application for lead generation and management, featuring automated data collection from LinkedIn and email outreach capabilities.

## Features

- LinkedIn profile data scraping
- Email template management
- Automated email outreach
- Lead status tracking
- Export functionality
- User authentication and authorization

## Prerequisites

- Python 3.8+
- PostgreSQL
- Docker (optional)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd lead-generation-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/lead_generation
SECRET_KEY=your-secret-key
LINKEDIN_EMAIL=your-linkedin-email
LINKEDIN_PASSWORD=your-linkedin-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

5. Initialize the database:
```bash
python app/db/init_db.py
```

## Running the Application

### Local Development
```bash
uvicorn app.main:app --reload
```

### Docker
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage

1. Access the web interface at `http://localhost:8000`
2. Log in with your credentials
3. Configure your LinkedIn and email settings
4. Start generating and managing leads

## Project Structure

```
lead-generation-app/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

