# Training Question Answerer

A modern, sleek sidebar helper application that uses OpenAI's vision and chat capabilities to help you answer training questions from screenshots or manual input.

## ✨ Features

- **🖥️ Screen Capture**: Full screen or click-and-drag region selection
- **📝 Question Extraction**: AI-powered question reading from screenshots
- **💡 Smart Answers**: Context-aware answers using loaded transcripts
- **🖱️ Auto-Click**: Automatically clicks the correct answer on screen (NEW!)
- **🎨 Modern UI**: Windows 11-style frosted glass design
- **📌 Stay on Top**: Pin the sidebar to keep it visible while working
- **⌨️ Keyboard Shortcuts**: Fast access to all features

## 🚀 Installation

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Setup Environment Variables

Create a `.env` file in `OpenAI-API/Environment-Variables/` with:

```
OPENAI_API_KEY=your_api_key_here
```

### 3. Run the Application

**GUI Mode (Recommended):**
```powershell
python gui.py
```

**CLI Mode:**
```powershell
python main.py
```

## 🎮 Usage

### GUI Controls

- **📁 Load Context**: Load a transcript file to provide context for answers (Ctrl+T)
- **🖥️ Full Screen**: Capture entire screen after 3-second delay (Ctrl+1)
- **✂️ Select Region**: Click and drag to select screen region (Ctrl+3)
- **⌨️ Type Question**: Manually type a question (Ctrl+4)
- **�️ Auto-Click**: Toggle automatic clicking of correct answers (Ctrl+A)
- **�📌 Pin**: Keep window always on top (Ctrl+P)
- **🗑️ Clear**: Clear output log (Ctrl+L)

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+1` | Full screen capture |
| `Ctrl+3` | Click & drag region |
| `Ctrl+4` | Type question |
| `Ctrl+T` | Load transcript |
| `Ctrl+P` | Toggle pin |
| `Ctrl+L` | Clear output |
| `Esc` | Cancel operation |

## 🎨 Design Features

### Modern Windows 11 Style
- **Frosted Glass Effect**: Acrylic/Mica background blur (requires `pywinstyles`)
- **Custom Scrollbars**: Sleek, minimal scrollbar design
- **Smooth Animations**: Hover effects and transitions
- **Dark Mode**: Eye-friendly color scheme optimized for long sessions

### Sidebar Layout
- **400px Width**: Perfect for side-by-side with study materials
- **Auto-Position**: Opens on right side of screen
- **Resizable**: Minimum 350x700, scales to your preference
- **Compact**: Efficient use of vertical space

## 🔧 Configuration

### Colors
Edit the color scheme in `gui.py`:
```python
self.bg_color = "#1a1a1a"          # Main background
self.accent_color = "#0078d4"      # Windows 11 blue
self.success_color = "#6cc644"     # Success messages
self.error_color = "#f85149"       # Error messages
self.warning_color = "#ffa657"     # Warnings
```

### Window Position
The window auto-positions on the right side. To change:
```python
x_position = screen_width - 420  # Adjust this value
y_position = 50                   # Adjust this value
```

## �️ Auto-Click Feature

The auto-click feature uses OCR to automatically find and click the correct answer on your screen!

### Additional Setup for Auto-Click:
1. Install Python package: `pip install pytesseract`
2. Install Tesseract-OCR: https://github.com/UB-Mannheim/tesseract/wiki
3. Toggle on with the **"🖱️ Auto-Click"** button or press `Ctrl+A`

**How it works:**
- AI determines the correct answer
- Returns ONLY the option text (e.g., "Machine Learning")
- OCR finds that text on your screen
- Automatically clicks it after 1-second delay

📖 **Full guide:** See `AUTO_CLICK_GUIDE.md` for detailed instructions and troubleshooting

## �📋 System Requirements

- **Windows 10/11** (for frosted glass effects)
- **Python 3.8+**
- **OpenAI API Key**
- **Screen resolution**: 1280x720 or higher recommended

## 🐛 Troubleshooting

### "Sorry, I can't assist with that"
- The screenshot may contain sensitive information
- Try capturing a smaller, more specific region
- Use "Type Question" mode to manually enter the question
- Check `debug_screenshot.png` to see what was captured

### Frosted Glass Not Working
- Ensure `pywinstyles` is installed: `pip install pywinstyles`
- Requires Windows 10/11
- App will still work without effects

### Window Closes After Screenshot
- Fixed in current version
- Check console for `[DEBUG]` messages
- Report any errors with stack traces

## 📝 How It Works

1. **Load Context**: Upload a transcript/study material text file
2. **Capture**: Take a screenshot of the question
3. **Extract**: AI reads and extracts the question text
4. **Answer**: AI generates answer using transcript context
5. **Review**: Answer appears in output log

## 🔐 Privacy

- Screenshots are processed in memory
- Only sent to OpenAI API for question extraction
- Debug screenshots saved locally as `debug_screenshot.png`
- No data stored or transmitted elsewhere

## 🎯 Tips

- **Pin the window** (Ctrl+P) while studying
- **Load transcript first** for better context-aware answers
- **Use click & drag** for precise question selection
- **Clear output regularly** to reduce clutter
- **Check status indicator** (●) for current operation state

## 📦 Project Structure

```
TrainingAnswerer/
├── gui.py                 # Modern GUI application
├── main.py                # CLI application
├── screen_reader.py       # Screenshot capture logic
├── openai_answerer.py     # OpenAI API integration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review console output for `[DEBUG]` messages
3. Ensure all dependencies are installed
4. Verify OpenAI API key is set correctly

## 📄 License

Part of the OpenAI-Api-Shenanigans repository.

---

**Made with ❤️ for efficient learning**
