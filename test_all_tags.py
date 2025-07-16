#!/usr/bin/env python3
"""
Comprehensive test script for any XML-like tag preservation in small caps conversion.
Tests the new general pattern that preserves any <tag> or <tag:value> formatting.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from core.formatter import to_small_caps
from core.reverser import from_small_caps

def test_all_tag_preservation():
    """Test that any XML-like tags are preserved during small caps conversion."""
    
    test_cases = [
        # Basic text
        ("hello world", "ʜᴇʟʟᴏ ᴡᴏʀʟᴅ"),
        
        # Newlines
        ("hello\\nworld", "ʜᴇʟʟᴏ\\nᴡᴏʀʟᴅ"),
        
        # Color codes (hex)
        ("<#b81838>erő", "<#b81838>ᴇʀő"),
        
        # Numbered tags
        ("<5>hello", "<5>ʜᴇʟʟᴏ"),
        
        # Shift commands
        ("<shift:-8>hello", "<shift:-8>ʜᴇʟʟᴏ"),
        
        # Glyph commands  
        ("<glyph:skills_gui>text", "<glyph:skills_gui>ᴛᴇxᴛ"),
        
        # Complex combination from user example
        ("<shift:-8><glyph:skills_gui>hello", "<shift:-8><glyph:skills_gui>ʜᴇʟʟᴏ"),
        
        # Any custom XML-like tags
        ("<custom:value>text", "<custom:value>ᴛᴇxᴛ"),
        ("<anything>text", "<anything>ᴛᴇxᴛ"),
        ("<test:123>hello", "<test:123>ʜᴇʟʟᴏ"),
        ("<bold>text</bold>", "<bold>ᴛᴇxᴛ</bold>"),
        ("<minecraft:diamond>gem", "<minecraft:diamond>ɢᴇᴍ"),
        ("<ui:button:large>click", "<ui:button:large>ᴄʟɪᴄᴋ"),
        
        # Traditional placeholders
        ("%player%", "%player%"),
        ("{world}", "{world}"),
        ("&c", "&c"),
        
        # Mixed content with multiple tags
        ("Hello <#ff0000>%player%\\nWelcome <shift:-2>back to <minecraft:world>!", 
         "ʜᴇʟʟᴏ <#ff0000>%player%\\nᴡᴇʟᴄᴏᴍᴇ <shift:-2>ʙᴀᴄᴋ ᴛᴏ <minecraft:world>!"),
        
        # User's specific example
        ("<#b81838>erő", "<#b81838>ᴇʀő"),
    ]
    
    print("🧪 Testing ANY XML-like tag preservation in small caps conversion...")
    print("=" * 70)
    
    all_passed = True
    
    for i, (input_text, expected) in enumerate(test_cases, 1):
        print(f"\n{i:2d}. Testing: {input_text}")
        
        # Test conversion to small caps
        result = to_small_caps(input_text)
        print(f"    Result:   {result}")
        print(f"    Expected: {expected}")
        
        if result == expected:
            print("    ✅ PASSED - Small caps conversion")
        else:
            print("    ❌ FAILED - Small caps conversion")
            all_passed = False
        
        # Test round-trip (back to normal)
        restored = from_small_caps(result)
        print(f"    Restored: {restored}")
        
        # Check if any XML-like tags are preserved
        import re
        xml_tags = re.findall(r'<[^>]*>', input_text)
        formatting_preserved = True
        
        for tag in xml_tags:
            if tag in result:
                print(f"    ✅ PRESERVED: {tag}")
            else:
                print(f"    ❌ LOST: {tag}")
                formatting_preserved = False
        
        # Check other formatting elements
        other_elements = ["\\n", "%player%", "{world}", "&c"]
        for element in other_elements:
            if element in input_text:
                if element in result:
                    print(f"    ✅ PRESERVED: {element}")
                else:
                    print(f"    ❌ LOST: {element}")
                    formatting_preserved = False
        
        if not formatting_preserved:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 All tests PASSED! ANY XML-like tag preservation is working correctly.")
        print("✨ The pattern <[^>]*> successfully preserves all kinds of tags!")
    else:
        print("❌ Some tests FAILED! Check the formatting preservation logic.")
    
    return all_passed

if __name__ == "__main__":
    test_all_tag_preservation()
