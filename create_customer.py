import pandas as pd

# Load reviews
reviews = pd.read_csv("data/amazon_reviews.csv")

# Create customer metadata
customer_metadata = reviews.groupby("reviewerID").agg(
    review_count=("reviewerID", "count"),
    avg_rating=("overall", "mean"),
    helpful_votes=("helpful_yes", "sum")
).reset_index()

# Create membership level
def membership_level(count):
    if count <= 5:
        return "Bronze"
    elif count <= 20:
        return "Silver"
    else:
        return "Gold"

customer_metadata["membership_level"] = (
    customer_metadata["review_count"]
    .apply(membership_level)
)

# Save file
customer_metadata.to_csv(
    "data/customer_metadata.csv",
    index=False
)

print("Customer metadata created successfully!")
print(customer_metadata.head())
print("Total customers:", len(customer_metadata))