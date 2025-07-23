#!/usr/bin/env python3
"""
Simple script to run the Opportunity Management API locally.
"""

import os
import sys
import subprocess

def main():
    print("🚀 Starting Opportunity Management API...")
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        print("📝 Creating .env file from example...")
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
    
    # Install dependencies with simpler versions
    print("📦 Installing dependencies...")
    simple_requirements = [
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.20.0", 
        "sqlalchemy>=2.0.0",
        "python-multipart>=0.0.6",
        "slowapi>=0.1.9",
        "aiofiles>=23.0.0",
        "python-dotenv>=1.0.0"
    ]
    
    for req in simple_requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {req}: {e}")
            continue
    
    print("✅ Dependencies installed successfully!")
    
    # Start the application
    print("🌟 Starting the API server on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/v1/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    print("\n🛑 Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
