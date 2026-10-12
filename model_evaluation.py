import pandas as pd
from textblob import TextBlob
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
import matplotlib.pyplot as plt
import os


# =========================================================
# 1. SAMPLE MANUALLY LABELLED TEST DATA
# =========================================================

test_data = {
    "review": [
        "This product is excellent and amazing",
        "The battery life is very good",
        "I love this product",
        "The camera quality is great",
        "The product is terrible",
        "Battery performance is very poor",
        "I hate this product",
        "The delivery was very bad",
        "The product is okay",
        "The quality is average",
        "The product is good",
        "The camera is excellent",
        "The battery is awful",
        "Very disappointed with this product",
        "It is an average product"
    ],

    "actual_sentiment": [
        "Positive",
        "Positive",
        "Positive",
        "Positive",
        "Negative",
        "Negative",
        "Negative",
        "Negative",
        "Neutral",
        "Neutral",
        "Positive",
        "Positive",
        "Negative",
        "Negative",
        "Neutral"
    ]
}


df = pd.DataFrame(test_data)


# =========================================================
# 2. SENTIMENT PREDICTION
# =========================================================

def predict_sentiment(text):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.1:
        return "Positive"

    elif polarity < -0.1:
        return "Negative"

    else:
        return "Neutral"


df["predicted_sentiment"] = df["review"].apply(
    predict_sentiment
)


# =========================================================
# 3. CALCULATE METRICS
# =========================================================

y_true = df["actual_sentiment"]

y_pred = df["predicted_sentiment"]


accuracy = accuracy_score(
    y_true,
    y_pred
)


precision = precision_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)


recall = recall_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)


f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)


# =========================================================
# 4. DISPLAY RESULTS
# =========================================================

print("\n==============================================")
print("SENTIMENT MODEL EVALUATION")
print("==============================================")

print("\nTest Samples:", len(df))

print("\nAccuracy :", round(accuracy, 4))

print("Precision:", round(precision, 4))

print("Recall   :", round(recall, 4))

print("F1-Score :", round(f1, 4))


# =========================================================
# 5. CLASSIFICATION REPORT
# =========================================================

print("\n==============================================")
print("CLASSIFICATION REPORT")
print("==============================================")

print(
    classification_report(
        y_true,
        y_pred,
        zero_division=0
    )
)


# =========================================================
# 6. CONFUSION MATRIX
# =========================================================

labels = [
    "Negative",
    "Neutral",
    "Positive"
]


cm = confusion_matrix(
    y_true,
    y_pred,
    labels=labels
)


print("\n==============================================")
print("CONFUSION MATRIX")
print("==============================================")

print(cm)


# =========================================================
# 7. SAVE EVALUATION RESULTS
# =========================================================

os.makedirs("reports", exist_ok=True)

results = pd.DataFrame({

    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1-Score"
    ],

    "Score": [
        accuracy,
        precision,
        recall,
        f1
    ]
})


results.to_csv(
    "reports/model_evaluation.csv",
    index=False
)


# =========================================================
# 8. SAVE TEST PREDICTIONS
# =========================================================

df.to_csv(
    "reports/evaluation_predictions.csv",
    index=False
)


# =========================================================
# 9. CONFUSION MATRIX VISUALIZATION
# =========================================================

plt.figure(figsize=(7, 5))

plt.imshow(cm)

plt.title("Sentiment Confusion Matrix")

plt.xlabel("Predicted Sentiment")

plt.ylabel("Actual Sentiment")

plt.xticks(
    range(len(labels)),
    labels
)

plt.yticks(
    range(len(labels)),
    labels
)


# Add values inside matrix
for i in range(len(labels)):

    for j in range(len(labels)):

        plt.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )
plt.tight_layout()

plt.savefig(
    "reports/confusion_matrix.png"
)
plt.close()
print("\n==============================================")
print("FILES GENERATED")
print("==============================================")

print("✓ reports/model_evaluation.csv")

print("✓ reports/evaluation_predictions.csv")

print("✓ reports/confusion_matrix.png")

print("\nModel evaluation completed successfully!")