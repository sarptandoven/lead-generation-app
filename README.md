# Lead Generation App

A powerful lead generation application that helps identify and score potential property management leads using AI and web scraping.

## Features

- 🔍 Advanced lead search with multiple criteria
- 💯 AI-powered lead scoring
- 📊 Detailed lead analysis
- 📥 Export leads to CSV
- 🌐 Modern web interface
- 🔒 Secure API endpoints

## Tech Stack

- Backend: FastAPI
- Frontend: HTML/JavaScript with Tailwind CSS
- AI: OpenAI GPT-4
- Data: Web scraping with async support
- Deployment: GitHub Pages + FastAPI on Cloud

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lead-generation-app.git
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

4. Create a `.env` file in the root directory:
   ```env
   PROJECT_NAME="Lead Generation API"
   API_V1_STR="/api/v1"
   BACKEND_CORS_ORIGINS=["http://localhost:5173"]
   SECRET_KEY="your-secret-key"
   OPENAI_API_KEY="your-openai-api-key"
   LINKEDIN_USERNAME="your-linkedin-username"
   LINKEDIN_PASSWORD="your-linkedin-password"
   ```

5. Start the backend server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. Open `app/static/index.html` in your browser or serve it with a local server:
   ```bash
   python -m http.server 5173 --directory app/static
   ```

## Deployment

### Backend Deployment

1. Set up your GitHub repository:
   - Push your code to GitHub
   - Go to Settings > Pages
   - Set up GitHub Pages from the `gh-pages` branch

2. Set up GitHub Secrets:
   - Go to Settings > Secrets
   - Add the following secrets:
     - `OPENAI_API_KEY`
     - `LINKEDIN_USERNAME`
     - `LINKEDIN_PASSWORD`
     - `SECRET_KEY`

3. The GitHub Actions workflow will automatically:
   - Run tests
   - Build the application
   - Deploy to GitHub Pages

### Frontend Deployment

The frontend is automatically deployed to GitHub Pages when you push to the main branch.

## API Documentation

Once the server is running, visit:
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Project Structure
```
lead-generation-app/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── leads.py
│   ├── core/
│   │   └── config.py
│   ├── services/
│   │   ├── lead_generation.py
│   │   ├── lead_scoring.py
│   │   └── web_scraper.py
│   ├── static/
│   │   └── index.html
│   └── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Adding New Features

1. Create new endpoints in `app/api/v1/endpoints/`
2. Add services in `app/services/`
3. Update the frontend in `app/static/index.html`
4. Update tests and documentation

## Testing

Run tests with:
```bash
python -m pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for your own purposes.

## Support

For support, please open an issue in the GitHub repository.

