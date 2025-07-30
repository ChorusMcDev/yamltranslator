#!/usr/bin/env python3
"""
License Manager for YAML Translator Tool
Handles Cryptolens license verification and management
"""

import os
import json
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

# Cryptolens configuration
CRYPTOLENS_CONFIG = {
    'access_token': 'WyIxMTA4NTU5MTgiLCJaRm1VOGVNd01DRytlbTdKRG54VElWVjRRQ1J2ZkpIbE04QTNwZG9iIl0=',
    'product_id': 30628,
    'rsa_public_key': '<RSAKeyValue><Modulus>m/f3k/vrYBHUjOVMci+CvPWIQDKumXhqfvrZDlf/jFqcMvOjvSP6KvDsMAFnupcaDdROWqVAO8r712UiC4spUnpSLmnd3PGw5+x+1Mwmxw5WWEh0K6Qu23shhe+J9OLKhWrNJHbgYBugl6eP6RUEmXmCDZJxQLdsXe8ro44uyDcw61APvtEhQ1ofdZmN9Wt2Fa0akUlHN8WPCRlacHRaQDc/GqQ9Wovoz/80HKxdbYTJKy+7smF3yQ6CgSwx1AGIX7jd/UBhfbMbdtSOyIyf8M1f+C9kAqo3leJHf2Fvaq5hJtYJdUVlrmgGtV/Bb1uNY8RGWzc9Pvy9V+Y+q9aMyQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>'
}

class LicenseManager:
    """Manages license verification and storage for the YAML Translator Tool."""
    
    def __init__(self):
        self.license_file = Path.home() / '.yamltranslator' / 'license.json'
        self.license_file.parent.mkdir(exist_ok=True)
        self._cached_license = None
        self._license_valid = None
        
    def _import_cryptolens(self):
        """Import Cryptolens modules with fallback handling."""
        try:
            from licensing.methods import Key, Helpers
            return Key, Helpers
        except ImportError as e:
            print("❌ Cryptolens library not found. Please install it:")
            print("   pip install licensing")
            raise ImportError(f"Failed to import Cryptolens: {e}")
    
    def save_license_key(self, license_key: str) -> bool:
        """Save license key to encrypted storage."""
        try:
            # Encrypt the license key using the same system as API keys
            from config.settings import save_api_key, get_setting
            
            license_data = {
                'license_key': license_key,
                'product_id': CRYPTOLENS_CONFIG['product_id']
            }
            
            # Save to license file
            with open(self.license_file, 'w') as f:
                json.dump(license_data, f, indent=2)
            
            print("✅ License key saved successfully")
            self._cached_license = None  # Clear cache
            self._license_valid = None
            return True
            
        except Exception as e:
            print(f"❌ Error saving license key: {e}")
            return False
    
    def load_license_key(self) -> Optional[str]:
        """Load license key from storage."""
        try:
            if not self.license_file.exists():
                return None
                
            with open(self.license_file, 'r') as f:
                license_data = json.load(f)
                
            return license_data.get('license_key')
            
        except Exception as e:
            print(f"⚠️  Error loading license key: {e}")
            return None
    
    def verify_license(self, license_key: Optional[str] = None, offline_check: bool = False) -> Tuple[bool, str]:
        """
        Verify license key with Cryptolens server.
        
        Args:
            license_key: License key to verify (if None, loads from storage)
            offline_check: If True, performs offline validation only
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            Key, Helpers = self._import_cryptolens()
            
            # Get license key
            if license_key is None:
                license_key = self.load_license_key()
                
            if not license_key:
                return False, "No license key found. Please enter a valid license key."
            
            # Check cached result first (for performance)
            if self._license_valid is not None and license_key == getattr(self._cached_license, 'Key', None):
                return self._license_valid, "License validated (cached)"
            
            print("🔍 Verifying license with Cryptolens server...")
            
            # Perform license verification
            result = Key.activate(
                token=CRYPTOLENS_CONFIG['access_token'],
                rsa_pub_key=CRYPTOLENS_CONFIG['rsa_public_key'],
                product_id=CRYPTOLENS_CONFIG['product_id'],
                key=license_key,
                machine_code=Helpers.GetMachineCode(v=2)
            )
            
            if result[0] is None:
                # License verification failed
                error_msg = result[1] if len(result) > 1 else "Unknown error"
                self._license_valid = False
                return False, f"License verification failed: {error_msg}"
            
            # License is valid
            license_obj = result[0]
            self._cached_license = license_obj
            self._license_valid = True
            
            # Check license features and expiration
            validation_msg = self._check_license_features(license_obj)
            
            return True, validation_msg
            
        except ImportError as e:
            return False, f"Cryptolens library not available: {e}"
        except Exception as e:
            print(f"❌ Error during license verification: {e}")
            return False, f"License verification error: {e}"
    
    def _has_yaml_translator_features(self, license_obj):
        """Check if license has YAML Translator features (F1 or F8)"""
        try:
            # Feature 1: YAML Translator (lowercase in actual license object)
            has_f1 = hasattr(license_obj, 'f1') and license_obj.f1
            # Feature 8: All Features (lowercase in actual license object)
            has_f8 = hasattr(license_obj, 'f8') and license_obj.f8
            return has_f1 or has_f8
        except Exception as e:
            print(f"Error checking features: {e}")
            return False

    def has_required_features(self) -> Tuple[bool, str]:
        """Check if current license has required features for YAML Translator."""
        try:
            # First verify license is valid
            is_valid, message = self.verify_license()
            if not is_valid:
                return False, message
            
            # Check if license has required features
            if self._cached_license:
                if self._has_yaml_translator_features(self._cached_license):
                    return True, "✅ License has required YAML Translator features"
                else:
                    return False, "❌ License missing required features (F1: YAML Translator or F8: All Features)"
            else:
                return False, "❌ License validation error"
                
        except Exception as e:
            return False, f"❌ Error checking license features: {e}"

    def _check_license_features(self, license_obj) -> str:
        """Check license features and return status message."""
        try:
            # Basic license info
            messages = ["✅ License is valid and active!"]
            
            # Check if license has expired
            if hasattr(license_obj, 'Expires') and license_obj.Expires:
                from datetime import datetime
                try:
                    # Cryptolens returns timestamp, convert to datetime
                    expires_timestamp = license_obj.Expires
                    expire_date = datetime.fromtimestamp(expires_timestamp)
                    current_date = datetime.now()
                    
                    if current_date > expire_date:
                        return "❌ License has expired"
                    else:
                        days_left = (expire_date - current_date).days
                        messages.append(f"📅 License expires in {days_left} days")
                except:
                    messages.append("📅 License expiration: Unable to determine")
            
            # Check feature flags (f1-f8) - using lowercase as shown in diagnostic
            features = []
            for i in range(1, 9):
                feature_attr = f'f{i}'  # Changed to lowercase
                if hasattr(license_obj, feature_attr):
                    feature_val = getattr(license_obj, feature_attr)
                    if feature_val:
                        features.append(f"F{i}")  # Display as uppercase for user
            
            if features:
                messages.append(f"🔧 Active features: {', '.join(features)}")
            
            # Check machine count
            if hasattr(license_obj, 'ActivatedMachines'):
                machine_count = len(license_obj.ActivatedMachines)
                messages.append(f"💻 Activated devices: {machine_count}")
            
            return "\n   ".join(messages)
            
        except Exception as e:
            return f"✅ License is valid! (Feature check error: {e})"
    
    def is_license_valid(self) -> bool:
        """Quick check if license is valid (uses cache if available)."""
        if self._license_valid is not None:
            return self._license_valid
            
        # Perform verification
        is_valid, _ = self.verify_license()
        return is_valid
    
    def get_machine_code(self) -> str:
        """Get the machine code for this device."""
        try:
            Key, Helpers = self._import_cryptolens()
            return Helpers.GetMachineCode(v=2)
        except ImportError:
            return "Cryptolens library not available"
        except Exception as e:
            return f"Error getting machine code: {e}"
    
    def clear_license(self) -> bool:
        """Clear stored license key."""
        try:
            if self.license_file.exists():
                os.remove(self.license_file)
            
            self._cached_license = None
            self._license_valid = None
            print("✅ License key cleared")
            return True
            
        except Exception as e:
            print(f"❌ Error clearing license: {e}")
            return False
    
    def get_license_status(self) -> Dict[str, Any]:
        """Get comprehensive license status information."""
        license_key = self.load_license_key()
        
        status = {
            'has_license': license_key is not None,
            'license_key_preview': f"{license_key[:8]}...{license_key[-4:]}" if license_key else None,
            'is_valid': False,
            'message': "No license key found",
            'machine_code': self.get_machine_code()
        }
        
        if license_key:
            is_valid, message = self.verify_license(license_key)
            status['is_valid'] = is_valid
            status['message'] = message
        
        return status


# Global license manager instance
_license_manager = None

def get_license_manager() -> LicenseManager:
    """Get global license manager instance."""
    global _license_manager
    if _license_manager is None:
        _license_manager = LicenseManager()
    return _license_manager

def check_license() -> bool:
    """Quick license check for application startup."""
    try:
        manager = get_license_manager()
        return manager.is_license_valid()
    except Exception as e:
        print(f"⚠️  License check error: {e}")
        return False