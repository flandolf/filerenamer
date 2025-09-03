import dotenv
import os
from colorama import Fore, init
from google import genai
from directory_selector import DirectorySelector

MODEL_NAME = "gemma-3-27b-it"

init()

dotenv.load_dotenv()
client = genai.Client(api_key=os.environ["API_KEY"])

def main():
    print(Fore.CYAN + "Welcome to File Renamer!" + Fore.RESET)
    selector = DirectorySelector()
    selected_dir = selector.select_directory_gui()

    if selected_dir:
        print(Fore.GREEN + f"\nSelected directory: {selected_dir}" + Fore.RESET)

        # Display files in the selected directory
        print("\nDirectory contents:")
        try:
            for item in sorted(os.listdir(selected_dir)):
                print(f"  - {item}")
        except PermissionError:
            print(Fore.RED + "Permission denied to access this directory." + Fore.RESET)
    else:
        print(Fore.YELLOW + "No directory selected. Exiting." + Fore.RESET)



if __name__ == "__main__":
    main()
