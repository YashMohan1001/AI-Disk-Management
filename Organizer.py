import os
import shutil
import joblib
import string
from pathlib import Path
from Categorizer import extract_text_from_file, clean_text

# Load model and vectorizer
model, vectorizer = joblib.load("file_classifier_model.pkl")

# Define paths
UNSORTED_DIR = Path("Unsorted")
TRAINING_DIR = Path("Training_data")  # Categories live here

# Make sure the unsorted folder exists
if not UNSORTED_DIR.exists():
    print("📁 Creating 'Unsorted' folder...")
    UNSORTED_DIR.mkdir()

# Process files
for file in UNSORTED_DIR.iterdir():
    if file.is_file():
        print(f"\n📦 Processing file: {file.name}")
        text = extract_text_from_file(file)
        if not text:
            print(f"⚠️ Skipping {file.name} (no text found)")
            continue

        cleaned = clean_text(text)
        vector = vectorizer.transform([cleaned])
        predicted_category = model.predict(vector)[0]
        
        target_dir = TRAINING_DIR / predicted_category
        target_dir.mkdir(exist_ok=True)

        shutil.move(str(file), target_dir / file.name)
        print(f"✅ Moved '{file.name}' to '{predicted_category}/'")
