# File Renamer

A Python utility for working with files and directories, featuring flexible directory selection tools.

## Features

- **Directory Selection**: Navigate and select directories using either:
  - GUI-based directory picker
  - Terminal-based interactive directory browser
- Both options start from the user's home directory (`~`) by default
- File listing and manipulation capabilities

## Installation

1. Clone this repository:
   ```bash
   git clone [repository-url]
   cd filerenamer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application:

```bash
python main.py
```

This will prompt you to choose between GUI and terminal-based directory selection.

### Using the Directory Selector Directly

You can also use the directory selector component in your own Python scripts:

```python
from directory_selector import DirectorySelector

# GUI-based selection
selected_dir = DirectorySelector.select_directory_gui(
    title="Select Directory",
    initial_dir="~"  # Starts from home directory
)

# OR Terminal-based selection
selected_dir = DirectorySelector.select_directory_terminal(
    prompt="Choose a directory: ",
    start_dir="~"    # Starts from home directory
)

# Process the selected directory
if selected_dir:
    print(f"Selected: {selected_dir}")
    # Do something with the selected directory
```

## Directory Selector Features

### GUI Selector
- Uses native file dialog for a familiar user experience
- Preserves the last selected location between invocations
- Simple one-line call to get a directory path

### Terminal Selector
- Works in environments without GUI support
- Intuitive navigation with numbered options
- Keyboard shortcuts for common operations:
  - `0`: Select current directory
  - `p`: Go to parent directory
  - `h`: Go to home directory
  - `q`: Quit selection

## Requirements

- Python 3.6+
- Tkinter (included with most Python installations)
- colorama (for terminal colors)

## License

This project is licensed under the MIT License - see the LICENSE file for details.