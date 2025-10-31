# Frosted Glass Customization Guide

## 🎨 The Best of Both Worlds

Your GUI now features **smart transparency** - the background has the beautiful frosted glass effect, while **all text and buttons remain at 100% opacity** for perfect readability!

## 🪟 How It Works

The `pywinstyles` library creates the frosted glass background effect **without** affecting the opacity of your UI elements. This means:

✅ **Background**: Beautiful frosted glass blur effect  
✅ **Text**: 100% sharp and readable  
✅ **Buttons**: Fully opaque and clear  
✅ **Best of both worlds**: Modern aesthetics + maximum usability

## 🎨 Customizing the Blur Style

You can change the blur effect type. Find this line in `gui.py` (~line 88):

```python
self.blur_amount = "acrylic"  # Options: "acrylic", "mica", "aero", "dark", "light"
```

**Available styles:**
- `"acrylic"` - Modern frosted glass (Windows 11 default) ⭐ **Recommended**
- `"mica"` - Subtle material effect (Windows 11)
- `"aero"` - Classic glass effect (Windows 7-style)
- `"dark"` - Dark theme with slight blur
- `"light"` - Light theme with slight blur
- `"auto"` - Matches Windows theme

**Example:**
```python
self.blur_amount = "mica"  # Subtle mica effect
```

## 🎯 Recommended Settings

### For Modern Windows 11 Look (Default)
```python
self.blur_amount = "acrylic"
```

### For Subtle Material Design
```python
self.blur_amount = "mica"
```

### For Classic Glass Effect
```python
self.blur_amount = "aero"
```

### For Dark Theme Blur
```python
self.blur_amount = "dark"
```

## 💡 Why This Approach is Better

**Previous approach** (using `-alpha`):
- ❌ Made EVERYTHING transparent (text, buttons, icons)
- ❌ Reduced readability
- ❌ Made UI elements harder to click

**New approach** (using `pywinstyles` only):
- ✅ Only background is frosted glass
- ✅ Text remains 100% opaque and sharp
- ✅ Buttons remain fully visible and clickable
- ✅ Perfect balance of aesthetics and usability

## 🔧 Troubleshooting

**Frosted glass not showing?**
- Make sure `pywinstyles` is installed: `pip install pywinstyles`
- Windows 10 (1903+) or Windows 11 required
- Check console for error messages

**Want to disable frosted glass entirely?**
- Uninstall pywinstyles: `pip uninstall pywinstyles`
- The app will work normally without effects

**Want to see through the window more?**
- Try different blur styles! Each has different transparency levels
- `"light"` and `"auto"` tend to be more transparent
- `"acrylic"` has a nice balance

## 📝 Quick Reference

| Style | Effect | Best For |
|-------|--------|----------|
| `acrylic` | Modern frosted glass | Windows 11 aesthetic |
| `mica` | Subtle material | Minimal distraction |
| `aero` | Classic glass | Nostalgic Win7 feel |
| `dark` | Dark blur | Dark themes |
| `light` | Light blur | Light themes |
| `auto` | System theme | Matching Windows |

---

**Enjoy crystal-clear text with beautiful frosted glass!** 🪟✨
