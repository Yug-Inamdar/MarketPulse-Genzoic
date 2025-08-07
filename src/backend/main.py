from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import aiohttp
import os
from datetime import datetime, timedelta
import logging
from cachetools import TTLCache
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="MarketPulse API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TTL Cache for API responses (10 minutes)
cache = TTLCache(maxsize=100, ttl=600)

# Configure Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# Pydantic models
class NewsItem(BaseModel):
    title: str
    description: str
    url: str

class MomentumData(BaseModel):
    returns: List[float]
    score: float

class MarketPulseResponse(BaseModel):
    ticker: str
    as_of: str
    momentum: MomentumData
    news: List[NewsItem]
    pulse: str
    llm_explanation: str

class StockDataService:
    """Service for fetching stock price data"""
    
    def __init__(self):
        self.finnhub_key = os.getenv("FINNHUB_API_KEY")
    
    async def get_stock_data(self, ticker: str) -> Dict:
        """Fetch last 5 days of stock data"""
        if self.finnhub_key:
            return await self._fetch_finnhub_data(ticker)
        elif self.alpha_vantage_key:
            return await self._fetch_alpha_vantage_data(ticker)
        else:
            # Fallback to mock data for demo purposes
            return await self._get_mock_stock_data(ticker)
    
    async def _fetch_finnhub_data(self, ticker: str) -> Dict:
        """Fetch data from Finnhub API"""
        try:
            # Calculate date range (last 10 days to ensure we get 5 trading days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=10)
            
            url = "https://finnhub.io/api/v1/stock/candle"
            params = {
                "symbol": ticker,
                "resolution": "D",
                "from": int(start_date.timestamp()),
                "to": int(end_date.timestamp()),
                "token": self.finnhub_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("s") == "ok" and data.get("c"):
                            # Get last 5 closing prices
                            closes = data["c"][-5:]
                            returns = []
                            
                            # Calculate daily returns
                            for i in range(1, len(closes)):
                                daily_return = (closes[i] - closes[i-1]) / closes[i-1]
                                returns.append(round(daily_return * 100, 2))  # Convert to percentage
                            
                            return {
                                "returns": returns,
                                "prices": closes
                            }
                    
                    logger.error(f"Finnhub API error: {response.status}")
                    return await self._get_mock_stock_data(ticker)
                    
        except Exception as e:
            logger.error(f"Error fetching Finnhub data: {e}")
            return await self._get_mock_stock_data(ticker)
    
    async def _fetch_alpha_vantage_data(self, ticker: str) -> Dict:
        """Fetch data from Alpha Vantage API"""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": ticker,
                "apikey": self.alpha_vantage_key,
                "outputsize": "compact"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        time_series = data.get("Time Series (Daily)", {})
                        
                        if time_series:
                            # Get last 5 days of data
                            sorted_dates = sorted(time_series.keys(), reverse=True)[:5]
                            closes = []
                            
                            for date in reversed(sorted_dates):
                                close_price = float(time_series[date]["4. close"])
                                closes.append(close_price)
                            
                            # Calculate returns
                            returns = []
                            for i in range(1, len(closes)):
                                daily_return = (closes[i] - closes[i-1]) / closes[i-1]
                                returns.append(round(daily_return * 100, 2))
                            
                            return {
                                "returns": returns,
                                "prices": closes
                            }
                    
                    logger.error(f"Alpha Vantage API error: {response.status}")
                    return await self._get_mock_stock_data(ticker)
                    
        except Exception as e:
            logger.error(f"Error fetching Alpha Vantage data: {e}")
            return await self._get_mock_stock_data(ticker)
    
    async def _get_mock_stock_data(self, ticker: str) -> Dict:
        """Generate mock data for demo purposes"""
        import random
        
        # Generate realistic mock returns
        returns = [round(random.uniform(-3.0, 3.0), 2) for _ in range(4)]
        prices = [100.0]  # Starting price
        
        # Calculate prices from returns
        for return_pct in returns:
            new_price = prices[-1] * (1 + return_pct / 100)
            prices.append(round(new_price, 2))
        
        logger.info(f"Using mock data for ticker: {ticker}")
        return {
            "returns": returns,
            "prices": prices[1:]  # Remove starting price
        }

class NewsService:
    """Service for fetching news data"""
    
    def __init__(self):
        self.gnews_key = os.getenv("GNEWS_API_KEY")
    
    async def get_news(self, ticker: str) -> List[Dict]:
        """Fetch latest news for a ticker"""
        if self.gnews_key:
            return await self._fetch_gnews_data(ticker)
        elif self.news_api_key:
            return await self._fetch_newsapi_data(ticker)
        else:
            # Fallback to mock data
            return await self._get_mock_news_data(ticker)
    
    async def _fetch_gnews_data(self, ticker: str) -> List[Dict]:
        """Fetch data from GNews API"""
        try:
            url = "https://gnews.io/api/v4/search"
            params = {
                "q": f"{ticker} stock",
                "token": self.gnews_key,
                "lang": "en",
                "max": 5
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get("articles", [])
                        
                        return [{
                            "title": article["title"],
                            "description": article.get("description", ""),
                            "url": article["url"]
                        } for article in articles[:5]]
                    
                    logger.error(f"GNews API error: {response.status}")
                    return await self._get_mock_news_data(ticker)
                    
        except Exception as e:
            logger.error(f"Error fetching GNews data: {e}")
            return await self._get_mock_news_data(ticker)
    
    async def _fetch_newsapi_data(self, ticker: str) -> List[Dict]:
        """Fetch data from NewsAPI"""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": f"{ticker} stock OR {ticker} earnings",
                "apiKey": self.news_api_key,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 5
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get("articles", [])
                        
                        return [{
                            "title": article["title"],
                            "description": article.get("description", ""),
                            "url": article["url"]
                        } for article in articles[:5]]
                    
                    logger.error(f"NewsAPI error: {response.status}")
                    return await self._get_mock_news_data(ticker)
                    
        except Exception as e:
            logger.error(f"Error fetching NewsAPI data: {e}")
            return await self._get_mock_news_data(ticker)
    
    async def _get_mock_news_data(self, ticker: str) -> List[Dict]:
        """Generate mock news data"""
        mock_news = [
            {
                "title": f"{ticker} reports strong quarterly earnings",
                "description": f"{ticker} exceeded analyst expectations with robust revenue growth and improved margins.",
                "url": f"https://example.com/news/{ticker}-earnings"
            },
            {
                "title": f"{ticker} announces new product launch",
                "description": f"{ticker} unveils innovative technology solution targeting enterprise customers.",
                "url": f"https://example.com/news/{ticker}-product"
            },
            {
                "title": f"Analyst upgrades {ticker} rating",
                "description": f"Major investment firm raises {ticker} price target citing strong fundamentals.",
                "url": f"https://example.com/news/{ticker}-upgrade"
            },
            {
                "title": f"{ticker} CEO speaks at industry conference",
                "description": f"{ticker} leadership discusses strategic vision and market opportunities.",
                "url": f"https://example.com/news/{ticker}-conference"
            },
            {
                "title": f"{ticker} stock shows strong technical momentum",
                "description": f"Technical analysis indicates {ticker} breaking through key resistance levels.",
                "url": f"https://example.com/news/{ticker}-technical"
            }
        ]
        
        logger.info(f"Using mock news data for ticker: {ticker}")
        return mock_news[:5]

class MomentumCalculator:
    """Calculate momentum score from price returns"""
    
    @staticmethod
    def calculate_momentum_score(returns: List[float]) -> float:
        """
        Calculate simple momentum score as average of returns
        Positive score indicates bullish momentum, negative indicates bearish
        """
        if not returns:
            return 0.0
        
        # Simple average momentum score
        avg_return = sum(returns) / len(returns)
        return round(avg_return, 2)

class LLMService:
    """Service for LLM analysis"""
    
    def __init__(self):
        self.model = None
        if gemini_api_key:
            try:
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                logger.error(f"Error initializing Gemini: {e}")
    
    async def analyze_market_pulse(self, ticker: str, momentum_data: Dict, news_data: List[Dict]) -> Dict:
        """Analyze market data and return pulse with explanation"""
        
        if not self.model:
            return self._get_fallback_analysis(ticker, momentum_data, news_data)
        
        try:
            # Create prompt for LLM
            prompt = self._create_analysis_prompt(ticker, momentum_data, news_data)
            
            # Generate response
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            
            # Parse response
            return self._parse_llm_response(response.text)
            
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return self._get_fallback_analysis(ticker, momentum_data, news_data)
    
    def _create_analysis_prompt(self, ticker: str, momentum_data: Dict, news_data: List[Dict]) -> str:
        """Create enhanced, contextual prompt for LLM analysis"""
        
        returns_str = ", ".join([f"{r:+.1f}%" for r in momentum_data["returns"]])
        score = momentum_data["score"]
        
        # Analyze return patterns for more context
        positive_days = sum(1 for r in momentum_data["returns"] if r > 0)
        negative_days = len(momentum_data["returns"]) - positive_days
        volatility = max(momentum_data["returns"]) - min(momentum_data["returns"])
        
        # Extract key themes from news
        news_analysis = []
        sentiment_keywords = {
            'positive': ['beat', 'strong', 'growth', 'rise', 'gain', 'up', 'increase', 'launch', 'partnership', 'deal'],
            'negative': ['miss', 'fall', 'drop', 'decline', 'loss', 'down', 'concern', 'challenge', 'risk'],
            'neutral': ['report', 'announce', 'update', 'meeting', 'conference', 'quarter']
        }
        
        news_sentiment_score = 0
        for news in news_data[:5]:
            title_desc = (news['title'] + ' ' + news.get('description', '')).lower()
            for word in sentiment_keywords['positive']:
                if word in title_desc:
                    news_sentiment_score += 1
            for word in sentiment_keywords['negative']:
                if word in title_desc:
                    news_sentiment_score -= 1
        
        # Create detailed news summary
        for i, news in enumerate(news_data[:3], 1):
            title = news['title'][:80] + "..." if len(news['title']) > 80 else news['title']
            desc = news.get('description', '')[:100] + "..." if len(news.get('description', '')) > 100 else news.get('description', '')
            news_analysis.append(f"{i}. {title}\n   Context: {desc}")
        
        news_text = "\n".join(news_analysis)
        
        # Get company context (basic company info based on ticker)
        company_context = self._get_company_context(ticker)
        
        prompt = f"""
You are a senior financial analyst providing market sentiment analysis for {ticker} ({company_context['name']}).

TECHNICAL ANALYSIS:
- Daily returns (last 4 days): {returns_str}
- Average momentum: {score:+.2f}%
- Trading pattern: {positive_days} up days, {negative_days} down days
- Volatility range: {volatility:.1f}%
- Price trend: {'Upward' if score > 0.5 else 'Downward' if score < -0.5 else 'Sideways'}

FUNDAMENTAL CONTEXT:
- Sector: {company_context['sector']}
- Market cap: {company_context['size']}
- News sentiment score: {news_sentiment_score:+d} (positive/negative themes)

RECENT NEWS ANALYSIS:
{news_text}

MARKET CONTEXT:
Consider broader market conditions, sector performance, and company-specific factors.

Provide your analysis in this EXACT format:

PULSE: [bullish/neutral/bearish]
EXPLANATION: [Provide a nuanced, 2-3 sentence analysis that feels conversational and insightful. Reference specific patterns, news themes, and market context. Avoid generic statements.]

Guidelines:
- Be specific about WHY you reached this conclusion
- Mention concrete numbers and patterns you observed
- Consider both technical momentum AND fundamental news
- Sound like an experienced analyst, not a robot
- Make it unique to this specific ticker and situation
"""
        return prompt
    
    def _get_company_context(self, ticker: str) -> Dict[str, str]:
        """Get basic company context for better LLM analysis"""
        # This could be expanded with a real company database
        company_db = {
            'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology', 'size': 'Large Cap'},
            'MSFT': {'name': 'Microsoft Corporation', 'sector': 'Technology', 'size': 'Large Cap'},
            'GOOGL': {'name': 'Alphabet Inc.', 'sector': 'Technology', 'size': 'Large Cap'},
            'NVDA': {'name': 'NVIDIA Corporation', 'sector': 'Semiconductors', 'size': 'Large Cap'},
            'TSLA': {'name': 'Tesla Inc.', 'sector': 'Automotive/Energy', 'size': 'Large Cap'},
            'AMZN': {'name': 'Amazon.com Inc.', 'sector': 'E-commerce/Cloud', 'size': 'Large Cap'},
            'META': {'name': 'Meta Platforms Inc.', 'sector': 'Social Media', 'size': 'Large Cap'},
            'NFLX': {'name': 'Netflix Inc.', 'sector': 'Streaming/Media', 'size': 'Large Cap'},
            'AMD': {'name': 'Advanced Micro Devices', 'sector': 'Semiconductors', 'size': 'Large Cap'},
            'BABA': {'name': 'Alibaba Group', 'sector': 'E-commerce', 'size': 'Large Cap'},
        }
        
        return company_db.get(ticker, {
            'name': f'{ticker} Corporation',
            'sector': 'General Market',
            'size': 'Mid Cap'
        })
    
    def _parse_llm_response(self, response_text: str) -> Dict:
        """Parse LLM response to extract pulse and explanation"""
        try:
            lines = response_text.strip().split('\n')
            pulse = "neutral"
            explanation = "Unable to determine market pulse from available data."
            
            for line in lines:
                if line.startswith("PULSE:"):
                    pulse_text = line.replace("PULSE:", "").strip().lower()
                    if "bullish" in pulse_text:
                        pulse = "bullish"
                    elif "bearish" in pulse_text:
                        pulse = "bearish"
                    else:
                        pulse = "neutral"
                
                elif line.startswith("EXPLANATION:"):
                    explanation = line.replace("EXPLANATION:", "").strip()
            
            return {"pulse": pulse, "explanation": explanation}
            
        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            return {"pulse": "neutral", "explanation": "Analysis unavailable due to parsing error."}
    
    def _get_fallback_analysis(self, ticker: str, momentum_data: Dict, news_data: List[Dict]) -> Dict:
        """Provide enhanced fallback analysis when LLM is unavailable"""
        score = momentum_data["score"]
        returns = momentum_data["returns"]
        
        # Enhanced pattern analysis
        positive_days = sum(1 for r in returns if r > 0)
        negative_days = len(returns) - positive_days
        volatility = max(returns) - min(returns) if returns else 0
        
        # Analyze news sentiment
        news_keywords = {
            'positive': ['beat', 'strong', 'growth', 'rise', 'gain', 'up', 'increase', 'launch', 'partnership', 'deal', 'profit', 'revenue'],
            'negative': ['miss', 'fall', 'drop', 'decline', 'loss', 'down', 'concern', 'challenge', 'risk', 'cut', 'lower']
        }
        
        news_sentiment = 0
        significant_news = []
        for news in news_data[:3]:
            title_desc = (news['title'] + ' ' + news.get('description', '')).lower()
            for word in news_keywords['positive']:
                if word in title_desc:
                    news_sentiment += 1
                    if word in ['beat', 'strong', 'growth', 'launch', 'deal']:
                        significant_news.append(f"positive {word}")
            for word in news_keywords['negative']:
                if word in title_desc:
                    news_sentiment -= 1
                    if word in ['miss', 'fall', 'decline', 'concern']:
                        significant_news.append(f"negative {word}")
        
        # Get company context
        company_context = self._get_company_context(ticker)
        
        # Rule-based pulse determination with more nuance
        if score > 0.5 and news_sentiment >= 0:
            pulse = "bullish"
        elif score < -0.5 and news_sentiment <= 0:
            pulse = "bearish"
        elif abs(score) <= 0.5 and abs(news_sentiment) <= 1:
            pulse = "neutral"
        elif news_sentiment > 1:  # Strong positive news can override weak negative momentum
            pulse = "bullish"
        elif news_sentiment < -1:  # Strong negative news can override weak positive momentum
            pulse = "bearish"
        else:
            pulse = "neutral"
        
        # Generate contextual explanation
        explanations = {
            "bullish": [
                f"{ticker} shows {positive_days} up days vs {negative_days} down days with {score:+.1f}% average momentum",
                f"Technical momentum of {score:+.1f}% combined with {company_context['sector']} sector strength",
                f"Positive price action ({score:+.1f}% momentum) aligns with {len([n for n in significant_news if 'positive' in n])} favorable developments"
            ],
            "bearish": [
                f"{ticker} exhibits weakness with {negative_days} declining days and {score:+.1f}% momentum drag",
                f"Downward pressure evident from {score:+.1f}% momentum amid {company_context['sector']} headwinds",
                f"Technical indicators show {score:+.1f}% negative momentum coinciding with concerning fundamentals"
            ],
            "neutral": [
                f"{ticker} trading sideways with {score:+.1f}% momentum and mixed {positive_days}/{negative_days} day pattern",
                f"Consolidation phase for {ticker} with {score:+.1f}% momentum in the {company_context['sector']} space",
                f"Balanced outlook with {score:+.1f}% momentum offset by mixed market signals"
            ]
        }
        
        # Add volatility and news context
        vol_desc = "high" if volatility > 3 else "moderate" if volatility > 1.5 else "low"
        news_desc = "supportive" if news_sentiment > 0 else "concerning" if news_sentiment < 0 else "mixed"
        
        base_explanation = explanations[pulse][hash(ticker) % len(explanations[pulse])]
        enhanced_explanation = f"{base_explanation} with {vol_desc} volatility and {news_desc} news flow."
        
        return {"pulse": pulse, "explanation": enhanced_explanation}

# Initialize services
stock_service = StockDataService()
news_service = NewsService()
momentum_calculator = MomentumCalculator()
llm_service = LLMService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "MarketPulse API is running", "version": "1.0.0"}

@app.get("/api/v1/market-pulse", response_model=MarketPulseResponse)
async def get_market_pulse(ticker: str = Query(..., description="Stock ticker symbol (e.g., AAPL, MSFT)")):
    """
    Get market pulse analysis for a stock ticker
    
    Returns momentum analysis, news sentiment, and AI-powered pulse prediction
    """
    
    # Check cache first
    cache_key = f"pulse_{ticker.upper()}"
    if cache_key in cache:
        logger.info(f"Returning cached data for {ticker}")
        return cache[cache_key]
    
    try:
        # Validate ticker format
        ticker = ticker.upper().strip()
        if not ticker or len(ticker) > 10:
            raise HTTPException(status_code=400, detail="Invalid ticker format")
        
        logger.info(f"Fetching market pulse for {ticker}")
        
        # Fetch data concurrently
        stock_task = stock_service.get_stock_data(ticker)
        news_task = news_service.get_news(ticker)
        
        stock_data, news_data = await asyncio.gather(stock_task, news_task)
        
        # Calculate momentum score
        returns = stock_data["returns"]
        momentum_score = momentum_calculator.calculate_momentum_score(returns)
        
        # Get LLM analysis
        momentum_data = {"returns": returns, "score": momentum_score}
        analysis = await llm_service.analyze_market_pulse(ticker, momentum_data, news_data)
        
        # Build response
        response = MarketPulseResponse(
            ticker=ticker,
            as_of=datetime.now().strftime("%Y-%m-%d"),
            momentum=MomentumData(returns=returns, score=momentum_score),
            news=[NewsItem(**item) for item in news_data],
            pulse=analysis["pulse"],
            llm_explanation=analysis["explanation"]
        )
        
        # Cache the response
        cache[cache_key] = response
        
        logger.info(f"Successfully generated market pulse for {ticker}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating market pulse for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/health")
async def health_check():
    """Detailed health check with service status"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "stock_api": "configured" if stock_service.finnhub_key or stock_service.alpha_vantage_key else "mock",
            "news_api": "configured" if news_service.gnews_key or news_service.news_api_key else "mock", 
            "llm_api": "configured" if gemini_api_key else "fallback"
        },
        "cache_size": len(cache)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)