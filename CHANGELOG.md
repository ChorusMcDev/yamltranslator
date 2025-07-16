# Changelog

All notable changes to the YAML Translator Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-07-16

### Enhanced
- 🎯 **Improved Small Caps Formatting Preservation**: Enhanced the placeholder preservation system to support ANY XML-like tags
- 🏷️ **Universal Tag Support**: Now preserves all `<tag>` and `<tag:value>` patterns instead of specific hardcoded ones
- 🎮 **Gaming Format Support**: Better support for Minecraft and gaming formatting codes like `<shift:-8>`, `<glyph:skills_gui>`, `<#color>` etc.
- 🔧 **Simplified Regex Pattern**: Changed from multiple specific patterns to a single universal `<[^>]*>` pattern

### Fixed
- 🐛 **Formatter Module**: Fixed placeholder preservation to handle any custom XML-like tags
- 🔄 **Reverser Module**: Updated reversal logic to match the improved formatting preservation
- 📝 **Pattern Matching**: Eliminated duplicate pattern definitions and improved consistency

### Technical Improvements
- **Regex Pattern**: Updated from `<#[^>]*>|<[0-9]+>|<shift:[^>]*>|<glyph:[^>]*>` to universal `<[^>]*>`
- **Test Coverage**: Added comprehensive test suite with 18+ test cases covering various tag formats
- **Round-trip Testing**: Verified that all formatting elements survive conversion to small caps and back
- **Future-proof Design**: New pattern automatically supports any future XML-like tag formats

### Developer Experience
- 🧪 **Enhanced Testing**: Added `test_all_tags.py` with comprehensive formatting preservation tests
- 📚 **Documentation**: Updated Copilot instructions for improved AI-assisted development
- 🔍 **Pattern Analysis**: Better understanding of formatting preservation requirements

## [1.0.0] - 2025-07-15

### Added
- 🎉 Initial release of YAML Translator Tool
- 🌐 AI-powered YAML translation using OpenAI GPT models
- 🔤 Small caps Unicode conversion functionality  
- 🔄 Small caps reversal back to normal text
- ⚙️ Runtime configuration system for all settings
- 💾 Encrypted API key storage using cryptography library
- 📊 Comprehensive telemetry and performance tracking
- 🎯 Batch processing for efficient handling of large files
- 🛡️ Placeholder preservation during translation (formatting codes, variables, etc.)
- 📁 Smart file management with backups and progress saving
- 🎨 Beautiful console UI with emojis and color coding
- 📋 Multiple file selection methods (browse, drag & drop, manual entry)
- 🌍 Support for 25+ languages including major world languages
- 📈 Translation history and operation analytics
- 🔧 Single executable build support with PyInstaller
- 🐧 Cross-platform support (Windows, Linux, Mac)

### Features
- **Translation Engine**: Advanced AI translation with retry logic and error handling
- **File Processing**: YAML structure preservation with flatten/unflatten operations
- **User Interface**: Interactive menu system with progress indicators
- **Configuration Management**: JSON-based settings with import/export capability
- **Security**: Encrypted API key storage for security
- **Performance**: Batch processing with detailed timing and progress tracking
- **Compatibility**: Fallback implementations for graceful degradation

### Technical Details
- **Dependencies**: PyYAML, OpenAI, more-itertools, cryptography
- **Build System**: PyInstaller with custom spec file for single executable
- **Architecture**: Modular design with separation of concerns
- **Error Handling**: Comprehensive error handling and user feedback
- **Logging**: Detailed operation logging and telemetry collection

### Initial Components
- `src/main.py` - Application entry point with dependency checking
- `src/core/translator.py` - AI translation module with OpenAI integration
- `src/core/formatter.py` - Small caps conversion functionality
- `src/core/reverser.py` - Small caps reversal functionality  
- `src/utils/menu.py` - Interactive user interface and file selection
- `src/utils/telemetry.py` - Performance tracking and operation history
- `src/config/settings.py` - Configuration management and encrypted storage
- Build scripts for Windows (`build.bat`) and Unix (`build.sh`)
- PyInstaller configuration (`YAMLTranslator.spec`)

---

## How to Read This Changelog

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes
