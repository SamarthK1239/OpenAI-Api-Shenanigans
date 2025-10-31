# Installing Tesseract-OCR for Auto-Click

## 🔧 Quick Install (Windows)

### Step 1: Download Tesseract-OCR

**Direct download link:**
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe

**Or visit:**
https://github.com/UB-Mannheim/tesseract/wiki

### Step 2: Run the Installer

1. Double-click the downloaded `.exe` file
2. **IMPORTANT**: During installation, note the installation path:
   - Default: `C:\Program Files\Tesseract-OCR`
   - Or choose your own location
3. Complete the installation

### Step 3: Verify Installation

Open PowerShell and run:
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

You should see:
```
tesseract 5.3.3
```

### Step 4: Restart Your Application

Close and restart:
- Your PowerShell/terminal
- VS Code (if using)
- The Python application

### Step 5: Test Auto-Click

Run the GUI and press `Ctrl+A` to enable auto-click!

---

## 🔧 If Tesseract is in a Different Location

If you installed Tesseract somewhere other than the default location, you need to tell Python where it is.

**Option 1: Add to PATH (Recommended)**

1. Press `Win + X`, select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", find "Path", click "Edit"
5. Click "New" and add: `C:\Your\Tesseract\Path`
6. Click OK, OK, OK
7. Restart terminal/IDE

**Option 2: Set Path in Code**

Add this to the top of `screen_reader.py` (after imports):

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Your\Custom\Path\tesseract.exe'
```

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Downloaded Tesseract-OCR installer (not just pytesseract)
- [ ] Ran the `.exe` installer
- [ ] Noted the installation path
- [ ] Can run `tesseract --version` in terminal
- [ ] Restarted terminal/IDE
- [ ] Python app shows "✓ Tesseract-OCR found and ready"

---

## 🐛 Troubleshooting

### "tesseract is not installed or it's not in your PATH"

**Cause**: Python can't find the Tesseract executable

**Solutions**:
1. Make sure you installed Tesseract-OCR (the executable, not just pytesseract)
2. Check if it's in the default location: `C:\Program Files\Tesseract-OCR\tesseract.exe`
3. Add Tesseract to your PATH (see above)
4. Or set `pytesseract.pytesseract.tesseract_cmd` in code

### "pytesseract installed but Tesseract-OCR engine not found"

**This is your current issue!**

You have pytesseract (✅) but not Tesseract-OCR (❌)

**Solution**: Install from link above

### Installer says "Already installed"

Tesseract might be installed but not in PATH:

1. Search your PC for `tesseract.exe`
2. Once found, add that folder to PATH
3. Or set the path in code

---

## 📦 Complete Setup Commands

```powershell
# 1. Install Python package (already done ✅)
pip install pytesseract

# 2. Download and install Tesseract-OCR
# Visit: https://digi.bib.uni-mannheim.de/tesseract/
# Run the installer

# 3. Verify installation
tesseract --version

# 4. Run your app
cd "F:\GitHub Repos\OpenAI-Api-Shenanigans\OpenAI-API\TrainingAnswerer"
python gui.py
```

---

## 🎯 After Installation

Once Tesseract is installed correctly, you'll see:
```
✓ Tesseract-OCR found and ready
✓ pywinstyles loaded - frosted glass effects enabled
```

Then auto-click will work! 🚀

---

## 💡 Quick Links

- **Windows Installer**: https://digi.bib.uni-mannheim.de/tesseract/
- **All Releases**: https://github.com/UB-Mannheim/tesseract/wiki
- **Documentation**: https://tesseract-ocr.github.io/

---

**Need help?** Check `AUTO_CLICK_DEBUG.md` for more troubleshooting tips!
