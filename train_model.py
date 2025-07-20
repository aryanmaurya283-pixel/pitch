# train_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import re
from textblob import TextBlob  # May need to install: pip install textblob
import textstat  # May need to install: pip install textstat
import numpy as np
from scipy.sparse import hstack

# Ensure NLTK data is downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Text Preprocessing Function (consistent with app)
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text) # Remove numbers
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    punctuations = string.punctuation
    filtered_tokens = [word for word in tokens if word not in stop_words and word not in punctuations and word.isalpha()]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    return " ".join(lemmatized_tokens)

# 1. Load the dataset
try:
    df = pd.read_csv('pitches_data.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'pitches_data.csv' not found. Please create it first.")
    exit()

# Ensure columns are correct
if 'pitch_text' not in df.columns or 'score' not in df.columns:
    print("Error: CSV must have 'pitch_text' and 'score' columns.")
    exit()

df.dropna(inplace=True) # Remove rows with missing data

# 2. Preprocess the pitch text
print("Preprocessing text data...")
df['processed_text'] = df['pitch_text'].apply(preprocess_text)

# --- Additional Features ---
print("Extracting additional features (sentiment, readability, length, section presence)...")
section_keywords = {
    'problem': ['problem', 'pain point', 'challenge'],
    'solution': ['solution', 'approach', 'how we solve'],
    'market': ['market', 'TAM', 'SAM', 'SOM', 'opportunity'],
    'team': ['team', 'founder', 'co-founder', 'background'],
    'business_model': ['business model', 'revenue', 'pricing', 'monetization'],
    'competition': ['competition', 'competitor', 'competitive'],
    'traction': ['traction', 'growth', 'metrics', 'users'],
    'ask': ['ask', 'funding', 'raise', 'investment']
}
def has_section(text, keywords):
    text = text.lower()
    return int(any(kw in text for kw in keywords))
for section, keywords in section_keywords.items():
    df[f'section_{section}'] = df['pitch_text'].apply(lambda x: has_section(x, keywords))

def get_sentiment(text):
    # pyright: ignore[reportAttributeAccessIssue]
    return TextBlob(text).sentiment.polarity

def get_readability(text):
    try:
        return len(text.split()) / (text.count('.') + 1)  # crude avg sentence length
    except Exception:
        return 20  # Neutral value if error

def get_length(text):
    return len(text.split())

df['sentiment'] = df['pitch_text'].apply(get_sentiment)
df['readability'] = df['pitch_text'].apply(get_readability)
df['length'] = df['pitch_text'].apply(get_length)

# 3. Define features (X) and target (y)
X_text = df['processed_text']
y = df['score']

# 4. Create and fit the TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=3000, min_df=2, ngram_range=(1, 2))
X_vectorized = vectorizer.fit_transform(X_text)
print("Text vectorization complete.")

# 4b. Combine with additional features
section_cols = [f'section_{s}' for s in section_keywords]
extra_features = df[['sentiment', 'readability', 'length'] + section_cols].values
X_full = hstack([X_vectorized, extra_features])

# 5. Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X_full, y, test_size=0.2, random_state=42)

# 6. Initialize and train the Machine Learning model
print("Training the RandomForestRegressor model...")
model = RandomForestRegressor(n_estimators=150, max_depth=10, min_samples_leaf=2, random_state=42)
model.fit(X_train, y_train)
print("Model training complete.")

# 7. Evaluate the model (optional but recommended)
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f"Model Performance (Mean Squared Error): {mse:.2f}")

# 8. Save the trained model and the vectorizer
joblib.dump(model, 'pitch_quality_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

print("\n✅ Model and vectorizer have been saved successfully!")
print("Files created: 'pitch_quality_model.pkl' and 'tfidf_vectorizer.pkl'") 