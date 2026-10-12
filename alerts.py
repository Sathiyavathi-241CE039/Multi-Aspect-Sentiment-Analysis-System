import pandas as pd


# Load sentiment results
df = pd.read_csv(
    "data/aspect_sentiment_results.csv"
)


# Convert review date
df["reviewTime"] = pd.to_datetime(
    df["reviewTime"],
    errors="coerce"
)


# Create month
df["month"] = df["reviewTime"].dt.to_period("M").astype(str)


# Calculate monthly sentiment counts
monthly = pd.crosstab(
    df["month"],
    df["sentiment"]
)


# Make sure all sentiment columns exist
for sentiment in [
    "Positive",
    "Neutral",
    "Negative"
]:

    if sentiment not in monthly.columns:
        monthly[sentiment] = 0


# Arrange columns
monthly = monthly[
    [
        "Positive",
        "Neutral",
        "Negative"
    ]
]


# Calculate total
monthly["Total"] = (
    monthly["Positive"]
    + monthly["Neutral"]
    + monthly["Negative"]
)


# Calculate negative percentage
monthly["Negative_Percentage"] = (
    monthly["Negative"]
    / monthly["Total"]
    * 100
)


# Calculate average negative percentage
average_negative = monthly[
    "Negative_Percentage"
].mean()


# Define alert threshold
threshold = average_negative * 1.5


# Generate alerts
monthly["Alert"] = monthly[
    "Negative_Percentage"
].apply(
    lambda x:
    "⚠️ NEGATIVE SENTIMENT SPIKE"
    if x > threshold
    else "Normal"
)


# Add month as a normal column
monthly = monthly.reset_index()

monthly = monthly.rename(
    columns={
        "month": "Month"
    }
)


# Save alert report
monthly.to_csv(
    "data/sentiment_alerts.csv",
    index=False
)


print(
    "Negative sentiment alert analysis completed!"
)

print("\nAverage Negative Percentage:")
print(
    round(average_negative, 2),
    "%"
)

print("\nAlert Threshold:")
print(
    round(threshold, 2),
    "%"
)


print("\nAlert Months:")

alerts = monthly[
    monthly["Alert"] != "Normal"
]


if len(alerts) == 0:

    print(
        "No negative sentiment spikes detected."
    )

else:

    print(
        alerts[
            [
                "Month",
                "Negative",
                "Total",
                "Negative_Percentage",
                "Alert"
            ]
        ].to_string(index=False)
    )


print(
    "\nAlert report saved successfully!"
)