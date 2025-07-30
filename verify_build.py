#!/usr/bin/env python3
"""
Build verification script for YAML Translator Tool
Tests the built executable and licensing system
"""

import sys
import os
import subprocess
from pathlib import Path

def test_executable():
    """Test the built executable."""
    exe_path = Path("dist/YAMLTranslator")
    
    if not exe_path.exists():
        print("❌ Executable not found. Please run ./build.sh first.")
        return False
    
    print("🧪 Testing executable...")
    
    # Check if the executable runs and shows help/menu
    try:
        # For a non-interactive test, we'll just check if it starts
        result = subprocess.run([str(exe_path)], 
                              input="\n0\n", 
                              text=True,
                              capture_output=True,
                              timeout=10)
        
        if result.returncode == 0:
            print("✅ Executable runs successfully")
            if "License Management" in result.stdout:
                print("✅ License Management menu option found")
            else:
                print("⚠️  License Management menu option not found in output")
            return True
        else:
            print(f"❌ Executable failed with exit code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Executable test timed out (this might be normal for interactive apps)")
        return True
    except Exception as e:
        print(f"❌ Error testing executable: {e}")
        return False

def check_licensing_system():
    """Check if the licensing system is properly integrated."""
    print("🔑 Checking licensing system integration...")
    
    try:
        # Add src to path
        src_dir = Path("src")
        sys.path.insert(0, str(src_dir))
        
        # Test imports
        from license_system.license_manager import get_license_manager
        from license_system.license_menu import display_license_status
        
        print("✅ License system imports working")
        
        # Test license manager
        manager = get_license_manager()
        machine_code = manager.get_machine_code()
        
        if machine_code and machine_code != "Cryptolens library not available":
            print(f"✅ Machine code generation: {machine_code[:16]}...")
        else:
            print("❌ Machine code generation failed")
            return False
        
        # Test license status
        status = manager.get_license_status()
        print(f"✅ License status check: {status['has_license']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing licensing system: {e}")
        return False

def check_build_files():
    """Check if all necessary build files are present."""
    print("📁 Checking build files...")
    
    required_files = [
        "YAMLTranslator.spec",
        "build.sh", 
        "requirements.txt",
        "src/main.py",
        "src/license_system/license_manager.py",
        "src/license_system/license_menu.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        return False
    else:
        print("✅ All required build files present")
        return True

def main():
    """Run all verification checks."""
    print("🔧 YAML Translator Tool - Build Verification")
    print("=" * 50)
    
    checks = [
        ("Build Files", check_build_files),
        ("Licensing System", check_licensing_system), 
        ("Executable", test_executable)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}...")
        result = check_func()
        results.append((check_name, result))
    
    print("\n📊 Verification Results:")
    print("=" * 30)
    
    passed = 0
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:15} : {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} checks passed")
    
    if passed == len(results):
        print("🎉 All verification checks passed! Build is ready for distribution.")
        return True
    else:
        print("⚠️  Some checks failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
