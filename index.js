const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000';

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Proxy API requests to Python FastAPI backend
app.use('/api', createProxyMiddleware({
    target: PYTHON_API_URL,
    changeOrigin: true,
    onError: (err, req, res) => {
        console.error('Proxy error:', err);
        res.status(500).json({ 
            error: 'Backend service unavailable', 
            message: 'Python API server is not running. Please start it with: uvicorn app:app --reload --port 8000' 
        });
    }
}));

// Route for the main landing page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        message: 'Promptify frontend is running',
        python_api_url: PYTHON_API_URL
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`🚀 Promptify frontend is running on http://localhost:${PORT}`);
    console.log(`🐍 Make sure Python API is running on ${PYTHON_API_URL}`);
    console.log(`📱 Open your browser and navigate to the URL above to view the app`);
});

module.exports = app;
