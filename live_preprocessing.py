
import re
import nltk
from nltk.stem import WordNetLemmatizer

# NLTK setup
lemmatizer = WordNetLemmatizer()


def preprocess_review(text):
    original_text = str(text or "")

    # 1. Convert text to lowercase
    cleaned_text = original_text.lower()

    # 2. Remove URLs
    cleaned_text = re.sub(
        r"http\S+|www\S+",
        "",
        cleaned_text
    )

    # 3. Remove special characters
    cleaned_text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        cleaned_text
    )

    # 4. Remove extra spaces
    cleaned_text = re.sub(
        r"\s+",
        " ",
        cleaned_text
    ).strip()

    # 5. Tokenization
    try:
        tokens = nltk.word_tokenize(cleaned_text)
    except LookupError:
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)
        tokens = nltk.word_tokenize(cleaned_text)

    # 6. Lemmatization
    try:
        lemmatized = [
            lemmatizer.lemmatize(word)
            for word in tokens
        ]
    except LookupError:
        nltk.download("wordnet", quiet=True)
        lemmatized = [
            lemmatizer.lemmatize(word)
            for word in tokens
        ]

    # 7. Optional spaCy processing
    spacy_tokens = []
    spacy_status = "Unavailable"

    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(original_text)
        spacy_tokens = [token.text for token in doc]
        spacy_status = "Available"
    except Exception:
        spacy_status = "Model unavailable or spaCy error"

    # 8. Return results
    return {
        "original_text": original_text,
        "cleaned_text": cleaned_text,
        "tokens": tokens,
        "lemmatized": lemmatized,
        "spacy_tokens": spacy_tokens,
        "spacy_status": spacy_status
    }
