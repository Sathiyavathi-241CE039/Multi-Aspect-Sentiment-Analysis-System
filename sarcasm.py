# ============================================================
# SARCASM & IRONY DETECTION
# Rule-Based Heuristic System
# ============================================================

import re


# ------------------------------------------------------------
# Strong sarcasm phrases
# ------------------------------------------------------------

strong_sarcasm_phrases = [
    "yeah right",
    "thanks for nothing",
    "what a surprise",
    "just great",
    "oh great",
    "love how",
    "as if",
    "sure thing"
]


# ------------------------------------------------------------
# Sarcasm indicator words
# These words alone are NOT enough to classify sarcasm.
# ------------------------------------------------------------

sarcasm_words = [
    "wow",
    "obviously",
    "sure"
]


# ------------------------------------------------------------
# Positive words
# ------------------------------------------------------------

positive_words = [
    "good",
    "great",
    "excellent",
    "amazing",
    "awesome",
    "perfect",
    "wonderful",
    "fantastic",
    "love"
]


# ------------------------------------------------------------
# Strong positive words for contrast detection
# ------------------------------------------------------------

positive_contrast_words = [
    "amazing",
    "excellent",
    "great",
    "perfect",
    "wonderful",
    "fantastic",
    "awesome"
]


# ------------------------------------------------------------
# Negative words
# ------------------------------------------------------------

negative_words = [
    "bad",
    "worst",
    "terrible",
    "awful",
    "horrible",
    "useless",
    "slow",
    "poor",
    "broken",
    "failed",
    "failure",
    "hate",
    "disappointed",
    "disappointing",
    "expensive",
    "problem",
    "issue",
    "waste",
    "died",
    "dies",
    "stopped",
    "not working"
]


# ------------------------------------------------------------
# Negative event words
# Used to detect situations such as:
# "amazing battery... it dies in two hours"
# ------------------------------------------------------------

negative_event_words = [
    "dies",
    "died",
    "stopped",
    "failed",
    "broken",
    "not working",
    "doesn't work",
    "does not work",
    "crashed",
    "crashes",
    "waste"
]


# ------------------------------------------------------------
# Clean text
# ------------------------------------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ------------------------------------------------------------
# Detect sarcasm
# ------------------------------------------------------------

def detect_sarcasm(text):

    text = clean_text(text)

    score = 0

    indicators = []


    # --------------------------------------------------------
    # Rule 1: Strong sarcasm phrases
    # --------------------------------------------------------

    for phrase in strong_sarcasm_phrases:

        if phrase in text:

            score += 3

            indicators.append(
                f"Strong sarcasm phrase: {phrase}"
            )


    # --------------------------------------------------------
    # Rule 2: Sarcasm indicator words
    # These require additional evidence.
    # --------------------------------------------------------

    for word in sarcasm_words:

        if word in text:

            score += 1

            indicators.append(
                f"Sarcasm indicator: {word}"
            )


    # --------------------------------------------------------
    # Rule 3: Positive + negative contradiction
    # --------------------------------------------------------

    has_positive = any(
        word in text
        for word in positive_words
    )

    has_negative = any(
        word in text
        for word in negative_words
    )


    if has_positive and has_negative:

        score += 3

        indicators.append(
            "Positive and negative sentiment contradiction"
        )


    # --------------------------------------------------------
    # Rule 4: Positive description followed by
    # negative event
    #
    # Example:
    # "amazing battery life... it dies in two hours"
    # --------------------------------------------------------

    has_positive_contrast = any(
        word in text
        for word in positive_contrast_words
    )

    has_negative_event = any(
        word in text
        for word in negative_event_words
    )


    if has_positive_contrast and has_negative_event:

        score += 3

        indicators.append(
            "Positive description followed by negative event"
        )


    # --------------------------------------------------------
    # Rule 5: Positive statement followed by "but"
    # and negative statement
    # --------------------------------------------------------

    if "but" in text:

        parts = text.split("but")


        if len(parts) >= 2:

            first_part = parts[0]

            second_part = parts[1]


            first_positive = any(
                word in first_part
                for word in positive_words
            )


            second_negative = any(
                word in second_part
                for word in negative_words
            )


            if first_positive and second_negative:

                score += 3

                indicators.append(
                    "Positive statement followed by negative statement"
                )


    # --------------------------------------------------------
    # Rule 6: Exaggerated punctuation
    #
    # Only considered when negative context exists.
    # This prevents:
    #
    # "The battery is amazing!!!"
    #
    # from automatically becoming sarcastic.
    # --------------------------------------------------------

    exaggerated_punctuation = (
        "!!!" in text or
        "???" in text
    )


    if exaggerated_punctuation and has_negative:

        score += 1

        indicators.append(
            "Exaggerated punctuation with negative context"
        )


    # --------------------------------------------------------
    # Rule 7: Sarcastic sentence patterns
    # --------------------------------------------------------

    sarcastic_patterns = [

        r"yeah right",

        r"thanks for nothing",

        r"what a surprise",

        r"just great",

        r"oh great",

        r"love how",

        r"amazing.*but",

        r"perfect.*but",

        r"great.*but"
    ]


    for pattern in sarcastic_patterns:

        if re.search(pattern, text):

            score += 2

            indicators.append(
                f"Sarcastic pattern: {pattern}"
            )


    # --------------------------------------------------------
    # Final classification
    # --------------------------------------------------------

    if score >= 3:

        sarcasm = True

    else:

        sarcasm = False


    # --------------------------------------------------------
    # Heuristic confidence
    #
    # This is NOT a statistical probability.
    # --------------------------------------------------------

    if score >= 8:

        confidence = 0.95

    elif score >= 6:

        confidence = 0.90

    elif score >= 4:

        confidence = 0.85

    elif score >= 3:

        confidence = 0.75

    else:

        confidence = 0.20


    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {

        "sarcasm": sarcasm,

        "confidence": round(
            confidence,
            2
        ),

        "score": score,

        "indicators": indicators
    }


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    test_reviews = [

        "Wow, amazing battery life... it dies in two hours.",

        "This product is excellent and works perfectly.",

        "Yeah right, this is the best battery ever.",

        "Great camera but it produces terrible photos.",

        "The product is good and reliable.",

        "Thanks for nothing, the product stopped working.",

        "The battery is amazing!!!",

        "The delivery was fast and the product is good.",

        "Perfect product but the battery stopped working.",

        "Amazing camera but the photos are terrible."
    ]


    print("=" * 60)

    print("SARCASM & IRONY DETECTION")

    print("=" * 60)


    for review in test_reviews:

        result = detect_sarcasm(review)


        print("\nReview:")

        print(review)


        print("Sarcasm:")

        print(result["sarcasm"])


        print("Confidence:")

        print(result["confidence"])


        print("Score:")

        print(result["score"])


        print("Indicators:")

        print(result["indicators"])


    print("\n" + "=" * 60)

    print("Sarcasm detection testing completed!")

    print("=" * 60)