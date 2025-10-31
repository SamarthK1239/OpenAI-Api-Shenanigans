# Building Training Q&A Helper Executable

## Prerequisites

Install PyInstaller:
```powershell
pip install pyinstaller
```

**Optional but Recommended - Install Tesseract-OCR:**
If you want auto-click to work out-of-the-box for users, install Tesseract first:
```
Download from: https://digi.bib.uni-mannheim.de/tesseract/
Install to: C:\Program Files\Tesseract-OCR (default location)
```

The build script will automatically detect and bundle Tesseract if found!

## Method 1: Using the Build Script (Recommended)

Simply run:
```powershell
python build_exe.py
```

The script will:
- ✅ Detect if Tesseract-OCR is installed
- ✅ Bundle it automatically if found (~50MB extra)
- ✅ Show you what's being included
- ✅ Create the executable in `dist/` folder

**With Tesseract bundled:**
```
✓ Tesseract-OCR found at: C:/Program Files/Tesseract-OCR
  Will bundle Tesseract with the executable
  (adds ~50MB but enables auto-click for users)
```

**Without Tesseract:**
```
⚠ Tesseract-OCR not found at: C:/Program Files/Tesseract-OCR
  Auto-click will require separate Tesseract installation
  (executable will be smaller but less convenient)
```

## Method 2: Using Batch File (Easiest)

Just double-click:
```
build_simple.bat
```

## Method 3: Manual PyInstaller Command

```powershell
pyinstaller --name=TrainingQA-Helper --onefile --windowed --hidden-import=pywinstyles --hidden-import=PIL._tkinter_finder --collect-all=pywinstyles gui.py
```

## After Building

### 1. Locate Your Executable
The `.exe` file will be in: `dist/TrainingQA-Helper.exe`

### 2. Setup Environment Variables

**IMPORTANT**: Place your `.env` file in the **same directory** as the executable!

Create this structure:
```
TrainingQA-Helper.exe
.env                    ← Your API key file (same folder!)
```

**OR** create a subfolder structure:
```
TrainingQA-Helper.exe
Environment-Variables/
    .env
```

Your `.env` file should contain:
```
OPENAI_API_KEY=your-api-key-here
```

The app will automatically search for the `.env` file in:
1. Same folder as the `.exe` (recommended for distribution)
2. `Environment-Variables/.env` subfolder
3. `../Environment-Variables/.env` (for development)

### 3. Optional: Include Transcript Files
You can bundle transcript files for easy access:
```
TrainingQA-Helper.exe
Environment-Variables/
    .env
transcripts/
    GenAITranscript.txt
    OtherTranscript.txt
```

## 🎯 Tesseract Bundling

### Why Bundle Tesseract?

**Without bundling:**
- ❌ Users must install Tesseract separately
- ❌ Extra setup steps
- ❌ Auto-click won't work out-of-the-box
- ✅ Smaller executable (~40-50MB)

**With bundling:**
- ✅ Auto-click works immediately
- ✅ No extra installation needed
- ✅ Better user experience
- ❌ Larger executable (~90-100MB)

### How to Bundle Tesseract

1. **Install Tesseract** on your build machine:
   ```
   Download: https://digi.bib.uni-mannheim.de/tesseract/
   Install to: C:\Program Files\Tesseract-OCR
   ```

2. **Run the build script**:
   ```powershell
   python build_exe.py
   ```

3. **The script automatically detects and bundles it!**

### Verify Bundling

After building, check the output:
```
✓ Tesseract-OCR is bundled!
  Users can use auto-click without installing Tesseract
```

### Manual Bundling (Advanced)

If Tesseract is in a custom location, edit `build_exe.py`:
```python
tesseract_default_path = Path("C:/Your/Custom/Path/Tesseract-OCR")
```

## Distribution

### If Tesseract is Bundled:
```
dist/
  └── TrainingQA-Helper.exe    (~90-100MB)
```

Users need:
- ✅ Just the `.exe` file
- ✅ `.env` file with API key
- ✅ **Auto-click works immediately!**

### If Tesseract is NOT Bundled:
```
dist/
  ├── TrainingQA-Helper.exe    (~40-50MB)
  └── TESSERACT_INSTALL.md     (instructions)
```

Users need:
- ✅ The `.exe` file
- ✅ `.env` file with API key
- ⚠️ **Must install Tesseract separately for auto-click**

### Distribution Checklist:
- ✅ `TrainingQA-Helper.exe`
- ✅ `.env` file (or `.env.template`)
- ✅ `README.md` (optional - user guide)
- ✅ `TESSERACT_INSTALL.md` (if not bundled)
- ⚠️ **WARNING**: Never share your API key publicly!

## Build Options Explained

- `--onefile`: Creates a single executable file
- `--windowed`: No console window (GUI only)
- `--hidden-import`: Includes modules that PyInstaller might miss
- `--collect-all`: Includes all pywinstyles files for frosted glass effects
- `--add-data`: Bundles external files/folders (like Tesseract)
- `--clean`: Clean PyInstaller cache before building
- `--noconfirm`: Overwrite output without asking

## Troubleshooting

### Issue: "Module not found" errors
**Solution**: Add the missing module with `--hidden-import=module_name`

### Issue: Frosted glass effects not working
**Solution**: Make sure `--collect-all=pywinstyles` is included

### Issue: .env file not found
**Solution**: Ensure the folder structure is correct:
```
dist/
    TrainingQA-Helper.exe
    Environment-Variables/
        .env
```

### Issue: Large file size
**Solution**: This is normal. The single-file executable includes:
- Python interpreter
- All dependencies (OpenAI, PIL, tkinter, pywinstyles, etc.)
- Typical size: 40-80 MB

## Advanced: Custom Icon

To add a custom icon:

1. Get an `.ico` file
2. Modify the build command:
```powershell
pyinstaller --name=TrainingQA-Helper --onefile --windowed --icon=myicon.ico --hidden-import=pywinstyles --collect-all=pywinstyles gui.py
```

Or update `build_exe.py`:
```python
'--icon=myicon.ico',
```

## Creating a Portable Package

For easy distribution, create a ZIP file:
```
TrainingQA-Helper-v1.0.zip
├── TrainingQA-Helper.exe
├── Environment-Variables/
│   └── .env.template (without actual API key)
├── transcripts/ (optional)
│   └── sample.txt
└── README.txt (usage instructions)
```

## Security Note

⚠️ **IMPORTANT**: The `.env` file with your API key should NEVER be included in public distributions. Users should add their own API key.

Create an `.env.template` instead:
```
OPENAI_API_KEY=paste-your-key-here
```

## Quick Reference

| Method | Command | Difficulty |
|--------|---------|-----------|
| Batch File | Double-click `build_simple.bat` | Easiest ⭐ |
| Python Script | `python build_exe.py` | Easy |
| Manual | Full PyInstaller command | Advanced |

---

**Ready to build?** Just double-click `build_simple.bat` and you're done! 🚀
