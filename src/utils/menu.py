import os
import sys
from pathlib import Path

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_main_menu():
    """Display the main menu with enhanced formatting."""
    clear_screen()
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 15 + "🔧 YAML Translator Tool 🔧" + " " * 15 + "║")
    print("╠" + "═" * 60 + "╣")
    print("║  1. 🌐 Translate YAML File                            ║")
    print("║  2. 🔤 Convert YAML to Small Caps                     ║")
    print("║  3. 🔄 Reverse Small Caps to Normal Text              ║")
    print("║  4. ⚙️  Settings & Configuration                       ║")
    print("║  5. 📊 View Translation History                       ║")
    print("║  6. 🔑 License Management                             ║")
    print("║  0. 🚪 Exit                                           ║")
    print("╚" + "═" * 60 + "╝")

def display_file_selection_menu():
    """Display file selection options."""
    print("\n📁 File Selection:")
    print("1. Enter file path manually")
    print("2. Browse current directory")
    print("3. Use drag & drop (paste path)")
    print("0. Back to main menu")

def get_yaml_files_in_directory(directory="."):
    """Get all YAML files in the specified directory."""
    try:
        yaml_files = []
        for file in Path(directory).iterdir():
            if file.is_file() and file.suffix.lower() in ['.yml', '.yaml']:
                yaml_files.append(file)
        return yaml_files
    except Exception as e:
        print(f"❌ Error reading directory: {e}")
        return []

def select_file():
    """Enhanced file selection with multiple options."""
    while True:
        display_file_selection_menu()
        choice = input("\n👉 Select option: ").strip()
        
        if choice == '0':
            return None
        elif choice == '1':
            file_path = input("\n📝 Enter YAML file path: ").strip().strip('"')
            if validate_yaml_file(file_path):
                return file_path
        elif choice == '2':
            return browse_directory()
        elif choice == '3':
            print("\n📋 Paste the file path here (you can drag & drop the file):")
            file_path = input("Path: ").strip().strip('"')
            if validate_yaml_file(file_path):
                return file_path
        else:
            print("❌ Invalid option. Please try again.")
        
        input("\n⏸️  Press Enter to continue...")

def browse_directory():
    """Browse and select files from current directory."""
    yaml_files = get_yaml_files_in_directory()
    
    if not yaml_files:
        print("\n❌ No YAML files found in current directory.")
        return None
    
    print(f"\n📂 Found {len(yaml_files)} YAML file(s):")
    for i, file in enumerate(yaml_files, 1):
        file_size = file.stat().st_size / 1024  # Size in KB
        print(f"  {i}. {file.name} ({file_size:.1f} KB)")
    
    print("  0. Back")
    
    try:
        choice = int(input("\n👉 Select file number: "))
        if choice == 0:
            return None
        elif 1 <= choice <= len(yaml_files):
            return str(yaml_files[choice - 1])
        else:
            print("❌ Invalid file number.")
            return None
    except ValueError:
        print("❌ Please enter a valid number.")
        return None

def validate_yaml_file(file_path):
    """Validate if the file exists and is a YAML file."""
    if not file_path:
        print("❌ No file path provided.")
        return False
    
    path = Path(file_path)
    if not path.exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    if not path.is_file():
        print(f"❌ Path is not a file: {file_path}")
        return False
    
    if path.suffix.lower() not in ['.yml', '.yaml']:
        print(f"❌ File is not a YAML file: {file_path}")
        return False
    
    print(f"✅ Valid YAML file: {path.name}")
    return True

def get_user_choice():
    """Get user choice with validation."""
    while True:
        try:
            choice = input("\n👉 Select option: ").strip()
            return choice
        except KeyboardInterrupt:
            print("\n\n🚪 Exiting...")
            sys.exit(0)

def handle_menu_selection(choice):
    """Handle menu selection with improved flow."""
    if choice == '1':
        handle_translation()
    elif choice == '2':
        handle_formatting()
    elif choice == '3':
        handle_reversing()
    elif choice == '4':
        handle_settings()
    elif choice == '5':
        handle_history()
    elif choice == '6':
        handle_license_management()
    elif choice == '0':
        print("\n👋 Thank you for using YAML Translator Tool!")
        sys.exit(0)
    else:
        print("❌ Invalid choice. Please try again.")
        input("\n⏸️  Press Enter to continue...")

def check_license_for_feature(feature_name):
    """Check if user has valid license for a specific feature."""
    try:
        from license_system.license_manager import get_license_manager
        
        manager = get_license_manager()
        
        # Check if license has required features
        has_features, message = manager.has_required_features()
        
        if not has_features:
            print(f"\n🔒 License Required for {feature_name.title()}")
            print("=" * 50)
            print(message)
            print()
            
            if "No license key found" in message:
                choice = input("❓ Would you like to enter your license key now? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    from license_system.license_menu import enter_license_key
                    return enter_license_key()
                else:
                    print("💡 You can manage your license from the main menu (option 6)")
                    return False
            else:
                print("� Your license is valid but missing required features:")
                print("   • Feature 1 (F1): YAML Translator")
                print("   • Feature 8 (F8): All Features")
                print()
                print("� To upgrade your license:")
                print("   📧 Email: support@yamltranslator.com")
                print("   🌐 Website: https://yamltranslator.com")
                return False
        
        return True
                
    except ImportError:
        print("⚠️  License system not available - feature available in trial mode")
        return True
    except Exception as e:
        print(f"⚠️  License check error: {e} - allowing access")
        return True

def handle_translation():
    """Handle translation workflow."""
    # Check license first
    if not check_license_for_feature("translation"):
        return
    
    try:
        from core.translator import Translator
    except ImportError:
        print("❌ Translation module not found. Please check installation.")
        input("\n⏸️  Press Enter to continue...")
        return
    
    print("\n🌐 YAML Translation")
    print("=" * 40)
    
    # File selection
    file_path = select_file()
    if not file_path:
        return
    
    # Language selection
    language = select_language()
    if not language:
        return
    
    # API key check/input
    api_key = get_api_key()
    if not api_key:
        return
    
    # Execute translation
    translator = Translator()
    result = translator.run(file_path, language, api_key)
    
    if result:
        print(f"\n✅ Translation completed successfully!")
        print(f"📁 Output file: {result}")
    
    input("\n⏸️  Press Enter to return to main menu...")

def handle_formatting():
    """Handle small caps formatting workflow."""
    # Check license first  
    if not check_license_for_feature("formatting"):
        return
        
    try:
        from core.formatter import Formatter
    except ImportError:
        print("❌ Formatter module not found. Please check installation.")
        input("\n⏸️  Press Enter to continue...")
        return
    
    print("\n🔤 Small Caps Conversion")
    print("=" * 40)
    
    file_path = select_file()
    if not file_path:
        return
    
    formatter = Formatter()
    result = formatter.run(file_path)
    
    if result:
        print(f"\n✅ Formatting completed successfully!")
        print(f"📁 Output file: {result}")
    
    input("\n⏸️  Press Enter to return to main menu...")

def handle_reversing():
    """Handle reverse formatting workflow."""
    # Check license first
    if not check_license_for_feature("reversing"):
        return
        
    try:
        from core.reverser import Reverser
    except ImportError:
        print("❌ Reverser module not found. Please check installation.")
        input("\n⏸️  Press Enter to continue...")
        return
    
    print("\n🔄 Reverse Small Caps")
    print("=" * 40)
    
    file_path = select_file()
    if not file_path:
        return
    
    reverser = Reverser()
    result = reverser.run(file_path)
    
    if result:
        print(f"\n✅ Reversing completed successfully!")
        print(f"📁 Output file: {result}")
    
    input("\n⏸️  Press Enter to return to main menu...")

def select_language():
    """Language selection with search functionality."""
    languages = {
        'en': 'English',
        'es': 'Spanish (Español)',
        'fr': 'French (Français)', 
        'de': 'German (Deutsch)',
        'it': 'Italian (Italiano)',
        'pt': 'Portuguese (Português)',
        'ru': 'Russian (Русский)',
        'zh': 'Chinese (中文)',
        'ja': 'Japanese (日本語)',
        'ko': 'Korean (한국어)',
        'ar': 'Arabic (العربية)',
        'hi': 'Hindi (हिन्दी)',
        'hu': 'Hungarian (Magyar)',
        'pl': 'Polish (Polski)',
        'cs': 'Czech (Čeština)',
        'sk': 'Slovak (Slovenčina)',
        'ro': 'Romanian (Română)',
        'bg': 'Bulgarian (Български)',
        'hr': 'Croatian (Hrvatski)',
        'sr': 'Serbian (Српски)',
        'nl': 'Dutch (Nederlands)',
        'tr': 'Turkish (Türkçe)',
        'sv': 'Swedish (Svenska)',
        'no': 'Norwegian (Norsk)',
        'da': 'Danish (Dansk)',
        'fi': 'Finnish (Suomi)'
    }
    
    print("\n🌍 Language Selection")
    print("=" * 40)
    print("💡 You can:")
    print("   • Enter language code (e.g., 'hu' for Hungarian)")
    print("   • Enter language name (e.g., 'Hungarian')")
    print("   • Type 'list' to see all supported languages")
    print("   • Type '0' to go back")
    
    while True:
        choice = input("\n🗣️  Enter target language: ").strip().lower()
        
        if choice == '0':
            return None
        elif choice == 'list':
            display_language_list(languages)
            continue
        elif choice in languages:
            print(f"✅ Selected: {languages[choice]}")
            return choice
        else:
            # Search by name
            for code, name in languages.items():
                if choice in name.lower():
                    print(f"✅ Found: {name} ({code})")
                    confirm = input("❓ Use this language? (y/n): ").strip().lower()
                    if confirm in ['y', 'yes']:
                        return code
                    break
            else:
                print("❌ Language not found. Type 'list' to see all options.")

def display_language_list(languages):
    """Display paginated language list."""
    print("\n📜 Supported Languages:")
    print("=" * 60)
    
    items_per_page = 15
    total_pages = (len(languages) + items_per_page - 1) // items_per_page
    current_page = 0
    
    while True:
        start_idx = current_page * items_per_page
        end_idx = min(start_idx + items_per_page, len(languages))
        
        lang_items = list(languages.items())[start_idx:end_idx]
        
        for i, (code, name) in enumerate(lang_items, start_idx + 1):
            print(f"  {i:2d}. {code:3s} - {name}")
        
        print(f"\nPage {current_page + 1}/{total_pages}")
        if current_page < total_pages - 1:
            print("  'n' - Next page")
        if current_page > 0:
            print("  'p' - Previous page")
        print("  'q' - Back to language selection")
        
        nav = input("\n👉 Navigation: ").strip().lower()
        if nav == 'n' and current_page < total_pages - 1:
            current_page += 1
        elif nav == 'p' and current_page > 0:
            current_page -= 1
        elif nav == 'q':
            break

def get_api_key():
    """Get API key with multiple options."""
    try:
        from config.settings import get_stored_api_key, save_api_key
    except ImportError:
        print("❌ Settings module not found. Using basic API key input.")
        api_key = input("\n🔐 Enter OpenAI API key: ").strip()
        return api_key if api_key else None
    
    stored_key = get_stored_api_key()
    
    if stored_key:
        print(f"\n🔑 Found stored API key: {stored_key[:10]}...{stored_key[-4:]}")
        use_stored = input("❓ Use stored API key? (y/n): ").strip().lower()
        if use_stored in ['y', 'yes']:
            return stored_key
    
    print("\n🔑 API Key Required")
    print("=" * 40)
    print("💡 Options:")
    print("   1. Enter API key now")
    print("   2. Set API key in environment variable")
    print("   0. Back to main menu")
    
    choice = input("\n👉 Select option: ").strip()
    
    if choice == '0':
        return None
    elif choice == '1':
        api_key = input("\n🔐 Enter OpenAI API key: ").strip()
        if api_key:
            try:
                save_option = input("💾 Save this API key for future use? (y/n): ").strip().lower()
                if save_option in ['y', 'yes']:
                    save_api_key(api_key)
            except:
                pass  # Ignore save errors
            return api_key
        else:
            print("❌ No API key provided.")
            return None
    elif choice == '2':
        print("\n📝 Set environment variable:")
        print("   Windows: set OPENAI_API_KEY=your_key_here")
        print("   Linux/Mac: export OPENAI_API_KEY=your_key_here")
        input("\n⏸️  Press Enter after setting the variable...")
        return os.getenv('OPENAI_API_KEY')
    else:
        print("❌ Invalid option.")
        return None

def handle_settings():
    """Handle settings and configuration."""
    try:
        from config.settings import display_settings, modify_settings
    except ImportError:
        print("❌ Settings module not found. Basic settings not available.")
        input("\n⏸️  Press Enter to continue...")
        return
    
    while True:
        clear_screen()
        print("⚙️  Settings & Configuration")
        print("=" * 40)
        
        display_settings()
        
        print("\n📋 Options:")
        print("  1. Modify API settings")
        print("  2. Change file handling settings")
        print("  3. Reset to defaults")
        print("  4. Export settings")
        print("  5. Import settings")
        print("  0. Back to main menu")
        
        choice = input("\n👉 Select option: ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            modify_settings('api')
        elif choice == '2':
            modify_settings('files')
        elif choice == '3':
            modify_settings('reset')
        elif choice == '4':
            modify_settings('export')
        elif choice == '5':
            modify_settings('import')
        else:
            print("❌ Invalid option.")
            input("\n⏸️  Press Enter to continue...")

def handle_history():
    """Handle translation history viewing."""
    try:
        from utils.telemetry import get_translation_history
    except ImportError:
        print("❌ History module not found. History not available.")
        input("\n⏸️  Press Enter to continue...")
        return
    
    clear_screen()
    print("📊 Translation History")
    print("=" * 40)
    
    history = get_translation_history()
    
    if not history:
        print("📭 No translation history found.")
    else:
        for i, entry in enumerate(history, 1):
            print(f"\n{i}. {entry.get('timestamp', 'Unknown time')}")
            print(f"   📁 File: {entry.get('file', 'Unknown')}")
            print(f"   🌍 Language: {entry.get('language', 'Unknown')}")
            print(f"   ⏱️  Duration: {entry.get('duration', 'Unknown')}")
            print(f"   📊 Status: {entry.get('status', 'Unknown')}")
    
    input("\n⏸️  Press Enter to return to main menu...")

def handle_license_management():
    """Handle license management workflow."""
    try:
        from license_system.license_menu import license_menu
        license_menu()
    except ImportError:
        print("❌ License management not available.")
        print("💡 Please ensure the licensing module is properly installed.")
        input("\n⏸️  Press Enter to continue...")
    except Exception as e:
        print(f"❌ Error accessing license management: {e}")
        input("\n⏸️  Press Enter to continue...")

def main_menu():
    """Main menu loop."""
    while True:
        try:
            display_main_menu()
            choice = get_user_choice()
            handle_menu_selection(choice)
        except KeyboardInterrupt:
            print("\n\n🚪 Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("\n⏸️  Press Enter to continue...")

if __name__ == "__main__":
    main_menu()