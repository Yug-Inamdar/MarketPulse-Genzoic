import React, { useState, useRef, useEffect } from 'react';
import { Send, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';
import axios from 'axios';
import TickerAutocomplete from './TickerAutocomplete';
import JsonViewer from './JsonViewer';

const MarketPulseChat = ({ isDark }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      text: 'Welcome to MarketPulse! 👋 Enter a stock ticker (like AAPL, MSFT, or GOOGL) to get AI-powered market sentiment analysis.',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const ticker = inputValue.trim().toUpperCase();
    
    if (!ticker || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: ticker,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // Add loading message
    const loadingMessage = {
      id: Date.now() + 1,
      type: 'assistant',
      text: null,
      loading: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, loadingMessage]);

    try {
      // Call the backend API
      const response = await axios.get(`/api/v1/market-pulse`, {
        params: { ticker },
        timeout: 30000
      });

      // Remove loading message and add result
      setMessages(prev => {
        const filtered = prev.filter(msg => !msg.loading);
        return [
          ...filtered,
          {
            id: Date.now() + 2,
            type: 'assistant',
            text: null,
            pulseData: response.data,
            timestamp: new Date()
          }
        ];
      });

    } catch (error) {
      // Remove loading message and add error
      setMessages(prev => {
        const filtered = prev.filter(msg => !msg.loading);
        return [
          ...filtered,
          {
            id: Date.now() + 3,
            type: 'assistant',
            text: `Sorry, I couldn't analyze ${ticker}. ${error.response?.data?.detail || error.message || 'Please check if the backend server is running and try again.'}`,
            error: true,
            timestamp: new Date()
          }
        ];
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const PulseCard = ({ data, isDark }) => {
    
    const getPulseIcon = (pulse) => {
      switch (pulse) {
        case 'bullish':
          return <TrendingUp size={20} />;
        case 'bearish':
          return <TrendingDown size={20} />;
        default:
          return <Minus size={20} />;
      }
    };

    const formatMomentumScore = (score) => {
      if (score > 0) return 'positive';
      if (score < 0) return 'negative';
      return 'neutral';
    };

    return (
      <div className="pulse-card">
        <div className="pulse-header">
          <h3 className="pulse-ticker">{data.ticker}</h3>
          <div className={`pulse-badge ${data.pulse}`}>
            {getPulseIcon(data.pulse)}
            {data.pulse}
          </div>
        </div>
        
        <p className="pulse-explanation">{data.llm_explanation}</p>
        
        <div className="momentum-info">
          <div className="momentum-text">
            <span>Momentum Score:</span>
            <span className={`momentum-score ${formatMomentumScore(data.momentum.score)}`}>
              {data.momentum.score > 0 ? '+' : ''}{data.momentum.score}%
            </span>
            <span className="momentum-details">
              (Avg of returns: {data.momentum.returns.map(r => `${r > 0 ? '+' : ''}${r}%`).join(', ')})
            </span>
          </div>
          
          {/* Price Sparkline Chart */}
          <div className="price-sparkline">
            <span className="sparkline-label">Last 5 Days:</span>
            <div className="sparkline-container">
              <ResponsiveContainer width="100%" height={40}>
                <LineChart data={data.momentum.returns.map((ret, idx) => ({ 
                  day: idx + 1, 
                  return: ret,
                  price: 100 * (1 + ret / 100) // Mock cumulative price for visualization
                }))}>
                  <Line 
                    type="monotone" 
                    dataKey="return" 
                    stroke={data.momentum.score > 0 ? "#10b981" : data.momentum.score < 0 ? "#ef4444" : "#f59e0b"}
                    strokeWidth={2}
                    dot={false}
                    activeDot={{ r: 3 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <JsonViewer 
          data={data} 
          isDark={isDark} 
          title="API Response Data"
        />
      </div>
    );
  };

  const MessageBubble = ({ message }) => {
    if (message.loading) {
      return (
        <div className="message assistant">
          <div className="message-bubble">
            <div className="loading-message">
              <div className="loading-spinner"></div>
              <span>Analyzing market data...</span>
            </div>
          </div>
        </div>
      );
    }

    if (message.pulseData) {
      return (
        <div className="message assistant">
          <div className="message-bubble" style={{ maxWidth: '90%' }}>
            <PulseCard data={message.pulseData} isDark={isDark} />
          </div>
        </div>
      );
    }

    return (
      <div className={`message ${message.type}`}>
        <div className={`message-bubble ${message.error ? 'error-message' : ''}`}>
          {message.text}
        </div>
      </div>
    );
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="chat-input-container">
        <form onSubmit={handleSubmit} className="chat-input-form">
          <TickerAutocomplete
            value={inputValue}
            onChange={setInputValue}
            onSubmit={handleSubmit}
            disabled={isLoading}
            placeholder="Type to search stocks (e.g., Apple, MSFT, Tesla, Google...)"
          />
          <button 
            type="submit" 
            className="send-button"
            disabled={isLoading || !inputValue.trim()}
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default MarketPulseChat;