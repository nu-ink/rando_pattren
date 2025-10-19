import os
import shutil

def organize_desktop():
    # Set the path to your desktop
    desktop_path = os.path.expanduser("~/Desktop")

    # File type categories and their extensions
    categories = {
        "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff"],
        "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
        "Music": [".mp3", ".wav", ".aac", ".flac"],
        "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
        "Code": [".py", ".js", ".html", ".css", ".cpp", ".java", ".rb", ".php"],
        "Others": []  # Files that don't fit into the above categories
    }

    # Create folders for categories if they don't exist
    for category in categories.keys():
        folder_path = os.path.join(desktop_path, category)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Get all files on the desktop
    files = [f for f in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, f))]

    # Move files into appropriate folders
    for file_name in files:
        file_path = os.path.join(desktop_path, file_name)
        file_ext = os.path.splitext(file_name)[1].lower()

        moved = False
        for category, extensions in categories.items():
            if file_ext in extensions:
                dest_folder = os.path.join(desktop_path, category)
                shutil.move(file_path, os.path.join(dest_folder, file_name))
                print(f"Moved: {file_name} to {category}")
                moved = True
                break

        if not moved:  # If file doesn't match any category, move to "Others"
            dest_folder = os.path.join(desktop_path, "Others")
            shutil.move(file_path, os.path.join(dest_folder, file_name))
            print(f"Moved: {file_name} to Others")

    print("Desktop organized successfully!")

if __name__ == "__main__":
    organize_desktop()
