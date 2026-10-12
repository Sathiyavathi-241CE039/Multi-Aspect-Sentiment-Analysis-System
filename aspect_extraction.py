import pandas as pd

# Load preprocessed dataset
df = pd.read_csv("data/processed_reviews.csv")

# Define product aspects and related keywords
aspect_keywords = {
    "Battery": [
        "battery", "battery life", "charging", "charge"
    ],
    "Price": [
        "price", "cost", "expensive", "cheap", "value"
    ],
    "Quality": [
        "quality", "build", "material", "durable"
    ],
    "Performance": [
        "performance", "speed", "fast", "slow", "processor"
    ],
    "Design": [
        "design", "look", "appearance", "style"
    ],
    "Size": [
        "size", "small", "large", "compact"
    ],
    "Display": [
        "display", "screen", "resolution", "brightness"
    ],
    "Camera": [
        "camera", "photo", "picture", "video"
    ],
    "Delivery": [
        "delivery", "shipping", "arrived", "package"
    ],
    "Customer_Service": [
        "service", "support", "customer service", "seller"
    ]
}


# Function to extract aspects
def extract_aspects(text):

    if pd.isna(text):
        return []

    text = str(text).lower()

    found_aspects = []

    for aspect, keywords in aspect_keywords.items():

        for keyword in keywords:

            if keyword in text:
                found_aspects.append(aspect)
                break

    return found_aspects


# Apply aspect extraction
df["aspects"] = df["cleaned_review"].apply(extract_aspects)

# Convert list into readable text
df["aspects"] = df["aspects"].apply(
    lambda x: ", ".join(x) if x else "No Aspect"
)

# Save result
df.to_csv(
    "data/aspect_reviews.csv",
    index=False
)

print("Aspect extraction completed successfully!")

print("\nSample Results:")
print(df[["cleaned_review", "aspects"]].head(10))

print("\nTotal reviews:", len(df))

print("\nAspect counts:")
print(
    df["aspects"]
    .str.split(", ")
    .explode()
    .value_counts()
)