"""
Build script for creating Training Q&A Helper executable
"""
import PyInstaller.__main__
import os
import shutil
from pathlib import Path

# Get the directory of this script
script_dir = Path(__file__).parent

# Check if Tesseract-OCR is installed
tesseract_default_path = Path("C:/Program Files/Tesseract-OCR")
tesseract_exe = tesseract_default_path / "tesseract.exe"

bundle_tesseract = tesseract_exe.exists()

print("="*60)
print("Building Training Q&A Helper")
print("="*60)

if bundle_tesseract:
    print(f"\n✓ Tesseract-OCR found at: {tesseract_default_path}")
    print("  Will bundle Tesseract with the executable")
    print("  (adds ~50MB but enables auto-click for users)")
else:
    print(f"\n⚠ Tesseract-OCR not found at: {tesseract_default_path}")
    print("  Auto-click will require separate Tesseract installation")
    print("  (executable will be smaller but less convenient)")

print("\nBuilding executable...\n")

# Base PyInstaller arguments
pyinstaller_args = [
    'gui.py',
    '--name=TrainingQA-Helper',
    '--onefile',
    '--windowed',
    '--icon=NONE',
    '--hidden-import=pywinstyles',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=pytesseract',
    '--collect-all=pywinstyles',
    '--clean',
    '--noconfirm',
]

# Add Tesseract binaries if available
if bundle_tesseract:
    # Bundle the entire Tesseract-OCR directory
    tesseract_data = f"{tesseract_default_path};tesseract"
    pyinstaller_args.append(f'--add-data={tesseract_data}')
    print(f"[PyInstaller] Adding Tesseract data: {tesseract_data}")

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print("\n" + "="*60)
print("✓ Build complete!")
print("="*60)
print(f"\nExecutable location: {script_dir / 'dist' / 'TrainingQA-Helper.exe'}")

if bundle_tesseract:
    print("\n✓ Tesseract-OCR is bundled!")
    print("  Users can use auto-click without installing Tesseract")
else:
    print("\n⚠ Tesseract-OCR is NOT bundled")
    print("  Users will need to install Tesseract separately for auto-click")
    print("  See TESSERACT_INSTALL.md for instructions")

print("\n📋 For distribution, include these files:")
print("  1. TrainingQA-Helper.exe")
print("  2. .env file with API key (or .env.template)")
print("  3. README.md (optional)")
print("  4. TESSERACT_INSTALL.md (if Tesseract not bundled)")
print("\nDone! 🎉\n")
