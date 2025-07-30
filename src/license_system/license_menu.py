#!/usr/bin/env python3
"""
License Menu for YAML Translator Tool
Provides user interface for license management with feature checking
"""

import os
import sys
from typing import Optional

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_license_banner():
    """Display license management banner."""
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 22 + "🔑 License Management 🔑" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

def display_license_status():
    """Display current license status with feature checking."""
    try:
        from license_system.license_manager import get_license_manager
        
        manager = get_license_manager()
        status = manager.get_license_status()
        
        print("📊 Current License Status:")
        print("─" * 40)
        
        if status['has_license']:
            print(f"🔑 License Key: {status['license_key_preview']}")
            print(f"✅ Valid: {'Yes' if status['is_valid'] else 'No'}")
            print(f"📝 Status: {status['message']}")
            
            # Check specific features if license is valid
            if status['is_valid']:
                has_yaml_feature = manager.has_required_features()
                if has_yaml_feature:
                    print("🎉 Features: YAML Translator features available")
                else:
                    print("⚠️  Features: License valid but missing YAML Translator features")
                    print("   Required: Feature 1 (YAML Translator) OR Feature 8 (All Features)")
        else:
            print("❌ No license key found")
            
        print(f"💻 Machine Code: {status['machine_code']}")
        print()
        
        return status['is_valid'] and (not status['has_license'] or manager.has_required_features())
        
    except ImportError:
        print("❌ License management system not available")
        return False
    except Exception as e:
        print(f"❌ Error checking license status: {e}")
        return False

def enter_license_key() -> bool:
    """Prompt user to enter a license key."""
    try:
        from license_system.license_manager import get_license_manager
        
        print("🔑 Enter License Key")
        print("─" * 30)
        print("Please enter your YAML Translator license key.")
        print("Your license must have Feature 1 (YAML Translator) or Feature 8 (All Features).")
        print()
        
        # Get machine code first
        manager = get_license_manager()
        machine_code = manager.get_machine_code()
        print(f"💻 Your Machine Code: {machine_code}")
        print("   (You may need this when purchasing/activating your license)")
        print()
        
        # Prompt for license key
        license_key = input("License Key: ").strip()
        
        if not license_key:
            print("❌ No license key entered")
            return False
        
        # Validate format (basic check)
        if len(license_key) < 10:
            print("❌ License key appears to be too short")
            return False
        
        # Save and verify license
        print("\n🔄 Saving and verifying license key...")
        
        if not manager.save_license_key(license_key):
            return False
        
        # Verify the license with feature checking
        is_valid, message = manager.verify_license(license_key)
        
        if is_valid:
            print(f"✅ {message}")
            
            # Check if it has the required features
            if manager.has_required_features():
                print("\n🎉 License activated successfully!")
                print("✅ Your license includes YAML Translator features!")
            else:
                print("\n⚠️  License is valid but missing required features!")
                print("❌ This license doesn't include YAML Translator features")
                print("💡 Required: Feature 1 (YAML Translator) OR Feature 8 (All Features)")
                print("🛒 Please contact support or purchase the correct license")
            return True
        else:
            print(f"❌ {message}")
            print("\n💡 Please check your license key and try again.")
            print("   If problems persist, contact support.")
            return False
            
    except ImportError:
        print("❌ License management system not available")
        return False
    except KeyboardInterrupt:
        print("\n🚪 License entry cancelled")
        return False
    except Exception as e:
        print(f"❌ Error processing license key: {e}")
        return False

def verify_existing_license() -> bool:
    """Verify the currently stored license."""
    try:
        from license_system.license_manager import get_license_manager
        
        manager = get_license_manager()
        license_key = manager.load_license_key()
        
        if not license_key:
            print("❌ No license key found to verify")
            return False
        
        print("🔄 Verifying license with server...")
        is_valid, message = manager.verify_license(license_key)
        
        if is_valid:
            print(f"✅ {message}")
            
            # Check features
            if manager.has_required_features():
                print("🎉 License includes required YAML Translator features!")
            else:
                print("⚠️  License is valid but missing YAML Translator features")
                print("Required: Feature 1 (YAML Translator) OR Feature 8 (All Features)")
            return True
        else:
            print(f"❌ {message}")
            return False
            
    except ImportError:
        print("❌ License management system not available")
        return False
    except Exception as e:
        print(f"❌ Error verifying license: {e}")
        return False

def clear_license() -> bool:
    """Clear the stored license key."""
    try:
        from license_system.license_manager import get_license_manager
        
        print("🗑️  Clear License Key")
        print("─" * 25)
        print("⚠️  This will remove your stored license key.")
        print("   You will need to re-enter it to use the application.")
        print()
        
        confirm = input("Are you sure? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            manager = get_license_manager()
            if manager.clear_license():
                print("✅ License key cleared successfully")
                return True
            else:
                print("❌ Failed to clear license key")
                return False
        else:
            print("🚪 Operation cancelled")
            return False
            
    except ImportError:
        print("❌ License management system not available")
        return False
    except Exception as e:
        print(f"❌ Error clearing license: {e}")
        return False

def show_purchase_info():
    """Display information about purchasing a license."""
    print("🛒 Purchase License Information")
    print("─" * 35)
    print()
    print("To purchase a license for YAML Translator Tool:")
    print()
    print("🌐 Website: https://store.steamdb.fun")
    print("📧 Email: contact@bali0531.hu")
    print()
    print("License Features Required:")
    print("• 🎯 Feature 1: YAML Translator (specific to this application)")
    print("• 🌟 Feature 8: All Features (includes everything)")
    print()
    print("⚠️  Important: Standard licenses without these features won't work!")
    print()
    print("License Benefits:")
    print("• ✅ Unlimited YAML file translations")
    print("• ✅ All supported languages (25+)")
    print("• ✅ Batch processing capabilities")
    print("• ✅ Advanced formatting options")
    print("• ✅ Priority support")
    print()
    print("💰 Pricing starts at $4.99 for YAML Translator license")
    print("🏢 Volume discounts available for multiple users")
    print("🌟 All Features license includes future applications")
    print()

def license_menu():
    """Main license management menu."""
    while True:
        try:
            clear_screen()
            show_license_banner()
            
            # Show current status
            is_licensed = display_license_status()
            
            print("📋 License Management Options:")
            print("─" * 35)
            print("1. 🔑 Enter License Key")
            print("2. 🔄 Verify Current License")
            print("3. 🗑️  Clear License Key")
            print("4. 🛒 Purchase Information")
            print("5. 🏠 Return to Main Menu")
            print()
            
            choice = input("Select an option (1-5): ").strip()
            
            if choice == '1':
                print("\n" + "=" * 50)
                if enter_license_key():
                    input("\n⏸️  Press Enter to continue...")
                else:
                    input("\n⏸️  Press Enter to continue...")
                    
            elif choice == '2':
                print("\n" + "=" * 50)
                verify_existing_license()
                input("\n⏸️  Press Enter to continue...")
                
            elif choice == '3':
                print("\n" + "=" * 50)
                clear_license()
                input("\n⏸️  Press Enter to continue...")
                
            elif choice == '4':
                print("\n" + "=" * 50)
                show_purchase_info()
                input("\n⏸️  Press Enter to continue...")
                
            elif choice == '5':
                break
                
            else:
                print("❌ Invalid option. Please choose 1-5.")
                input("\n⏸️  Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n🚪 Returning to main menu...")
            break
        except Exception as e:
            print(f"\n❌ Error in license menu: {e}")
            input("\n⏸️  Press Enter to continue...")

def quick_license_check() -> bool:
    """Quick license check for application startup."""
    try:
        from license_system.license_manager import get_license_manager
        
        manager = get_license_manager()
        if not manager.is_license_valid():
            return False
        
        # Check if license has required features
        return manager.has_required_features()
        
    except ImportError:
        print("⚠️  License system not available - running in trial mode")
        return False
    except Exception as e:
        print(f"⚠️  License check error: {e}")
        return False

def prompt_for_license() -> bool:
    """Prompt user to enter license if none exists."""
    print("\n🔑 License Required")
    print("─" * 25)
    print("This application requires a valid license with YAML Translator features.")
    print("Required: Feature 1 (YAML Translator) OR Feature 8 (All Features)")
    print()
    print("You can:")
    print("1. Enter your license key now")
    print("2. Purchase a license")
    print("3. Exit the application")
    print()
    
    choice = input("Choose an option (1-3): ").strip()
    
    if choice == '1':
        return enter_license_key()
    elif choice == '2':
        show_purchase_info()
        print("\nAfter purchasing, please restart the application and enter your license key.")
        return False
    else:
        return False