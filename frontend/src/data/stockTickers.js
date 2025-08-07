// Comprehensive stock ticker database for autocomplete
export const stockTickers = [
  // Major Tech Companies
  { symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology' },
  { symbol: 'MSFT', name: 'Microsoft Corporation', sector: 'Technology' },
  { symbol: 'GOOGL', name: 'Alphabet Inc. (Class A)', sector: 'Technology' },
  { symbol: 'GOOG', name: 'Alphabet Inc. (Class C)', sector: 'Technology' },
  { symbol: 'AMZN', name: 'Amazon.com Inc.', sector: 'E-commerce' },
  { symbol: 'META', name: 'Meta Platforms Inc.', sector: 'Social Media' },
  { symbol: 'TSLA', name: 'Tesla Inc.', sector: 'Automotive' },
  { symbol: 'NVDA', name: 'NVIDIA Corporation', sector: 'Semiconductors' },
  { symbol: 'NFLX', name: 'Netflix Inc.', sector: 'Streaming' },
  { symbol: 'AMD', name: 'Advanced Micro Devices Inc.', sector: 'Semiconductors' },
  { symbol: 'INTC', name: 'Intel Corporation', sector: 'Semiconductors' },
  { symbol: 'CRM', name: 'Salesforce Inc.', sector: 'Software' },
  { symbol: 'ORCL', name: 'Oracle Corporation', sector: 'Software' },
  { symbol: 'ADBE', name: 'Adobe Inc.', sector: 'Software' },
  { symbol: 'NOW', name: 'ServiceNow Inc.', sector: 'Software' },

  // Financial Services
  { symbol: 'JPM', name: 'JPMorgan Chase & Co.', sector: 'Banking' },
  { symbol: 'BAC', name: 'Bank of America Corporation', sector: 'Banking' },
  { symbol: 'WFC', name: 'Wells Fargo & Company', sector: 'Banking' },
  { symbol: 'GS', name: 'Goldman Sachs Group Inc.', sector: 'Investment Banking' },
  { symbol: 'MS', name: 'Morgan Stanley', sector: 'Investment Banking' },
  { symbol: 'V', name: 'Visa Inc.', sector: 'Financial Services' },
  { symbol: 'MA', name: 'Mastercard Incorporated', sector: 'Financial Services' },
  { symbol: 'AXP', name: 'American Express Company', sector: 'Financial Services' },
  { symbol: 'BRK.A', name: 'Berkshire Hathaway Inc. (Class A)', sector: 'Conglomerate' },
  { symbol: 'BRK.B', name: 'Berkshire Hathaway Inc. (Class B)', sector: 'Conglomerate' },

  // Healthcare & Pharmaceuticals
  { symbol: 'JNJ', name: 'Johnson & Johnson', sector: 'Pharmaceuticals' },
  { symbol: 'PFE', name: 'Pfizer Inc.', sector: 'Pharmaceuticals' },
  { symbol: 'MRNA', name: 'Moderna Inc.', sector: 'Biotechnology' },
  { symbol: 'UNH', name: 'UnitedHealth Group Incorporated', sector: 'Healthcare' },
  { symbol: 'CVS', name: 'CVS Health Corporation', sector: 'Healthcare' },
  { symbol: 'ABBV', name: 'AbbVie Inc.', sector: 'Pharmaceuticals' },
  { symbol: 'TMO', name: 'Thermo Fisher Scientific Inc.', sector: 'Healthcare' },

  // Consumer & Retail
  { symbol: 'WMT', name: 'Walmart Inc.', sector: 'Retail' },
  { symbol: 'HD', name: 'Home Depot Inc.', sector: 'Retail' },
  { symbol: 'PG', name: 'Procter & Gamble Company', sector: 'Consumer Goods' },
  { symbol: 'KO', name: 'Coca-Cola Company', sector: 'Beverages' },
  { symbol: 'PEP', name: 'PepsiCo Inc.', sector: 'Beverages' },
  { symbol: 'NKE', name: 'Nike Inc.', sector: 'Apparel' },
  { symbol: 'COST', name: 'Costco Wholesale Corporation', sector: 'Retail' },
  { symbol: 'SBUX', name: 'Starbucks Corporation', sector: 'Food & Beverage' },
  { symbol: 'MCD', name: 'McDonald\'s Corporation', sector: 'Food & Beverage' },

  // Energy & Utilities
  { symbol: 'XOM', name: 'Exxon Mobil Corporation', sector: 'Energy' },
  { symbol: 'CVX', name: 'Chevron Corporation', sector: 'Energy' },
  { symbol: 'NEE', name: 'NextEra Energy Inc.', sector: 'Utilities' },

  // Industrial & Manufacturing
  { symbol: 'BA', name: 'Boeing Company', sector: 'Aerospace' },
  { symbol: 'CAT', name: 'Caterpillar Inc.', sector: 'Manufacturing' },
  { symbol: 'GE', name: 'General Electric Company', sector: 'Conglomerate' },
  { symbol: 'MMM', name: '3M Company', sector: 'Manufacturing' },

  // Communications & Media
  { symbol: 'DIS', name: 'Walt Disney Company', sector: 'Entertainment' },
  { symbol: 'VZ', name: 'Verizon Communications Inc.', sector: 'Telecommunications' },
  { symbol: 'T', name: 'AT&T Inc.', sector: 'Telecommunications' },
  { symbol: 'CMCSA', name: 'Comcast Corporation', sector: 'Media' },

  // International & ETFs
  { symbol: 'BABA', name: 'Alibaba Group Holding Limited', sector: 'E-commerce' },
  { symbol: 'TSM', name: 'Taiwan Semiconductor Manufacturing', sector: 'Semiconductors' },
  { symbol: 'NVO', name: 'Novo Nordisk A/S', sector: 'Pharmaceuticals' },
  { symbol: 'ASML', name: 'ASML Holding N.V.', sector: 'Semiconductors' },
  
  // Popular ETFs
  { symbol: 'SPY', name: 'SPDR S&P 500 ETF Trust', sector: 'ETF' },
  { symbol: 'QQQ', name: 'Invesco QQQ Trust', sector: 'ETF' },
  { symbol: 'VTI', name: 'Vanguard Total Stock Market ETF', sector: 'ETF' },
  { symbol: 'IWM', name: 'iShares Russell 2000 ETF', sector: 'ETF' },

  // Popular Meme/Growth Stocks
  { symbol: 'GME', name: 'GameStop Corp.', sector: 'Retail' },
  { symbol: 'AMC', name: 'AMC Entertainment Holdings Inc.', sector: 'Entertainment' },
  { symbol: 'RIVN', name: 'Rivian Automotive Inc.', sector: 'Automotive' },
  { symbol: 'LCID', name: 'Lucid Group Inc.', sector: 'Automotive' },
  { symbol: 'PLTR', name: 'Palantir Technologies Inc.', sector: 'Software' },
  { symbol: 'COIN', name: 'Coinbase Global Inc.', sector: 'Cryptocurrency' },

  // Emerging Growth
  { symbol: 'SHOP', name: 'Shopify Inc.', sector: 'E-commerce' },
  { symbol: 'SQ', name: 'Block Inc.', sector: 'Financial Technology' },
  { symbol: 'PYPL', name: 'PayPal Holdings Inc.', sector: 'Financial Technology' },
  { symbol: 'ZM', name: 'Zoom Video Communications Inc.', sector: 'Software' },
  { symbol: 'ROKU', name: 'Roku Inc.', sector: 'Streaming' },
  { symbol: 'SPOT', name: 'Spotify Technology S.A.', sector: 'Music Streaming' },
];

// Additional search terms and aliases
export const searchAliases = {
  'apple': 'AAPL',
  'microsoft': 'MSFT',
  'google': 'GOOGL',
  'alphabet': 'GOOGL',
  'amazon': 'AMZN',
  'tesla': 'TSLA',
  'facebook': 'META',
  'meta': 'META',
  'netflix': 'NFLX',
  'nvidia': 'NVDA',
  'intel': 'INTC',
  'amd': 'AMD',
  'disney': 'DIS',
  'walmart': 'WMT',
  'mcdonalds': 'MCD',
  'starbucks': 'SBUX',
  'boeing': 'BA',
  'coca cola': 'KO',
  'pepsi': 'PEP',
  'nike': 'NKE',
  'visa': 'V',
  'mastercard': 'MA',
  'jpmorgan': 'JPM',
  'goldman': 'GS',
  'berkshire': 'BRK.B',
  'johnson': 'JNJ',
  'pfizer': 'PFE',
  'moderna': 'MRNA',
  'alibaba': 'BABA',
  'gamestop': 'GME',
  'coinbase': 'COIN',
  'paypal': 'PYPL',
  'zoom': 'ZM',
  'spotify': 'SPOT',
  'shopify': 'SHOP',
};

export default stockTickers;