import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark, oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { 
  ChevronDown, 
  ChevronUp, 
  Copy, 
  Check, 
  Code2, 
  Download,
  Eye,
  EyeOff 
} from 'lucide-react';

const JsonViewer = ({ data, isDark, title = "Raw JSON Response" }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [copied, setCopied] = useState(false);
  const [viewMode, setViewMode] = useState('formatted'); // 'formatted' or 'tree'
  const [expandedSections, setExpandedSections] = useState({
    '0-momentum': true,  // Expand momentum by default
    '0-news': false,     // Keep news collapsed initially
  });

  const jsonString = JSON.stringify(data, null, 2);

  // Copy to clipboard
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(jsonString);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  // Download as JSON file
  const handleDownload = () => {
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `market-pulse-${data.ticker}-${data.as_of}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Toggle expanded sections in tree view
  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Tree view component for better organization
  const TreeView = ({ data }) => {
    const renderValue = (key, value, level = 0) => {
      const isExpanded = expandedSections[`${level}-${key}`];
      
      if (typeof value === 'object' && value !== null) {
        if (Array.isArray(value)) {
          return (
            <div key={key} className={`tree-item level-${level}`}>
              <div 
                className="tree-header array"
                onClick={() => toggleSection(`${level}-${key}`)}
              >
                {isExpanded ? <ChevronDown size={14} /> : <ChevronDown size={14} className="rotated" />}
                <span className="key">{key}</span>
                <span className="type">Array ({value.length} items)</span>
              </div>
              {isExpanded && (
                <div className="tree-content">
                  {value.map((item, index) => 
                    renderValue(`[${index}]`, item, level + 1)
                  )}
                </div>
              )}
            </div>
          );
        } else {
          const keys = Object.keys(value);
          return (
            <div key={key} className={`tree-item level-${level}`}>
              <div 
                className="tree-header object"
                onClick={() => toggleSection(`${level}-${key}`)}
              >
                {isExpanded ? <ChevronDown size={14} /> : <ChevronDown size={14} className="rotated" />}
                <span className="key">{key}</span>
                <span className="type">Object ({keys.length} properties)</span>
              </div>
              {isExpanded && (
                <div className="tree-content">
                  {keys.map(k => renderValue(k, value[k], level + 1))}
                </div>
              )}
            </div>
          );
        }
      }

      // Primitive values
      const getValueClass = (val) => {
        if (typeof val === 'string') return 'string';
        if (typeof val === 'number') return 'number';
        if (typeof val === 'boolean') return 'boolean';
        if (val === null) return 'null';
        return '';
      };

      return (
        <div key={key} className={`tree-item level-${level} leaf`}>
          <span className="key">{key}</span>
          <span className={`value ${getValueClass(value)}`}>
            {typeof value === 'string' ? `"${value}"` : String(value)}
          </span>
        </div>
      );
    };

    return (
      <div className="tree-view">
        {Object.keys(data).map(key => renderValue(key, data[key]))}
      </div>
    );
  };

  if (!isExpanded) {
    return (
      <div className="json-section compact">
        <button 
          className="json-toggle compact"
          onClick={() => setIsExpanded(true)}
        >
          <Code2 size={16} />
          <span>View {title}</span>
          <ChevronDown size={16} />
        </button>
      </div>
    );
  }

  return (
    <div className="json-section expanded">
      <div className="json-header">
        <div className="json-title">
          <Code2 size={16} />
          <span>{title}</span>
        </div>
        
        <div className="json-controls">
          <div className="view-mode-toggle">
            <button 
              className={`mode-btn ${viewMode === 'formatted' ? 'active' : ''}`}
              onClick={() => setViewMode('formatted')}
              title="Formatted JSON"
            >
              <Code2 size={14} />
            </button>
            <button 
              className={`mode-btn ${viewMode === 'tree' ? 'active' : ''}`}
              onClick={() => setViewMode('tree')}
              title="Tree View"
            >
              {viewMode === 'tree' ? <Eye size={14} /> : <EyeOff size={14} />}
            </button>
          </div>
          
          <button 
            className="json-action"
            onClick={handleCopy}
            title="Copy to clipboard"
          >
            {copied ? <Check size={14} /> : <Copy size={14} />}
          </button>
          
          <button 
            className="json-action"
            onClick={handleDownload}
            title="Download JSON"
          >
            <Download size={14} />
          </button>
          
          <button 
            className="json-toggle"
            onClick={() => setIsExpanded(false)}
            title="Collapse"
          >
            <ChevronUp size={16} />
          </button>
        </div>
      </div>

      <div className="json-content">
        {viewMode === 'formatted' ? (
          <SyntaxHighlighter
            language="json"
            style={isDark ? oneDark : oneLight}
            customStyle={{
              margin: 0,
              borderRadius: '8px',
              fontSize: '0.85rem',
              lineHeight: '1.4'
            }}
            showLineNumbers={true}
            lineNumberStyle={{
              minWidth: '3em',
              paddingRight: '1em',
              color: isDark ? '#6B7280' : '#9CA3AF',
              borderRight: `1px solid ${isDark ? '#374151' : '#E5E7EB'}`,
              marginRight: '1em'
            }}
            wrapLines={true}
            wrapLongLines={true}
          >
            {jsonString}
          </SyntaxHighlighter>
        ) : (
          <div className="tree-container">
            <TreeView data={data} />
          </div>
        )}
      </div>

      <div className="json-footer">
        <div className="json-stats">
          <span>Size: {(new Blob([jsonString]).size / 1024).toFixed(1)} KB</span>
          <span>•</span>
          <span>Lines: {jsonString.split('\n').length}</span>
          <span>•</span>
          <span>Generated: {data.as_of}</span>
        </div>
        
        {copied && (
          <div className="copy-notification">
            <Check size={12} />
            Copied to clipboard!
          </div>
        )}
      </div>
    </div>
  );
};

export default JsonViewer;