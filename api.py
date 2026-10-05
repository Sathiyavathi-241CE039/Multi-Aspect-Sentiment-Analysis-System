from flask import Flask, request, jsonify
import re

import nltk
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

from src.multilingual import translate_tamil_to_english
from src.sarcasm import detect_sarcasm

app = Flask(__name__)

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet", quiet=True)

try:
    nltk.data.find("corpora/omw-1.4")
except LookupError:
    nltk.download("omw-1.4", quiet=True)


lemmatizer = WordNetLemmatizer()

nlp = None
spacy_status = "Not loaded"


def load_spacy():

    global nlp
    global spacy_status

    if nlp is not None:
        return nlp

    try:

        import spacy

        nlp = spacy.load(
            "en_core_web_sm"
        )

        spacy_status = "Available"

        return nlp

    except Exception as e:

        nlp = None

        spacy_status = (
            "Unavailable: "
            + str(e)
        )

        return None

aspect_keywords = {

    "Battery": [
        "battery",
        "battery life",
        "charging",
        "charge"
    ],

    "Price": [
        "price",
        "cost",
        "expensive",
        "cheap",
        "value"
    ],

    "Quality": [
        "quality",
        "build",
        "material",
        "durable"
    ],

    "Performance": [
        "performance",
        "speed",
        "fast",
        "slow",
        "processor"
    ],

    "Design": [
        "design",
        "look",
        "appearance",
        "style"
    ],

    "Size": [
        "size",
        "small",
        "large",
        "compact"
    ],

    "Display": [
        "display",
        "screen",
        "resolution",
        "brightness"
    ],

    "Camera": [
        "camera",
        "photo",
        "picture",
        "video"
    ],

    "Delivery": [
        "delivery",
        "shipping",
        "arrived",
        "package"
    ],

    "Customer_Service": [
        "service",
        "support",
        "customer service",
        "seller"
    ]
}
emotion_keywords = {

    "Joy": [
        "happy",
        "love",
        "excellent",
        "amazing",
        "awesome",
        "great",
        "good",
        "wonderful",
        "fantastic",
        "satisfied",
        "joy",
        "like"
    ],
    "Sadness": [
        "sad",
        "unhappy",
        "disappointed",
        "disappointment",
        "upset",
        "cry"
    ],

    "Anger": [
        "angry",
        "anger",
        "hate",
        "worst",
        "furious",
        "annoyed",
        "irritated"
    ],

    "Fear": [
        "fear",
        "scared",
        "danger",
        "dangerous",
        "afraid",
        "worry",
        "worried"
    ],

    "Surprise": [
        "surprise",
        "surprised",
        "unexpected",
        "wow",
        "shocked"
    ],

    "Disgust": [
        "disgusting",
        "disgust",
        "awful",
        "gross",
        "terrible"
    ],

    "Trust": [
        "trust",
        "reliable",
        "safe",
        "secure",
        "honest"
    ],

    "Anticipation": [
        "expect",
        "expected",
        "waiting",
        "hope",
        "hopefully",
        "looking forward"
    ]
}

def clean_text(text):

    if text is None:
        return ""

    text = str(text)

    try:

        text = translate_tamil_to_english(
            text
        )

    except Exception:

        pass


    # -----------------------------------------
    # Lowercase
    # -----------------------------------------

    text = text.lower()


    # -----------------------------------------
    # Remove URLs
    # -----------------------------------------

    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )


    # -----------------------------------------
    # Remove special characters
    # -----------------------------------------

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )


    # -----------------------------------------
    # Remove extra spaces
    # -----------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()


    return text


# =========================================================
# NLTK TOKENIZATION
# =========================================================

def get_tokens(text):

    try:

        return nltk.word_tokenize(
            text
        )

    except Exception:

        return text.split()


# =========================================================
# NLTK LEMMATIZATION
# =========================================================

def get_lemmatized(tokens):

    lemmatized_words = []

    for word in tokens:

        try:

            lemma = lemmatizer.lemmatize(
                word
            )

        except Exception:

            lemma = word

        lemmatized_words.append(
            lemma
        )

    return lemmatized_words


# =========================================================
# OPTIONAL SPACY TOKENS
# =========================================================

def get_spacy_tokens(text):

    model = load_spacy()

    if model is None:

        return []


    try:

        doc = model(
            text
        )

        return [
            token.text
            for token in doc
        ]

    except Exception:

        return []


# =========================================================
# COMPLETE PREPROCESSING
# =========================================================

def preprocess_review(text):

    original_text = str(
        text
    )


    # Clean text
    cleaned_text = clean_text(
        original_text
    )


    # NLTK tokens
    tokens = get_tokens(
        cleaned_text
    )


    # NLTK lemmatization
    lemmatized = get_lemmatized(
        tokens
    )


    # Optional spaCy
    spacy_tokens = get_spacy_tokens(
        original_text
    )


    return {

        "original_text":
            original_text,

        "cleaned_text":
            cleaned_text,

        "tokens":
            tokens,

        "lemmatized":
            lemmatized,

        "spacy_tokens":
            spacy_tokens
    }


# =========================================================
# ASPECT EXTRACTION
# =========================================================

def extract_aspects(text):

    text = text.lower()

    detected_aspects = []


    for aspect, keywords in aspect_keywords.items():

        for keyword in keywords:

            if keyword.lower() in text:

                detected_aspects.append(
                    aspect
                )

                break


    return detected_aspects


# =========================================================
# EMOTION DETECTION
# =========================================================

def detect_emotion_custom(text):

    text = text.lower()

    emotion_scores = {}


    for emotion, keywords in emotion_keywords.items():

        score = 0

        for keyword in keywords:

            if keyword.lower() in text:

                score += 1

        emotion_scores[
            emotion
        ] = score


    if not emotion_scores:

        return "No Emotion"


    best_emotion = max(

        emotion_scores,

        key=emotion_scores.get
    )


    best_score = emotion_scores[
        best_emotion
    ]


    if best_score == 0:

        return "No Emotion"


    return best_emotion


# =========================================================
# SENTIMENT ANALYSIS
# =========================================================

def analyze_sentiment(text):

    if not text.strip():

        return {

            "sentiment":
                "Neutral",

            "polarity":
                0.0
        }


    blob = TextBlob(
        text
    )


    polarity = (
        blob.sentiment.polarity
    )


    if polarity > 0.1:

        sentiment = "Positive"

    elif polarity < -0.1:

        sentiment = "Negative"

    else:

        sentiment = "Neutral"


    return {

        "sentiment":
            sentiment,

        "polarity":
            round(
                polarity,
                3
            )
    }


# =========================================================
# HOME ROUTE
# =========================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return jsonify({

        "message":
            "Multi-Aspect Sentiment Analysis API",

        "status":
            "running",

        "endpoint":
            "/predict",

        "method":
            "POST",

        "spacy":
            spacy_status,

        "example": {

            "review":
                "The battery life is excellent."
        }
    })


# =========================================================
# PREDICT ROUTE
# =========================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        # -----------------------------------------
        # Get JSON
        # -----------------------------------------

        data = request.get_json(
            silent=True
        )


        if not data:

            return jsonify({

                "error":
                    "Request body must contain JSON."
            }), 400


        # -----------------------------------------
        # Get review
        # -----------------------------------------

        review = data.get(
            "review",
            ""
        )


        if not isinstance(
            review,
            str
        ):

            review = str(
                review
            )


        if not review.strip():

            return jsonify({

                "error":
                    "Review cannot be empty."
            }), 400


        # -----------------------------------------
        # Tamil translation
        # -----------------------------------------

        try:

            processed_review = (
                translate_tamil_to_english(
                    review
                )
            )

        except Exception:

            processed_review = review


        # -----------------------------------------
        # PREPROCESSING
        # -----------------------------------------

        preprocessing = (
            preprocess_review(
                processed_review
            )
        )


        cleaned_review = (
            preprocessing[
                "cleaned_text"
            ]
        )


        tokens = (
            preprocessing[
                "tokens"
            ]
        )


        lemmatized = (
            preprocessing[
                "lemmatized"
            ]
        )


        spacy_tokens = (
            preprocessing[
                "spacy_tokens"
            ]
        )


        # -----------------------------------------
        # SENTIMENT
        # -----------------------------------------

        sentiment_result = (
            analyze_sentiment(
                cleaned_review
            )
        )


        sentiment = (
            sentiment_result[
                "sentiment"
            ]
        )


        polarity = (
            sentiment_result[
                "polarity"
            ]
        )


        # -----------------------------------------
        # ASPECT
        # -----------------------------------------

        aspects = extract_aspects(
            cleaned_review
        )


        # -----------------------------------------
        # EMOTION
        # -----------------------------------------

        emotion = (
            detect_emotion_custom(
                cleaned_review
            )
        )


        # -----------------------------------------
        # SARCASM
        # -----------------------------------------

        try:

            sarcasm_result = (
                detect_sarcasm(
                    cleaned_review
                )
            )

        except Exception:

            sarcasm_result = {

                "sarcasm":
                    False,

                "confidence":
                    0.0,

                "score":
                    0,

                "indicators":
                    []
            }


        # -----------------------------------------
        # FINAL RESPONSE
        # -----------------------------------------

        response = {

            # Original
            "review":
                review,

            # Tamil translation / processed
            "processed_review":
                processed_review,

            # Preprocessing
            "cleaned_review":
                cleaned_review,

            "tokens":
                tokens,

            "lemmatized":
                lemmatized,

            "spacy_tokens":
                spacy_tokens,

            "spacy_status":
                spacy_status,

            # Sentiment
            "sentiment":
                sentiment,

            "polarity":
                polarity,

            # Aspect
            "aspects":
                aspects,

            # Emotion
            "emotion":
                emotion,

            # Sarcasm
            "sarcasm":
                sarcasm_result.get(
                    "sarcasm",
                    False
                ),

            "sarcasm_confidence":
                sarcasm_result.get(
                    "confidence",
                    0.0
                ),

            "sarcasm_score":
                sarcasm_result.get(
                    "score",
                    0
                ),

            "sarcasm_indicators":
                sarcasm_result.get(
                    "indicators",
                    []
                )
        }


        return jsonify(
            response
        )


    except Exception as e:

        return jsonify({

            "error":
                str(e)

        }), 500


# =========================================================
# START FLASK
# =========================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=False,

        use_reloader=False
    )
