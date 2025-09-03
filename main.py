import curses
from dotenv import load_dotenv
import os
from colorama import Fore, init
from google import genai
from sys import exit
from directory_selector import directory_selector
MODEL_NAME = "gemma-3-27b-it"

init()
load_dotenv()

client = genai.Client(api_key=os.environ["API_KEY"])

def main():
    print(Fore.CYAN + "Welcome to File Renamer!" + Fore.RESET)
    selected_dir = curses.wrapper(directory_selector)
    files = []
    if selected_dir:
        for item in sorted(os.listdir(selected_dir)):
            subdir_path = os.path.join(selected_dir, item)
            if os.path.isdir(subdir_path):
                try:
                    for file in sorted(os.listdir(subdir_path)):
                        file_path = os.path.join(subdir_path, file)
                        if os.path.isfile(file_path):
                            files.append(file_path)
                except PermissionError:
                    print(Fore.RED + f"Permission denied: {subdir_path}" + Fore.RESET)
        print(Fore.GREEN + f"Selected directory: {selected_dir}" + Fore.RESET)
        print(Fore.BLUE + f"Files: {files}" + Fore.RESET)
    else:
        print(Fore.YELLOW + "No directory selected. Exiting." + Fore.RESET)
        exit(0)

if __name__ == "__main__":
    main()
