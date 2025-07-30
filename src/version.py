"""
Version information for YAML Translator Tool
This file is automatically updated during the build process
"""

__version__ = "1.0.1-dev"
__build_number__ = "0"
__build_date__ = "Unknown"

def get_version():
    """Get the full version string."""
    return __version__

def get_version_info():
    """Get detailed version information."""
    return {
        'version': __version__,
        'build_number': __build_number__,
        'build_date': __build_date__
    }

def print_version():
    """Print version information."""
    print(f"YAML Translator Tool v{__version__}")
    if __build_number__ != "0":
        print(f"Build: {__build_number__}")
    if __build_date__ != "Unknown":
        print(f"Built: {__build_date__}")
