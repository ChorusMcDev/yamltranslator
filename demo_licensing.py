#!/usr/bin/env python3
"""
Simple demo of the licensing system
"""

import sys
import os
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))

def demo_license_system():
    """Demonstrate the licensing system functionality."""
    print("🔑 YAML Translator - Licensing System Demo")
    print("=" * 50)
    
    try:
        from license_system.license_manager import get_license_manager
        from license_system.license_menu import display_license_status
        
        # Get license manager
        manager = get_license_manager()
        
        print("1. Getting machine code...")
        machine_code = manager.get_machine_code()
        print(f"   💻 Your Machine Code: {machine_code}")
        
        print("\n2. Checking current license status...")
        display_license_status()
        
        print("\n3. Testing license verification...")
        status = manager.get_license_status()
        
        if status['has_license']:
            print("   ✅ License key found - testing verification...")
            is_valid, message = manager.verify_license()
            print(f"   📊 Verification result: {message}")
            
            if is_valid:
                print("   🎉 License is valid and active!")
            else:
                print("   ❌ License verification failed")
        else:
            print("   ℹ️  No license key found")
            print("   💡 To add a license, use the main application menu (option 6)")
        
        print("\n✅ Demo completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    demo_license_system()
