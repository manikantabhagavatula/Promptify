# Promptify - AI-Powered Caption Generator

A full-stack web application that generates engaging social media captions using AI. Built with Node.js frontend and Python FastAPI backend.

## Features

- 🤖 AI-powered caption generation using OpenAI GPT
- 📱 Multi-platform support (Instagram, Twitter, TikTok, LinkedIn, Facebook)
- 🎭 Multiple tone options (Funny, Poetic, Inspirational, Sarcastic)
- 🖼️ Image analysis and description
- 📋 One-click copy to clipboard
- 🏷️ Automatic hashtag generation
- 🎨 Modern, responsive UI

## Architecture

- **Frontend**: Node.js + Express (serves static files and proxies API calls)
- **Backend**: Python FastAPI (handles AI processing and image analysis)
- **AI**: OpenAI GPT-4o-mini for caption generation
- **Image Processing**: PIL (Python Imaging Library)

## Quick Start

### Option 1: Automated Setup
```bash
./setup.sh
```

### Option 2: Manual Setup

1. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Set your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

4. **Start the Python backend (Terminal 1):**
   ```bash
   uvicorn app:app --reload --port 8000
   ```

5. **Start the Node.js frontend (Terminal 2):**
   ```bash
   npm start
   ```

6. **Open your browser:**
   Navigate to `http://localhost:3000`

## Project Structure

```
node-project/
├── app.py                  # Python FastAPI backend
├── requirements.txt        # Python dependencies
├── index.js               # Node.js Express server
├── package.json           # Node.js dependencies
├── public/
│   └── index.html         # Frontend UI
├── setup.sh              # Automated setup script
└── README.md             # This file
```

## API Endpoints

### Python Backend (Port 8000)
- `GET /health` - Health check
- `POST /api/improve_caption` - Generate captions

### Node.js Frontend (Port 3000)
- `GET /` - Main application
- `GET /health` - Frontend health check
- `POST /api/*` - Proxied to Python backend

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - OpenAI model to use (default: gpt-4o-mini)
- `PYTHON_API_URL` - Python backend URL (default: http://localhost:8000)
- `PORT` - Node.js server port (default: 3000)

## Usage

1. **Enter a description** of your post in the text input
2. **Select platform** (Instagram, Twitter, etc.)
3. **Choose tone** (Default, Funny, Poetic, etc.)
4. **Upload an image** (optional) for context
5. **Click "Improve Caption"** to generate suggestions
6. **Copy captions** with one click

## Development

### Frontend Development
```bash
npm run dev  # Auto-restart on changes
```

### Backend Development
```bash
uvicorn app:app --reload --port 8000  # Auto-restart on changes
```

## Troubleshooting

### Backend Not Running
- Ensure Python backend is running on port 8000
- Check that all Python dependencies are installed
- Verify your OpenAI API key is set

### CORS Issues
- The Python backend includes CORS middleware for localhost:3000
- If using different ports, update CORS origins in `app.py`

### API Key Issues
- Make sure `OPENAI_API_KEY` environment variable is set
- Verify the API key is valid and has sufficient credits

## Technologies Used

### Backend
- **Python 3.8+** - Runtime
- **FastAPI** - Web framework
- **OpenAI API** - AI caption generation
- **PIL (Pillow)** - Image processing
- **httpx** - HTTP client

### Frontend
- **Node.js** - Runtime
- **Express.js** - Web server
- **http-proxy-middleware** - API proxying
- **HTML5/CSS3/JavaScript** - UI

## License

ISC
