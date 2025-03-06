import pandas as pd
# Load the dataset
df = pd.read_csv("Downloads/FastFood.csv")

# Count where both Afternoon Snack and McFlurry exist
count_x = df[
    (df["What time do you usually go to McDonalds?"].str.contains("Afternoon Snack", na=False)) &
    (df["Which dessert/s do you usually order from McDonalds?"].str.contains("McFlurry", na=False))
].shape[0]

# Count where X₁, X₂, and Y are ordered
count_xy = df[
    (df["What time do you usually go to McDonalds?"].str.contains("Afternoon Snack", na=False)) &
    (df["Which dessert/s do you usually order from McDonalds?"].str.contains("McFlurry", na=False)) &
    (df["What other meal/s you usually order from McDonalds?"].str.contains("Fries", na=False))
].shape[0]

# Compute confidence
confidence = (count_xy / count_x) * 100 if count_x > 0 else 0

# Create DataFrame for tabular display
result = pd.DataFrame({
    "Formula": ["Count(Afternoon Snack, Mcflurry", "Count(Afternoon Snack, Mcflurry → Fries)"],
    "Value": [count_xy, count_x]
})

# Display results
print(result)
print(f"\nConfidence(Afternoon Snack, Mcflurry → Fries): {confidence:.2f}%")
