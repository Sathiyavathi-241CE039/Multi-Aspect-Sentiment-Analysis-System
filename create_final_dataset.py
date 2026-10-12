import pandas as pd

# Load files
reviews = pd.read_csv("data/amazon_reviews.csv")
customers = pd.read_csv("data/customer_metadata.csv")
products = pd.read_csv("data/product_metadata.csv")

# Merge reviews + customer metadata
merged = reviews.merge(
    customers,
    on="reviewerID",
    how="left"
)

# Merge with product metadata using ASIN
final_dataset = merged.merge(
    products,
    on="asin",
    how="left"
)

# Save final dataset
final_dataset.to_csv(
    "data/final_dataset.csv",
    index=False
)

print("Final dataset created successfully!")
print("Shape:", final_dataset.shape)

print("\nColumns:")
print(final_dataset.columns.tolist())

print("\nFirst 5 rows:")
print(final_dataset.head())