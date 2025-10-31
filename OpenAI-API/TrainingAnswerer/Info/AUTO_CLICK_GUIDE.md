# Auto-Click Feature Guide

## 🖱️ What is Auto-Click?

The auto-click feature automatically finds and clicks the correct answer option on your screen after the AI determines which one is correct.

## ✨ How It Works

1. **Capture** a screenshot containing the question and answer options
2. **AI analyzes** the question using your transcript context
3. **AI returns** ONLY the exact text of the correct option (e.g., "Machine Learning")
4. **OCR scans** your screen using **EXACT matching** to find that text
5. **Auto-clicks** on the correct answer!

**🎯 Exact Matching**: The system uses strict exact matching to prevent false clicks. The text must match **exactly** (case-insensitive) - no partial matches accepted. See `EXACT_MATCHING.md` for details.

## 🚀 Setup

### 1. Install Python Package
```powershell
pip install pytesseract
```

### 2. Install Tesseract-OCR
Download and install from:
https://github.com/UB-Mannheim/tesseract/wiki

**Default install path:** `C:\Program Files\Tesseract-OCR\tesseract.exe`

### 3. Configure Path (if needed)
If installed in a non-default location, add to your script:
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Your\Path\tesseract.exe'
```

## 🎮 Usage

### Enable Auto-Click
1. Click the **"🖱️ Auto-Click: OFF"** button (or press `Ctrl+A`)
2. Status changes to **"🖱️ Auto-Click: ON"**
3. Now when you capture screenshots, it will auto-click!

### Workflow
```
1. Toggle auto-click ON (Ctrl+A)
2. Capture screenshot (Ctrl+1, Ctrl+3, or Ctrl+4)
3. AI finds the answer
4. AI returns ONLY the correct option text
5. OCR finds that text on screen
6. Auto-clicks after 1 second delay
7. ✓ Answer selected!
```

## 💡 Tips for Best Results

### ✅ DO:
- **Keep answer options visible** on screen after capturing
- **Use clear, readable fonts** in your training interface
- **Ensure good contrast** between text and background
- **Position windows** so options are unobstructed
- **Wait for the click** - there's a 1-second safety delay

### ❌ DON'T:
- Cover the answer options with other windows
- Minimize the training window after capturing
- Use very small font sizes (OCR works better with larger text)
- Move the mouse during auto-click countdown

## 🔧 How the AI is Prompted

### Regular Mode (Auto-Click OFF):
```
Returns: Full explanation with context and reasoning
Example: "The correct answer is Machine Learning. This is because 
the transcript mentions that ML algorithms learn from data..."
```

### Auto-Click Mode (Auto-Click ON):
```
Returns: ONLY the exact option text
Example: "Machine Learning"
```

The system prompt changes to:
> "Return ONLY the exact text of the correct answer option. 
> Do not include explanations, letters (A/B/C/D), or any other text."

## 🐛 Troubleshooting

### "OCR not available" Error
**Problem:** pytesseract not installed  
**Solution:** Run `pip install pytesseract`

### "Tesseract not found" Error
**Problem:** Tesseract-OCR not installed or not in PATH  
**Solution:** 
1. Download from https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location
3. Restart your terminal/IDE

### "Could not find text on screen"
**Problem:** OCR can't locate the option text  
**Solutions:**
- Make sure the answer options are fully visible
- Check that no windows are covering them
- Try capturing a cleaner screenshot
- Verify the text matches exactly (case-sensitive)
- Increase font size if possible

### Clicks the Wrong Location
**Problem:** Multiple instances of the same text on screen  
**Solution:** 
- OCR finds the FIRST match from top-left
- Hide or minimize duplicate text
- Make sure the question interface is in the foreground

### Works but Doesn't Click
**Problem:** 1-second delay might seem like nothing is happening  
**Solution:** Watch the output log - it shows:
```
🔍 Searching for text: 'Your Answer'
✓ Found text at (x, y)
⏱️ Clicking in 1 seconds...
✓ Clicked at (x, y)
```

## 🎯 Best Practices

### For Multiple Choice Questions:
1. **Capture the full question** including all options
2. **Keep options visible** after capturing
3. **Enable auto-click** before starting a quiz session
4. **Position your windows** so the helper doesn't cover answers

### For Training Sessions:
1. Enable auto-click at the start
2. Use `Ctrl+3` for fast region selection
3. Select just the question + options area
4. Let the app work its magic!
5. Watch for the green "✓ Successfully clicked!" message

## 📊 Success Rate

Auto-click works best when:
- ✅ Text is **12pt or larger**
- ✅ **High contrast** (dark text on light background or vice versa)
- ✅ **Sans-serif fonts** (Arial, Segoe UI, Helvetica)
- ✅ Options are **fully visible** and **unobstructed**
- ✅ **Standard text** (not handwritten or artistic fonts)

## 🔐 Safety Features

- **1-second delay** before clicking (time to cancel if needed)
- **Visual feedback** in output log at each step
- **Graceful failure** - if it can't find text, it just won't click
- **Can be toggled** on/off instantly with `Ctrl+A`

## 🎨 Example Output

```
🖱️ Auto-click enabled - finding answer on screen...
  Looking for: 'Machine Learning'

🔍 Searching for text: 'Machine Learning'
✓ Found text 'Machine Learning' at (850, 450)
⏱️ Clicking in 1 seconds...
✓ Clicked at (850, 450)
✓ Successfully clicked!
```

---

**Ready to automate your training quizzes?** Just press `Ctrl+A` and let the AI do the clicking! 🚀
