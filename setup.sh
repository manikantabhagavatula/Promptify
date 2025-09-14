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

# Create and activate Python virtual environment
echo "🐍 Creating Python virtual environment..."
if [ -d "promptify-env" ]; then
    echo "⚠️  Virtual environment 'promptify-env' already exists. Removing it..."
    rm -rf promptify-env
fi

python3 -m venv promptify-env

# Check if virtual environment was created successfully
if [ ! -d "promptify-env" ]; then
    echo "❌ Failed to create virtual environment. Please check your Python installation."
    exit 1
fi

echo "🔧 Activating virtual environment..."
source promptify-env/bin/activate

# Verify virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Failed to activate virtual environment."
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"

# Upgrade pip in virtual environment
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

echo ""
echo "🎉 Setup complete! Now you can run the application:"
echo ""
echo "📝 IMPORTANT: Always activate the virtual environment before running the Python backend!"
echo ""
echo "1. Activate the virtual environment:"
echo "   source promptify-env/bin/activate"
echo ""
echo "2. Set your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "3. Start the Python backend (in one terminal):"
echo "   uvicorn app:app --reload --port 8000"
echo ""
echo "4. Start the Node.js frontend (in another terminal):"
echo "   npm start"
echo ""
echo "5. Open your browser to: http://localhost:3000"
echo ""
echo "💡 To deactivate the virtual environment when done:"
echo "   deactivate"
echo ""
echo "🔄 To reactivate the virtual environment later:"
echo "   source promptify-env/bin/activate"
