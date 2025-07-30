#!/usr/bin/env python3
"""
License Diagnostic Tool - Debug license object structure and features
"""

import sys
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))

def diagnose_license():
    """Get detailed information about the current license object."""
    print("🔍 License Diagnostic Tool")
    print("=" * 50)
    
    try:
        from license_system.license_manager import get_license_manager
        
        manager = get_license_manager()
        
        # Get the license key
        license_key = manager.load_license_key()
        if not license_key:
            print("❌ No license key found")
            return
        
        print(f"🔑 License Key: {license_key}")
        print(f"💻 Machine Code: {manager.get_machine_code()}")
        print()
        
        # Import Cryptolens directly
        Key, Helpers = manager._import_cryptolens()
        
        print("🔄 Activating license and getting full object details...")
        
        # Get the license object directly
        result = Key.activate(
            token='WyIxMTA4NTU5MTgiLCJaRm1VOGVNd01DRytlbTdKRG54VElWVjRRQ1J2ZkpIbE04QTNwZG9iIl0=',
            rsa_pub_key='<RSAKeyValue><Modulus>m/f3k/vrYBHUjOVMci+CvPWIQDKumXhqfvrZDlf/jFqcMvOjvSP6KvDsMAFnupcaDdROWqVAO8r712UiC4spUnpSLmnd3PGw5+x+1Mwmxw5WWEh0K6Qu23shhe+J9OLKhWrNJHbgYBugl6eP6RUEmXmCDZJxQLdsXe8ro44uyDcw61APvtEhQ1ofdZmN9Wt2Fa0akUlHN8WPCRlacHRaQDc/GqQ9Wovoz/80HKxdbYTJKy+7smF3yQ6CgSwx1AGIX7jd/UBhfbMbdtSOyIyf8M1f+C9kAqo3leJHf2Fvaq5hJtYJdUVlrmgGtV/Bb1uNY8RGWzc9Pvy9V+Y+q9aMyQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>',
            product_id=30628,
            key=license_key,
            machine_code=Helpers.GetMachineCode(v=2)
        )
        
        if result[0] is None:
            print(f"❌ License activation failed: {result[1]}")
            return
        
        license_obj = result[0]
        
        print("✅ License activated successfully!")
        print()
        print("📊 COMPLETE LICENSE OBJECT ANALYSIS:")
        print("=" * 50)
        
        # Print all attributes of the license object
        print("🔍 All attributes:")
        attrs = dir(license_obj)
        for attr in sorted(attrs):
            if not attr.startswith('_'):
                try:
                    value = getattr(license_obj, attr)
                    print(f"   {attr}: {value} (type: {type(value).__name__})")
                except Exception as e:
                    print(f"   {attr}: <error getting value: {e}>")
        
        print()
        print("🎯 FEATURE ANALYSIS:")
        print("=" * 30)
        
        # Check all features F1-F8
        features_found = []
        for i in range(1, 9):
            feature_name = f'F{i}'
            if hasattr(license_obj, feature_name):
                value = getattr(license_obj, feature_name)
                status = "✅ ENABLED" if value else "❌ DISABLED"
                print(f"   Feature {i} (F{i}): {status} (value: {value})")
                if value:
                    features_found.append(f"F{i}")
            else:
                print(f"   Feature {i} (F{i}): ❓ NOT FOUND")
        
        print()
        print("📋 SUMMARY:")
        print("=" * 20)
        print(f"   Active Features: {', '.join(features_found) if features_found else 'None'}")
        print(f"   Has F1 (YAML Translator): {'✅ YES' if 'F1' in features_found else '❌ NO'}")
        print(f"   Has F8 (All Features): {'✅ YES' if 'F8' in features_found else '❌ NO'}")
        print(f"   Should have access: {'✅ YES' if ('F1' in features_found or 'F8' in features_found) else '❌ NO'}")
        
        # Test our current feature checking logic
        print()
        print("🧪 TESTING CURRENT LOGIC:")
        print("=" * 30)
        
        has_f1 = hasattr(license_obj, 'F1') and license_obj.F1
        has_f8 = hasattr(license_obj, 'F8') and license_obj.F8
        should_work = has_f1 or has_f8
        
        print(f"   hasattr(license_obj, 'F1'): {hasattr(license_obj, 'F1')}")
        print(f"   license_obj.F1 (if exists): {getattr(license_obj, 'F1', 'NOT FOUND')}")
        print(f"   has_f1 result: {has_f1}")
        print(f"   hasattr(license_obj, 'F8'): {hasattr(license_obj, 'F8')}")
        print(f"   license_obj.F8 (if exists): {getattr(license_obj, 'F8', 'NOT FOUND')}")
        print(f"   has_f8 result: {has_f8}")
        print(f"   Final result (has_f1 or has_f8): {should_work}")
        
        # Check license object type and structure
        print()
        print("🔬 OBJECT STRUCTURE:")
        print("=" * 25)
        print(f"   Type: {type(license_obj)}")
        print(f"   Module: {type(license_obj).__module__}")
        print(f"   Class: {type(license_obj).__name__}")
        
        # Raw object representation
        print()
        print("📜 RAW OBJECT:")
        print("=" * 15)
        print(repr(license_obj))
        
        return True
        
    except Exception as e:
        print(f"❌ Error during diagnosis: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    diagnose_license()
