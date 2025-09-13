#!/bin/bash

echo "🚀 Setting up Promptify - Full Stack Integration"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

echo ""
echo "🎉 Setup complete! Now you can run the application:"
echo ""
echo "1. Start the Python backend (in one terminal):"
echo "   uvicorn app:app --reload --port 8000"
echo ""
echo "2. Start the Node.js frontend (in another terminal):"
echo "   npm start"
echo ""
echo "3. Open your browser to: http://localhost:3000"
echo ""
echo "⚠️  Don't forget to set your OPENAI_API_KEY environment variable!"
echo "   export OPENAI_API_KEY='your-api-key-here'"
