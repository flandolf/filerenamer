import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


class DirectorySelector:
    """
    A utility class for selecting directories, starting from the home directory.

    This class provides both GUI and terminal-based methods for directory selection.
    """

    @staticmethod
    def select_directory_gui(title="Select Directory", initial_dir=None):
        """
        Opens a GUI dialog to select a directory, starting from the home directory by default.

        Args:
            title (str): The title for the directory selection dialog
            initial_dir (str, optional): The initial directory to start from.
                                       Defaults to home directory if None.

        Returns:
            str: The selected directory path, or None if selection was canceled
        """
        # Initialize Tkinter root window but hide it
        root = tk.Tk()
        root.withdraw()

        # Determine the initial directory
        if initial_dir is None:
            initial_dir = str(Path.home())
        else:
            # Expand ~ if present in the initial_dir
            initial_dir = os.path.expanduser(initial_dir)

        # Open the directory selection dialog
        selected_dir = filedialog.askdirectory(
            title=title,
            initialdir=initial_dir
        )

        # Destroy the hidden root window
        root.destroy()

        # Return None if the user cancelled, otherwise return the selected path
        return selected_dir if selected_dir else None

    @staticmethod
    def select_directory_terminal(prompt="Select a directory: ", start_dir=None):
        """
        Provides a terminal-based directory navigation and selection interface.

        Args:
            prompt (str): The prompt message to display
            start_dir (str, optional): The directory to start navigation from.
                                     Defaults to home directory if None.

        Returns:
            str: The selected directory path
        """
        # Start from the home directory if not specified
        current_dir = os.path.expanduser(start_dir if start_dir else "~")

        while True:
            # Clear the screen (works on Windows and Unix-like systems)
            os.system('cls' if os.name == 'nt' else 'clear')

            print(f"Current directory: {current_dir}")
            print("\nDirectories:")

            # List all directories in the current directory
            directories = []
            try:
                items = os.listdir(current_dir)
                for i, item in enumerate(sorted(items)):
                    item_path = os.path.join(current_dir, item)
                    if os.path.isdir(item_path):
                        directories.append(item)
                        print(f"  {i + 1}. {item}/")
            except PermissionError:
                print("  Permission denied to access this directory.")
                directories = []

            # Show navigation options
            print("\nOptions:")
            print("  0. Select current directory")
            print("  p. Go to parent directory")
            print("  h. Go to home directory")
            print("  q. Quit")

            # Get user input
            choice = input(f"\n{prompt}")

            if choice == 'q':
                return None
            elif choice == '0':
                return current_dir
            elif choice == 'p':
                current_dir = os.path.dirname(current_dir)
            elif choice == 'h':
                current_dir = os.path.expanduser("~")
            elif choice.isdigit() and 1 <= int(choice) <= len(directories):
                selected = directories[int(choice) - 1]
                current_dir = os.path.join(current_dir, selected)
            else:
                input("Invalid option. Press Enter to continue...")


# Example usage
if __name__ == "__main__":
    print("GUI Directory Selector Demo")
    selected_gui = DirectorySelector.select_directory_gui()
    print(f"Selected directory (GUI): {selected_gui}")

    print("\nTerminal Directory Selector Demo")
    selected_terminal = DirectorySelector.select_directory_terminal()
    print(f"Selected directory (Terminal): {selected_terminal}")
