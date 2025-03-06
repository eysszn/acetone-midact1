import pandas as pd
import re

# Load dataset
df = pd.read_csv("Downloads/FastFood.csv")

# Process "Other Meals" column
df["Meals"] = df["What other meal/s you usually order from McDonalds?"].apply(lambda x: x.split(", ") if pd.notna(x) else ["None"])

# Clean and split "Promotion Type" column
df["Promo"] = df["What types of promotions are most likely to catch your attention? (Select all that apply)"].apply(
    lambda x: re.sub(r"\(.*?\)", "", x).strip().split(", ") if pd.notna(x) else ["None"]
)

# Expand lists into rows
df = df.explode("Meals").explode("Promo")

# Strip spaces
df["Meals"] = df["Meals"].str.strip()
df["Promo"] = df["Promo"].str.strip()

# Get most ordered meal
meal_counts = df["Meals"].value_counts().reset_index()
meal_counts.columns = ["Meal", "Count"]
top_meal = meal_counts.iloc[0]["Meal"]
top_count = meal_counts.iloc[0]["Count"]

# Filter by top meal and count promotions
filtered = df[df["Meals"] == top_meal]
promo_counts = filtered["Promo"].value_counts().reset_index()
promo_counts.columns = ["Promo", "Count"]
promo_counts.insert(0, "Meal", top_meal)

# Display results (without confidence in the table)
print(f"\nMost Ordered Meal: {top_meal} ({top_count} orders)\n")
print(promo_counts.to_string(index=False))

# Compute and display confidence values below the table
print("\nConfidence Values for Each Combination:")
for _, row in promo_counts.iterrows():
    confidence = (row["Count"] / top_count) * 100
    print(f"Confidence({top_meal} ➝ {row['Promo']}): {confidence:.2f}%")
