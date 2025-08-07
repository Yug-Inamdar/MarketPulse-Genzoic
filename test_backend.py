#!/usr/bin/env python3
"""
Simple test script to verify MarketPulse backend is working
"""

import requests
import json
import sys
import time

def test_backend():
    print("🧪 Testing MarketPulse Backend...")
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health check
    print("\n1️⃣ Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            health_data = response.json()
            print(f"   Status: {health_data.get('status')}")
            print(f"   Services: {health_data.get('services')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("   Make sure the server is running: python run_server.py")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Market pulse endpoint
    print("\n2️⃣ Testing market pulse endpoint...")
    test_ticker = "AAPL"
    
    try:
        print(f"   Analyzing {test_ticker}...")
        response = requests.get(
            f"{base_url}/api/v1/market-pulse",
            params={"ticker": test_ticker},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Market pulse endpoint working")
            data = response.json()
            print(f"   Ticker: {data.get('ticker')}")
            print(f"   Pulse: {data.get('pulse')}")
            print(f"   Momentum Score: {data.get('momentum', {}).get('score')}%")
            print(f"   Explanation: {data.get('llm_explanation')[:100]}...")
            
            # Validate response structure
            required_fields = ['ticker', 'as_of', 'momentum', 'news', 'pulse', 'llm_explanation']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"⚠️  Missing fields: {missing_fields}")
            else:
                print("✅ Response structure valid")
            
            return True
        else:
            print(f"❌ Market pulse failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Market pulse error: {e}")
        return False

def main():
    success = test_backend()
    
    if success:
        print("\n🎉 All tests passed! Backend is ready.")
        print("\n📋 Next steps:")
        print("   1. Start frontend: cd frontend && npm start")
        print("   2. Open http://localhost:3000")
        print("   3. Test with different tickers (MSFT, GOOGL, etc.)")
        return 0
    else:
        print("\n❌ Tests failed. Check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure backend is running: python run_server.py")
        print("   2. Check if port 8000 is available")
        print("   3. Install dependencies: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())