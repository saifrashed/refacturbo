# helpers.py
import os

def delete_files_in_directory(path):
    """
    Recursively delete all files in the specified directory and its subdirectories.
    Directories themselves are not deleted.
    """
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            try:
                print(f"Deleting file: {item_path}")
                os.remove(item_path)  # Delete the file
            except OSError as e:
                print(f"Error deleting file {item_path}: {e}")
        elif os.path.isdir(item_path):
            # Recursively process subdirectories
            delete_files_in_directory(item_path)