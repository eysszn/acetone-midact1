import pandas as pd
from collections import Counter

df = pd.read_csv("/Users/acengaosi/Downloads/Acetone-Midact1.csv")

# find the rice meal with the most frequency
rice_meals = df["Which rice meals do you usually order from McDonalds?"].dropna().str.split(", ").explode()
most_common_rice_meal, _ = Counter(rice_meals).most_common(1)[0]

# Filter rows where the most ordered rice meal is present
filtered_df = df[df["Which rice meals do you usually order from McDonalds?"].str.contains(most_common_rice_meal, na=False)]

# count frequency for each drink
drinks = filtered_df["Which drink/s do you usually order from McDonalds?"].dropna().str.split(", ").explode()
drink_counts = Counter(drinks)

total_orders = len(df)
total_rice_meal_orders = len(filtered_df)

# compute support for each drink
support_data = [(most_common_rice_meal, drink, count / total_orders) for drink, count in drink_counts.items()]
support_df = pd.DataFrame(support_data, columns=["Rice Meal", "Drink", "Support"])

# compute conviction
all_drink_counts = df["Which drink/s do you usually order from McDonalds?"].dropna().str.split(", ").explode()
total_drink_counts = Counter(all_drink_counts)

conviction_data = []
for drink, support in zip(support_df["Drink"], support_df["Support"]):
    drink_probability = total_drink_counts[drink] / total_orders if drink in total_drink_counts else 0
    confidence = support / (total_rice_meal_orders / total_orders)
    conviction = (1 - drink_probability) / (1 - confidence) if (1 - confidence) != 0 else float('inf')
    conviction_data.append((most_common_rice_meal, drink, round(conviction, 3)))

conviction_df = pd.DataFrame(conviction_data, columns=["Rice Meal", "Drink", "Conviction"])

# display results
print("Most ordered rice meal:", most_common_rice_meal)

print("\nConviction Table:")
print(conviction_df)
