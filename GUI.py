import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import joblib
from Categorizer import extract_text_from_file, predict_category  # Adjust if you use different names

# Load the trained model
model = joblib.load("file_classifier_model.pkl")

# Categories directory (you can change this path)
CATEGORIES = ['audio', 'code', 'documents', 'images', 'videos']

def categorize_files_in_directory(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                text = extract_text_from_file(file_path)
                if text:
                    category = predict_category(model, text)
                    category_folder = os.path.join(folder_path, category)
                    os.makedirs(category_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(category_folder, filename))
            except Exception as e:
                print(f"Error processing {filename}: {e}")

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        categorize_files_in_directory(folder_path)
        messagebox.showinfo("Success", "Files categorized successfully!")

# GUI setup
root = tk.Tk()
root.title("AI File Categorizer")
root.geometry("400x200")

label = tk.Label(root, text="AI-Powered File Categorizer", font=("Arial", 14))
label.pack(pady=20)

browse_btn = tk.Button(root, text="Choose Folder and Categorize", command=browse_folder, font=("Arial", 12))
browse_btn.pack(pady=10)

root.mainloop()
