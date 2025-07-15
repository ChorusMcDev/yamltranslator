"""
YAML Small Caps Formatter
Converts regular text to small caps Unicode characters
"""

import yaml
import re
from pathlib import Path

# Small caps mapping
SMALL_CAPS_MAP = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ',
    'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
    'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
    'y': 'ʏ', 'z': 'ᴢ'
}

def flatten_yaml(d, prefix=""):
    """Flatten nested YAML structure."""
    items = {}
    for k, v in d.items():
        new_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.update(flatten_yaml(v, new_key))
        else:
            items[new_key] = v
    return items

def unflatten_yaml(d):
    """Unflatten YAML structure."""
    result = {}
    for k, v in d.items():
        keys = k.split(".")
        ref = result
        for part in keys[:-1]:
            ref = ref.setdefault(part, {})
        ref[keys[-1]] = v
    return result

def to_small_caps(text):
    """Convert text to small caps, preserving placeholders and special characters."""
    if not isinstance(text, str):
        return text
    
    # Preserve placeholders and formatting codes
    placeholder_pattern = r'(%[^%]*%|\{[^}]*\}|&[a-zA-Z0-9])'
    placeholders = []
    temp_text = text
    
    # Extract placeholders
    for match in re.finditer(placeholder_pattern, text):
        placeholder = f"__PLACEHOLDER_{len(placeholders)}__"
        placeholders.append(match.group())
        temp_text = temp_text.replace(match.group(), placeholder, 1)
    
    # Convert to small caps
    result = ""
    for char in temp_text:
        result += SMALL_CAPS_MAP.get(char.lower(), char)
    
    # Restore placeholders
    for i, placeholder_text in enumerate(placeholders):
        result = result.replace(f"__PLACEHOLDER_{i}__", placeholder_text)
    
    return result

class Formatter:
    def __init__(self):
        self.converted_count = 0
        self.total_count = 0

    def run(self, file_path):
        """Main formatting workflow."""
        return self.format_yaml_file(file_path)

    def format_yaml_file(self, file_path):
        """Convert YAML file text to small caps."""
        print(f"🔄 Loading file: {file_path}")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Error loading YAML file: {e}")
            return None

        # Flatten and process
        flat = flatten_yaml(original)
        processed = {}
        
        self.converted_count = 0
        self.total_count = 0
        
        print("🔤 Converting text to small caps...")
        
        for key, value in flat.items():
            self.total_count += 1
            if isinstance(value, str) and value.strip():
                # Convert to small caps
                converted = to_small_caps(value)
                processed[key] = converted
                if converted != value:
                    self.converted_count += 1
                    print(f"✓ {key}: '{value}' → '{converted}'")
            else:
                processed[key] = value

        # Unflatten and save
        result = unflatten_yaml(processed)
        
        # Generate output filename
        input_path = Path(file_path)
        output_file = f"smallcaps_{input_path.name}"
        
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                yaml.dump(result, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            
            print(f"\n✅ Small caps conversion completed!")
            print(f"📊 Converted {self.converted_count}/{self.total_count} text values")
            print(f"📁 Output file: {output_file}")
            
            return output_file
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return None

    def format_to_small_caps(self, yaml_data):
        """Convert YAML data to small caps format."""
        return to_small_caps(yaml_data)

    def process_file(self, file_path):
        """Process file and return results."""
        return self.format_yaml_file(file_path)

    def display_results(self, results):
        """Display formatting results."""
        if results:
            print(f"✅ Small caps formatting completed: {results}")
        else:
            print("❌ Small caps formatting failed")