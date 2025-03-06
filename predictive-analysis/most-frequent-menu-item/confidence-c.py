import pandas as pd

# Load the dataset
df = pd.read_csv("Downloads/FastFood.csv")

# Define X (Antecedents) and Y (Consequents)
item = "Rice Meals"
other_meal = "Fries"
type_1 = "Combo Deals"
type_2 = "Percentage Discount"

# Count transactions where Rice Meals and Fries are ordered (X)
count_x = df[
    (df["Which of the menu items do you usually order?"].str.contains(item, na=False)) &
    (df["What other meal/s you usually order from McDonalds?"].str.contains(other_meal, na=False))
].shape[0]

# Count transactions where Rice Meals, Fries, and both promotions exist (X → Y)
count_x_y = df[
    (df["Which of the menu items do you usually order?"].str.contains(item, na=False)) &
    (df["What other meal/s you usually order from McDonalds?"].str.contains(other_meal, na=False)) &
    (df["What types of promotions are most likely to catch your attention? (Select all that apply)"].str.contains(type_1, na=False)) &
    (df["What types of promotions are most likely to catch your attention? (Select all that apply)"].str.contains(type_2, na=False))
].shape[0]

# Compute Confidence
confidence = (count_x_y / count_x) * 100 if count_x > 0 else 0

# Create DataFrame for tabular display
result = pd.DataFrame({
    "Formula": [
        f"Count({item}, {other_meal} ∪ {type_1}, {type_2})",
        f"Count({item} ∪ {other_meal})"
    ],
    "Value": [count_x_y, count_x]
})

# Display results
print(result)

# Print confidence separately
print(f"\nConfidence({item}, {other_meal} → {type_1}, {type_2}): {confidence:.2f}%")
