#!/usr/bin/env python3
"""
Test just the Rooms API from the main backend_test.py file
"""

import sys
import os
sys.path.append('/app')

from backend_test import RUDNScheduleAPITester

def main():
    """Test only the Rooms API"""
    tester = RUDNScheduleAPITester()
    
    print("🚀 Testing Rooms API from main backend_test.py")
    print(f"🌐 Backend URL: {tester.base_url}")
    print("=" * 60)
    
    success = tester.test_rooms_api_comprehensive()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 ROOMS API TEST SUMMARY")
    print("=" * 60)
    
    for result in tester.test_results:
        if "Rooms API" in result['test'] or "POST /api/rooms" in result['test']:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())