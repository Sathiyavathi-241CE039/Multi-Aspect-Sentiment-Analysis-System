import re
import nltk
import spacy

from nltk.stem import WordNetLemmatizer

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# NLTK lemmatizer
lemmatizer = WordNetLemmatizer()


def preprocess_review(text):

    # -----------------------------
    # 1. Original Text
    # -----------------------------
    original_text = str(text)

    # -----------------------------
    # 2. Lowercase
    # -----------------------------
    cleaned_text = original_text.lower()

    # -----------------------------
    # 3. Remove URLs
    # -----------------------------
    cleaned_text = re.sub(
        r"http\S+|www\S+",
        "",
        cleaned_text
    )

    # -----------------------------
    # 4. Remove special characters
    # -----------------------------
    cleaned_text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        cleaned_text
    )

    # -----------------------------
    # 5. Remove extra spaces
    # -----------------------------
    cleaned_text = re.sub(
        r"\s+",
        " ",
        cleaned_text
    ).strip()

    # -----------------------------
    # 6. Tokens
    # -----------------------------
    tokens = nltk.word_tokenize(cleaned_text)

    # -----------------------------
    # 7. NLTK Lemmatization
    # -----------------------------
    lemmatized = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    # -----------------------------
    # 8. spaCy Processing
    # -----------------------------
    doc = nlp(original_text)

    spacy_tokens = [
        token.text
        for token in doc
    ]

    # -----------------------------
    # Return all results
    # -----------------------------
    return {
        "original_text": original_text,
        "cleaned_text": cleaned_text,
        "tokens": tokens,
        "lemmatized": lemmatized,
        "spacy_tokens": spacy_tokens
    }