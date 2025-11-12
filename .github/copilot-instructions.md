# GitHub Copilot Instructions for OpenAI-API-Shenanigans

## Project Overview
This repository contains various Python projects demonstrating different OpenAI API capabilities, including:
- **DALL-E 2** image generation and variations
- **Sentiment analysis** using GPT-4 models
- **Speech-to-text and audio translation** with Whisper-1
- **Token counting** with TikToken
- **Interactive storytelling** with conversation history
- **GPT-4 Vision** examples and advanced vision-based applications
- **TrainingAnswerer**: A modern GUI application with screen capture, AI-powered question answering, OCR, and auto-click features
- **StarterCodeGenerator**: An image-to-code generator using GPT-4o (in development)

Additionally, the repository uses **GitHub Agentic Workflows** for automated maintenance tasks including documentation updates and weekly research reports.

## Code Style and Standards

### Python Conventions
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Keep functions focused and single-purpose
- Add docstrings for complex functions and modules

### Import Organization
- Standard library imports first
- Third-party imports second (e.g., `dotenv`, `openai`)
- Local imports last
- Use `from pathlib import Path` for file paths

## Project Structure

### Main Directory Layout
```
OpenAI-API/
├── EquationSolver/        # Equation solving with GPT and Wolfram Alpha (ON HOLD)
│   ├── chatGPT.py
│   ├── equation_solver.py
│   ├── image_to_text.py
│   ├── problem_to_equation.py
│   └── run.py
├── StarterCodeGenerator/  # Image-to-code generator using GPT-4o (IN DEVELOPMENT)
│   ├── Image Prompt Generator.py  # Vision-based design to code prompt
│   └── main.py
├── Storyteller/           # Interactive storytelling application
│   ├── file_operations.py
│   ├── run.py
│   ├── starter_prompts.json
│   ├── starter_prompts.txt
│   └── storyteller.py
├── Summarizer/            # Speech-to-text and summarization
│   ├── speech_to_text.py
│   ├── summarizer.py
│   ├── transcription.txt
│   └── video_to_audio.py
├── TrainingAnswerer/      # Modern GUI app for training question answering
│   ├── gui.py              # Main GUI with frosted glass design
│   ├── main.py             # CLI version
│   ├── openai_answerer.py  # OpenAI API integration
│   ├── screen_reader.py    # Screen capture utilities
│   ├── build_exe.py        # PyInstaller build script
│   ├── test_frosted_glass.py # Testing utility for pywinstyles installation
│   ├── requirements.txt    # Project dependencies
│   ├── README.md
│   └── Info/               # Documentation folder
│       ├── AUTO_CLICK_GUIDE.md
│       ├── AUTO_CLICK_TECHNICAL.md
│       ├── AUTO_CLICK_DEBUG.md
│       ├── BUILD_INSTRUCTIONS.md
│       ├── EXACT_MATCHING.md
│       ├── FROSTED_GLASS_GUIDE.md
│       ├── TESSERACT_BUNDLE.md
│       └── TESSERACT_INSTALL.md
├── audio_translation.py   # Audio translation and transcription with Whisper
├── image_generator.py     # DALL-E 2 image generation
├── image_variation.py     # Image variation creation
├── sentiment_analyzer.py  # Sentiment analysis with GPT-4
├── token_splitter.py      # Token counting utilities with TikToken
├── vision.py              # GPT-4 Vision preview examples
└── main.py                # Entry point for testing image functions
```

## API Configuration

### Environment Variables
- **ALWAYS** use environment variables for API keys
- Create a folder called `Environment-Variables` in the repository root (not tracked in git)
- Place a `.env` file in this folder with your credentials
- Load from `Environment-Variables/.env` using `dotenv`
- Required variables:
  - `api_key`: OpenAI API key (most projects use this)
  - `OPENAI_API_KEY`: Alternative key name used in TrainingAnswerer
  - `organization`: OpenAI organization key (optional, some older code may reference this)
- **NEVER** hardcode API keys in source files

### Standard Setup Pattern

**For scripts in the root OpenAI-API directory:**
```python
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from openai import OpenAI

# Get environment variables
path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

# Set up openai client (using modern pattern without organization)
client = OpenAI(
    api_key=os.getenv("api_key")
)
```

**For scripts in subdirectories (e.g., Summarizer/, TrainingAnswerer/):**
```python
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

path = Path("../Environment-Variables/.env")
load_dotenv(dotenv_path=path)

# Set up openai client
client = OpenAI(
    api_key=os.getenv("api_key")
)

# OR for TrainingAnswerer which uses OPENAI_API_KEY:
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
```

## OpenAI API Best Practices

### Model Selection
- The codebase uses various models depending on the task:
  - `gpt-3.5-turbo-1106` for storytelling and general chat tasks
  - `gpt-4-1106-preview` for sentiment analysis and summarization
  - `gpt-4-vision-preview` for basic vision examples (vision.py)
  - `gpt-4o` for advanced vision-based tasks (TrainingAnswerer, StarterCodeGenerator)
  - `whisper-1` for speech-to-text and audio translation
  - `dall-e-2` for image generation and variations
- Use GPT-4 models sparingly (not all developers have access)
- Consider cost implications of model choices
- **GPT-4o** is the preferred model for vision tasks that require high accuracy
- Note: When adding new features, choose the model appropriate for the task complexity

### Prompt Design
- Test prompts on ChatGPT website first before coding
- Be specific and clear in instructions
- Use system and user message roles appropriately
- Monitor token usage to control costs

### Token Management
- Use TikToken for counting tokens before API calls
- Be aware of model token limits
- For long content, consider chunking strategies
- GPT-4 preview models support up to 128,000 input tokens

## Security Guidelines

### Sensitive Data
- Never commit `.env` files (already in `.gitignore`)
- Don't log or print API keys
- Be cautious with user inputs to prevent prompt injection
- Validate and sanitize all user inputs

### Error Handling
- Implement proper error handling for API calls
- Handle rate limits and timeouts gracefully
- Provide informative error messages to users

## File Handling

### Generated Files
- Images are saved with descriptive names (e.g., `generated_image.jpg`)
- Clean up temporary files after processing
- Use appropriate file permissions

### Path Handling
- Use `pathlib.Path` for cross-platform compatibility
- Use relative paths from the script location
- Handle missing directories gracefully

## Testing and Validation

### Manual Testing
- Use `main.py` as the entry point for testing image functions
- Test with various inputs including edge cases
- Verify API responses match expectations
- For GUI applications, test UI responsiveness and error handling

### Cost Awareness
- Be mindful of API costs during testing
- Use simpler models for development/testing when possible
- Monitor usage on OpenAI platform
- Consider token limits before processing large content
- GPT-4o and GPT-4 are more expensive than GPT-3.5-Turbo

### Project-Specific Testing
- **TrainingAnswerer**: Test screen capture delays, OCR accuracy, context loading
- **Storyteller**: Test conversation flow and history maintenance
- **Summarizer**: Test with various audio lengths and quality
- **Vision projects**: Test with different image types and sizes

## Important Notes

### API Updates
- All projects updated to use OpenAI Python SDK v1.0.0+
- Uses `client.chat.completions.create()` instead of legacy patterns
- Most projects use `api_key` in .env (except TrainingAnswerer uses `OPENAI_API_KEY`)
- Organization parameter is optional and largely unused in current code

### Model Availability
- GPT-4 models used selectively (not all developers have access)
- Most projects use GPT-3.5-Turbo-1106 for consistency
- GPT-4o used for advanced vision tasks requiring high accuracy
- Whisper-1 is the standard for audio transcription

### Development Approach
- Test prompts on ChatGPT website before coding
- Start with simpler models, upgrade if needed
- Monitor token usage with TikToken
- GPT-4 preview models support up to 128,000 input tokens
- Consider batch API for non-urgent processing

### Platform Considerations
- TrainingAnswerer GUI optimized for Windows 10/11
- Frosted glass effects require Windows and pywinstyles
- Auto-click feature requires Tesseract-OCR installation
- Core functionality works cross-platform (screen capture, API calls)
- PyInstaller can build standalone executables (see build_exe.py)

### Vision API Best Practices
- Use GPT-4o for production vision tasks (better accuracy than gpt-4-vision-preview)
- Base64 encoding for local images, URLs for remote images
- Handle content policy refusals gracefully
- Set appropriate max_tokens (500+ for vision tasks)
- Combine vision with OCR for automation tasks

## Dependencies

### Key Libraries
- `openai>=1.0.0`: Official OpenAI Python client (modern SDK)
- `python-dotenv>=1.0.0`: Environment variable management
- `tiktoken`: Token counting for cost estimation
- `Pillow>=10.0.0`: Image processing (for DALL-E and screenshots)
- `requests`: HTTP requests for downloading generated images

### TrainingAnswerer-Specific Dependencies
- `pyautogui>=0.9.53`: Screen capture and mouse/keyboard automation
- `pywinstyles>=1.0.0`: Windows 11 frosted glass effects (Windows 10/11 only)
- `pytesseract>=0.3.10`: OCR for auto-click feature (requires Tesseract-OCR installation)
- `pyinstaller>=6.0.0`: For building standalone executables

### Dependency Management
- Keep dependencies minimal and well-documented
- Specify version requirements when necessary
- Be aware of package limitations (e.g., PyDub requires executable file management)
- The TrainingAnswerer project has its own `requirements.txt` file
- Use `pip install -r requirements.txt` for TrainingAnswerer dependencies

## Common Patterns

### API Response Handling
```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "System instructions"},
        {"role": "user", "content": "User input"}
    ]
)
result = response.choices[0].message.content
```

### Conversation History (Storyteller pattern)
```python
conversation_history = [{"role": "user", "content": initial_prompt}]

response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=conversation_history
)

# Append responses to maintain context
conversation_history.append({"role": "system", "content": response.choices[0].message.content})
conversation_history.append({"role": "user", "content": user_response})
```

### Image Generation
```python
response = client.images.generate(
    model="dall-e-2",
    prompt="Image description",
    n=1,
    size="1024x1024"
)
image_url = response.data[0].url
```

### Vision API Usage
```python
# For URL-based images (basic vision example)
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": "https://example.com/image.jpg"}
            ]
        }
    ],
    max_tokens=500
)

# For base64-encoded images (TrainingAnswerer pattern)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract the question from this screenshot"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                }
            ]
        }
    ],
    max_tokens=500
)
```

### Whisper Audio Transcription
```python
audio_file = open(audio_path, "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
print(transcription.text)
```

## Known Issues and Workarounds

### WolframAlpha Integration
- Equation solver project is on hold
- GPT-3.5 sometimes ignores instructions
- Implement safeguards for input validation

### Audio Processing
- Avoid PyDub due to executable file requirements
- Use native libraries or simpler alternatives

### Vision Model Content Restrictions
- GPT-4 Vision may refuse to process certain types of screenshots
- Response: "Sorry, I can't assist with that" indicates content restrictions
- Workarounds:
  - Capture smaller, more specific regions
  - Use manual question input mode
  - Check `debug_screenshot.png` to identify problematic content
  - The TrainingAnswerer handles this gracefully with fallback options

### Platform-Specific Features
- **Frosted Glass Effects**: Requires `pywinstyles` and Windows 10/11
  - Application works without these effects on other platforms
  - Check `HAS_PYWINSTYLES` flag before applying effects
- **Auto-Click Feature**: Requires Tesseract-OCR installation
  - Windows users: Install from UB-Mannheim repository
  - Check `HAS_TESSERACT` flag before enabling feature

## GUI Development Patterns (TrainingAnswerer)

### Modern Windows 11 Design
The TrainingAnswerer project demonstrates modern GUI development with:
- **Tkinter** for cross-platform GUI framework
- **pywinstyles** for Windows 11 acrylic/frosted glass effects
- Custom styling for buttons, scrollbars, and text widgets
- Sidebar layout optimized for screen real estate

### Key GUI Patterns
```python
# Check for optional dependencies
try:
    import pywinstyles as pws
    HAS_PYWINSTYLES = True
except ImportError:
    HAS_PYWINSTYLES = False
    # Application continues to work without effects

# Apply frosted glass effect (Windows only)
if HAS_PYWINSTYLES:
    pws.apply_style(window, "acrylic")
    
# Threading for non-blocking operations
def capture_in_thread():
    thread = threading.Thread(target=actual_capture_function)
    thread.daemon = True
    thread.start()
```

### Screen Capture Integration
```python
import pyautogui
from PIL import Image
import base64
import io

# Full screen capture
screenshot = pyautogui.screenshot()

# Region capture with coordinates
screenshot = pyautogui.screenshot(region=(x, y, width, height))

# Convert to base64 for API
buffered = io.BytesIO()
screenshot.save(buffered, format="PNG")
img_base64 = base64.b64encode(buffered.getvalue()).decode()
```

### OCR Integration (Auto-Click Feature)
```python
import pytesseract
from PIL import ImageGrab

# Capture and read text from screen
screenshot = ImageGrab.grab()
text_data = pytesseract.image_to_string(screenshot)

# Find text coordinates
boxes = pytesseract.image_to_boxes(screenshot)

# Auto-click at found location
import pyautogui
pyautogui.click(x, y)
```

### File Organization for GUI Projects
- Separate UI logic (gui.py) from business logic (openai_answerer.py, screen_reader.py)
- Use classes to encapsulate functionality
- Implement threaded operations for long-running tasks (screen capture, API calls)
- Provide both GUI and CLI interfaces when possible (gui.py and main.py)

## Project-Specific Guidelines

### TrainingAnswerer
A modern GUI application for answering training questions using AI vision and context.

**Key Features:**
- Screen capture with click-and-drag region selection
- GPT-4o vision for question extraction from screenshots
- Context-aware answering using loaded transcripts
- Auto-click feature with OCR (pytesseract)
- Windows 11 frosted glass UI design
- Keyboard shortcuts for efficiency

**When working on TrainingAnswerer:**
- Use threading for non-blocking UI operations
- Handle optional dependencies gracefully (pywinstyles, pytesseract)
- Provide informative error messages in the GUI
- Test both with and without transcript context
- Consider the 3-second delay for screen capture to allow window switching

**Environment Setup:**
- Uses `OPENAI_API_KEY` instead of `api_key` in .env
- Requires additional dependencies in requirements.txt
- See README.md and Info/ folder for detailed documentation

**Testing Utilities:**
- `test_frosted_glass.py`: Diagnostic script to verify pywinstyles installation and Windows 11 effects
  - Checks if pywinstyles is installed and functioning
  - Verifies Windows version compatibility (Windows 10+)
  - Creates a test window with acrylic frosted glass effect
  - Useful for troubleshooting UI effects before running the main application

### StarterCodeGenerator
An image-to-code generator using GPT-4o (currently in development).

**Purpose:**
- Takes screenshots of designs or pseudocode
- Generates frontend code or starter code
- Helps kickstart coding process from visual mockups

**Implementation Notes:**
- Uses both local (base64) and remote (URL) image methods
- Leverages GPT-4o's vision capabilities
- Two-step process: vision analysis → code generation
- Consider using batch API for non-immediate results

### Storyteller
Interactive storytelling with GPT-3.5-Turbo maintaining conversation history.

**Key Patterns:**
- JSON-based prompt categories (starter_prompts.json)
- Conversation history maintained throughout interaction
- Random prompt selection from categories
- Each response includes a question for user interaction

### Summarizer
Speech-to-text and summarization pipeline.

**Components:**
- `speech_to_text.py`: Whisper-1 transcription
- `video_to_audio.py`: Extract audio from video
- `summarizer.py`: GPT-4 comprehensive summarization
- Uses bullet points for organized output
- Optimized prompts for university-level content

### Sentiment Analyzer
Simple sentiment classification using GPT-4.

**Features:**
- Classifies text as Positive/Negative/Neutral
- Provides 1-10 rating scale
- Uses GPT-4-1106-preview for accuracy

### Image Generator & Image Variation
DALL-E 2 image generation and variation tools.

**Usage:**
- `image_generator.py`: Generate from text prompts
- `image_variation.py`: Create variations of existing images
- Downloads and saves images locally
- 1024x1024 default size

## Contributing Guidelines

### When Making Changes
- Test changes with actual API calls when possible (be mindful of costs)
- Update documentation if adding new features
- Follow existing code patterns and structure
- Consider backward compatibility
- Be mindful of API costs in new features
- For GUI applications, test on target platform (Windows for frosted glass effects)
- Handle optional dependencies gracefully with try/except blocks
- Provide both CLI and GUI interfaces when appropriate

### Code Review Focus
- API key security (never commit .env files)
- Error handling completeness
- Token usage optimization
- Code clarity and maintainability
- Cost implications of changes
- Cross-platform compatibility considerations
- Threading safety for GUI applications
- Proper cleanup of resources (file handles, screenshots)

### Adding New Projects
When adding new OpenAI API demonstrations:
1. Create a new subdirectory in `OpenAI-API/`
2. Include a README.md explaining the project
3. Use the standard environment variable pattern
4. Add requirements.txt if project-specific dependencies are needed
5. Choose appropriate model for the task (consider cost vs. capability)
6. Include error handling for API failures
7. Update the main README.md with project description
8. Update these Copilot instructions with project-specific guidelines

### Testing Guidelines
- **Manual Testing**: Use API calls sparingly during development
- **Test Prompt Design**: Use ChatGPT website first (free testing)
- **Cost Awareness**: Monitor token usage and API costs
- **Model Selection**: Use simpler models for development/testing when possible
- **Edge Cases**: Test with various inputs including edge cases
- **Error Scenarios**: Test API failures, rate limits, and invalid inputs

## GitHub Agentic Workflows

This repository uses GitHub Agentic Workflows for automated maintenance tasks. These are AI-powered workflows that help keep documentation up-to-date and perform regular research tasks.

### Active Workflows

- **update-copilot-instructions.md**: Runs weekdays at 12am EST to analyze recent commits and update this Copilot instructions file
  - Reviews recent Python code changes
  - Updates documentation for new projects or features
  - Creates pull requests with changes
  
- **nightly-readme-update.md**: Runs weekdays at 12am EST to update the main README
  - Scans repository structure for changes
  - Updates project listings and descriptions
  - Maintains the "Last Updated" timestamp
  
- **weekly-research.md**: Runs weekly to research developments related to the repository

### Workflow File Structure

Agentic workflows use a markdown + YAML frontmatter format:
- `.md` files in `.github/workflows/` define the workflow instructions
- `.lock.yml` files are the compiled GitHub Actions workflows (generated automatically)
- Workflow prompts and templates are stored in `.github/prompts/`

### Working with Agentic Workflows

When modifying agentic workflows:
1. Edit the `.md` file, NOT the `.lock.yml` file
2. The `.lock.yml` file is auto-generated from the `.md` file
3. Use the `gh aw compile` command to regenerate `.lock.yml` after changes
4. Workflow instructions in `.github/instructions/github-agentic-workflows.instructions.md` provide detailed guidance

### Agentic Workflow Best Practices

- Use `safe-outputs` for GitHub API operations (issue creation, PR creation, comments)
- Specify minimal `permissions` for security
- Set appropriate `timeout_minutes` to prevent runaway costs
- Use the `edit` tool for file modifications
- Leverage GitHub context expressions like `${{ github.repository }}` for dynamic content
- Keep workflow instructions clear and focused on a single task
