"""
YAML Small Caps Reverser
Converts small caps Unicode characters back to regular text
"""

import yaml
import re
from pathlib import Path

# Reverse small caps mapping
REVERSE_SMALL_CAPS_MAP = {
    'ᴀ': 'a', 'ʙ': 'b', 'ᴄ': 'c', 'ᴅ': 'd', 'ᴇ': 'e', 'ꜰ': 'f', 'ɢ': 'g', 'ʜ': 'h',
    'ɪ': 'i', 'ᴊ': 'j', 'ᴋ': 'k', 'ʟ': 'l', 'ᴍ': 'm', 'ɴ': 'n', 'ᴏ': 'o', 'ᴘ': 'p',
    'ǫ': 'q', 'ʀ': 'r', 's': 's', 'ᴛ': 't', 'ᴜ': 'u', 'ᴠ': 'v', 'ᴡ': 'w', 'x': 'x',
    'ʏ': 'y', 'ᴢ': 'z'
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

def from_small_caps(text):
    """Convert small caps text back to regular text, preserving placeholders."""
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
    
    # Convert from small caps
    result = ""
    for char in temp_text:
        result += REVERSE_SMALL_CAPS_MAP.get(char, char)
    
    # Restore placeholders
    for i, placeholder_text in enumerate(placeholders):
        result = result.replace(f"__PLACEHOLDER_{i}__", placeholder_text)
    
    return result

class Reverser:
    def __init__(self):
        self.converted_count = 0
        self.total_count = 0

    def run(self, file_path):
        """Main reversing workflow."""
        return self.reverse_yaml_file(file_path)

    def reverse_yaml_file(self, file_path):
        """Convert small caps YAML file back to regular text."""
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
        
        print("🔄 Converting small caps back to regular text...")
        
        for key, value in flat.items():
            self.total_count += 1
            if isinstance(value, str) and value.strip():
                # Convert from small caps
                converted = from_small_caps(value)
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
        output_file = f"reversed_{input_path.name}"
        
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                yaml.dump(result, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            
            print(f"\n✅ Small caps reversal completed!")
            print(f"📊 Converted {self.converted_count}/{self.total_count} text values")
            print(f"📁 Output file: {output_file}")
            
            return output_file
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return None

    def reverse_yaml(self, file_path):
        """Legacy method for compatibility."""
        return self.reverse_yaml_file(file_path)

    def convert_yaml_recursive(self, data):
        """Recursively convert YAML data from small caps."""
        if isinstance(data, dict):
            return {key: self.convert_yaml_recursive(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_yaml_recursive(item) for item in data]
        elif isinstance(data, str):
            return from_small_caps(data)
        else:
            return data