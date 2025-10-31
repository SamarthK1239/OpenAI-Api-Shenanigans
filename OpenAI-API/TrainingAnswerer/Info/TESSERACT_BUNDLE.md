# Bundling Tesseract with Your Executable - Quick Guide

## 📦 What Gets Bundled

When you build with Tesseract installed, PyInstaller bundles:
- ✅ `tesseract.exe` - The OCR engine
- ✅ `tessdata/` - Language data files
- ✅ Required DLLs - Dependencies
- ✅ Configuration files

**Total size: ~50MB additional**

## 🚀 Build Process

### Step 1: Install Tesseract
```
Download: https://digi.bib.uni-mannheim.de/tesseract/
Install to: C:\Program Files\Tesseract-OCR (default)
```

### Step 2: Build
```powershell
python build_exe.py
```

### Step 3: Check Output
```
✓ Tesseract-OCR found at: C:/Program Files/Tesseract-OCR
  Will bundle Tesseract with the executable
```

### Step 4: Test
```powershell
cd dist
.\TrainingQA-Helper.exe
```

You should see:
```
✓ Using bundled Tesseract: ...\tesseract\tesseract.exe
✓ Tesseract-OCR 5.3.3 found and ready
```

## 🎯 How It Works

### During Build:
1. `build_exe.py` checks for Tesseract at default location
2. If found, adds `--add-data` flag to PyInstaller
3. PyInstaller copies entire `Tesseract-OCR/` folder into the bundle
4. Executable size increases by ~50MB

### During Runtime:
1. App detects it's running as compiled executable (`sys.frozen`)
2. Looks for `tesseract/` in temporary extraction folder (`sys._MEIPASS`)
3. Sets `pytesseract.tesseract_cmd` to bundled exe path
4. Auto-click works without external installation!

## 📊 Size Comparison

| Build Type | Size | Auto-Click | User Setup |
|------------|------|------------|------------|
| Without Tesseract | ~40-50MB | ❌ Needs install | ⚠️ Extra steps |
| With Tesseract | ~90-100MB | ✅ Works immediately | ✅ Just run! |

## 🔧 Advanced: Custom Tesseract Location

If Tesseract is installed elsewhere, edit `build_exe.py`:

```python
# Around line 13
tesseract_default_path = Path("D:/MyPrograms/Tesseract-OCR")
```

Or use environment variable:
```python
tesseract_default_path = Path(os.getenv('TESSERACT_PATH', 'C:/Program Files/Tesseract-OCR'))
```

## 🎨 Distribution Options

### Option 1: Full Bundle (Recommended)
```
MyApp-v1.0-Full.zip
├── TrainingQA-Helper.exe    (~100MB)
├── .env.template
└── README.md
```

**Pros:**
- ✅ Works immediately
- ✅ Auto-click enabled
- ✅ Best user experience

**Cons:**
- ❌ Larger download (~100MB)
- ❌ Longer upload time

### Option 2: Lite Version
```
MyApp-v1.0-Lite.zip
├── TrainingQA-Helper.exe    (~45MB)
├── .env.template
├── README.md
└── TESSERACT_INSTALL.md
```

**Pros:**
- ✅ Smaller download
- ✅ Faster upload
- ✅ Still works (without auto-click)

**Cons:**
- ❌ Auto-click requires setup
- ❌ Extra user steps

### Option 3: Both Versions
Provide both downloads:
```
TrainingQA-Helper-v1.0-Full.exe    (100MB, auto-click ready)
TrainingQA-Helper-v1.0-Lite.exe    (45MB, requires Tesseract)
```

## 🔍 Verification

### Check if Tesseract is Bundled:

**Method 1: Run the app**
```powershell
dist\TrainingQA-Helper.exe
```
Look for: `✓ Using bundled Tesseract`

**Method 2: Extract and inspect**
```powershell
# PyInstaller creates temporary extraction folder
# Check %TEMP% while app is running
dir %TEMP%\_MEI*\tesseract
```

**Method 3: Check file size**
- Without Tesseract: ~40-50MB
- With Tesseract: ~90-100MB

## 🐛 Troubleshooting

### "Tesseract not found" after bundling

**Cause**: Bundle path detection failed

**Solution**: Check `gui.py` and `screen_reader.py`:
```python
if getattr(sys, 'frozen', False):
    bundle_dir = Path(sys._MEIPASS)
    tesseract_bundled = bundle_dir / 'tesseract' / 'tesseract.exe'
    
    if tesseract_bundled.exists():
        pytesseract.pytesseract.tesseract_cmd = str(tesseract_bundled)
        print(f"✓ Using bundled Tesseract: {tesseract_bundled}")
```

### Build fails with Tesseract errors

**Cause**: Permissions or path issues

**Solutions:**
1. Run build script as Administrator
2. Check Tesseract path has no special characters
3. Verify Tesseract is actually installed:
   ```powershell
   & "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
   ```

### Large executable size

**Expected**: With Tesseract, 90-100MB is normal

**To reduce:**
1. Build without Tesseract (remove/rename `C:\Program Files\Tesseract-OCR`)
2. Use `--exclude-module` for unused packages
3. Consider not using `--onefile` (create folder with DLLs)

## 📋 Build Checklist

Before building:
- [ ] Tesseract installed at `C:\Program Files\Tesseract-OCR`
- [ ] Can run: `tesseract --version`
- [ ] PyInstaller installed: `pip install pyinstaller`
- [ ] All dependencies installed: `pip install -r requirements.txt`

During build:
- [ ] See: "✓ Tesseract-OCR found"
- [ ] See: "Will bundle Tesseract"
- [ ] Build completes without errors

After build:
- [ ] Executable exists in `dist/`
- [ ] Size is ~90-100MB (if bundled)
- [ ] Test run shows bundled Tesseract message
- [ ] Auto-click works (press Ctrl+A)

## 🎯 Best Practices

1. **Always bundle for end users** - Better experience
2. **Provide lite version for developers** - Can install Tesseract themselves
3. **Document bundling status** in README
4. **Test on clean machine** without Tesseract installed
5. **Include TESSERACT_INSTALL.md** even if bundled (for reference)

---

**Result**: Users get a fully functional auto-click feature without any setup! 🎉
