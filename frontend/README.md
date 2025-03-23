# Lead Generation Platform Frontend

This is the frontend application for the AI-powered Lead Generation Platform. It provides a modern, responsive interface for managing leads, generating new leads from various sources, and analyzing lead data.

## Features

- Modern, responsive UI built with Material-UI
- Real-time lead generation from LinkedIn, Airbnb, and web sources
- Lead management with status tracking and scoring
- AI-powered lead scoring and enrichment
- Comprehensive dashboard with key metrics
- Configurable settings for all scraping sources
- Secure authentication system

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Backend API running on http://localhost:8000

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd lead-gen-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory with the following content:
```
REACT_APP_API_URL=http://localhost:8000
```

## Development

To start the development server:

```bash
npm start
```

The application will be available at http://localhost:3000.

## Building for Production

To create a production build:

```bash
npm run build
```

The build output will be in the `build` directory.

## Testing

To run the test suite:

```bash
npm test
```

## Project Structure

```
src/
  ├── components/     # Reusable UI components
  ├── pages/         # Page components
  ├── services/      # API service functions
  ├── hooks/         # Custom React hooks
  ├── utils/         # Utility functions
  ├── theme.ts       # Material-UI theme configuration
  ├── App.tsx        # Main application component
  └── index.tsx      # Application entry point
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 