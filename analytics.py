import pandas as pd
import matplotlib.pyplot as plt

# Load sentiment results
df = pd.read_csv(
    "data/aspect_sentiment_results.csv"
)

# Convert review date
df["reviewTime"] = pd.to_datetime(
    df["reviewTime"],
    errors="coerce"
)

# Remove rows without date
df = df.dropna(
    subset=["reviewTime"]
)

# Create month
df["month"] = df["reviewTime"].dt.to_period("M").astype(str)

# Count sentiment by month
trend = pd.crosstab(
    df["month"],
    df["sentiment"]
)

# Add missing sentiment columns
for sentiment in ["Positive", "Neutral", "Negative"]:
    if sentiment not in trend.columns:
        trend[sentiment] = 0

# Arrange columns
trend = trend[
    ["Positive", "Neutral", "Negative"]
]

# Save trend data
trend.to_csv(
    "data/sentiment_trend.csv"
)

print("Sentiment trend analysis completed!")

print("\nMonthly Sentiment Trend:")
print(trend)

# Create reports folder if needed
import os

os.makedirs(
    "reports",
    exist_ok=True
)

# Create graph
trend.plot(
    kind="line",
    marker="o",
    figsize=(12, 6)
)

plt.title("Sentiment Trend Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=45)
plt.legend(title="Sentiment")
plt.tight_layout()

# Save graph
plt.savefig(
    "reports/sentiment_trend.png"
)

plt.close()

print("\nTrend graph saved successfully!")
print("Created: data/sentiment_trend.csv")
print("Created: reports/sentiment_trend.png")