import os
import time
import threading
from pathlib import Path
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from screen_reader import ScreenReader
from openai_answerer import OpenAIAnswerer

# Check if OCR is available
try:
    import pytesseract
    import sys
    
    # Check for bundled Tesseract (when running as .exe)
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        bundle_dir = Path(sys._MEIPASS)
        tesseract_bundled = bundle_dir / 'tesseract' / 'tesseract.exe'
        
        if tesseract_bundled.exists():
            pytesseract.pytesseract.tesseract_cmd = str(tesseract_bundled)
            print(f"✓ Using bundled Tesseract: {tesseract_bundled}")
    
    try:
        pytesseract.get_tesseract_version()
        HAS_TESSERACT = True
    except:
        HAS_TESSERACT = False
except ImportError:
    HAS_TESSERACT = False

# Try to import pywinstyles for modern Windows effects
try:
    import pywinstyles as pws
    HAS_PYWINSTYLES = True
    print("✓ pywinstyles loaded - frosted glass effects enabled")
except ImportError:
    HAS_PYWINSTYLES = False
    print("⚠ pywinstyles not found - install with: pip install pywinstyles")
    print("  App will work without frosted glass effects.")


class ToolTip:
    """Simple tooltip class for widgets"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            tw, text=self.text, justify=tk.LEFT,
            background="#2d2d2d", foreground="#d4d4d4",
            relief=tk.SOLID, borderwidth=1,
            font=("Segoe UI", 9), padx=8, pady=4
        )
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class TrainingAnswererGUI:
    """
    Minimalist dark mode GUI for Training Question Answerer
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Q&A Helper")
        self.root.geometry("400x850")
        self.root.minsize(350, 700)
        
        # Position on the right side of screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = screen_width - 420  # 20px padding from right edge
        y_position = 50  # Some padding from top
        self.root.geometry(f"400x850+{x_position}+{y_position}")
        
        # Dark mode color scheme - Modern with transparency support
        self.bg_color = "#1a1a1a"  # Darker for better contrast with frosted glass
        self.fg_color = "#e8e8e8"
        self.input_bg = "#252525"
        self.button_bg = "#2d2d2d"
        self.button_hover = "#3d3d3d"
        self.accent_color = "#0078d4"  # Windows 11 blue
        self.success_color = "#6cc644"
        self.error_color = "#f85149"
        self.warning_color = "#ffa657"
        
        self.root.configure(bg=self.bg_color)
        
        # Frosted glass settings (must be defined before applying effects)
        self.blur_amount = "dark"  # Options: "acrylic", "mica", "aero", "dark", "light"
        
        # Apply modern Windows effects if available
        if HAS_PYWINSTYLES:
            try:
                # Wait for window to be created
                self.root.update()
                
                # Apply dark mode to title bar
                pws.change_header_color(self.root, color="#1a1a1a")
                
                # Apply acrylic blur effect (Windows 11)
                # Options: "dark", "light", "auto", "acrylic", "mica", "aero"
                # This creates the frosted glass background WITHOUT affecting text/button opacity
                pws.apply_style(self.root, self.blur_amount)
                
                print(f"✓ Frosted glass effects applied (style: {self.blur_amount})")
                print(f"  Text and buttons remain at 100% opacity")
            except Exception as e:
                print(f"⚠ Could not apply frosted glass effects: {e}")
                print(f"  This is normal on older Windows versions.")
        
        # Initialize components
        self.screen_reader = None
        self.answerer = None
        self.transcript_loaded = False
        self.is_pinned = False  # Track pin status
        self.auto_click_enabled = False  # Auto-click toggle
        
        # Setup UI
        self.setup_modern_styles()
        self.setup_ui()
        self.setup_keyboard_shortcuts()
        
        # Initialize OpenAI
        self.initialize_openai()
    
    def setup_modern_styles(self):
        """Setup modern ttk styles for scrollbars and other widgets"""
        style = ttk.Style()
        
        # Modern scrollbar style
        style.theme_use('default')
        
        # Vertical scrollbar
        style.configure(
            "Modern.Vertical.TScrollbar",
            background=self.input_bg,
            troughcolor=self.bg_color,
            bordercolor=self.bg_color,
            arrowcolor=self.fg_color,
            relief="flat"
        )
        
        style.map(
            "Modern.Vertical.TScrollbar",
            background=[
                ("active", self.button_hover),
                ("!active", self.button_bg)
            ]
        )
        
        # Separator style
        style.configure(
            "Modern.TSeparator",
            background="#333333"
        )
    
    def setup_ui(self):
        """Create the UI elements"""
        
        # Compact header
        header = tk.Frame(self.root, bg=self.bg_color)
        header.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        # Title and pin in one row
        title_label = tk.Label(
            header,
            text="Q&A Helper",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Pin button (compact and modern)
        pin_container = tk.Frame(header, bg=self.button_bg, highlightthickness=0)
        pin_container.pack(side=tk.RIGHT)
        
        self.pin_button = tk.Button(
            pin_container,
            text="📌",
            command=self.toggle_pin,
            font=("Segoe UI", 12),
            bg=self.button_bg,
            fg=self.fg_color,
            activebackground=self.button_hover,
            activeforeground=self.fg_color,
            relief=tk.FLAT,
            cursor="hand2",
            width=3,
            height=1,
            borderwidth=0,
            highlightthickness=0
        )
        self.pin_button.pack(padx=2, pady=2)
        self.create_tooltip(self.pin_button, "Pin window (Ctrl+P)")
        
        # Modern hover effects for pin button
        def pin_enter(e):
            if not self.is_pinned:
                self.pin_button.config(bg=self.button_hover)
                pin_container.config(bg=self.button_hover)
        
        def pin_leave(e):
            if not self.is_pinned:
                self.pin_button.config(bg=self.button_bg)
                pin_container.config(bg=self.button_bg)
        
        self.pin_button.bind("<Enter>", pin_enter)
        self.pin_button.bind("<Leave>", pin_leave)
        
        # Status indicator (compact)
        self.status_label = tk.Label(
            self.root,
            text="● Initializing...",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.warning_color,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Transcript section (compact)
        transcript_section = tk.Frame(self.root, bg=self.bg_color)
        transcript_section.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(
            transcript_section,
            text="TRANSCRIPT",
            font=("Segoe UI", 9, "bold"),
            bg=self.bg_color,
            fg=self.warning_color,
            anchor=tk.W
        ).pack(fill=tk.X)
        
        self.transcript_label = tk.Label(
            transcript_section,
            text="None loaded",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.error_color,
            wraplength=350,
            justify=tk.LEFT,
            anchor=tk.W
        )
        self.transcript_label.pack(fill=tk.X, pady=(3, 5))
        
        load_transcript_btn = self.create_compact_button(
            transcript_section,
            "📁 Load Context",
            self.load_transcript
        )
        load_transcript_btn.pack(fill=tk.X)
        
        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL, style="Modern.TSeparator").pack(fill=tk.X, padx=15, pady=12)
        
        # Capture actions (vertical stack)
        actions_frame = tk.Frame(self.root, bg=self.bg_color)
        actions_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(
            actions_frame,
            text="CAPTURE",
            font=("Segoe UI", 9, "bold"),
            bg=self.bg_color,
            fg=self.warning_color,
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 8))
        
        # Stack buttons vertically
        self.create_compact_button(
            actions_frame,
            "🖥️  Full Screen",
            self.capture_full_screen,
            "Ctrl+1"
        ).pack(fill=tk.X, pady=2)
        
        self.create_compact_button(
            actions_frame,
            "✂️  Select Region",
            self.capture_mouse_region,
            "Ctrl+3"
        ).pack(fill=tk.X, pady=2)
        
        self.create_compact_button(
            actions_frame,
            "⌨️  Type Question",
            self.type_question,
            "Ctrl+4"
        ).pack(fill=tk.X, pady=2)
        
        # Auto-click toggle button
        self.auto_click_btn = self.create_compact_button(
            actions_frame,
            "🖱️  Auto-Click: OFF",
            self.toggle_auto_click,
            "Ctrl+A"
        )
        self.auto_click_btn.pack(fill=tk.X, pady=2)
        
        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL, style="Modern.TSeparator").pack(fill=tk.X, padx=15, pady=12)
        
        # Output area (takes remaining space)
        output_frame = tk.Frame(self.root, bg=self.bg_color)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        tk.Label(
            output_frame,
            text="OUTPUT",
            font=("Segoe UI", 9, "bold"),
            bg=self.bg_color,
            fg=self.warning_color,
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        # Modern scrolled text with custom scrollbar
        text_frame = tk.Frame(output_frame, bg=self.bg_color)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add subtle border for depth
        text_border = tk.Frame(text_frame, bg="#333333", highlightthickness=0)
        text_border.pack(fill=tk.BOTH, expand=True)
        
        text_inner = tk.Frame(text_border, bg=self.input_bg)
        text_inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Custom scrollbar
        scrollbar = ttk.Scrollbar(
            text_inner,
            style="Modern.Vertical.TScrollbar"
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(2, 2), pady=2)
        
        self.output_text = tk.Text(
            text_inner,
            font=("Segoe UI", 9),
            bg=self.input_bg,
            fg=self.fg_color,
            insertbackground=self.accent_color,
            selectbackground=self.accent_color,
            selectforeground="#ffffff",
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=12,
            pady=12,
            yscrollcommand=scrollbar.set,
            borderwidth=0,
            highlightthickness=0
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(2, 0), pady=2)
        scrollbar.config(command=self.output_text.yview)
        
        # Clear button
        self.create_compact_button(
            output_frame,
            "🗑️  Clear",
            self.clear_output,
            "Ctrl+L"
        ).pack(fill=tk.X, pady=(5, 0))
        
        # Footer with shortcuts
        footer = tk.Frame(self.root, bg=self.input_bg)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        shortcuts_text = "Ctrl+1/3/4 • Ctrl+T • Ctrl+A • Ctrl+P"
        tk.Label(
            footer,
            text=shortcuts_text,
            font=("Segoe UI", 8),
            bg=self.input_bg,
            fg=self.warning_color,
            pady=8
        ).pack()
    
    def create_button(self, parent, text, command, width=30):
        """Create a styled button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10),
            bg=self.button_bg,
            fg=self.fg_color,
            activebackground=self.button_hover,
            activeforeground=self.fg_color,
            relief=tk.FLAT,
            cursor="hand2",
            width=width,
            padx=10,
            pady=8
        )
        
        # Hover effects
        btn.bind("<Enter>", lambda e: btn.config(bg=self.button_hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.button_bg))
        
        return btn
    
    def create_compact_button(self, parent, text, command, shortcut=None):
        """Create a modern compact sidebar-style button"""
        # Container for button with rounded effect
        container = tk.Frame(parent, bg=self.bg_color)
        
        btn_frame = tk.Frame(container, bg=self.button_bg, highlightthickness=0)
        btn_frame.pack(fill=tk.X, padx=1, pady=1)
        
        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            font=("Segoe UI", 10),
            bg=self.button_bg,
            fg=self.fg_color,
            activebackground=self.button_hover,
            activeforeground=self.fg_color,
            relief=tk.FLAT,
            cursor="hand2",
            anchor=tk.W,
            padx=12,
            pady=10,
            borderwidth=0,
            highlightthickness=0
        )
        btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Store reference to the actual button widget in the container
        container.button = btn
        
        if shortcut:
            shortcut_label = tk.Label(
                btn_frame,
                text=shortcut,
                font=("Segoe UI", 8),
                bg=self.button_bg,
                fg=self.warning_color,
                padx=10
            )
            shortcut_label.pack(side=tk.RIGHT)
            
            # Modern hover effects with smooth color transition
            def on_enter(e):
                btn.config(bg=self.button_hover)
                btn_frame.config(bg=self.button_hover)
                shortcut_label.config(bg=self.button_hover)
            
            def on_leave(e):
                btn.config(bg=self.button_bg)
                btn_frame.config(bg=self.button_bg)
                shortcut_label.config(bg=self.button_bg)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn_frame.bind("<Enter>", on_enter)
            btn_frame.bind("<Leave>", on_leave)
            shortcut_label.bind("<Enter>", on_enter)
            shortcut_label.bind("<Leave>", on_leave)
            shortcut_label.bind("<Button-1>", lambda e: command())
        else:
            # Hover effects for button only
            def on_enter(e):
                btn.config(bg=self.button_hover)
                btn_frame.config(bg=self.button_hover)
            
            def on_leave(e):
                btn.config(bg=self.button_bg)
                btn_frame.config(bg=self.button_bg)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn_frame.bind("<Enter>", on_enter)
            btn_frame.bind("<Leave>", on_leave)
        
        return container
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        return ToolTip(widget, text)
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-Key-1>', lambda e: self.capture_full_screen())
        self.root.bind('<Control-Key-3>', lambda e: self.capture_mouse_region())
        self.root.bind('<Control-Key-4>', lambda e: self.type_question())
        self.root.bind('<Control-t>', lambda e: self.load_transcript())
        self.root.bind('<Control-T>', lambda e: self.load_transcript())
        self.root.bind('<Control-l>', lambda e: self.clear_output())
        self.root.bind('<Control-L>', lambda e: self.clear_output())
        self.root.bind('<Control-p>', lambda e: self.toggle_pin())
        self.root.bind('<Control-P>', lambda e: self.toggle_pin())
        self.root.bind('<Control-a>', lambda e: self.toggle_auto_click())
        self.root.bind('<Control-A>', lambda e: self.toggle_auto_click())
        self.root.bind('<Escape>', lambda e: self.cancel_operation())
    
    def initialize_openai(self):
        """Initialize OpenAI components"""
        try:
            # Try multiple locations for .env file
            # 1. Next to executable (for .exe distribution)
            # 2. In Environment-Variables folder (for development)
            # 3. In parent's Environment-Variables folder (for development)
            
            possible_paths = [
                Path(".env"),  # Same directory as executable
                Path("Environment-Variables/.env"),  # Subfolder next to exe
                Path("../Environment-Variables/.env"),  # Development structure
            ]
            
            api_key = None
            env_file_found = False
            
            for path in possible_paths:
                if path.exists():
                    print(f"[DEBUG] Found .env file at: {path.absolute()}")
                    load_dotenv(dotenv_path=path)
                    api_key = os.getenv("OPENAI_API_KEY")
                    env_file_found = True
                    if api_key:
                        break
            
            if not env_file_found:
                self.log_output("❌ Error: .env file not found!", self.error_color)
                self.log_output("Expected locations:", self.fg_color)
                self.log_output("  - Same folder as .exe: .env", self.fg_color)
                self.log_output("  - Or: Environment-Variables/.env", self.fg_color)
                self.update_status("Missing .env File", self.error_color)
                return
            
            if not api_key:
                self.log_output("❌ Error: OPENAI_API_KEY not found in .env file!", self.error_color)
                self.log_output("Add this line to your .env file:", self.fg_color)
                self.log_output("OPENAI_API_KEY=your-key-here", self.warning_color)
                self.update_status("API Key Error", self.error_color)
                return
            
            self.screen_reader = ScreenReader()
            self.answerer = OpenAIAnswerer(api_key=api_key)
            
            width, height = self.screen_reader.get_screen_size()
            
            self.log_output(f"✓ Initialized successfully", self.success_color)
            self.log_output(f"Screen size: {width}x{height}", self.fg_color)
            
            # Show frosted glass status
            if HAS_PYWINSTYLES:
                self.log_output(f"✓ Frosted glass effects enabled", self.success_color)
            else:
                self.log_output(f"⚠ Frosted glass disabled (install pywinstyles)", self.warning_color)
            
            self.log_output("", self.fg_color)  # Blank line
            self.update_status("Ready", self.success_color)
            
        except Exception as e:
            self.log_output(f"❌ Initialization error: {e}", self.error_color)
            self.update_status("Initialization Failed", self.error_color)
    
    def update_status(self, message, color=None):
        """Update status label"""
        self.status_label.config(text=f"● {message}")
        if color:
            self.status_label.config(fg=color)
    
    def log_output(self, message, color=None):
        """Add message to output text area"""
        self.output_text.insert(tk.END, message + "\n")
        if color:
            # Tag the last line with color
            last_line_start = self.output_text.index("end-2c linestart")
            last_line_end = self.output_text.index("end-1c")
            tag_name = f"color_{color}"
            self.output_text.tag_add(tag_name, last_line_start, last_line_end)
            self.output_text.tag_config(tag_name, foreground=color)
        
        self.output_text.see(tk.END)
        self.root.update()
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
        self.log_output("Output cleared.", self.warning_color)
    
    def cancel_operation(self):
        """Cancel current operation"""
        self.update_status("Operation cancelled", self.warning_color)
    
    def toggle_auto_click(self):
        """Toggle auto-click feature on/off"""
        # Check if Tesseract is available
        if not HAS_TESSERACT and not self.auto_click_enabled:
            self.log_output("❌ Auto-click requires Tesseract-OCR", self.error_color)
            self.log_output("  pytesseract is installed ✓", self.fg_color)
            self.log_output("  Tesseract-OCR engine is NOT installed ✗", self.error_color)
            self.log_output("", self.fg_color)
            self.log_output("📥 Install from:", self.accent_color)
            self.log_output("  https://github.com/UB-Mannheim/tesseract/wiki", self.warning_color)
            self.log_output("", self.fg_color)
            self.log_output("See TESSERACT_INSTALL.md for detailed instructions", self.fg_color)
            return
        
        self.auto_click_enabled = not self.auto_click_enabled
        
        if self.auto_click_enabled:
            self.auto_click_btn.button.config(text="🖱️  Auto-Click: ON")
            self.log_output("✓ Auto-click enabled", self.success_color)
            self.log_output("  Will automatically click correct answer", self.fg_color)
        else:
            self.auto_click_btn.button.config(text="🖱️  Auto-Click: OFF")
            self.log_output("Auto-click disabled", self.warning_color)
    
    def toggle_pin(self):
        """Toggle window always-on-top state"""
        self.is_pinned = not self.is_pinned
        self.root.attributes('-topmost', self.is_pinned)
        
        # Get the pin container (parent of pin_button)
        pin_container = self.pin_button.master
        
        if self.is_pinned:
            self.pin_button.config(
                text="📌",
                bg=self.accent_color,
                fg="#ffffff"
            )
            pin_container.config(bg=self.accent_color)
            self.update_status("Pinned", self.success_color)
        else:
            self.pin_button.config(
                text="📌",
                bg=self.button_bg,
                fg=self.fg_color
            )
            pin_container.config(bg=self.button_bg)
            self.update_status("Unpinned", self.warning_color)
    
    def load_transcript(self):
        """Load transcript file"""
        filepath = filedialog.askopenfilename(
            title="Select Transcript File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if filepath:
            if self.answerer.load_transcript(filepath):
                self.transcript_loaded = True
                filename = os.path.basename(filepath)
                # Truncate long filenames
                if len(filename) > 30:
                    filename = filename[:27] + "..."
                self.transcript_label.config(
                    text=f"✓ {filename}",
                    fg=self.success_color
                )
                self.log_output(f"✓ Loaded: {os.path.basename(filepath)}", self.success_color)
                self.update_status("Ready", self.success_color)
            else:
                self.log_output("❌ Failed to load transcript", self.error_color)
                self.update_status("Load Failed", self.error_color)
    
    def capture_full_screen(self):
        """Capture full screen and process"""
        try:
            self.log_output("=" * 45, self.accent_color)
            self.log_output("FULL SCREEN CAPTURE", self.accent_color)
            self.log_output("=" * 45, self.accent_color)
            self.update_status("Capturing in 3s...", self.warning_color)
            
            def capture_task():
                try:
                    time.sleep(3)
                    screenshot = self.screen_reader.capture_screenshot()
                    
                    if screenshot:
                        self.root.after(0, lambda: self.process_screenshot(screenshot))
                    else:
                        self.root.after(0, lambda: self.log_output("❌ Failed to capture screenshot", self.error_color))
                        self.root.after(0, lambda: self.update_status("Capture Failed", self.error_color))
                except Exception as e:
                    self.root.after(0, lambda: self.log_output(f"❌ Capture error: {e}", self.error_color))
                    self.root.after(0, lambda: self.update_status("Error", self.error_color))
            
            threading.Thread(target=capture_task, daemon=True).start()
        except Exception as e:
            self.log_output(f"❌ Error: {e}", self.error_color)
            self.update_status("Error", self.error_color)
    
    def capture_custom_region(self):
        """Capture custom region with coordinates"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Custom Region")
        dialog.geometry("350x250")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        width, height = self.screen_reader.get_screen_size()
        
        tk.Label(
            dialog,
            text=f"Screen Size: {width}x{height}",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(pady=10)
        
        tk.Label(
            dialog,
            text="Enter region coordinates:",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=5)
        
        # Entry fields
        entries_frame = tk.Frame(dialog, bg=self.bg_color)
        entries_frame.pack(pady=10)
        
        entries = {}
        for i, label in enumerate(["X:", "Y:", "Width:", "Height:"]):
            row_frame = tk.Frame(entries_frame, bg=self.bg_color)
            row_frame.pack(pady=3)
            
            tk.Label(
                row_frame,
                text=label,
                font=("Segoe UI", 10),
                bg=self.bg_color,
                fg=self.fg_color,
                width=10,
                anchor=tk.E
            ).pack(side=tk.LEFT, padx=5)
            
            entry = tk.Entry(
                row_frame,
                font=("Segoe UI", 10),
                bg=self.input_bg,
                fg=self.fg_color,
                insertbackground=self.fg_color,
                relief=tk.FLAT,
                width=15
            )
            entry.pack(side=tk.LEFT, padx=5)
            entries[label.rstrip(':')] = entry
        
        def capture():
            try:
                x = int(entries['X'].get())
                y = int(entries['Y'].get())
                w = int(entries['Width'].get())
                h = int(entries['Height'].get())
                
                dialog.destroy()
                
                self.log_output(f"\nCapturing region: ({x}, {y}, {w}, {h})", self.fg_color)
                self.update_status("Capturing...", self.warning_color)
                
                time.sleep(1)
                screenshot = self.screen_reader.capture_screenshot(region=(x, y, w, h))
                
                if screenshot:
                    self.process_screenshot(screenshot)
                else:
                    self.log_output("❌ Failed to capture screenshot", self.error_color)
            except ValueError:
                self.log_output("❌ Invalid coordinates. Please enter numbers.", self.error_color)
                dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.bg_color)
        btn_frame.pack(pady=15)
        
        self.create_button(btn_frame, "Capture", capture, width=12).pack(side=tk.LEFT, padx=5)
        self.create_button(btn_frame, "Cancel", dialog.destroy, width=12).pack(side=tk.LEFT, padx=5)
    
    def capture_mouse_region(self):
        """Capture region using mouse click and drag"""
        try:
            self.log_output("=" * 45, self.accent_color)
            self.log_output("SELECT REGION", self.accent_color)
            self.log_output("=" * 45, self.accent_color)
            self.log_output("Click & drag to select. ESC to cancel.", self.warning_color)
            self.update_status("Select region...", self.warning_color)
            self.root.update()
            
            # Schedule the capture to happen after a brief delay to let UI update
            self.root.after(100, self._do_mouse_capture)
                
        except Exception as e:
            self.log_output(f"❌ Selection error: {e}", self.error_color)
            self.update_status("Error", self.error_color)
    
    def _do_mouse_capture(self):
        """Internal method to perform mouse capture"""
        try:
            screenshot = self.screen_reader.capture_region_with_mouse(parent=self.root)
            
            if screenshot:
                # Process screenshot in a thread
                self.process_screenshot(screenshot)
            else:
                self.log_output("Selection cancelled or failed", self.warning_color)
                self.update_status("Ready", self.success_color)
        except Exception as e:
            print(f"[DEBUG] Mouse capture error: {e}")
            import traceback
            traceback.print_exc()
            self.log_output(f"❌ Selection error: {e}", self.error_color)
            self.update_status("Error", self.error_color)
    
    def type_question(self):
        """Manually type a question"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Type Question")
        dialog.geometry("500x320")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Apply modern effects to dialog if available
        if HAS_PYWINSTYLES:
            try:
                dialog.update()
                pws.change_header_color(dialog, color="#1a1a1a")
                pws.apply_style(dialog, "acrylic")
            except:
                pass
        
        tk.Label(
            dialog,
            text="Enter your question:",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=15, padx=20, anchor=tk.W)
        
        # Modern text area with border
        text_container = tk.Frame(dialog, bg="#333333")
        text_container.pack(padx=20, pady=(0, 15), fill=tk.BOTH, expand=True)
        
        text_inner = tk.Frame(text_container, bg=self.input_bg)
        text_inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        scrollbar = ttk.Scrollbar(text_inner, style="Modern.Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=2, pady=2)
        
        text_area = tk.Text(
            text_inner,
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.fg_color,
            insertbackground=self.accent_color,
            selectbackground=self.accent_color,
            selectforeground="#ffffff",
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=12,
            pady=12,
            height=8,
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.config(command=text_area.yview)
        text_area.focus()
        
        def submit():
            question = text_area.get(1.0, tk.END).strip()
            if question:
                dialog.destroy()
                self.log_output("\n" + "="*60, self.accent_color)
                self.log_output("MANUAL QUESTION", self.accent_color)
                self.log_output("="*60, self.accent_color)
                self.log_output(f"Question: {question}", self.fg_color)
                self.update_status("Generating answer...", self.warning_color)
                
                def answer_task():
                    answer = self.answerer.answer_question(question, use_transcript=self.transcript_loaded)
                    self.root.after(0, lambda: self.display_result(question, answer))
                
                threading.Thread(target=answer_task, daemon=True).start()
            else:
                dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        self.create_button(btn_frame, "Submit", submit, width=12).pack(side=tk.LEFT, padx=5)
        self.create_button(btn_frame, "Cancel", dialog.destroy, width=12).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter to submit (with Ctrl modifier to allow newlines)
        dialog.bind('<Control-Return>', lambda e: submit())
    
    def process_screenshot(self, screenshot):
        """Process captured screenshot"""
        try:
            self.log_output("✓ Screenshot captured", self.success_color)
            self.update_status("Processing...", self.warning_color)
            self.root.update()  # Force UI update
            
            def process_task():
                try:
                    print("[DEBUG] Starting screenshot processing...")
                    image_base64 = self.screen_reader.image_to_base64(screenshot)
                    
                    if image_base64:
                        print("[DEBUG] Image encoded, sending to OpenAI...")
                        question, answer = self.answerer.answer_from_screenshot(image_base64, use_transcript=self.transcript_loaded)
                        print(f"[DEBUG] Got response - Question: {bool(question)}, Answer: {bool(answer)}")
                        
                        if question and answer:
                            self.root.after(0, lambda q=question, a=answer: self.display_result(q, a))
                        elif question and not answer:
                            self.root.after(0, lambda: self.log_output("\n⚠️  OpenAI refused to process the image.", self.warning_color))
                            self.root.after(0, lambda: self.log_output("Screenshot saved as 'debug_screenshot.png'", self.warning_color))
                            self.screen_reader.save_screenshot("debug_screenshot.png")
                            self.root.after(0, lambda: self.update_status("Processing Failed", self.error_color))
                        else:
                            self.root.after(0, lambda: self.log_output("❌ Failed to extract question", self.error_color))
                            self.root.after(0, lambda: self.update_status("Extraction Failed", self.error_color))
                    else:
                        print("[DEBUG] Failed to encode image")
                        self.root.after(0, lambda: self.log_output("❌ Failed to encode image", self.error_color))
                        self.root.after(0, lambda: self.update_status("Encoding Failed", self.error_color))
                except Exception as e:
                    print(f"[DEBUG] Exception in process_task: {e}")
                    import traceback
                    traceback.print_exc()
                    self.root.after(0, lambda err=str(e): self.log_output(f"❌ Processing error: {err}", self.error_color))
                    self.root.after(0, lambda: self.update_status("Error", self.error_color))
            
            threading.Thread(target=process_task, daemon=False).start()
        except Exception as e:
            print(f"[DEBUG] Exception in process_screenshot: {e}")
            self.log_output(f"❌ Screenshot processing error: {e}", self.error_color)
            self.update_status("Error", self.error_color)
    
    def display_result(self, question, answer):
        """Display question and answer"""
        print(f"[DEBUG] Displaying result - Q len: {len(question)}, A len: {len(answer)}")
        try:
            self.log_output("\n" + "=" * 45, self.success_color)
            self.log_output("RESULT", self.success_color)
            self.log_output("=" * 45, self.success_color)
            self.log_output("\n📝 Question:", self.accent_color)
            self.log_output(question, self.fg_color)
            self.log_output("\n💡 Answer:", self.accent_color)
            self.log_output(answer, self.fg_color)
            
            # If auto-click is enabled, get just the option text and click it
            if self.auto_click_enabled:
                self.log_output("\n🖱️  Auto-click enabled - finding answer on screen...", self.warning_color)
                
                def auto_click_task():
                    try:
                        # Get just the option text (not the full answer with explanation)
                        option_text = self.answerer.answer_question(question, use_transcript=self.transcript_loaded, return_option_only=True)
                        
                        print(f"[DEBUG] Option text for clicking: '{option_text}'")
                        self.root.after(0, lambda: self.log_output(f"  Looking for: '{option_text}'", self.fg_color))
                        
                        # Try to click on it
                        if self.screen_reader.click_on_text(option_text, delay=1.0):
                            self.root.after(0, lambda: self.log_output("✓ Successfully clicked!", self.success_color))
                        else:
                            self.root.after(0, lambda: self.log_output("❌ Could not find option on screen", self.error_color))
                            self.root.after(0, lambda: self.log_output("  Try positioning the window to show options", self.warning_color))
                    except Exception as e:
                        print(f"[DEBUG] Auto-click error: {e}")
                        self.root.after(0, lambda: self.log_output(f"❌ Auto-click error: {e}", self.error_color))
                
                threading.Thread(target=auto_click_task, daemon=True).start()
            self.log_output("\n" + "=" * 45 + "\n", self.success_color)
            self.update_status("Complete", self.success_color)
            print("[DEBUG] Result displayed successfully")
        except Exception as e:
            print(f"[DEBUG] Error displaying result: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Launch the GUI"""
    root = tk.Tk()
    app = TrainingAnswererGUI(root)
    
    # Prevent accidental closure - ask for confirmation
    def on_closing():
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            print("[DEBUG] Application closing normally")
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    print("[DEBUG] Starting main loop...")
    try:
        root.mainloop()
    except Exception as e:
        print(f"[DEBUG] Mainloop exception: {e}")
        import traceback
        traceback.print_exc()
    print("[DEBUG] Mainloop ended")


if __name__ == "__main__":
    main()
