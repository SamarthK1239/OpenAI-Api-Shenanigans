# Security Policy

## Supported Versions

This project contains demonstration code for using various OpenAI API models. Since this is primarily an educational/example repository, there are no formal versioned releases. The `main` branch contains the most up-to-date and tested code.

| Branch/Status | Supported          |
| ------------- | ------------------ |
| main          | :white_check_mark: |
| Other branches| :x:                |

**Important**: Always ensure you're using the latest version of the OpenAI Python SDK (`openai>=1.0.0`) and Python 3.8 or higher.

## Security Best Practices

When using this code, please follow these security guidelines:

### API Key Management

**CRITICAL**: Never commit API keys or secrets to the repository.

- **Always use environment variables** for API keys. Create an `Environment-Variables` folder in the repository root (already in `.gitignore`)
- Place a `.env` file in `Environment-Variables/` with your credentials:
  ```
  api_key=your_openai_api_key_here
  OPENAI_API_KEY=your_openai_api_key_here
  ```
- **Never hardcode** API keys directly in source files
- If you accidentally commit an API key, immediately revoke it on the [OpenAI platform](https://platform.openai.com/api-keys) and generate a new one

### Dependencies

- Keep dependencies updated, especially:
  - `openai>=1.0.0` (OpenAI Python SDK)
  - `python-dotenv>=1.0.0` (Environment variable management)
  - `Pillow>=10.0.0` (Image processing)
  - `pyautogui>=0.9.53` (Screen automation - TrainingAnswerer)
  - `tiktoken>=0.5.0` (Token counting for cost estimation)
  - `requests>=2.31.0` (HTTP client for downloading generated images)
  - `pytesseract>=0.3.10` (OCR for auto-click feature - TrainingAnswerer; requires Tesseract-OCR installation, which involves external binary execution)
- Review dependency security advisories regularly
- Use `pip install --upgrade` to update packages when security patches are released

### Input Validation

- Validate and sanitize all user inputs before sending to OpenAI APIs
- Be aware of prompt injection risks when accepting user-provided prompts
- Set appropriate `max_tokens` limits to prevent unexpected API costs

### Platform-Specific Security (TrainingAnswerer)

- The TrainingAnswerer project includes screen capture and OCR capabilities
- Be cautious about what content is captured and sent to OpenAI APIs
- Avoid capturing sensitive information (passwords, personal data, etc.)
- Review `debug_screenshot.png` files before sharing them

### Cost Management

- Monitor your OpenAI API usage on the [platform dashboard](https://platform.openai.com/usage)
- Set usage limits in your OpenAI account settings
- Use token counting (TikToken) to estimate costs before API calls
- Consider using GPT-3.5-Turbo for development/testing (less expensive than GPT-4)

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do NOT open a public issue** for security vulnerabilities
2. **Email the repository owner** directly through GitHub or contact them via:
   - GitHub: [@SamarthK1239](https://github.com/SamarthK1239)
3. **Include in your report**:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if available)

### Response Timeline

- **Initial Response**: Within 48-72 hours of report
- **Status Update**: Weekly updates on investigation progress
- **Resolution**: Security fixes will be prioritized and released as soon as possible

### What to Expect

- **Accepted vulnerabilities**: We'll work on a fix, keep you updated, and credit you in the release notes (unless you prefer to remain anonymous)
- **Declined reports**: We'll explain why the issue isn't considered a vulnerability or is out of scope

Thank you for helping keep this project secure!
