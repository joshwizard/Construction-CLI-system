#!/bin/bash
echo "Starting Construction CLI Web Terminal..."
cd web-frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo ""
echo "🏗️  Construction CLI Web Terminal"
echo "================================="
echo "Starting server..."
echo "Once started, open: http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm start