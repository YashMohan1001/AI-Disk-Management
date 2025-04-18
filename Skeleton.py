import os
import shutil
from pathlib import Path

# === Configuration ===
path1=input("Enter Path: ")
SOURCE_DIR = path1  # Replace with your target directory
DESTINATION_DIR = "organized_files" 
# === Supported categories (these will be AI-predicted later) ===
CATEGORIES = ["documents", "images", "videos", "audio", "code", "others"]

def setup_directories():
    """Create folders for each category inside destination directory."""
    os.makedirs(DESTINATION_DIR, exist_ok=True)
    for category in CATEGORIES:
        os.makedirs(os.path.join(DESTINATION_DIR, category), exist_ok=True)

def categorize_file(file_path):
    """
    Placeholder for AI categorization.
    For now, categorize based on file extension.
    """
    ext = file_path.suffix.lower()
    if ext in ['.txt', '.pdf', '.docx', '.pptx']:
        return "documents"
    elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
        return "images"
    elif ext in ['.mp4', '.mov', '.avi']:
        return "videos"
    elif ext in ['.mp3', '.wav']:
        return "audio"
    elif ext in ['.py', '.java', '.cpp', '.js']:
        return "code"
    else:
        return "others"

def organize_files():
    """Scan and move files based on simple categorization."""
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = Path(root) / file
            category = categorize_file(file_path)
            dest_path = Path(DESTINATION_DIR) / category / file_path.name
            print(f"Moving: {file_path} → {dest_path}")
            shutil.copy2(file_path, dest_path)

if __name__ == "__main__":
    setup_directories()
    organize_files()
    print("✅ File organization completed.")
