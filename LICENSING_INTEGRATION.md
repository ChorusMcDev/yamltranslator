# YAML Translator - Cryptolens Licensing Integration

This document describes the Cryptolens licensing system integrated into the YAML Translator Tool.

## Overview

The YAML Translator Tool now includes professional licensing through Cryptolens, providing secure license key validation and feature protection.

## Features

- 🔐 **Secure License Validation**: Uses Cryptolens server-side validation with RSA signature verification
- 💻 **Machine Binding**: Licenses are tied to specific machine codes for security
- 🔄 **Online/Offline Operation**: Supports both online validation and cached offline verification
- 📊 **License Status Monitoring**: Real-time license status checking and reporting
- 🛡️ **Feature Protection**: Individual features can be license-protected
- 📁 **Secure Storage**: License keys are stored securely in user's home directory

## License Configuration

The application is configured with the following Cryptolens settings:

- **Product ID**: 30628
- **Access Token**: WyIxMTA4NTU5MTgiLCJaRm1VOGVNd01DRytlbTdKRG54VElWVjRRQ1J2ZkpIbE04QTNwZG9iIl0=
- **RSA Public Key**: Embedded in the application for signature verification

## License Manager API

### Core Classes

#### `LicenseManager`
Main class for license operations:

```python
from license_system.license_manager import LicenseManager

# Create instance
manager = LicenseManager()

# Get machine code
machine_code = manager.get_machine_code()

# Save license key
success = manager.save_license_key("YOUR-LICENSE-KEY")

# Verify license
is_valid, message = manager.verify_license()

# Get comprehensive status
status = manager.get_license_status()
```

#### Key Methods

- `save_license_key(license_key: str) -> bool`: Save and encrypt license key
- `load_license_key() -> Optional[str]`: Load saved license key
- `verify_license(license_key: Optional[str] = None) -> Tuple[bool, str]`: Verify license with server
- `is_license_valid() -> bool`: Quick validation check (uses cache)
- `get_machine_code() -> str`: Get unique machine identifier
- `get_license_status() -> Dict[str, Any]`: Get comprehensive license information
- `clear_license() -> bool`: Remove stored license key

### Global Instance

```python
from license_system.license_manager import get_license_manager, check_license

# Get global manager instance
manager = get_license_manager()

# Quick license check
is_licensed = check_license()
```

## License Menu System

### Interactive License Management

Access through main menu option 6:

1. **Enter License Key**: Add new license key with validation
2. **Verify Current License**: Re-validate existing license
3. **Clear License Key**: Remove stored license
4. **Purchase Information**: Display purchase details
5. **Return to Main Menu**: Go back

### Programmatic Access

```python
from license_system.license_menu import (
    license_menu,           # Full interactive menu
    quick_license_check,    # Startup validation
    enter_license_key,      # Prompt for key entry
    display_license_status  # Show current status
)
```

## Feature Protection

### Protecting Application Features

Features are automatically protected when accessed:

```python
from utils.menu import check_license_for_feature

# Check if user can access a feature
if not check_license_for_feature("translation"):
    return  # User will be prompted to enter license

# Feature code here...
```

### Currently Protected Features

- **Translation**: YAML file translation to different languages
- **Formatting**: Small caps conversion
- **Reversing**: Reverse small caps formatting

## Integration Points

### Application Startup

License checking is integrated into the main application startup:

1. Dependency validation
2. License verification
3. Feature availability assessment

```python
# In main.py
def initialize_app():
    # ... other initialization
    
    print("🔑 Checking license...")
    license_valid = check_license_status()
    
    if not license_valid:
        print("⚠️  License check failed or no license found")
        print("💡 Some features may be limited without a valid license")
    else:
        print("✅ License verified successfully!")
```

### Menu Integration

The main menu includes license management:

- Option 6: 🔑 License Management
- Automatic license checking before accessing protected features

## License Storage

### Storage Location

License keys are stored in:
```
~/.yamltranslator/license.json
```

### Storage Format

```json
{
  "license_key": "YOUR-LICENSE-KEY",
  "product_id": 30628
}
```

### Security

- Stored in user's home directory (restricted access)
- JSON format for easy parsing
- Can be encrypted in future versions

## Error Handling

### Common Scenarios

1. **No License Key**: Prompts user to enter key
2. **Invalid License**: Shows error message and allows re-entry
3. **Blocked License**: Informs user of blocked status
4. **Network Issues**: Falls back to cached validation
5. **Cryptolens Library Missing**: Graceful degradation to trial mode

### Error Messages

- ❌ License verification failed: [specific error]
- ⚠️ License system not available - running in trial mode
- 🔒 License Required for [Feature Name]
- 💡 You can manage your license from the main menu

## Testing

### Automated Tests

Run the licensing test suite:

```bash
python3 test_licensing_integration.py
```

Tests include:
- License manager functionality
- License menu operations
- Main application integration
- Cryptolens server connectivity

### Manual Testing

Use the demo script:

```bash
python3 demo_licensing.py
```

### Machine Code

Your machine code for license activation:
```
Use: python3 -c "from license_system.license_manager import get_license_manager; print(get_license_manager().get_machine_code())"
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure `licensing` package is installed: `pip install licensing`
   - Check for naming conflicts with local modules

2. **Connection Issues**
   - Verify internet connectivity
   - Check firewall settings for api.cryptolens.io

3. **License Not Working**
   - Verify license key format (XXXXX-XXXXX-XXXXX-XXXXX)
   - Check if license is blocked or expired
   - Ensure machine code matches activation

4. **Module Not Found**
   - License system degrades gracefully to trial mode
   - Features remain accessible but may prompt for licensing

### Debug Commands

```bash
# Test Cryptolens connection directly
python3 -c "from licensing.methods import Key, Helpers; print('Machine:', Helpers.GetMachineCode(v=2))"

# Check license manager import
python3 -c "from license_system.license_manager import get_license_manager; print('OK')"

# Run comprehensive test
python3 test_licensing_integration.py
```

## Dependencies

### Required Packages

- `licensing` (Cryptolens Python SDK)
- `pathlib` (Python standard library)
- `json` (Python standard library)
- `os` (Python standard library)

### Installation

```bash
pip install licensing
```

Or from requirements.txt:
```bash
pip install -r requirements.txt
```

## Purchase Information

### Licensing Options

- **Single User License**: $29.99
- **Multi-User License**: Volume discounts available
- **Enterprise License**: Custom pricing

### Features Included

- ✅ Unlimited YAML file translations
- ✅ All supported languages
- ✅ Batch processing capabilities
- ✅ Advanced formatting options
- ✅ Priority support

### Contact

- **Website**: https://yamltranslator.com
- **Email**: support@yamltranslator.com

## API Reference

### License Manager

```python
class LicenseManager:
    def __init__(self)
    def save_license_key(self, license_key: str) -> bool
    def load_license_key(self) -> Optional[str]
    def verify_license(self, license_key: Optional[str] = None, offline_check: bool = False) -> Tuple[bool, str]
    def is_license_valid(self) -> bool
    def get_machine_code(self) -> str
    def clear_license(self) -> bool
    def get_license_status(self) -> Dict[str, Any]
```

### License Menu Functions

```python
def license_menu()                          # Full interactive menu
def quick_license_check() -> bool           # Startup validation
def enter_license_key() -> bool             # Interactive key entry
def verify_existing_license() -> bool       # Re-validate current license
def clear_license() -> bool                 # Remove stored license
def display_license_status()                # Show current status
def show_purchase_info()                    # Display purchase information
def prompt_for_license() -> bool            # Prompt if no license exists
```

### Integration Functions

```python
def check_license_for_feature(feature_name: str) -> bool  # Feature protection
def get_license_manager() -> LicenseManager               # Global instance
def check_license() -> bool                               # Quick validation
```

---

*This documentation covers the complete Cryptolens licensing integration for the YAML Translator Tool.*
