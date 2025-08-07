import React, { useState, useRef, useEffect } from 'react';
import { Send, TrendingUp, TrendingDown, Minus, ChevronDown, ChevronUp, Moon, Sun } from 'lucide-react';
import MarketPulseChat from './components/MarketPulseChat';
import './App.css';

function App() {
  const [isDark, setIsDark] = useState(false);

  return (
    <div className={`App ${isDark ? 'dark' : 'light'}`}>
      <header className="app-header">
        <div className="header-content">
          <h1>
            <TrendingUp className="logo-icon" />
            MarketPulse
          </h1>
          <p>AI-Powered Stock Sentiment Analysis</p>
          <button 
            className="theme-toggle"
            onClick={() => setIsDark(!isDark)}
            aria-label="Toggle theme"
          >
            {isDark ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </div>
      </header>
      
      <main className="app-main">
        <MarketPulseChat isDark={isDark} />
      </main>
      
      <footer className="app-footer">
        <p>Created by Yug Inamdar. Powered by Claude Code.</p>
      </footer>
    </div>
  );
}

export default App;