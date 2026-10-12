import pandas as pd


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/processed_reviews.csv"
)


# ==========================================
# EMOTION KEYWORDS
# ==========================================

emotion_keywords = {

    "Joy": [
        "happy",
        "love",
        "excellent",
        "great",
        "amazing",
        "wonderful",
        "perfect",
        "awesome",
        "fantastic",
        "satisfied"
    ],

    "Sadness": [
        "sad",
        "disappointed",
        "disappointing",
        "unhappy",
        "regret",
        "miss",
        "poor",
        "failed"
    ],

    "Anger": [
        "angry",
        "hate",
        "annoying",
        "annoyed",
        "frustrated",
        "worst",
        "terrible",
        "useless",
        "ridiculous"
    ],

    "Fear": [
        "afraid",
        "fear",
        "scared",
        "worried",
        "danger",
        "risk",
        "unsafe",
        "problem"
    ],

    "Surprise": [
        "surprised",
        "unexpected",
        "surprising",
        "amazing",
        "wow",
        "shock",
        "shocked"
    ],

    "Disgust": [
        "disgusting",
        "disgusted",
        "awful",
        "gross",
        "horrible",
        "dirty",
        "bad smell"
    ],

    "Trust": [
        "trust",
        "reliable",
        "safe",
        "dependable",
        "genuine",
        "authentic",
        "recommend",
        "recommended"
    ],

    "Anticipation": [
        "expect",
        "expected",
        "waiting",
        "future",
        "hope",
        "hopefully",
        "looking forward",
        "excited"
    ]
}


# ==========================================
# EMOTION DETECTION
# ==========================================

def detect_emotion(text):

    if pd.isna(text):
        return "No Emotion"

    text = str(text).lower()

    scores = {}

    for emotion, keywords in emotion_keywords.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[emotion] = score


    # Find emotion with highest score
    max_score = max(
        scores.values()
    )


    # No emotion detected
    if max_score == 0:
        return "No Emotion"


    # Return strongest emotion
    for emotion, score in scores.items():

        if score == max_score:
            return emotion


# ==========================================
# APPLY EMOTION CLASSIFICATION
# ==========================================

df["emotion"] = df[
    "cleaned_review"
].apply(
    detect_emotion
)


# ==========================================
# SAVE RESULTS
# ==========================================

df.to_csv(
    "data/emotion_results.csv",
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print(
    "8-Emotion classification completed!"
)

print("\nEmotion Distribution:")

print(
    df["emotion"].value_counts()
)

print("\nSample Results:")

print(
    df[
        [
            "reviewText",
            "emotion"
        ]
    ].head(10)
)

print(
    "\nEmotion results saved successfully!"
)