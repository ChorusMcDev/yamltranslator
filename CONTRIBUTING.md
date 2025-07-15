# Contributing to YAML Translator Tool

Thank you for your interest in contributing to the YAML Translator Tool! We welcome contributions from everyone.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Test your changes thoroughly
6. Submit a pull request

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ChorusMcDev/yamltranslator.git
   cd yamltranslator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python src/main.py
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Add comments for complex logic

## Project Structure

```
src/
├── main.py              # Application entry point
├── core/                # Core functionality modules
│   ├── translator.py    # AI translation logic
│   ├── formatter.py     # Small caps conversion
│   └── reverser.py      # Small caps reversal
├── utils/               # Utility modules
│   ├── menu.py          # User interface
│   └── telemetry.py     # Performance tracking
└── config/              # Configuration management
    └── settings.py      # Settings and encryption
```

## Testing

Before submitting a pull request, please test your changes:

1. **Manual Testing:**
   - Test all menu options
   - Test with various YAML files
   - Test error handling scenarios

2. **Build Testing:**
   - Test the build process works
   - Verify the executable functions correctly

## Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Update the README.md** if needed
3. **Ensure your code follows** the existing style
4. **Write clear commit messages**
5. **Link any relevant issues** in your PR description

## Bug Reports

When filing a bug report, please include:

- Your operating system and Python version
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Any error messages or logs
- Sample YAML files if relevant

## Feature Requests

We welcome feature requests! Please:

- Check if the feature already exists or is planned
- Describe the use case and benefits
- Consider if it fits with the project's goals
- Be willing to help implement it

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment for everyone

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the "question" label
- Start a discussion in the GitHub Discussions section

Thank you for contributing to make YAML Translator Tool better!
