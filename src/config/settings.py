"""
Configuration and settings management for YAML Translator Tool
"""

import os
import json
from pathlib import Path

class Settings:
    def __init__(self):
        self.config_dir = Path.home() / '.yaml-translator'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(exist_ok=True)
        
        self.default_settings = {
            'api': {
                'model': 'gpt-4.1',
                'batch_size': 50,
                'timeout': 30,
                'max_retries': 3
            },
            'files': {
                'auto_backup': True,
                'output_suffix': 'translated_',
                'preserve_formatting': True,
                'max_file_size_mb': 10
            },
            'ui': {
                'show_progress': True,
                'detailed_logging': True,
                'auto_clear_screen': True
            },
            'history': {
                'max_entries': 100,
                'auto_save': True
            }
        }
        
        self.settings = self.load_settings()
    
    def get_encryption_key(self):
        """Get or create encryption key for API key storage."""
        try:
            from cryptography.fernet import Fernet
            key_file = self.config_dir / 'key.key'
            
            if key_file.exists():
                with open(key_file, 'rb') as f:
                    return f.read()
            else:
                key = Fernet.generate_key()
                with open(key_file, 'wb') as f:
                    f.write(key)
                return key
        except ImportError:
            # Fallback if cryptography is not available
            return None
    
    def load_settings(self):
        """Load settings from file or create defaults."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                # Merge with defaults to ensure all keys exist
                settings = self.default_settings.copy()
                self._deep_update(settings, loaded)
                return settings
            except Exception as e:
                print(f"⚠️  Error loading settings: {e}")
                return self.default_settings.copy()
        else:
            return self.default_settings.copy()
    
    def save_settings(self):
        """Save current settings to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving settings: {e}")
    
    def _deep_update(self, base_dict, update_dict):
        """Recursively update nested dictionaries."""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def get(self, category, key=None):
        """Get setting value."""
        if key is None:
            return self.settings.get(category, {})
        return self.settings.get(category, {}).get(key)
    
    def set(self, category, key, value):
        """Set setting value."""
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][key] = value
        self.save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = self.default_settings.copy()
        self.save_settings()

# Global settings instance
_settings = Settings()

def get_stored_api_key():
    """Get stored API key (encrypted if possible)."""
    api_key_file = _settings.config_dir / 'api_key.enc'
    if api_key_file.exists():
        try:
            from cryptography.fernet import Fernet
            key = _settings.get_encryption_key()
            if key:
                fernet = Fernet(key)
                with open(api_key_file, 'rb') as f:
                    encrypted_key = f.read()
                return fernet.decrypt(encrypted_key).decode()
        except Exception:
            pass
    
    # Fallback: check for plain text (less secure)
    plain_key_file = _settings.config_dir / 'api_key.txt'
    if plain_key_file.exists():
        try:
            with open(plain_key_file, 'r') as f:
                return f.read().strip()
        except Exception:
            pass
    
    return None

def save_api_key(api_key):
    """Save API key (encrypted if possible, otherwise plain text)."""
    try:
        from cryptography.fernet import Fernet
        key = _settings.get_encryption_key()
        if key:
            fernet = Fernet(key)
            encrypted_key = fernet.encrypt(api_key.encode())
            api_key_file = _settings.config_dir / 'api_key.enc'
            with open(api_key_file, 'wb') as f:
                f.write(encrypted_key)
            print("✅ API key saved securely (encrypted).")
            return
    except ImportError:
        pass
    
    # Fallback: save as plain text
    try:
        plain_key_file = _settings.config_dir / 'api_key.txt'
        with open(plain_key_file, 'w') as f:
            f.write(api_key)
        print("✅ API key saved (plain text - less secure).")
    except Exception as e:
        print(f"❌ Error saving API key: {e}")

def get_setting(category, key=None):
    """Get setting value."""
    return _settings.get(category, key)

def set_setting(category, key, value):
    """Set setting value."""
    _settings.set(category, key, value)

def display_settings():
    """Display current settings."""
    print("📋 Current Settings:")
    print("-" * 40)
    
    for category, settings in _settings.settings.items():
        print(f"\n🔧 {category.upper()}:")
        for key, value in settings.items():
            print(f"   {key}: {value}")

def modify_settings(section):
    """Modify specific settings section."""
    if section == 'api':
        modify_api_settings()
    elif section == 'files':
        modify_file_settings()
    elif section == 'reset':
        confirm = input("⚠️  Reset all settings to defaults? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            _settings.reset_to_defaults()
            print("✅ Settings reset to defaults.")
    elif section == 'export':
        export_settings()
    elif section == 'import':
        import_settings()

def modify_api_settings():
    """Modify API-related settings."""
    current = get_setting('api')
    
    print("\n🔧 API Settings:")
    print(f"Current model: {current['model']}")
    new_model = input("Enter new model (or press Enter to keep current): ").strip()
    if new_model:
        set_setting('api', 'model', new_model)
    
    print(f"Current batch size: {current['batch_size']}")
    new_batch = input("Enter new batch size (or press Enter to keep current): ").strip()
    if new_batch and new_batch.isdigit():
        set_setting('api', 'batch_size', int(new_batch))
    
    print("✅ API settings updated.")

def modify_file_settings():
    """Modify file-related settings."""
    current = get_setting('files')
    
    print("\n📁 File Settings:")
    print(f"Auto backup: {current['auto_backup']}")
    backup = input("Enable auto backup? (y/n): ").strip().lower()
    if backup in ['y', 'yes', 'n', 'no']:
        set_setting('files', 'auto_backup', backup in ['y', 'yes'])
    
    print(f"Current output suffix: {current['output_suffix']}")
    suffix = input("Enter new output suffix (or press Enter to keep current): ").strip()
    if suffix:
        set_setting('files', 'output_suffix', suffix)
    
    print("✅ File settings updated.")

def export_settings():
    """Export settings to a file."""
    export_path = input("Enter export file path (default: settings_export.json): ").strip()
    if not export_path:
        export_path = "settings_export.json"
    
    try:
        with open(export_path, 'w') as f:
            json.dump(_settings.settings, f, indent=2)
        print(f"✅ Settings exported to {export_path}")
    except Exception as e:
        print(f"❌ Error exporting settings: {e}")

def import_settings():
    """Import settings from a file."""
    import_path = input("Enter import file path: ").strip()
    
    try:
        with open(import_path, 'r') as f:
            imported_settings = json.load(f)
        
        _settings._deep_update(_settings.settings, imported_settings)
        _settings.save_settings()
        print("✅ Settings imported successfully.")
    except Exception as e:
        print(f"❌ Error importing settings: {e}")