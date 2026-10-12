import pandas as pd


# Load sentiment results
df = pd.read_csv(
    "data/aspect_sentiment_results.csv"
)


# Calculate sentiment counts for each customer
customer_sentiment = pd.crosstab(
    df["reviewerID"],
    df["sentiment"]
)


# Make sure all sentiment columns exist
for sentiment in [
    "Positive",
    "Neutral",
    "Negative"
]:
    if sentiment not in customer_sentiment.columns:
        customer_sentiment[sentiment] = 0


# Arrange columns
customer_sentiment = customer_sentiment[
    [
        "Positive",
        "Neutral",
        "Negative"
    ]
]


# Total sentiment records
customer_sentiment["Total"] = (
    customer_sentiment["Positive"]
    + customer_sentiment["Neutral"]
    + customer_sentiment["Negative"]
)


# Calculate sentiment percentages
customer_sentiment["Positive_Percentage"] = (
    customer_sentiment["Positive"]
    / customer_sentiment["Total"]
    * 100
)

customer_sentiment["Neutral_Percentage"] = (
    customer_sentiment["Neutral"]
    / customer_sentiment["Total"]
    * 100
)

customer_sentiment["Negative_Percentage"] = (
    customer_sentiment["Negative"]
    / customer_sentiment["Total"]
    * 100
)


# Customer segmentation function
def classify_customer(row):

    if row["Negative_Percentage"] >= 50:
        return "Negative-Oriented"

    elif row["Positive_Percentage"] >= 70:
        return "Positive-Oriented"

    elif row["Neutral_Percentage"] >= 50:
        return "Neutral-Oriented"

    else:
        return "Mixed-Sentiment"


# Apply segmentation
customer_sentiment["Segment"] = customer_sentiment.apply(
    classify_customer,
    axis=1
)


# Reset index
customer_sentiment = customer_sentiment.reset_index()


# Save segmentation results
customer_sentiment.to_csv(
    "data/customer_segments.csv",
    index=False
)


print("Customer segmentation completed!")

print("\nCustomer Segment Distribution:")

print(
    customer_sentiment[
        "Segment"
    ].value_counts()
)


print("\nSample Customer Segments:")

print(
    customer_sentiment.head(10)
)


print("\nCustomer segmentation file saved successfully!")
