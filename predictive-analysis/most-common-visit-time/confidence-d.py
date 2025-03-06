import pandas as pd
# Load the dataset
df = pd.read_csv("Downloads/FastFood.csv")

# most frequent age group
age_group = df["Age"].mode()[0]

# most common visit time age group
visit_time = df[df["Age"] == age_group]["What time do you usually go to McDonalds?"].mode()[0]

# Define Menu Item (Consequent Y)
menu_item = "Rice Meals"

# Count where customers in this visit time order anything
count_x = df[df["What time do you usually go to McDonalds?"] == visit_time].shape[0]

# Count where customers in this visit time specifically order Rice Meals
count_x_y = df[
    (df["What time do you usually go to McDonalds?"] == visit_time) &
    (df["Which of the menu items do you usually order?"].str.contains(menu_item, na=False))
].shape[0]

# Compute Confidence
confidence = (count_x_y / count_x) * 100 if count_x > 0 else 0

# Create DataFrame for tabular display
result = pd.DataFrame({
    "Formula": [
        f"Count({visit_time} ∪ {menu_item})",
        f"Count({visit_time})"
    ],
    "Value": [count_x_y, count_x]
})

# Display results
print(result)
print(f"\nConfidence({visit_time} → {menu_item}): {confidence:.2f}%")
