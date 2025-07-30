#!/bin/bash

echo "========================================"
echo "   YAML Translator Tool - Build Script"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

echo "[1/4] Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo
echo "[2/4] Installing PyInstaller..."
pip3 install pyinstaller

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install PyInstaller"
    exit 1
fi

echo
echo "[3/4] Building executable..."
pyinstaller YAMLTranslator.spec --clean

if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

echo
echo "[4/4] Build completed successfully!"
echo
echo "Executable location: dist/YAMLTranslator"
echo

# Test the executable
echo "Testing the executable..."
./dist/YAMLTranslator --help &> /dev/null

if [ $? -ne 0 ]; then
    echo "WARNING: Executable test failed, but file was created"
else
    echo "SUCCESS: Executable is working correctly"
fi

echo
echo "Build process completed!"
echo "You can find the executable in the 'dist' folder."
