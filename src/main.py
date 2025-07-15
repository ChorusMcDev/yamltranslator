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
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 20 + "🔧 YAML Translator Tool v1.0 🔧" + " " * 19 + "║")
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
    
    print("\n🚀 Starting YAML Translator Tool...")
    input("\n⏸️  Press Enter to continue...")

def main():
    """Main application entry point."""
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