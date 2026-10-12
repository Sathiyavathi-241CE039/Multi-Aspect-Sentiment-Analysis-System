import pandas as pd
import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required resources
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

# Load dataset
df = pd.read_csv("data/final_dataset.csv")

# Stopwords
stop_words = set(stopwords.words("english"))

# Keep important negative words
important_words = {"no", "not", "never", "neither", "nor"}

stop_words = stop_words - important_words


# Text cleaning function
def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Tokenization
    words = word_tokenize(text)

    # Remove stopwords
    words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(words)


# Apply cleaning
df["cleaned_review"] = df["reviewText"].apply(clean_text)

# Save processed dataset
df.to_csv(
    "data/processed_reviews.csv",
    index=False
)

print("Preprocessing completed successfully!")

print("\nOriginal Review:")
print(df["reviewText"].iloc[0])

print("\nCleaned Review:")
print(df["cleaned_review"].iloc[0])

print("\nDataset Shape:")
print(df.shape)