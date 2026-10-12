# ============================================================
# MULTILINGUAL SENTIMENT SUPPORT
# English + Tamil
# ============================================================

import re


# ------------------------------------------------------------
# Tamil to English word / phrase mapping
# ------------------------------------------------------------

TAMIL_TRANSLATIONS = {

    # Positive words
    "மிகவும் நல்லது": "very good",
    "நன்றாக உள்ளது": "is good",
    "சிறந்தது": "excellent",
    "அருமை": "excellent",
    "நல்லது": "good",
    "நன்றாக": "well",
    "சிறப்பு": "excellent",
    "பிடிக்கும்": "like",

    # Negative words
    "மோசமாக உள்ளது": "is bad",
    "மோசமான": "bad",
    "மோசம்": "bad",
    "பிடிக்கவில்லை": "do not like",
    "மோசமாக": "bad",

    # Product-related words
    "பேட்டரி ஆயுள்": "battery life",
    "பேட்டரி": "battery",
    "கேமரா": "camera",
    "திரை": "display",
    "தரம்": "quality",
    "விலை அதிகம்": "price expensive",
    "விலை குறைவு": "price cheap",
    "விலை": "price",
    "வேகம்": "speed",
    "வேகமாக": "fast",
    "மெதுவாக": "slow",

    # Emotion words
    "சந்தோஷம்": "happy",
    "வருத்தம்": "sad",
    "கோபம்": "anger",
    "பயம்": "fear",

    # Common connectors
    "ஆனால்": "but",
    "மற்றும்": "and",
    "அல்லது": "or",
    "இல்லை": "not",
    "மிகவும்": "very",
    "உள்ளது": "is",
    "இது": "this",
    "அது": "that",
    "ஒரு": "a"
}


# ------------------------------------------------------------
# Translate Tamil words / phrases
# ------------------------------------------------------------

def translate_tamil_to_english(text):

    if not text or not text.strip():
        return ""

    translated_text = text

    # Replace longer phrases first
    # This prevents smaller words from being replaced first.
    sorted_words = sorted(
        TAMIL_TRANSLATIONS.keys(),
        key=len,
        reverse=True
    )

    for tamil_word in sorted_words:

        translated_text = translated_text.replace(
            tamil_word,
            " " + TAMIL_TRANSLATIONS[tamil_word] + " "
        )

    # Remove extra spaces
    translated_text = re.sub(
        r"\s+",
        " ",
        translated_text
    ).strip()

    return translated_text


# ------------------------------------------------------------
# Multilingual processing function
# ------------------------------------------------------------

def multilingual_sentiment_text(text):

    english_text = translate_tamil_to_english(text)

    return {
        "original_text": text,
        "processed_text": english_text
    }


# ------------------------------------------------------------
# Test the multilingual system
# ------------------------------------------------------------

if __name__ == "__main__":

    test_reviews = [

        # English
        "This product is excellent",

        # Tamil + English
        "இந்த product மிகவும் நல்லது",

        "இந்த product மோசமாக உள்ளது",

        "பேட்டரி ஆயுள் நன்றாக உள்ளது",

        "கேமரா நல்லது ஆனால் விலை அதிகம்",

        "Battery நல்லது but price அதிகம்",

        "கேமரா சிறந்தது மற்றும் battery நன்றாக உள்ளது",

        "விலை அதிகம் ஆனால் quality நல்லது"
    ]

    print("=" * 60)
    print("MULTILINGUAL SENTIMENT SUPPORT")
    print("=" * 60)

    for review in test_reviews:

        result = multilingual_sentiment_text(review)

        print("\nOriginal:")
        print(result["original_text"])

        print("Processed:")
        print(result["processed_text"])

    print("\n" + "=" * 60)
    print("Multilingual processing completed successfully!")
    print("=" * 60)