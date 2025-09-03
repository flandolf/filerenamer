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

# Example usage
if __name__ == "__main__":
    print("GUI Directory Selector Demo")
    selected_gui = DirectorySelector.select_directory_gui()
    print(f"Selected directory (GUI): {selected_gui}")
