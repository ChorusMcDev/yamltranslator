#!/usr/bin/env python3
"""
YAML Translator Tool - Main Entry Point
A comprehensive tool for translating and formatting YAML files
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path for imports
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

def check_dependencies():
    """Check if required dependencies are available."""
    missing_deps = []
    
    try:
        import yaml
    except ImportError:
        missing_deps.append("PyYAML")
    
    try:
        import openai
    except ImportError:
        missing_deps.append("openai")
    
    try:
        from more_itertools import chunked
    except ImportError:
        missing_deps.append("more-itertools")
    
    try:
        import licensing
    except ImportError:
        missing_deps.append("licensing")
    
    if missing_deps:
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\n💡 To install missing dependencies, run:")
        print(f"   pip install {' '.join(missing_deps)}")
        return False
    
    return True

def show_banner():
    """Display application banner."""
    try:
        from version import get_version
        version = get_version()
    except ImportError:
        version = "1.0.1"
    
    print("╔" + "═" * 70 + "╗")
    print("║" + f" " * 20 + f"🔧 YAML Translator Tool v{version} 🔧" + " " * (49 - len(version)) + "║")
    print("║" + " " * 70 + "║")
    print("║" + " " * 10 + "🌐 Translate • 🔤 Format • 🔄 Reverse • ⚙️ Configure" + " " * 11 + "║")
    print("╚" + "═" * 70 + "╝")
    print()

def initialize_app():
    """Initialize the application and check requirements."""
    show_banner()
    
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        input("\n⏸️  Press Enter to exit...")
        sys.exit(1)
    
    print("✅ All dependencies found!")
    
    # Initialize configuration if needed
    try:
        from config.settings import get_setting
        print("⚙️  Configuration system ready")
    except ImportError:
        print("⚠️  Configuration system not available (using defaults)")
    
    # Check license status
    print("🔑 Checking license...")
    license_valid = check_license_status()
    
    if not license_valid:
        print("⚠️  License check failed or no license found")
        # You can choose to allow trial mode or require license
        # For now, we'll show a warning but continue
        print("💡 Some features may be limited without a valid license")
    else:
        print("✅ License verified successfully!")
    
    print("\n🚀 Starting YAML Translator Tool...")
    input("\n⏸️  Press Enter to continue...")

def check_license_status():
    """Check license status during application startup."""
    try:
        from license_system.license_menu import quick_license_check
        return quick_license_check()
    except ImportError:
        print("⚠️  License system not available")
        return False
    except Exception as e:
        print(f"⚠️  License check error: {e}")
        return False

def main():
    """Main application entry point."""
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--version', '-v']:
            try:
                from version import print_version
                print_version()
            except ImportError:
                print("YAML Translator Tool v1.0.1")
            return
        elif sys.argv[1] in ['--help', '-h']:
            print("YAML Translator Tool")
            print("Usage:")
            print("  YAMLTranslator            - Start interactive mode")
            print("  YAMLTranslator --version  - Show version information")
            print("  YAMLTranslator --help     - Show this help message")
            return
    
    try:
        # Initialize the application
        initialize_app()
        
        # Import and run the main menu
        from utils.menu import main_menu
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\n🚪 Application interrupted by user. Goodbye!")
        sys.exit(0)
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("💡 Make sure all required files are present in the application directory.")
        input("\n⏸️  Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please report this error if it persists.")
        input("\n⏸️  Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()