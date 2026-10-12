import pandas as pd
from textblob import TextBlob

# Load aspect dataset
df = pd.read_csv(
    "data/aspect_reviews.csv"
)


# Sentiment function
def get_sentiment(text):

    if pd.isna(text) or str(text).strip() == "":
        return "Neutral"

    polarity = TextBlob(str(text)).sentiment.polarity

    if polarity > 0.1:
        return "Positive"

    elif polarity < -0.1:
        return "Negative"

    else:
        return "Neutral"


# Store results
results = []


# Process each review
for index, row in df.iterrows():

    review = str(row["cleaned_review"])
    aspects = str(row["aspects"])

    if aspects == "No Aspect":
        continue

    aspect_list = aspects.split(", ")

    for aspect in aspect_list:

        sentiment = get_sentiment(review)

        results.append({
            "reviewerID": row["reviewerID"],
            "asin": row["asin"],
            "review": review,
            "reviewTime": row["reviewTime"],
            "aspect": aspect,
            "sentiment": sentiment
        })


# Create dataframe
aspect_sentiment_df = pd.DataFrame(results)


# Save result
aspect_sentiment_df.to_csv(
    "data/aspect_sentiment_results.csv",
    index=False
)


print("Aspect-based sentiment analysis completed!")

print("\nTotal aspect records:")
print(len(aspect_sentiment_df))

print("\nSample Results:")
print(aspect_sentiment_df.head(10))

print("\nSentiment Distribution:")
print(
    aspect_sentiment_df["sentiment"].value_counts()
)