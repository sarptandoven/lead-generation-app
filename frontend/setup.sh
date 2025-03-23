#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "REACT_APP_API_URL=http://localhost:8000" > .env
    echo "REACT_APP_ENV=development" >> .env
fi

# Start the development server
echo "Starting development server..."
npm start 