# Copilot Instructions for YAML Translator Tool

## Architecture Overview

This is a modular console application with a three-layer architecture:
- **`src/core/`** - Business logic modules (translator, formatter, reverser)
- **`src/utils/`** - User interface and telemetry systems
- **`src/config/`** - Settings management with encrypted storage

## Key Patterns

### Module Import Strategy
```python
try:
    from utils.telemetry import BatchTelemetry
    from config.settings import get_setting
except ImportError:
    # Always provide fallback implementations
    def get_setting(category, key=None):
        defaults = {'api': {'model': 'gpt-4o-mini'}}
        return defaults.get(category, {}).get(key)
```

### YAML Processing Pipeline
1. **Flatten** nested YAML using dot notation (`server.name`, `features.enabled`)
2. **Filter** translatable strings (exclude booleans, numbers, preserve structure)
3. **Batch process** in chunks for API efficiency
4. **Unflatten** back to original structure

### Placeholder Preservation Critical Patterns
The AI translation system must preserve these formats EXACTLY:
- `{value}`, `{player}`, `{xp_unit}` - Variable placeholders
- `&7`, `&a`, `&c` - Minecraft color codes  
- `%placeholder%` - Plugin variables
- `\n` - Literal newline characters (DO NOT CONVERT)
- `<#RRGGBB>` - Hex color codes (e.g., `<#FF0000>` for red)
- `__PH0__`, `__PH1__` - Temporary placeholder tokens

**Current system prompt pattern:**
```python
"Translate these texts to {lang}. Keep ALL placeholders like {value}, {player}, &7, &a, %placeholders%, \\n, <#RRGGBB> EXACTLY as they are. Do not change newlines (\\n), hex colors (<#RRGGBB>), or any formatting codes."
```

### Telemetry System
Uses `BatchTelemetry` class for performance tracking:
- `telemetry.start_batch(idx)` / `telemetry.finish_batch(idx)`
- Tracks API time vs file operations separately
- Auto-saves progress after each batch

## Development Workflows

### Testing Translation
```bash
python src/main.py
# Select option 1, use test.yml, choose language, enter API key
```

### Building Executable
```bash
# Windows
build.bat

# Linux/Mac  
chmod +x build.sh && ./build.sh
```

### Settings Configuration
Settings are stored in JSON with encrypted API keys:
```python
from config.settings import get_setting, save_api_key
model = get_setting('api', 'model')  # Returns 'gpt-4o-mini'
save_api_key(api_key)  # Encrypts and stores
```

## Critical Implementation Details

### File Structure Preservation
- Use `flatten_yaml()` / `unflatten_yaml()` for nested YAML processing
- Always preserve YAML structure with `sort_keys=False`
- Create backups before translation if `auto_backup` enabled

### Error Handling Pattern
All core modules use graceful degradation:
```python
try:
    from core.translator import Translator
except ImportError:
    print("❌ Translation module not found")
    return
```

### Progress Saving
Save after each batch to allow resuming interrupted translations:
```python
save_progress(output_dict, output_file)
```

## Integration Points

- **OpenAI API**: Uses `openai` library with retry logic and timeout handling
- **Encryption**: `cryptography.fernet` for API key storage
- **YAML Processing**: `PyYAML` with Unicode support and structure preservation
- **Batch Processing**: `more-itertools.chunked()` for efficient API calls

## Adding New Features

When extending translation logic, always:
1. Update placeholder preservation patterns in system prompts
2. Add fallback implementations for missing dependencies  
3. Include telemetry tracking for performance monitoring
4. Test with both simple and complex nested YAML structures
5. Ensure cross-platform compatibility (Windows/Linux/Mac)
