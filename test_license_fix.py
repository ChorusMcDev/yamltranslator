#!/usr/bin/env python3
"""
Test the fixed license feature detection
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from license_system.license_manager import get_license_manager

def test_license_features():
    print("🧪 Testing License Feature Detection")
    print("=" * 50)
    
    manager = get_license_manager()
    
    # Load the license key
    license_key = manager.load_license_key()
    print(f"🔑 License Key: {license_key}")
    
    # Verify license
    is_valid, message = manager.verify_license()
    print(f"✅ License Valid: {is_valid}")
    print(f"📝 Message: {message}")
    
    # Check required features
    has_features, feature_message = manager.has_required_features()
    print(f"🎯 Has Required Features: {has_features}")
    print(f"📝 Feature Message: {feature_message}")
    
    # Direct license object inspection
    if manager._cached_license:
        license_obj = manager._cached_license
        print(f"\n🔍 Direct Feature Check:")
        print(f"   hasattr(license_obj, 'f1'): {hasattr(license_obj, 'f1')}")
        if hasattr(license_obj, 'f1'):
            print(f"   license_obj.f1: {license_obj.f1}")
        print(f"   hasattr(license_obj, 'f8'): {hasattr(license_obj, 'f8')}")
        if hasattr(license_obj, 'f8'):
            print(f"   license_obj.f8: {license_obj.f8}")
        
        # Test the method directly
        result = manager._has_yaml_translator_features(license_obj)
        print(f"   _has_yaml_translator_features result: {result}")

if __name__ == "__main__":
    test_license_features()
