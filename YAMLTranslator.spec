# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Build configuration
app_name = 'YAMLTranslator'
version = '1.0.2-dev'  # This will be updated by GitHub Actions
main_script = 'src/main.py'
icon_file = None  # Can be added later if needed

# Get the directory containing this spec file
spec_dir = Path(SPECPATH)
src_dir = spec_dir / 'src'

# Data files to include
datas = []

# Hidden imports for PyInstaller
hiddenimports = [
    'yaml',
    'openai',
    'more_itertools',
    'licensing',
    'licensing.methods',
    'licensing.models',
    'cryptography',
    'cryptography.fernet',
    'pathlib',
    'json',
    'os',
    'sys',
    'time',
    'datetime',
    'base64',
    'getpass',
    'urllib',
    'urllib.request',
    'urllib.parse',
    'ssl',
]

# Additional module paths
pathex = [
    str(spec_dir),
    str(src_dir),
]

# Collect all Python files from src directory
def collect_src_files():
    """Collect all Python files from the src directory."""
    src_files = []
    for py_file in src_dir.rglob('*.py'):
        if py_file.name != '__pycache__':
            rel_path = py_file.relative_to(spec_dir)
            src_files.append(str(rel_path))
    return src_files

# Include all source files
src_files = collect_src_files()

a = Analysis(
    [main_script],
    pathex=pathex,
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'pygame',
        'wx',
        'PySide2',
        'PyQt5',
        'test',
        'unittest',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove duplicate entries
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
    version_file=None,  # Could add version file for Windows
)

# Build info
print(f"Building {app_name} v{version}...")
print(f"Main script: {main_script}")
print(f"Source directory: {src_dir}")
print(f"Hidden imports: {len(hiddenimports)} modules")
print(f"Source files included: {len(src_files)}")
