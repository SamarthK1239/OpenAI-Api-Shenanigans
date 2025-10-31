import pyautogui
from PIL import Image, ImageGrab, ImageDraw, ImageFont
import io
import base64
import tkinter as tk
import time
import re
from difflib import SequenceMatcher

# Try to import pytesseract for OCR
try:
    import pytesseract
    import sys
    from pathlib import Path as PathlibPath
    
    HAS_OCR = True
    
    # Check for bundled Tesseract (when running as .exe)
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        bundle_dir = PathlibPath(sys._MEIPASS)
        tesseract_bundled = bundle_dir / 'tesseract' / 'tesseract.exe'
        
        if tesseract_bundled.exists():
            pytesseract.pytesseract.tesseract_cmd = str(tesseract_bundled)
            print(f"✓ Using bundled Tesseract: {tesseract_bundled}")
    
    # Try to verify Tesseract is actually installed
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✓ Tesseract-OCR {version} found and ready")
    except Exception as e:
        print("⚠ pytesseract installed but Tesseract-OCR engine not found")
        print("  Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Windows installer: https://digi.bib.uni-mannheim.de/tesseract/")
        print("  After installing, restart your terminal/IDE")
        HAS_OCR = False
except ImportError:
    HAS_OCR = False
    print("⚠ pytesseract not found - auto-click feature disabled")
    print("  Install with: pip install pytesseract")
    print("  Also install Tesseract-OCR from: https://github.com/UB-Mannheim/tesseract/wiki")


class ScreenReader:
    """
    Class to capture screenshots and prepare them for OpenAI Vision API
    """
    
    def __init__(self):
        self.last_screenshot = None
    
    def capture_screenshot(self, region=None):
        """
        Capture a screenshot of the entire screen or a specific region
        
        Args:
            region: Optional tuple (x, y, width, height) to capture specific region
            
        Returns:
            PIL Image object
        """
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            self.last_screenshot = screenshot
            return screenshot
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None
    
    def image_to_base64(self, image):
        """
        Convert PIL Image to base64 string for OpenAI API
        
        Args:
            image: PIL Image object
            
        Returns:
            Base64 encoded string
        """
        try:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return None
    
    def save_screenshot(self, filepath, image=None):
        """
        Save screenshot to file
        
        Args:
            filepath: Path to save the image
            image: Optional PIL Image object (uses last screenshot if None)
        """
        try:
            img_to_save = image if image else self.last_screenshot
            if img_to_save:
                img_to_save.save(filepath)
                print(f"Screenshot saved to {filepath}")
            else:
                print("No screenshot to save")
        except Exception as e:
            print(f"Error saving screenshot: {e}")
    
    def get_screen_size(self):
        """
        Get the screen resolution
        
        Returns:
            Tuple (width, height)
        """
        return pyautogui.size()
    
    def capture_region_with_mouse(self, parent=None):
        """
        Capture a screenshot by letting the user select a region with mouse click and drag
        
        Args:
            parent: Optional parent window (for GUI mode)
        
        Returns:
            PIL Image object of the selected region, or None if cancelled
        """
        # Create either a new root or a toplevel depending on context
        if parent:
            root = tk.Toplevel(parent)
            # Important: Keep parent visible but disabled
            parent.attributes('-disabled', True)
        else:
            root = tk.Tk()
        
        root.attributes('-fullscreen', True)
        root.attributes('-alpha', 0.3)
        root.attributes('-topmost', True)
        root.configure(bg='gray')
        root.focus_force()
        
        canvas = tk.Canvas(root, cursor="cross", bg='gray', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Variables to store selection coordinates
        selection = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0, 'rect': None, 'cancelled': False, 'done': False}
        
        def on_mouse_down(event):
            """Handle mouse button press"""
            selection['x1'] = event.x
            selection['y1'] = event.y
            if selection['rect']:
                canvas.delete(selection['rect'])
            selection['rect'] = canvas.create_rectangle(
                selection['x1'], selection['y1'], 
                selection['x1'], selection['y1'],
                outline='red', width=2
            )
        
        def on_mouse_drag(event):
            """Handle mouse drag"""
            if selection['rect']:
                canvas.delete(selection['rect'])
            selection['rect'] = canvas.create_rectangle(
                selection['x1'], selection['y1'], 
                event.x, event.y,
                outline='red', width=2
            )
        
        def on_mouse_up(event):
            """Handle mouse button release"""
            selection['x2'] = event.x
            selection['y2'] = event.y
            selection['done'] = True
            if parent:
                # In GUI mode, just destroy the window - parent's mainloop continues
                root.destroy()
            else:
                # In CLI mode, quit the mainloop
                root.quit()
        
        def on_escape(event):
            """Cancel selection on Escape key"""
            selection['cancelled'] = True
            selection['done'] = True
            if parent:
                # In GUI mode, just destroy the window
                root.destroy()
            else:
                # In CLI mode, quit the mainloop
                root.quit()
        
        # Bind events
        canvas.bind('<ButtonPress-1>', on_mouse_down)
        canvas.bind('<B1-Motion>', on_mouse_drag)
        canvas.bind('<ButtonRelease-1>', on_mouse_up)
        root.bind('<Escape>', on_escape)
        
        # Show instructions
        instructions = canvas.create_text(
            root.winfo_screenwidth() // 2, 50,
            text="Click and drag to select region. Press ESC to cancel.",
            fill='white', font=('Arial', 16, 'bold')
        )
        
        # Handle differently for CLI vs GUI mode
        if not parent:
            # CLI mode - use mainloop
            root.mainloop()
            root.destroy()
        else:
            # GUI mode - wait for window to be destroyed by event handlers
            # This doesn't block the parent's mainloop
            parent.wait_window(root)
            # Re-enable parent window
            parent.attributes('-disabled', False)
            parent.focus_force()
        
        # Check if cancelled
        if selection['cancelled']:
            print("Selection cancelled")
            return None
        
        # Calculate the region coordinates
        x1 = min(selection['x1'], selection['x2'])
        y1 = min(selection['y1'], selection['y2'])
        x2 = max(selection['x1'], selection['x2'])
        y2 = max(selection['y1'], selection['y2'])
        
        width = x2 - x1
        height = y2 - y1
        
        # Check if region is valid
        if width < 5 or height < 5:
            print("Selected region too small")
            return None
        
        print(f"Selected region: ({x1}, {y1}, {width}, {height})")
        
        # Capture the selected region
        screenshot = self.capture_screenshot(region=(x1, y1, width, height))
        return screenshot
    
    def find_text_on_screen(self, text_to_find, confidence=0.8, debug=True):
        """
        Find text on the screen using multiple strategies
        
        Args:
            text_to_find: The exact text to search for on screen
            confidence: Matching confidence (0.0 to 1.0)
            debug: Whether to save debug images
            
        Returns:
            Tuple (x, y) coordinates of the text center, or None if not found
        """
        if not HAS_OCR:
            print("❌ OCR not available. Install pytesseract to use auto-click.")
            return None
        
        try:
            # Capture current screen
            screenshot = pyautogui.screenshot()
            
            # Try multiple OCR configurations for better accuracy
            configs = [
                '--psm 6',  # Assume uniform block of text
                '--psm 11',  # Sparse text
                '--psm 3',  # Fully automatic
            ]
            
            # Normalize search text
            search_text = text_to_find.strip().lower()
            search_words = search_text.split()
            
            print(f"🔍 Searching for: '{text_to_find}'")
            print(f"   Trying {len(configs)} OCR configurations...")
            
            for config_idx, config in enumerate(configs):
                try:
                    # Get text and positions with current config
                    data = pytesseract.image_to_data(screenshot, config=config, output_type=pytesseract.Output.DICT)
                    
                    # Strategy 1: Exact single word match
                    for i, word in enumerate(data['text']):
                        if not word.strip() or data['conf'][i] < 40:  # Higher confidence threshold
                            continue
                        
                        detected_text = word.strip().lower()
                        
                        # Remove common OCR artifacts
                        detected_text = re.sub(r'[^\w\s\-]', '', detected_text)
                        
                        # EXACT match only - no partial matches
                        if detected_text == search_text:
                            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                            center_x, center_y = x + w // 2, y + h // 2
                            print(f"✓ Found exact single-word match at ({center_x}, {center_y}) [confidence: {data['conf'][i]}]")
                            return (center_x, center_y)
                    
                    # Strategy 2: Multi-word exact phrase matching
                    if len(search_words) > 1:
                        for i in range(len(data['text']) - len(search_words) + 1):
                            phrase_words = []
                            phrase_boxes = []
                            all_high_confidence = True
                            
                            for j in range(len(search_words)):
                                if i + j < len(data['text']) and data['text'][i + j].strip():
                                    if data['conf'][i + j] < 40:  # Skip low confidence words
                                        all_high_confidence = False
                                        break
                                    word = re.sub(r'[^\w\s\-]', '', data['text'][i + j].strip().lower())
                                    phrase_words.append(word)
                                    phrase_boxes.append({
                                        'x': data['left'][i + j],
                                        'y': data['top'][i + j],
                                        'w': data['width'][i + j],
                                        'h': data['height'][i + j],
                                        'conf': data['conf'][i + j]
                                    })
                            
                            if not all_high_confidence or len(phrase_words) != len(search_words):
                                continue
                            
                            phrase = ' '.join(phrase_words)
                            
                            # EXACT phrase match only
                            if phrase == search_text:
                                box = phrase_boxes[0]
                                center_x = box['x'] + box['w'] // 2
                                center_y = box['y'] + box['h'] // 2
                                avg_conf = sum(b['conf'] for b in phrase_boxes) / len(phrase_boxes)
                                print(f"✓ Found exact phrase match at ({center_x}, {center_y}) [avg confidence: {avg_conf:.0f}]")
                                return (center_x, center_y)
                    
                except Exception as e:
                    print(f"   Config {config_idx + 1} failed: {e}")
                    continue
            
            # Strategy 3: Fuzzy matching ONLY if exact matches fail (disabled by default for accuracy)
            # Uncomment below if you want fuzzy matching as a last resort
            """
            print("   Trying fuzzy matching...")
            try:
                data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
                best_match = None
                best_ratio = 0
                best_pos = None
                
                for i, word in enumerate(data['text']):
                    if not word.strip() or data['conf'][i] < 40:
                        continue
                    
                    detected_text = re.sub(r'[^\w\s\-]', '', word.strip().lower())
                    ratio = SequenceMatcher(None, search_text, detected_text).ratio()
                    
                    if ratio > best_ratio and ratio > 0.85:  # 85% similarity threshold (stricter)
                        best_ratio = ratio
                        best_match = detected_text
                        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                        best_pos = (x + w // 2, y + h // 2)
                
                if best_pos:
                    print(f"✓ Found fuzzy match '{best_match}' (similarity: {best_ratio:.1%}) at {best_pos}")
                    return best_pos
            except Exception as e:
                print(f"   Fuzzy matching failed: {e}")
            """
            
            # If we get here, save debug image
            if debug:
                debug_path = "ocr_debug_screenshot.png"
                screenshot.save(debug_path)
                print(f"📸 Saved debug screenshot to: {debug_path}")
                
                # Try to show what OCR detected
                try:
                    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
                    print(f"\n📝 OCR detected {len([t for t in data['text'] if t.strip()])} text elements:")
                    detected_texts = [t.strip() for t in data['text'] if t.strip() and len(t.strip()) > 2][:20]
                    for idx, text in enumerate(detected_texts, 1):
                        print(f"   {idx}. '{text}'")
                    if len(detected_texts) >= 20:
                        print(f"   ... and more")
                except:
                    pass
            
            print(f"❌ Could not find text '{text_to_find}' on screen")
            return None
            
        except Exception as e:
            print(f"❌ Error finding text on screen: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def click_on_text(self, text_to_click, delay=0.5):
        """
        Find and click on specific text on the screen with multiple strategies
        
        Args:
            text_to_click: The text to find and click
            delay: Delay in seconds before clicking (for safety)
            
        Returns:
            bool: True if clicked successfully, False otherwise
        """
        print(f"\n🔍 Searching for text: '{text_to_click}'")
        
        # Strategy 1: Find text on current screen
        location = self.find_text_on_screen(text_to_click, debug=True)
        
        if location:
            x, y = location
            print(f"⏱️  Clicking in {delay} seconds...")
            print(f"💡 Tip: Don't move windows or minimize the training interface!")
            time.sleep(delay)
            
            try:
                pyautogui.click(x, y)
                print(f"✓ Clicked at ({x}, {y})")
                return True
            except Exception as e:
                print(f"❌ Error clicking: {e}")
                return False
        
        # Strategy 2: Try searching in the last captured screenshot
        print("\n🔄 Trying alternative: Searching in captured screenshot region...")
        if self.last_screenshot:
            try:
                # If we captured a region, try finding text there
                data = pytesseract.image_to_data(self.last_screenshot, output_type=pytesseract.Output.DICT)
                search_text = text_to_click.strip().lower()
                
                for i, word in enumerate(data['text']):
                    if not word.strip():
                        continue
                    
                    detected_text = re.sub(r'[^\w\s\-]', '', word.strip().lower())
                    
                    # Only exact matches in verification
                    if detected_text == search_text:
                        print(f"   ✓ Found exact match '{detected_text}' in captured region!")
                        print(f"   💡 The text was in your screenshot but may have moved")
                        print(f"   💡 Try keeping the training window in the same position")
                        break
            except:
                pass
        
        print(f"\n❌ Could not find or click text: '{text_to_click}'")
        print(f"\n💡 Troubleshooting tips:")
        print(f"   1. Text must match EXACTLY (no partial matches)")
        print(f"   2. Make sure the answer options are still visible on screen")
        print(f"   3. Don't minimize or move the training window after capturing")
        print(f"   4. Try using larger font sizes (12pt or higher)")
        print(f"   5. Ensure good contrast (dark text on light background)")
        print(f"   6. Check 'ocr_debug_screenshot.png' to see what OCR detected")
        print(f"   7. AI returned: '{text_to_click}' - verify this text appears on screen")
        return False
