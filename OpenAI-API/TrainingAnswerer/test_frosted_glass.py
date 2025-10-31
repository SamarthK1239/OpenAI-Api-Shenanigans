"""
Test script to verify pywinstyles installation and functionality
Run this to check if frosted glass effects can be applied
"""

import sys
import tkinter as tk

print("="*60)
print("Frosted Glass Effects Test")
print("="*60)

# Test 1: Check if pywinstyles is installed
print("\n1. Checking pywinstyles installation...")
try:
    import pywinstyles as pws
    print("   ✓ pywinstyles is installed")
    print(f"   Version: {pws.__version__ if hasattr(pws, '__version__') else 'Unknown'}")
except ImportError as e:
    print("   ✗ pywinstyles is NOT installed")
    print(f"   Error: {e}")
    print("\n   Install with: pip install pywinstyles")
    sys.exit(1)

# Test 2: Check Windows version
print("\n2. Checking Windows version...")
import platform
if platform.system() == "Windows":
    win_ver = platform.win32_ver()[0]
    print(f"   ✓ Running on Windows {win_ver}")
    if int(platform.win32_ver()[1].split('.')[0]) >= 10:
        print("   ✓ Windows 10+ detected - effects should work")
    else:
        print("   ⚠ Older Windows version - effects may not work")
else:
    print(f"   ✗ Not running on Windows (detected: {platform.system()})")
    print("   Frosted glass effects only work on Windows 10+")

# Test 3: Create a test window
print("\n3. Creating test window with frosted glass...")
try:
    root = tk.Tk()
    root.title("Frosted Glass Test")
    root.geometry("400x300")
    root.configure(bg="#1a1a1a")
    
    label = tk.Label(
        root,
        text="Frosted Glass Effect Test\n\n"
             "If you see a blurred/translucent background\n"
             "behind this window, it's working!\n\n"
             "Move other windows behind this one to test.",
        font=("Segoe UI", 11),
        bg="#1a1a1a",
        fg="#e8e8e8",
        pady=50
    )
    label.pack(fill=tk.BOTH, expand=True)
    
    # Apply effects
    root.update()
    
    print("   Applying dark title bar...")
    pws.change_header_color(root, color="#1a1a1a")
    print("   ✓ Dark title bar applied")
    
    print("   Applying acrylic effect...")
    pws.apply_style(root, "acrylic")
    print("   ✓ Acrylic effect applied")
    
    print("\n" + "="*60)
    print("SUCCESS! Check the window that appeared.")
    print("You should see a blurred/frosted glass effect.")
    print("Close the window to exit this test.")
    print("="*60)
    
    root.mainloop()
    
except Exception as e:
    print(f"   ✗ Error applying effects: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "="*60)
    print("FAILED - See error above")
    print("="*60)
    sys.exit(1)

print("\nTest completed successfully!")
