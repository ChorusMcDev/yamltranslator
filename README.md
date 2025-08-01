# YAML Translator Tool v1.0.1

## 🎯 Overview
The YAML Translator Tool is a comprehensive, user-friendly application designed to facilitate the translation and formatting of YAML configuration files. It provides functionalities to translate text, convert text to small caps, and reverse text values while preserving placeholders and special formatting. This tool is particularly useful for developers and system administrators who work with YAML files and need to manage localization or formatting tasks efficiently.

## ✨ Features
- **🌐 AI-Powered Translation**: Translate YAML files into 25+ languages using OpenAI's GPT models
- **🔤 Smart Formatting**: Convert text values to small caps while preserving placeholders and color codes
- **🔄 Intelligent Reversing**: Convert small caps back to normal text
- **🔑 Professional Licensing**: Secure Cryptolens-based license management system
- **⚙️ Configurable Settings**: Customize API settings, file handling, and UI preferences
- **📊 Detailed Telemetry**: Track performance with comprehensive batch and timing information
- **💾 History Tracking**: Keep track of all translations and operations
- **🔐 Secure API Key Storage**: Encrypted storage of OpenAI API keys
- **📁 Flexible File Selection**: Multiple ways to select and process files
- **🎨 Beautiful UI**: Enhanced console interface with emojis and colors

## 🔑 Licensing System

This application includes a professional licensing system powered by Cryptolens:

- **Secure License Validation**: Server-side validation with RSA signature verification
- **Machine Binding**: Licenses are tied to specific device identifiers
- **Feature Protection**: Core features require valid license activation
- **License Management**: Built-in license management interface (Menu Option 6)

### Getting Your License

1. **Purchase**: Visit [yamltranslator.com](https://yamltranslator.com) to purchase a license
2. **Machine Code**: Use the application to get your unique machine code
3. **Activation**: Enter your license key through the License Management menu
4. **Verification**: The system automatically validates your license online

For detailed licensing information, see [LICENSING_INTEGRATION.md](LICENSING_INTEGRATION.md).

## 🏗️ Build & Release System

### Automated Builds

This project features a fully automated CI/CD pipeline using GitHub Actions:

- **Automatic Builds**: Every push to `main` or `develop` triggers a build
- **Cross-Platform**: Builds are generated for both Windows x64 and Linux x64
- **Version Management**: Automatic version numbering with format `1.0.1-{build_number}`
- **Pre-Release Publishing**: Automatic pre-release creation with downloadable executables
- **Artifact Management**: Old pre-releases are automatically cleaned up (keeps latest 5)

### Download Pre-Built Executables

1. Visit the [Releases](https://github.com/ChorusMcDev/yamltranslator/releases) page
2. Look for the latest pre-release version
3. Download the appropriate executable:
   - **Windows**: `YAMLTranslator-windows-x64.exe`
   - **Linux**: `YAMLTranslator-linux-x64`

### Build Process

The automated build process:
1. **Version Generation**: Creates version string like `1.0.1-42` (base version + build number)
2. **File Updates**: Updates version in spec files and source code
3. **Cross-Platform Build**: Uses PyInstaller to create standalone executables
4. **Testing**: Validates executables can run and show version info
5. **Release Creation**: Publishes pre-release with both executables attached
6. **Cleanup**: Removes old pre-releases to keep repository clean

### Manual Building

To build locally:

```bash
# Windows
build.bat

# Linux/Mac
chmod +x build.sh && ./build.sh
```

## 🏗️ Project Structure
```
yaml-translator-tool/
├── src/
│   ├── main.py                # 🚀 Entry point for the application
│   ├── core/
│   │   ├── __init__.py        # Package initialization
│   │   ├── translator.py      # 🌐 AI-powered translation functionality
│   │   ├── formatter.py       # 🔤 Small caps formatting functionality
│   │   └── reverser.py        # 🔄 Text reversal functionality
│   ├── utils/
│   │   ├── __init__.py        # Package initialization
│   │   ├── menu.py            # 🎨 Enhanced menu and user interface
│   │   └── telemetry.py       # 📊 Performance tracking and logging
│   ├── config/
│   │   ├── __init__.py        # Package initialization
│   │   └── settings.py        # ⚙️ Configuration and settings management
│   └── license_system/        # 🔑 Licensing system
│       ├── __init__.py        # Package initialization
│       ├── license_manager.py # License validation and management
│       └── license_menu.py    # Interactive license interface
├── requirements.txt           # 📦 Project dependencies
├── YAMLTranslator.spec        # 🔧 PyInstaller build configuration
├── build.bat                  # 🪟 Windows build script
├── build.sh                   # 🐧 Linux/Mac build script
├── LICENSING_INTEGRATION.md   # 🔑 Licensing documentation
└── README.md                  # 📖 Project documentation
```

## 🚀 Quick Start

### Method 1: Run from Source
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd yaml-translator-tool
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python src/main.py
   ```

### Method 2: Build Single Executable
1. **Windows:**
   ```cmd
   build.bat
   ```

2. **Linux/Mac:**
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

3. **Run the executable:**
   - Windows: `dist\YAMLTranslator.exe`
   - Linux/Mac: `./dist/YAMLTranslator`

## 🎮 Usage

### First Time Setup
1. Start the application
2. Select "🌐 Translate YAML File" for your first translation
3. When prompted, enter your OpenAI API key
4. Choose to save the API key for future use

### Main Menu Options
- **🌐 Translate YAML File**: AI-powered translation to any supported language
- **🔤 Convert YAML to Small Caps**: Format text with small caps while preserving placeholders
- **🔄 Reverse Small Caps**: Convert small caps back to normal text
- **⚙️ Settings & Configuration**: Customize application behavior
- **📊 View Translation History**: Review past operations

### File Selection
The tool offers multiple ways to select files:
1. **Manual Input**: Type the file path directly
2. **Directory Browser**: Browse and select from current directory
3. **Drag & Drop**: Paste a file path (copy from file explorer)

### Supported Languages
The tool supports translation to 25+ languages including:
- European: English, Spanish, French, German, Italian, Polish, Russian, etc.
- Asian: Chinese, Japanese, Korean, Hindi, Thai, Vietnamese, etc.
- Others: Arabic, Hebrew, Turkish, Dutch, Swedish, and many more

## ⚙️ Configuration

### Settings Categories
- **API Settings**: Model selection, batch size, timeout, retries
- **File Settings**: Auto-backup, output naming, file size limits
- **UI Settings**: Progress display, logging verbosity
- **History Settings**: Auto-save, maximum entries

### Environment Variables
You can also set your API key as an environment variable:
```bash
# Windows
set OPENAI_API_KEY=your_key_here

# Linux/Mac
export OPENAI_API_KEY=your_key_here
```

## 📊 Features in Detail

### Translation
- Preserves all YAML placeholders (`{value}`, `%player%`, `&7`, etc.)
- Batch processing for efficiency
- Real-time progress tracking
- Comprehensive error handling
- Automatic backup creation

### Formatting
- Converts text to small caps Unicode characters
- Preserves color codes and placeholders
- Handles complex nested YAML structures
- Preview functionality

### Telemetry
- Detailed timing for each batch
- API request time tracking
- File operation performance
- Final summary with statistics

## 🔧 Dependencies
- **PyYAML**: YAML file parsing and generation
- **openai**: OpenAI API integration
- **more-itertools**: Enhanced iteration utilities
- **cryptography**: Secure API key storage
- **pathlib**: Modern path handling

## 🏗️ Building Executable

### Requirements
- Python 3.7+
- PyInstaller (automatically installed by build scripts)

### Build Process
The build scripts automatically:
1. Install required dependencies
2. Install PyInstaller
3. Build single executable
4. Test the executable

### Customization
Edit `YAMLTranslator.spec` to customize the build:
- Add/remove hidden imports
- Include additional data files
- Exclude unnecessary modules
- Add application icon

## 🐛 Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Verify your OpenAI API key is valid
3. **File Not Found**: Check file paths and permissions
4. **Build Failures**: Ensure PyInstaller is compatible with your Python version

### Debug Mode
Run with detailed logging by modifying settings or using verbose output.

## 🤝 Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support
For issues, questions, or contributions, please create an issue in the repository or contact the maintainers.

---

**🎉 Happy Translating!** 🌐✨
Follow the on-screen menu to select the desired operation (translation, formatting, or reversing).

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the GNU License. See the LICENSE file for more details.
