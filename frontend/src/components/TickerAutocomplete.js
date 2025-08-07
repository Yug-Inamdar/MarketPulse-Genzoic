import React, { useState, useRef, useEffect } from 'react';
import { Search, TrendingUp, Building2 } from 'lucide-react';
import Fuse from 'fuse.js';
import { stockTickers, searchAliases } from '../data/stockTickers';

const TickerAutocomplete = ({ value, onChange, onSubmit, disabled, placeholder }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filteredResults, setFilteredResults] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const inputRef = useRef(null);
  const dropdownRef = useRef(null);

  // Configure Fuse.js for fuzzy search
  const fuse = new Fuse(stockTickers, {
    keys: [
      { name: 'symbol', weight: 0.4 },
      { name: 'name', weight: 0.3 },
      { name: 'sector', weight: 0.1 }
    ],
    threshold: 0.4, // How fuzzy the search should be (0 = exact, 1 = very fuzzy)
    includeScore: true,
    minMatchCharLength: 1,
    ignoreLocation: true
  });

  // Search function
  const searchTickers = (query) => {
    console.log('Searching for:', query); // Debug log
    if (!query || query.length < 1) {
      setFilteredResults([]);
      setIsOpen(false);
      return;
    }

    const queryLower = query.toLowerCase().trim();
    
    // Check for direct alias match first
    if (searchAliases[queryLower]) {
      const aliasResult = stockTickers.find(stock => stock.symbol === searchAliases[queryLower]);
      if (aliasResult) {
        setFilteredResults([{ item: aliasResult, score: 0 }]);
        return;
      }
    }

    // Perform fuzzy search
    const results = fuse.search(query);
    
    // Also search for partial symbol matches (high priority)
    const symbolMatches = stockTickers.filter(stock => 
      stock.symbol.toLowerCase().includes(queryLower)
    ).map(item => ({ item, score: 0.1 }));

    // Combine and deduplicate results
    const combined = [...symbolMatches, ...results];
    const seen = new Set();
    const deduped = combined.filter(result => {
      if (seen.has(result.item.symbol)) return false;
      seen.add(result.item.symbol);
      return true;
    });

    // Sort by score and limit results
    deduped.sort((a, b) => a.score - b.score);
    const finalResults = deduped.slice(0, 8);
    setFilteredResults(finalResults);
    console.log('Found results:', finalResults.length); // Debug log
  };

  // Handle input changes
  const handleInputChange = (e) => {
    const newValue = e.target.value.toUpperCase();
    onChange(newValue);
    searchTickers(newValue);
    setSelectedIndex(-1);
    
    if (newValue.length > 0) {
      setIsOpen(true);
      console.log('Setting dropdown open:', true); // Debug log
    } else {
      setIsOpen(false);
      console.log('Setting dropdown open:', false); // Debug log
    }
  };

  // Handle selection from dropdown
  const handleSelect = (ticker) => {
    onChange(ticker.symbol);
    setIsOpen(false);
    setSelectedIndex(-1);
    setFilteredResults([]);
    inputRef.current?.focus();
  };

  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    if (!isOpen || filteredResults.length === 0) {
      if (e.key === 'Enter') {
        e.preventDefault();
        onSubmit(e);
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => 
          prev < filteredResults.length - 1 ? prev + 1 : prev
        );
        break;
      
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => prev > 0 ? prev - 1 : prev);
        break;
      
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && selectedIndex < filteredResults.length) {
          handleSelect(filteredResults[selectedIndex].item);
        } else {
          onSubmit(e);
        }
        break;
      
      case 'Escape':
        setIsOpen(false);
        setSelectedIndex(-1);
        inputRef.current?.blur();
        break;
      
      default:
        break;
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        dropdownRef.current && 
        !dropdownRef.current.contains(event.target) &&
        !inputRef.current?.contains(event.target)
      ) {
        setIsOpen(false);
        setSelectedIndex(-1);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Get sector icon
  const getSectorIcon = (sector) => {
    if (sector.toLowerCase().includes('tech')) return <TrendingUp size={14} />;
    if (sector.toLowerCase().includes('financial')) return <Building2 size={14} />;
    return <Building2 size={14} />;
  };

  // Highlight matching text
  const highlightMatch = (text, query) => {
    if (!query) return text;
    
    const regex = new RegExp(`(${query})`, 'gi');
    const parts = text.split(regex);
    
    return parts.map((part, index) => 
      part.toLowerCase() === query.toLowerCase() ? 
        <mark key={index} className="highlight-match">{part}</mark> : part
    );
  };

  return (
    <div className="ticker-autocomplete">
      <div className="input-container">
        <Search className="search-icon" size={20} />
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={() => {
            if (value.length > 0) {
              searchTickers(value);
              setIsOpen(true);
            }
          }}
          placeholder={placeholder || "Enter ticker symbol (e.g., AAPL, Apple, Microsoft...)"}
          className="ticker-input"
          disabled={disabled}
          maxLength={10}
          autoComplete="off"
          spellCheck="false"
        />
      </div>

      {isOpen && filteredResults.length > 0 && (
        <div 
          ref={dropdownRef} 
          className="dropdown"
          style={{
            position: 'absolute',
            bottom: '100%',
            left: 0,
            right: 0,
            zIndex: 9999,
            backgroundColor: 'var(--bg-primary)',
            border: '2px solid var(--accent)',
            borderRadius: '12px',
            marginBottom: '0.5rem'
          }}
        >
          {console.log('Rendering dropdown with', filteredResults.length, 'results')}
          <div className="dropdown-header">
            <span className="results-count">
              {filteredResults.length} result{filteredResults.length !== 1 ? 's' : ''}
            </span>
          </div>
          <ul className="dropdown-list">
            {filteredResults.map((result, index) => (
              <li
                key={result.item.symbol}
                className={`dropdown-item ${index === selectedIndex ? 'selected' : ''}`}
                onClick={() => handleSelect(result.item)}
                onMouseEnter={() => setSelectedIndex(index)}
              >
                <div className="item-main">
                  <div className="item-symbol">
                    {highlightMatch(result.item.symbol, value)}
                  </div>
                  <div className="item-name">
                    {highlightMatch(result.item.name, value)}
                  </div>
                </div>
                <div className="item-sector">
                  {getSectorIcon(result.item.sector)}
                  <span>{result.item.sector}</span>
                </div>
              </li>
            ))}
          </ul>
          
          <div className="dropdown-footer">
            <span className="tip">
              Use ↑↓ arrow keys to navigate, Enter to select
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default TickerAutocomplete;