import pandas as pd
from collections import Counter

df = pd.read_csv("/Users/acengaosi/Downloads/Acetone-Midact1.csv")

# find the dessert with the most frequency
desserts = df["Which dessert/s do you usually order from McDonalds?"].dropna().str.split(", ").explode()
most_common_dessert, _ = Counter(desserts).most_common(1)[0]

# Filter rows where the most ordered dessert is present
filtered_df = df[df["Which dessert/s do you usually order from McDonalds?"].str.contains(most_common_dessert, na=False)]

# count frequency for each other meal
other_meals = filtered_df["What other meal/s you usually order from McDonalds?"].dropna().str.split(", ").explode()
other_meal_counts = Counter(other_meals)

total_orders = len(df)
total_dessert_orders = len(filtered_df)

# Compute support for each other meal
support_data = [(most_common_dessert, other_meal, count / total_orders) for other_meal, count in other_meal_counts.items()]
support_df = pd.DataFrame(support_data, columns=["Dessert", "Other Meal", "Support"])

# compute conviction
all_other_meal_counts = df["What other meal/s you usually order from McDonalds?"].dropna().str.split(", ").explode()
total_other_meal_counts = Counter(all_other_meal_counts)

conviction_data = []
for other_meal, support in zip(support_df["Other Meal"], support_df["Support"]):
    other_meal_probability = total_other_meal_counts[other_meal] / total_orders if other_meal in total_other_meal_counts else 0
    confidence = support / (total_dessert_orders / total_orders)
    conviction = (1 - other_meal_probability) / (1 - confidence) if (1 - confidence) != 0 else float('inf')
    conviction_data.append((most_common_dessert, other_meal, round(conviction, 3)))

conviction_df = pd.DataFrame(conviction_data, columns=["Dessert", "Other Meal", "Conviction"])

# display results
print("Most ordered dessert:", most_common_dessert)

print("\nConviction Table:")
print(conviction_df)
