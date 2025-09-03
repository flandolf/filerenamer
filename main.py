import mimetypes
import dotenv
import os
from colorama import Fore, init
from google import genai
from google.genai import types
from directory_selector import DirectorySelector
from sys import exit
import pathlib
MODEL_NAME = "gemma-3-27b-it"

init()

dotenv.load_dotenv()
client = genai.Client(api_key=os.environ["API_KEY"])

def main():
    print(Fore.CYAN + "Welcome to File Renamer!" + Fore.RESET)
    selector = DirectorySelector()
    selected_dir = selector.select_directory_gui()
    dirs = []
    files = []
    if selected_dir:
        print(Fore.GREEN + f"\nSelected directory: {selected_dir}" + Fore.RESET)
        # Display files in the selected directory
        print("\nDirectory contents:")
        try:
            for item in sorted(os.listdir(selected_dir)):
                # Check if item is a directory or file
                if os.path.isdir(os.path.join(selected_dir, item)):
                    dirs.append(os.path.join(selected_dir, item))
        except PermissionError:
            print(Fore.RED + "Permission denied to access this directory." + Fore.RESET)
        for dir in dirs:
            print(Fore.CYAN + f"\nEntering directory: {dir}" + Fore.RESET)
            # print full path of files in the directory
            try:
                for item in sorted(os.listdir(dir)):
                    if os.path.isfile(os.path.join(dir, item)):
                        print(Fore.BLUE + f"- {item}")
                        files.append(os.path.join(dir, item))
            except PermissionError:
                print(Fore.RED + "Permission denied to access this directory." + Fore.RESET)

            for file in files:
                print(Fore.MAGENTA + f"\nProcessing file: {file}" + Fore.RESET)
                file_basename = os.path.basename(file)
                file_extension = pathlib.Path(file).suffix
                if file_extension.lower() not in ['.pdf', '.docx']:
                    print(Fore.YELLOW + f"Skipping unsupported file type: {file_extension}" + Fore.RESET)
                    continue
                prompt= f"""
                Suggest a better filename for: '{file_basename}'.
                Rules:
                - Return only the new filename (no extension).
                - Do not include any extra words, punctuation, or explanations.
                - Improve readability by capitalising words and removing unnecessary symbols.
                """
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=[prompt]
                )
                new_filename = str(response.text).strip() + file_extension
                if input(Fore.YELLOW + f"Rename '{file_basename}' to '{new_filename}'? (y/n): " + Fore.RESET).lower() == 'y':
                    new_file_path = os.path.join(dir, new_filename)
                    try:
                        os.rename(file, new_file_path)
                        print(Fore.GREEN + f"Renamed to: {new_filename}" + Fore.RESET)
                    except Exception as e:
                        print(Fore.RED + f"Error renaming file: {e}" + Fore.RESET)
    else:
        print(Fore.YELLOW + "No directory selected. Exiting." + Fore.RESET)
        exit(0)





if __name__ == "__main__":
    main()
