@echo off
echo ========================================
echo    YAML Translator Tool - Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Installing PyInstaller...
pip install pyinstaller

if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/4] Building executable...
pyinstaller YAMLTranslator.spec --clean

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [4/4] Build completed successfully!
echo.
echo Executable location: dist\YAMLTranslator.exe
echo.

REM Test the executable
echo Testing the executable...
dist\YAMLTranslator.exe --help >nul 2>&1

if errorlevel 1 (
    echo WARNING: Executable test failed, but file was created
) else (
    echo SUCCESS: Executable is working correctly
)

echo.
echo Build process completed!
echo You can find the executable in the 'dist' folder.
pause
