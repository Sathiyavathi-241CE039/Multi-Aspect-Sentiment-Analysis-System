import pandas as pd

# Load aspect sentiment results
df = pd.read_csv(
    "data/aspect_sentiment_results.csv"
)

# Count sentiment for each aspect
summary = pd.crosstab(
    df["aspect"],
    df["sentiment"]
)

# Make sure columns exist
for sentiment in ["Positive", "Neutral", "Negative"]:

    if sentiment not in summary.columns:
        summary[sentiment] = 0

# Arrange columns
summary = summary[
    ["Positive", "Neutral", "Negative"]
]

# Calculate total
summary["Total"] = summary.sum(axis=1)

# Calculate negative percentage
summary["Negative_Percentage"] = (
    summary["Negative"] /
    summary["Total"] * 100
)

# Sort by negative percentage
summary = summary.sort_values(
    "Negative_Percentage",
    ascending=False
)


# Recommendation function
def get_recommendation(aspect):

    recommendations = {

        "Battery":
        "Improve battery life and charging performance.",

        "Price":
        "Review pricing and provide better value for customers.",

        "Quality":
        "Improve product quality and durability.",

        "Performance":
        "Improve product speed and overall performance.",

        "Design":
        "Improve product design and appearance.",

        "Size":
        "Provide better size options based on customer needs.",

        "Display":
        "Improve display quality, brightness and resolution.",

        "Camera":
        "Improve camera quality and image performance.",

        "Delivery":
        "Improve delivery speed, packaging and tracking.",

        "Customer_Service":
        "Improve customer support and response time."
    }

    return recommendations.get(
        aspect,
        "Analyze customer feedback and improve this aspect."
    )


# Add recommendations
summary["Recommendation"] = summary.index.map(
    get_recommendation
)


# Save results
summary.to_csv(
    "data/business_recommendations.csv"
)

print("Business recommendations generated!")

print("\nBusiness Analysis:")
print(summary)