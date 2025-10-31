# GitHub Copilot Instructions for OpenAI-API-Shenanigans

## Project Overview
This repository contains various Python projects demonstrating different OpenAI API capabilities, including:
- DALL-E image generation and variations
- Sentiment analysis using GPT models
- Speech-to-text with Whisper
- Token counting with TikToken
- Interactive storytelling
- GPT-4 Vision examples

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
├── EquationSolver/        # Equation solving with GPT and Wolfram Alpha
├── StarterCodeGenerator/  # Code generation utilities
├── Storyteller/           # Interactive storytelling application
├── Summarizer/            # Speech-to-text summarization
├── TrainingAnswerer/      # Training-related utilities
├── audio_translation.py   # Audio translation with Whisper
├── image_generator.py     # DALL-E image generation
├── image_variation.py     # Image variation creation
├── sentiment_analyzer.py  # Sentiment analysis tool
├── token_splitter.py      # Token counting utilities
├── vision.py              # GPT-4 Vision examples
└── main.py                # Entry point for testing functions
```

## API Configuration

### Environment Variables
- **ALWAYS** use environment variables for API keys
- Create a folder called `Environment-Variables` in the repository root (not tracked in git)
- Place a `.env` file in this folder with your credentials
- Load from `Environment-Variables/.env` using `dotenv`
- Required variables:
  - `organization`: OpenAI organization key
  - `api_key`: OpenAI API key
- **NEVER** hardcode API keys in source files

### Standard Setup Pattern
```python
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from Environment-Variables/.env
# Note: This folder must be created by the user and is not tracked in git
path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

openai = OpenAI(
    organization=os.getenv('organization'),
    api_key=os.getenv("api_key")
)
```

## OpenAI API Best Practices

### Model Selection
- The codebase uses various models depending on the task:
  - `gpt-3.5-turbo-1106` for storytelling
  - `gpt-4-1106-preview` for sentiment analysis and summarization
  - `gpt-4-vision-preview` for vision examples (vision.py)
  - `gpt-4o` for advanced vision-based tasks (TrainingAnswerer)
  - `whisper-1` for speech-to-text
  - `dall-e-2` for image generation
- Use GPT-4 models sparingly (not all developers have access)
- Consider cost implications of model choices
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
- Use `main.py` as the entry point for testing functions
- Test with various inputs including edge cases
- Verify API responses match expectations

### Cost Awareness
- Be mindful of API costs during testing
- Use simpler models for development/testing when possible
- Monitor usage on OpenAI platform

## Dependencies

### Key Libraries
- `openai`: Official OpenAI Python client
- `python-dotenv`: Environment variable management
- `tiktoken`: Token counting
- `Pillow`: Image processing (for DALL-E)

### Dependency Management
- Keep dependencies minimal and well-documented
- Specify version requirements when necessary
- Be aware of package limitations (e.g., PyDub requires executable file management)

## Common Patterns

### API Response Handling
```python
response = openai.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "System instructions"},
        {"role": "user", "content": "User input"}
    ]
)
result = response.choices[0].message.content
```

### Image Generation
```python
response = openai.images.generate(
    prompt="Image description",
    n=1,
    size="1024x1024"
)
image_url = response.data[0].url
```

## Known Issues and Workarounds

### WolframAlpha Integration
- Equation solver project is on hold
- GPT-3.5 sometimes ignores instructions
- Implement safeguards for input validation

### Audio Processing
- Avoid PyDub due to executable file requirements
- Use native libraries or simpler alternatives

## Contributing Guidelines

### When Making Changes
- Test changes with actual API calls when possible
- Update documentation if adding new features
- Follow existing code patterns and structure
- Consider backward compatibility
- Be mindful of API costs in new features

### Code Review Focus
- API key security
- Error handling completeness
- Token usage optimization
- Code clarity and maintainability
- Cost implications of changes
