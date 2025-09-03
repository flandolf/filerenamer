# File Renamer

A Python utility that uses AI (Google's Gemma model) to intelligently rename files with cleaner, more readable names.

## Overview

File Renamer is a command-line tool that helps you clean up messy filenames by leveraging Google's Gemma AI model. It automatically removes special characters, fixes capitalization, replaces underscores/dashes with spaces, and makes filenames more concise and readable.

## Features

- Interactive directory navigation using a curses-based UI
- AI-powered filename cleaning and standardization
- Configurable safe mode to preview changes before applying
- Support for batch processing files in directories and subdirectories
- Color-coded terminal output for better user experience

## Requirements

- Python 3.13 or higher
- Google AI API key for accessing the Gemma model

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/flandolf/filerenamer
   cd filerenamer
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Configuration

Create a `.env` file in the root directory with the following settings:

```
API_KEY=your_google_ai_api_key
SAFE_MODE=y  # Set to 'n' to skip confirmation prompts
START_PATH=~/  # Default starting directory
```

## Usage

Run the application:

```bash
python main.py
```

1. Navigate through directories using arrow keys
2. Press Enter to select a directory
3. The tool will scan for files and suggest new names
4. In safe mode, confirm each rename with 'y' or 'n'
5. Files will be renamed with improved, cleaner filenames

## How It Works

1. The tool scans selected directories (and optionally subdirectories) for files
2. Each filename is sent to Google's Gemma AI model with a prompt to clean it up
3. The model responds with a cleaned version of the name
4. The tool renames the file, preserving the original extension

## License

[License information](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
