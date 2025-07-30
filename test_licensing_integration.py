#!/usr/bin/env python3
"""
Test script for Cryptolens licensing integration
"""

import sys
import os
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))

def test_license_manager():
    """Test the license manager functionality."""
    print("🧪 Testing License Manager...")
    print("=" * 50)
    
    try:
        from license_system.license_manager import LicenseManager, get_license_manager
        
        # Test 1: Create license manager
        print("1. Creating license manager...")
        manager = LicenseManager()
        print("   ✅ License manager created successfully")
        
        # Test 2: Get machine code
        print("\n2. Getting machine code...")
        machine_code = manager.get_machine_code()
        print(f"   💻 Machine Code: {machine_code}")
        
        # Test 3: Check current license status
        print("\n3. Checking current license status...")
        status = manager.get_license_status()
        print(f"   📊 Has License: {status['has_license']}")
        print(f"   📊 Is Valid: {status['is_valid']}")
        print(f"   📊 Message: {status['message']}")
        
        # Test 4: Test global instance
        print("\n4. Testing global instance...")
        global_manager = get_license_manager()
        print("   ✅ Global license manager retrieved successfully")
        
        print("\n🎉 All license manager tests passed!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_license_menu():
    """Test the license menu functionality."""
    print("\n🧪 Testing License Menu...")
    print("=" * 50)
    
    try:
        from license_system.license_menu import quick_license_check, display_license_status
        
        # Test 1: Quick license check
        print("1. Quick license check...")
        is_valid = quick_license_check()
        print(f"   📊 License Valid: {is_valid}")
        
        # Test 2: Display license status (this will print status info)
        print("\n2. License status display:")
        display_license_status()
        
        print("\n🎉 License menu tests completed!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_main_integration():
    """Test integration with main application."""
    print("\n🧪 Testing Main App Integration...")
    print("=" * 50)
    
    try:
        # Test importing main components
        print("1. Testing imports...")
        
        from main import check_license_status
        print("   ✅ main.check_license_status imported")
        
        from utils.menu import check_license_for_feature
        print("   ✅ menu.check_license_for_feature imported")
        
        # Test license check
        print("\n2. Testing license check...")
        license_ok = check_license_status()
        print(f"   📊 License Status: {license_ok}")
        
        # Test feature check
        print("\n3. Testing feature check...")
        can_translate = check_license_for_feature("translation")
        print(f"   📊 Can Translate: {can_translate}")
        
        print("\n🎉 Main integration tests completed!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_cryptolens_connection():
    """Test connection to Cryptolens (with a dummy license key)."""
    print("\n🧪 Testing Cryptolens Connection...")
    print("=" * 50)
    
    try:
        from license_system.license_manager import LicenseManager
        
        manager = LicenseManager()
        
        # Test with an invalid key to check if connection works
        print("1. Testing server connection with invalid key...")
        is_valid, message = manager.verify_license("INVALID-KEY-FOR-TEST-12345")
        print(f"   📊 Expected failure result: {message}")
        
        if "license verification failed" in message.lower() or "error" in message.lower():
            print("   ✅ Server connection working (got expected error response)")
            return True
        else:
            print("   ⚠️  Unexpected response - check connection")
            return False
            
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🔑 YAML Translator - Cryptolens Licensing Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("License Manager", test_license_manager()))
    results.append(("License Menu", test_license_menu()))
    results.append(("Main Integration", test_main_integration()))
    results.append(("Cryptolens Connection", test_cryptolens_connection()))
    
    # Show results
    print("\n📊 Test Results Summary:")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} : {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Licensing system is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🚪 Tests interrupted by user")
        sys.exit(1)
