import pandas as pd
# Load the dataset
df = pd.read_csv("Downloads/FastFood.csv")

# Count Fried Chicken with Rice
count_fc = df[
    df["Which rice meals do you usually order from McDonalds?"].str.contains("Fried Chicken with Rice", na=False)
].shape[0]

# Count Fried Chicken Rice & Soft Drinks
count_fc_sd = df[
    (df["Which rice meals do you usually order from McDonalds?"].str.contains("Fried Chicken with Rice", na=False)) &
    (df["Which drink/s do you usually order from McDonalds?"].str.contains("Soft Drinks", na=False))
].shape[0]

# Compute confidence
confidence_fc_to_sd = (count_fc_sd / count_fc) * 100 if count_fc > 0 else 0

# Create a DataFrame to display results in a tabular format
result = pd.DataFrame({
    "Formula": ["Count(Fried Chicken with Rice ∪ Soft Drinks)", "Count(Fried Chicken with Rice)"],
    "Value": [count_fc_sd, count_fc]
})

# Display the table
print(result)
print(f"\nConfidence(Fried Chicken with Rice → Soft Drinks): {confidence_fc_to_sd:.2f}%")
