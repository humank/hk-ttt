#!/usr/bin/env python3
"""
Simple test script to verify the application works.
"""

import os
import sys
import subprocess
import time
import requests
import json

def test_application():
    print("🧪 Testing Opportunity Management API...")
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to API: {e}")
        return False
    
    # Test API documentation
    try:
        response = requests.get("http://localhost:8000/api/v1/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API documentation is accessible!")
        else:
            print(f"⚠️  API documentation returned status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not access API documentation: {e}")
    
    # Test OpenAPI spec
    try:
        response = requests.get("http://localhost:8000/api/v1/openapi.json", timeout=5)
        if response.status_code == 200:
            print("✅ OpenAPI specification is accessible!")
            spec = response.json()
            print(f"   API Title: {spec.get('info', {}).get('title', 'Unknown')}")
            print(f"   API Version: {spec.get('info', {}).get('version', 'Unknown')}")
            print(f"   Available paths: {len(spec.get('paths', {}))}")
        else:
            print(f"⚠️  OpenAPI spec returned status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not access OpenAPI spec: {e}")
    
    # Test creating an opportunity
    try:
        opportunity_data = {
            "title": "Test Opportunity",
            "customer_id": "123e4567-e89b-12d3-a456-426614174000",
            "customer_name": "Test Customer",
            "sales_manager_id": "123e4567-e89b-12d3-a456-426614174001",
            "description": "This is a test opportunity to verify the API is working correctly",
            "priority": "HIGH",
            "annual_recurring_revenue": 50000.0,
            "geographic_requirements": {
                "region_id": "123e4567-e89b-12d3-a456-426614174002",
                "name": "Test Region",
                "requires_physical_presence": False,
                "allows_remote_work": True
            }
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/opportunities",
            json=opportunity_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ Opportunity creation test passed!")
            result = response.json()
            opportunity_id = result.get("data", {}).get("result", {}).get("id")
            if opportunity_id:
                print(f"   Created opportunity ID: {opportunity_id}")
                return opportunity_id
        else:
            print(f"❌ Opportunity creation failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not create opportunity: {e}")
        return False
    
    return True

def main():
    print("🚀 Starting API Test Suite...")
    print("=" * 50)
    
    # Check if server is running
    print("📡 Checking if API server is running...")
    
    result = test_application()
    
    print("=" * 50)
    if result:
        print("🎉 All tests passed! The API is working correctly.")
        print("\n📚 Next steps:")
        print("   • Visit http://localhost:8000/api/v1/docs for interactive documentation")
        print("   • Use the curl examples in curl_examples.md to test all endpoints")
        print("   • Check the README.md for complete usage instructions")
    else:
        print("❌ Some tests failed. Please check the server logs.")
        print("\n🔧 Troubleshooting:")
        print("   • Make sure the server is running: python -m uvicorn app.main:app --reload")
        print("   • Check if port 8000 is available")
        print("   • Verify all dependencies are installed")

if __name__ == "__main__":
    main()
