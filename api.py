from flask import Flask, request, jsonify
from textblob import TextBlob
import re

from src.multilingual import translate_tamil_to_english
from src.sarcasm import detect_sarcasm


app = Flask(__name__)


# =========================================================
# ASPECT KEYWORDS
# =========================================================

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


# =========================================================
# EMOTION KEYWORDS
# =========================================================

emotion_keywords = {

    "Joy": [
        "happy",
        "excellent",
        "amazing",
        "awesome",
        "love",
        "great",
        "wonderful",
        "good"
    ],

    "Sadness": [
        "sad",
        "disappointed",
        "unhappy",
        "upset"
    ],

    "Anger": [
        "angry",
        "hate",
        "worst",
        "terrible",
        "furious"
    ],

    "Fear": [
        "fear",
        "scared",
        "danger",
        "afraid",
        "worried"
    ],

    "Surprise": [
        "surprised",
        "unexpected",
        "wow",
        "shocked"
    ],

    "Disgust": [
        "disgusting",
        "awful",
        "horrible",
        "dirty"
    ],

    "Trust": [
        "reliable",
        "trusted",
        "safe",
        "secure"
    ],

    "Anticipation": [
        "expect",
        "waiting",
        "hope",
        "looking forward"
    ]
}


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):

    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Keep English letters, numbers and spaces
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# =========================================================
# SENTIMENT ANALYSIS
# =========================================================

def get_sentiment(text):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.1:
        sentiment = "Positive"

    elif polarity < -0.1:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return sentiment, polarity


# =========================================================
# ASPECT EXTRACTION
# =========================================================

def extract_aspects(text):

    detected_aspects = []

    for aspect, keywords in aspect_keywords.items():

        for keyword in keywords:

            if keyword in text:

                detected_aspects.append(aspect)

                break

    return detected_aspects


# =========================================================
# EMOTION DETECTION
# =========================================================

def detect_emotion(text):

    emotion_scores = {}

    for emotion, keywords in emotion_keywords.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        emotion_scores[emotion] = score

    max_emotion = max(
        emotion_scores,
        key=emotion_scores.get
    )

    max_score = emotion_scores[max_emotion]

    if max_score == 0:

        return "No Emotion"

    return max_emotion


# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "message": "MULTILINGUAL SENTIMENT ANALYSIS API",

        "supported_languages": [
            "English",
            "Tamil"
        ],

        "features": [
            "Sentiment Analysis",
            "Aspect Extraction",
            "8-Emotion Classification",
            "Sarcasm Detection",
            "Multilingual Support"
        ],

        "endpoint": "/predict",

        "method": "POST"

    })


# =========================================================
# PREDICTION API
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get JSON request
        data = request.get_json()

        # Validate request
        if not data:

            return jsonify({
                "error": "Request body is empty"
            }), 400

        # Get review
        review = data.get("review")

        if not review:

            return jsonify({
                "error": "Please provide a review"
            }), 400

        # -------------------------------------------------
        # STEP 1: TRANSLATE TAMIL
        # -------------------------------------------------

        processed_review = translate_tamil_to_english(review)

        # -------------------------------------------------
        # STEP 2: CLEAN TEXT
        # -------------------------------------------------

        cleaned_review = clean_text(processed_review)

        # -------------------------------------------------
        # STEP 3: SENTIMENT
        # -------------------------------------------------

        sentiment, polarity = get_sentiment(
            cleaned_review
        )

        # -------------------------------------------------
        # STEP 4: ASPECTS
        # -------------------------------------------------

        aspects = extract_aspects(
            cleaned_review
        )

        # -------------------------------------------------
        # STEP 5: EMOTION
        # -------------------------------------------------

        emotion = detect_emotion(
            cleaned_review
        )

        # -------------------------------------------------
        # STEP 6: SARCASM
        # -------------------------------------------------

        sarcasm_result = detect_sarcasm(
            cleaned_review
        )

        # -------------------------------------------------
        # FINAL RESPONSE
        # -------------------------------------------------

        response = {

            "review": review,

            "processed_review": processed_review,

            "cleaned_review": cleaned_review,

            "sentiment": sentiment,

            "polarity": round(
                polarity,
                3
            ),

            "aspects": aspects,

            "emotion": emotion,

            "sarcasm": sarcasm_result["sarcasm"],

            "sarcasm_confidence":
                sarcasm_result["confidence"],

            "sarcasm_score":
                sarcasm_result["score"],

            "sarcasm_indicators":
                sarcasm_result["indicators"]
        }

        return jsonify(response)

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


# =========================================================
# RUN API
# =========================================================

if __name__ == "__main__":

    print("\n==========================================")
    print("MULTILINGUAL SENTIMENT ANALYSIS API")
    print("==========================================")

    print("\nSupported Languages:")
    print("1. English")
    print("2. Tamil")

    print("\nFeatures:")
    print("1. Sentiment Analysis")
    print("2. Aspect Extraction")
    print("3. Emotion Classification")
    print("4. Sarcasm Detection")
    print("5. Multilingual Support")

    print("\nAPI Endpoint:")
    print("http://127.0.0.1:5000/predict")

    print("\nStarting server...\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )