# YAML Translator Tool - Build Guide

## 🎯 Overview

This guide covers building the YAML Translator Tool into a standalone executable with Cryptolens licensing integration.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows, Linux, or macOS
- **Internet Connection**: Required for dependency installation and license verification

### Required Dependencies
All dependencies are automatically installed by the build script:
```
PyYAML>=6.0
openai>=1.0.0
more-itertools>=10.0.0
cryptography>=3.0.0
licensing>=0.51
```

## 🔧 Build Process

### Linux/macOS Build
```bash
# Make the build script executable
chmod +x build.sh

# Run the build
./build.sh
```

### Windows Build
```cmd
# Run the build script
build.bat
```

### Manual Build (if scripts fail)
```bash
# Install dependencies
pip install -r requirements.txt

# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller YAMLTranslator.spec --clean
```

## 📁 Build Output

After successful build, you'll find:

```
dist/
└── YAMLTranslator          # Main executable (Linux/macOS)
    YAMLTranslator.exe      # Main executable (Windows)

build/                      # Temporary build files
└── YAMLTranslator/
    ├── Analysis-00.toc
    ├── PYZ-00.pyz
    ├── warn-YAMLTranslator.txt
    └── xref-YAMLTranslator.html
```

## 🧪 Verification

Run the verification script to ensure everything works:

```bash
python3 verify_build.py
```

This checks:
- ✅ All required files present
- ✅ Licensing system functional
- ✅ Executable runs correctly

## 🔑 Licensing Integration

The built executable includes:

### Core Features
- **Cryptolens Integration**: Server-side license validation
- **Machine Binding**: Licenses tied to device identifiers
- **Feature Protection**: Core functions require valid licenses
- **Secure Storage**: License keys stored in user directory

### License Management
Access through the main menu:
1. **Enter License Key**: Add and validate new licenses
2. **Verify License**: Re-check existing license status
3. **Clear License**: Remove stored license data
4. **Purchase Info**: Display purchasing information

### Configuration
- **Product ID**: 30628
- **Access Token**: Embedded securely
- **RSA Public Key**: Built-in for signature verification
- **Storage Location**: `~/.yamltranslator/license.json`

## 📦 Distribution

### Single File Distribution
The built executable is self-contained and includes:
- Python runtime
- All dependencies
- Licensing system
- Application code

### File Size
Typical executable size: ~50-80 MB (varies by OS)

### No Installation Required
Users can run the executable directly without:
- Python installation
- Dependency management
- Configuration setup

## 🛠️ Troubleshooting

### Common Build Issues

#### 1. Missing Dependencies
```
ERROR: Failed to install dependencies
```
**Solution**: Ensure internet connection and try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. PyInstaller Not Found
```
ERROR: pyinstaller: command not found
```
**Solution**: Install PyInstaller manually:
```bash
pip install pyinstaller
```

#### 3. Import Errors in Built Executable
**Symptoms**: Executable fails to start or shows import errors
**Solution**: Check the spec file includes all required modules:
- Verify `hiddenimports` list
- Ensure all source files are included
- Check for missing binary dependencies

#### 4. Licensing System Not Working
**Symptoms**: License verification fails or shows errors
**Solution**: Verify:
- `licensing` package is properly installed
- No naming conflicts with local modules
- Internet connection for server validation

### Build Warnings

PyInstaller may show warnings - most are harmless:
- Module exclusion warnings
- Binary dependency notifications
- Hook processing messages

Critical errors will stop the build process.

## 🔍 Debugging

### Build Logs
Check these files for detailed information:
- `build/YAMLTranslator/warn-YAMLTranslator.txt` - Warnings
- `build/YAMLTranslator/xref-YAMLTranslator.html` - Dependencies

### Testing Executable
```bash
# Basic functionality test
./dist/YAMLTranslator

# License system test  
python3 -c "
import sys
sys.path.insert(0, 'src')
from license_system.license_manager import get_license_manager
print('Machine Code:', get_license_manager().get_machine_code())
"
```

### Debug Mode
For troubleshooting, build with debug enabled:
```python
# In YAMLTranslator.spec, change:
debug=True
console=True
```

## 📋 Spec File Configuration

The `YAMLTranslator.spec` file controls the build process:

### Key Settings
```python
# Application name and main script
app_name = 'YAMLTranslator'
main_script = 'src/main.py'

# Hidden imports for licensing
hiddenimports = [
    'licensing',
    'licensing.methods', 
    'licensing.models',
    'cryptography',
    # ... other dependencies
]

# Excluded modules (reduces file size)
excludes = [
    'tkinter',
    'matplotlib',
    'numpy',
    # ... UI frameworks not needed
]
```

### Customization Options
- **Icon**: Add `icon='path/to/icon.ico'`
- **Version Info**: Add version resource information
- **Console Mode**: Set `console=False` for GUI apps
- **Compression**: Adjust `upx=True` for smaller files

## 🚀 Advanced Build Options

### Cross-Platform Building
- Build on each target platform
- Use virtual machines for testing
- Consider platform-specific dependencies

### Optimization
```bash
# Smaller executable (longer build time)
pyinstaller YAMLTranslator.spec --clean --upx-dir=/path/to/upx

# Debug build (larger, easier to troubleshoot)
pyinstaller YAMLTranslator.spec --clean --debug=all
```

### Multiple Builds
```bash
# Clean previous builds
rm -rf build/ dist/

# Build with fresh cache
pyinstaller YAMLTranslator.spec --clean --noconfirm
```

## 📊 Build Statistics

Typical build process:
- **Duration**: 30-120 seconds (depends on system)
- **Disk Space**: ~200MB during build (includes temp files)
- **Final Size**: 50-80MB executable
- **Dependencies**: ~20-30 Python packages included

## 🔐 Security Considerations

### Code Protection
- Source code is compiled to bytecode
- Strings and constants may be visible
- Consider code obfuscation for sensitive parts

### License Security
- RSA public key embedded (safe to include)
- Access tokens secured in application
- Private keys never included in distribution

### Distribution Security
- Sign executables with code signing certificates
- Provide checksums for integrity verification
- Use secure distribution channels

## 📚 Additional Resources

### PyInstaller Documentation
- [Official PyInstaller Guide](https://pyinstaller.readthedocs.io/)
- [Advanced Usage](https://pyinstaller.readthedocs.io/en/stable/advanced-topics.html)
- [Troubleshooting](https://pyinstaller.readthedocs.io/en/stable/when-things-go-wrong.html)

### Cryptolens Documentation
- [Python SDK Guide](https://help.cryptolens.io/sdk/python)
- [License Management](https://help.cryptolens.io/licensing-models)
- [API Reference](https://help.cryptolens.io/api)

---

*This build guide ensures reliable creation of standalone YAML Translator Tool executables with integrated licensing.*
