
import os
import textract
import joblib
import string
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Define training directory
TRAINING_DIR = Path("Training_data")

# Categories (these are your subfolder names inside Training_data)
CATEGORIES = [d.name for d in TRAINING_DIR.iterdir() if d.is_dir()]

# Smart extractor function
def extract_text_from_file(file_path):
    try:
        file_path=Path(file_path)
        if file_path.suffix.lower() in [".txt", ".py", ".md", ".json", ".csv",".css",".pptx",".docx",".jpg",".mp4",".mp3",".png"]:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        else:
            return textract.process(str(file_path)).decode("utf-8")
    except Exception as e:
        print(f"❌ Failed to extract {file_path.name}: {e}")
        return None

# Clean text
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

# Load training data
print("🔍 Loading training data...")
texts = []
labels = []

for category in CATEGORIES:
    category_path = TRAINING_DIR / category
    for file in category_path.iterdir():
        if file.is_file():
            print(f"🔎 Trying to extract from: {file}")
            raw_text = extract_text_from_file(file)
            if raw_text:
                texts.append(clean_text(raw_text))
                labels.append(category)

# Vectorize the text
print("🧠 Training classifier...")
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
y = np.array(labels)

# Train classifier
model = MultinomialNB()
model.fit(X, y)

# Save model and vectorizer as a tuple
joblib.dump((model, vectorizer), "file_classifier_model.pkl")
print("✅ Model saved to file_classifier_model.pkl")

# Prediction function for GUI use
def predict_category(model_tuple, raw_text):
    model, vectorizer = model_tuple
    cleaned = clean_text(raw_text)
    vector = vectorizer.transform([cleaned])
    return model.predict(vector)[0]
