#!/usr/bin/env python3
"""
MarketPulse API Server Startup Script
"""

import sys
import os
import subprocess

def main():
    print("Starting MarketPulse API Server...")
    
    # Add src/backend to Python path
    backend_path = os.path.join(os.path.dirname(__file__), 'src', 'backend')
    sys.path.insert(0, backend_path)
    
    # Change to backend directory
    os.chdir(backend_path)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\nShutting down MarketPulse API Server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())