import curses
from dotenv import load_dotenv
import os
from colorama import Fore, init
from google import genai
from sys import exit
from directory_selector import directory_selector
from functools import partial
MODEL_NAME = "gemma-3n-e2b-it"

def prompt(filename):
    return (
        f"Clean and rename this messy filename: {filename}. "
        f"Respond only with the new filename, without the extension. "
        f"Fix common issues by capitalizing words, replacing underscores/dashes with spaces, "
        f"removing numbers and special characters, and making it concise and readable. "
        f"Do not add extra words, explanations, or punctuation."
    )

init()
load_dotenv()

def main():
    print(Fore.CYAN + "Welcome to File Renamer!" + Fore.RESET)
    safe_mode = os.getenv("SAFE_MODE", "y").lower()
    start_path = os.getenv("START_PATH", "~")
    selected_dir = curses.wrapper(partial(directory_selector, start_path=start_path))
    files = []
    if selected_dir:
        # Get all items in the selected directory
        try:
            items = sorted(os.listdir(selected_dir))
        except (PermissionError, InterruptedError, FileNotFoundError) as e:
            print(Fore.RED + f"Cannot access {selected_dir} ({e.__class__.__name__})" + Fore.RESET)
            items = []

        # Separate directories and files
        subdirs = [os.path.join(selected_dir, item) for item in items if os.path.isdir(os.path.join(selected_dir, item))]
        files_in_dir = [os.path.join(selected_dir, item) for item in items if os.path.isfile(os.path.join(selected_dir, item))]

        if subdirs:
            # Iterate through subdirectories if they exist
            for subdir_path in subdirs:
                try:
                    for file in sorted(os.listdir(subdir_path)):
                        file_path = os.path.join(subdir_path, file)
                        if os.path.isfile(file_path):
                            files.append(file_path)
                except (PermissionError, InterruptedError, FileNotFoundError) as e:
                    print(Fore.RED + f"Skipping {subdir_path} ({e.__class__.__name__})" + Fore.RESET)
        else:
            # No subdirectories, use files in the selected directory directly
            files.extend(files_in_dir)


        print(Fore.GREEN + f"Selected directory: {selected_dir}" + Fore.RESET)
        client = genai.Client(api_key=os.getenv("API_KEY"))
        for file in files:
            filename = os.path.basename(file)
            extension = filename.split('.')[-1]
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[prompt(filename)]
            )
            new_filename = str(response.text).strip()
            if safe_mode == 'n':
                rename_file(file, new_filename, extension)

            else:
                # Ask the user for confirmation
                if input(Fore.YELLOW + f"Rename '{filename}' to '{new_filename + '.' + extension}'? (y/n): " + Fore.RESET).lower() == 'y':
                    rename_file(file, new_filename, extension)


    else:
        print(Fore.YELLOW + "No directory selected. Exiting." + Fore.RESET)
        exit(0)

def rename_file(old_path, new_name, extension):
    new_path = os.path.join(os.path.dirname(old_path), new_name + '.' + extension)
    if file_exists_case_sensitive(new_path, new_name + '.' + extension):
        print(Fore.RED + f"Error: A file named '{new_name + '.' + extension}' already exists. Skipping." + Fore.RESET)
        return False
    try:
        os.rename(old_path, new_path)
        print(Fore.GREEN + f"Renamed to '{new_name + '.' + extension}'" + Fore.RESET)
        return True
    except Exception as e:
        print(Fore.RED + f"Error renaming file: {e}" + Fore.RESET)
        return False

def file_exists_case_sensitive(path, filename):
    directory = os.path.dirname(path) or "."
    return filename in os.listdir(directory)


if __name__ == "__main__":
    main()
