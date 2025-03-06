import pandas as pd
import re

# Load dataset
df = pd.read_csv("Downloads/FastFood.csv")

# Process Menu Item and Promotion Type columns
df["Menu"] = df["Which of the menu items do you usually order?"].apply(lambda x: x.split(", ") if pd.notna(x) else ["None"])
df["Promo"] = df["What types of promotions are most likely to catch your attention? (Select all that apply)"].apply(
    lambda x: re.sub(r"\(.*?\)", "", x).strip().split(", ") if pd.notna(x) else ["None"]
)

# Expand lists into rows
df = df.explode("Menu").explode("Promo")

# Strip spaces
df["Menu"] = df["Menu"].str.strip()
df["Promo"] = df["Promo"].str.strip()

# Get most ordered menu item
menu_counts = df["Menu"].value_counts().reset_index()
menu_counts.columns = ["Menu", "Count"]
top_menu = menu_counts.iloc[0]["Menu"]
top_count = menu_counts.iloc[0]["Count"]

# Filter by top menu and count promotions
filtered = df[df["Menu"] == top_menu]
promo_counts = filtered["Promo"].value_counts().reset_index()
promo_counts.columns = ["Promo", "Count"]
promo_counts.insert(0, "Menu", top_menu)

# Display results (without confidence in the table)
print(f"\nMost Ordered Menu Item: {top_menu} ({top_count} orders)\n")
print(promo_counts.to_string(index=False))

# Compute and display confidence values below the table for the top two promotions
print("\nConfidence Values for Top Two Promotions:")
for _, row in promo_counts.head(4).iterrows():
    confidence = (row["Count"] / top_count) * 100
    print(f"Confidence({top_menu} ➝ {row['Promo']}): {confidence:.2f}%")
