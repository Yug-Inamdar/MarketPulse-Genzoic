# MarketPulse - AI-Powered Stock Sentiment Analysis

> **Genzoic Coding Assessment Solution** - 4-hour MVP Challenge

A microservice that answers: *"Is TICKER looking bullish, bearish, or neutral for tomorrow, and why?"*

Built with FastAPI backend, React frontend, and AI-powered analysis using real market data and news sentiment.

## 🎯 Assignment Requirements Met

✅ **Two Raw Signals**: Price momentum (last 5 trading days) + News feed (5 latest headlines)  
✅ **LLM Integration**: Google Gemini API for pulse analysis with contextual explanations  
✅ **REST Endpoint**: `GET /api/v1/market-pulse?ticker=MSFT`  
✅ **React Frontend**: Chat-style interface with JSON response viewer  
✅ **Docker Support**: Slim, non-root containers with health checks  
✅ **K8s Manifests**: Production-ready deployment and service configs  

### 🧪 Quick Test
```bash
# Test the API directly
curl -X GET "http://localhost:8000/api/v1/market-pulse?ticker=AAPL" \
     -H "Accept: application/json"

# Expected response format:
{
  "ticker": "AAPL",
  "as_of": "2025-01-07", 
  "momentum": { "returns": [0.5, -1.2, 2.1, -0.8, 1.4], "score": 0.40 },
  "news": [{"title": "Apple announces...", "description": "...", "url": "..."}],
  "pulse": "bullish",
  "llm_explanation": "Strong momentum with positive sentiment..."
}
```

## 🚀 Features

### Backend (FastAPI)
- **Real-time Stock Analysis**: Fetches last 5 trading days of price data and calculates momentum scores
- **News Sentiment Integration**: Aggregates latest headlines from multiple news sources
- **AI-Powered Insights**: Uses Google Gemini LLM for intelligent market pulse analysis
- **High Performance**: Async FastAPI backend with TTL caching (10+ minutes)
- **Robust Fallbacks**: Works with mock data when APIs are unavailable
- **Production Ready**: Docker support, error handling, and comprehensive logging

### Frontend (React)
- **Chat-Style Interface**: Clean, intuitive UI for entering stock tickers
- **Real-time Analysis**: Instant API calls with loading states and error handling
- **Beautiful Pulse Cards**: Visually appealing display of sentiment analysis
- **Collapsible JSON**: Raw API response viewer for detailed inspection
- **Price Sparklines**: Interactive Recharts visualization of 5-day returns
- **Dark/Light Theme**: Toggle between themes for better user experience
- **Responsive Design**: Works on desktop and mobile devices

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [API Specification](#-api-specification)
- [Setup Instructions](#-setup-instructions)
- [Environment Variables](#-environment-variables)
- [Design Trade-offs](#-design-trade-offs)
- [Architecture](#-architecture)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Next Steps](#-next-steps)

## ⚡ Quick Start

### Option 1: Full Stack (Recommended)
```bash
# Start both backend and frontend automatically
start_full_stack.bat

# Then open http://localhost:3000 for the UI
```

### Option 2: Backend Only
```bash
# 1. Install dependencies and start backend
cd D:\Genzoic\MarketPulse-Genzoic
pip install -r requirements.txt
python run_server.py

# 2. Test the API
python test_backend.py

# 3. View API documentation at http://localhost:8000/docs
```

### Option 3: Frontend Only (after backend is running)
```bash
# Start React frontend
cd frontend
npm install
npm start

# Open http://localhost:3000
```

## 📡 API Specification

### Base URL
```
http://localhost:8000
```

### Endpoints

#### `GET /api/v1/market-pulse`
Analyze market sentiment for a given stock ticker.

**Query Parameters:**
- `ticker` (required): Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)

**Response Format:**
```json
{
  "ticker": "MSFT",
  "as_of": "2025-01-07",
  "momentum": {
    "returns": [-0.3, 0.4, 1.1, -0.2, 0.7],
    "score": 0.34
  },
  "news": [
    {
      "title": "Microsoft unveils AI chips",
      "description": "Microsoft announced new AI acceleration...",
      "url": "https://example.com/news/msft-ai"
    }
  ],
  "pulse": "bullish",
  "llm_explanation": "Momentum is moderately positive (0.34%) and recent headlines highlight strong product launches and earnings beats; hence bullish outlook."
}
```

#### `GET /api/v1/health`
Health check endpoint with service status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-07T10:30:00",
  "services": {
    "stock_api": "configured",
    "news_api": "configured", 
    "llm_api": "configured"
  },
  "cache_size": 5
}
```

#### `GET /`
Root endpoint for basic health check.

## 🛠 Setup Instructions

### Prerequisites
- Python 3.8+
- Internet connection for API calls

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration (Optional)**
   ```bash
   # Copy example environment file
   copy .env.example .env
   
   # Edit .env with your API keys (app works with mock data if no keys provided)
   notepad .env
   ```

3. **Start the Server**
   ```bash
   # Option 1: Using startup script (recommended)
   python run_server.py
   
   # Option 2: Direct uvicorn command
   cd src\backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Verify Installation**
   ```bash
   # Test health check
   curl http://localhost:8000/api/v1/health
   
   # Test market pulse
   curl "http://localhost:8000/api/v1/market-pulse?ticker=AAPL"
   ```

## 🔑 Environment Variables

All environment variables are optional. The application provides mock data fallbacks.

```env
# Stock Price APIs (choose one)
FINNHUB_API_KEY=your_finnhub_key        # Free: https://finnhub.io
ALPHA_VANTAGE_API_KEY=your_av_key       # Free: https://alphavantage.co

# News APIs (choose one)
GNEWS_API_KEY=your_gnews_key            # Free: https://gnews.io  
NEWS_API_KEY=your_newsapi_key           # Free: https://newsapi.org

# LLM API
GEMINI_API_KEY=your_gemini_key          # Free: https://makersuite.google.com
```

### Getting API Keys (5 minutes total)

1. **Stock Data** - Choose one:
   - [Finnhub](https://finnhub.io) - Sign up → API Key (60 calls/minute free)
   - [Alpha Vantage](https://alphavantage.co) - Sign up → API Key (5 calls/minute free)

2. **News Data** - Choose one:
   - [GNews](https://gnews.io) - Sign up → API Key (100 requests/day free)
   - [NewsAPI](https://newsapi.org) - Sign up → API Key (1000 requests/day free)

3. **AI Analysis**:
   - [Google AI Studio](https://makersuite.google.com) - Sign up → Create API Key (free tier)

## ⚖️ Design Trade-offs

### Momentum Calculation
**Choice**: Simple average of last 4 daily returns  
**Rationale**: 
- ✅ Easy to understand and implement
- ✅ Provides clear directional signal
- ✅ Fast computation
- ❌ Doesn't account for volatility or volume
- **Alternative**: Could use RSI, MACD, or weighted moving averages

### Caching Strategy
**Choice**: In-memory TTL cache (10 minutes)  
**Rationale**:
- ✅ Reduces API costs and improves response times
- ✅ Appropriate for demo/prototype phase
- ❌ Lost on server restart
- **Production**: Would use Redis or database-backed cache

### API Integration
**Choice**: Multiple provider support with graceful fallbacks  
**Rationale**:
- ✅ Resilient to API outages
- ✅ Easy to demo without API keys
- ✅ Cost optimization (choose cheapest provider)
- ❌ Slightly more complex code
- **Alternative**: Single provider with better error handling

### LLM Prompting
**Choice**: Structured prompt with explicit format requirements  
**Rationale**:
- ✅ Consistent response parsing
- ✅ Combines multiple data sources effectively
- ✅ Easy to modify prompt for better results
- ❌ Dependent on LLM following instructions
- **Alternative**: Fine-tuned model or more complex parsing

## 🏗 Architecture

```
MarketPulse-Genzoic/
├── src/backend/
│   └── main.py              # FastAPI application with all services
├── requirements.txt         # Python dependencies
├── run_server.py           # Server startup script
├── .env.example            # Environment variables template
├── SETUP.md                # Quick setup guide
└── README.md               # This file

Services Architecture:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   StockDataService  │    │   NewsService    │    │   LLMService     │
│   - Finnhub         │    │   - GNews        │    │   - Gemini       │
│   - Alpha Vantage   │    │   - NewsAPI      │    │   - Fallback     │
│   - Mock fallback   │    │   - Mock fallback│    │                  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   FastAPI        │
                    │   - TTL Cache    │
                    │   - Error Handle │
                    │   - CORS         │
                    └─────────────────┘
```

### Key Components

1. **FastAPI Application**: Async web framework with automatic API documentation
2. **StockDataService**: Handles price data fetching with multiple provider support
3. **NewsService**: Aggregates news from various sources with fallback
4. **MomentumCalculator**: Computes simple momentum scores from price returns
5. **LLMService**: Interfaces with Gemini API for intelligent analysis
6. **TTLCache**: In-memory caching with 10-minute expiration

## 🧪 Testing

### Manual Testing
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Test various tickers
curl "http://localhost:8000/api/v1/market-pulse?ticker=AAPL"
curl "http://localhost:8000/api/v1/market-pulse?ticker=MSFT"
curl "http://localhost:8000/api/v1/market-pulse?ticker=GOOGL"

# Test error handling
curl "http://localhost:8000/api/v1/market-pulse?ticker=INVALID"
```

### Sample curl Command
```bash
curl -X GET "http://localhost:8000/api/v1/market-pulse?ticker=MSFT" \
     -H "Accept: application/json"
```

### Expected Response Time
- **First request**: ~2-3 seconds (API calls)
- **Cached requests**: ~50ms (cache hit)

## 🐳 Deployment

### Local Development
```bash
python run_server.py
```

### Docker Deployment
```bash
# Option 1: Quick start (backend only)
docker-start.bat

# Option 2: Full stack with docker-compose
docker-compose-start.bat

# Option 3: Manual build and run
docker build -t marketpulse-backend .
docker run -d -p 8000:8000 --env-file .env marketpulse-backend
```

### Kubernetes Deployment
```bash
# 1. Create namespace (optional)
kubectl create namespace marketpulse

# 2. Apply secrets (optional - app works with mock data)
# Edit k8s/secrets-template.yaml with base64 encoded API keys
kubectl apply -f k8s/secrets-template.yaml -n marketpulse

# 3. Deploy the application  
kubectl apply -f k8s/deployment.yaml -n marketpulse
kubectl apply -f k8s/service.yaml -n marketpulse

# 4. Check deployment status
kubectl get pods -n marketpulse
kubectl get services -n marketpulse

# 5. Access via NodePort (development)
kubectl get nodes -o wide  # Get node IP
# Access via: http://<NODE_IP>:30080

# 6. Port forward (testing)
kubectl port-forward service/marketpulse-backend-service 8000:80 -n marketpulse
```

**K8s Features:**
- **High Availability**: 2 replicas with rolling updates
- **Health Checks**: Liveness and readiness probes on `/api/v1/health`
- **Resource Limits**: 512Mi memory, 500m CPU limits
- **Security**: Non-root containers, no privilege escalation
- **Secrets Management**: API keys stored in Kubernetes secrets

### Production Considerations
- Use environment-specific `.env` files
- Configure reverse proxy (nginx)
- Set up monitoring and logging
- Implement rate limiting
- Use external cache (Redis)

## 🎯 Current Status

### ✅ Completed (Phase 1 & 2 - MVP + Frontend)
- [x] **Backend Setup**: FastAPI with async endpoints
- [x] **Data Integration**: Stock prices + news fetching
- [x] **Momentum Logic**: Simple average calculation
- [x] **LLM Integration**: Gemini API with structured prompts
- [x] **Caching**: TTL cache for performance
- [x] **Error Handling**: Graceful fallbacks and mock data
- [x] **Documentation**: API specs and setup guides
- [x] **Frontend**: React chat-style interface with beautiful UI
- [x] **API Integration**: Frontend communicates with backend
- [x] **Pulse Cards**: Pretty display of sentiment analysis
- [x] **JSON Viewer**: Collapsible raw response viewer
- [x] **Theme Toggle**: Dark/light mode support
- [x] **Responsive Design**: Mobile and desktop support

### ✅ Phase 2 Complete - Production Ready
- [x] **Dockerization**: Complete Docker setup with slim, non-root images
- [x] **Docker Compose**: Full stack orchestration
- [x] **Kubernetes**: Production-ready manifests with health checks
- [x] **Security**: Non-root containers, resource limits, secrets management

### ✅ **ALL REQUIREMENTS COMPLETE**
- [x] **Testing**: Unit tests for momentum calculation
- [x] **CI/CD**: GitHub Actions workflow with lint + tests
- [x] **UI Polish**: Recharts sparklines + dark/light theme  
- [x] **Security**: Vulnerability scanning in CI/CD

### 🚧 Future Enhancements
- [ ] **Monitoring**: Prometheus metrics and dashboards
- [ ] **Advanced Analytics**: RSI, MACD, Bollinger Bands
- [ ] **Real-time Updates**: WebSocket for live data

### 📋 Next Steps

#### Phase 3: Testing & Polish (30 minutes)
1. **Backend Testing** (10 min)
   - Run: `python test_backend.py`
   - Unit tests for momentum calculation
   - Test API error handling

2. **Frontend Testing** (10 min)
   - Test different stock tickers
   - Verify error states and loading
   - Test theme toggle and responsiveness

3. **End-to-End Testing** (10 min)
   - Full stack integration testing
   - Performance testing with real APIs
   - User experience validation

#### Phase 4: Production Enhancements (30 minutes)
1. **Docker & DevOps** (15 min)
   - Dockerfile with slim, non-root image
   - docker-compose.yml for full stack
   - Basic Kubernetes manifests

2. **Testing & CI/CD** (15 min)
   - pytest for momentum functions
   - GitHub Actions workflow
   - Linting setup

#### Phase 4: Advanced Features (Optional)
- **Enhanced Analytics**: RSI, MACD, Bollinger Bands
- **Real-time Updates**: WebSocket connections
- **User Accounts**: Portfolio tracking
- **Advanced Caching**: Redis integration
- **Monitoring**: Prometheus metrics
- **Security**: Rate limiting, API authentication

## 🤝 Contributing

This is a demo project created for the Genzoic coding assessment. The implementation prioritizes:
1. **Functional MVP** over perfect architecture
2. **Clear documentation** over exhaustive features  
3. **Rapid development** over optimization

## 📞 Support

For questions or issues:
- Check the [API Documentation](http://localhost:8000/docs) when server is running
- Review the [Setup Guide](SETUP.md) for common issues
- Examine server logs for detailed error information

---

**Built with**: FastAPI, Python 3.8+, Google Gemini AI  
**Status**: Full Stack Complete ✅ | Production Ready 🚧  
**Demo Ready**: Yes | **Production Ready**: Phase 2+

## 🤖 AI Assistance Acknowledgment

This project was developed with assistance from **Claude (Anthropic)** for:
- FastAPI backend architecture and async implementation
- React component structure and modern UI patterns  
- Docker containerization and Kubernetes manifests
- LLM prompt engineering for consistent analysis
- Professional documentation and code organization

All core business logic, design decisions, and technical trade-offs reflect the developer's choices and understanding of the requirements.

## 👨‍💻 Created By

**Yug Inamdar** - Full Stack Developer  
*Powered by Claude Code*