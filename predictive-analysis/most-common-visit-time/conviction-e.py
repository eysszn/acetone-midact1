import pandas as pd
from collections import Counter

# Step 1: Identify the most frequent age group
most_common_age_group, _ = Counter(df["Age"].dropna()).most_common(1)[0]

# Step 2: Filter dataset for the most common age group and find the most common visit time
filtered_age_df = df[df["Age"] == most_common_age_group]
most_common_visit_time, _ = Counter(filtered_age_df["What time do you usually go to McDonalds?"].dropna().explode()).most_common(1)[0]

# Step 3: Filter dataset for rows where the most common visit time is part of the string
filtered_time_df = df[df["What time do you usually go to McDonalds?"].astype(str).apply(lambda x: most_common_visit_time in x)]

# Step 4: Count occurrences of each rice meal in this subset
rice_meals = filtered_time_df["Which rice meals do you usually order from McDonalds?"].dropna().str.split(", ").explode()
rice_meal_counts = Counter(rice_meals)

# Step 5: Compute support for each rice meal
total_orders = len(df)
total_time_orders = len(filtered_time_df)
support_data = [(most_common_visit_time, rice_meal, count / total_orders) for rice_meal, count in rice_meal_counts.items()]
support_df = pd.DataFrame(support_data, columns=["Visit Time", "Rice Meal", "Support"])

# Step 6: Compute conviction
all_rice_meal_counts = df["Which rice meals do you usually order from McDonalds?"].dropna().str.split(", ").explode()
total_rice_meal_counts = Counter(all_rice_meal_counts)

conviction_data = []
for rice_meal, support in zip(support_df["Rice Meal"], support_df["Support"]):
    rice_meal_probability = total_rice_meal_counts[rice_meal] / total_orders if rice_meal in total_rice_meal_counts else 0
    confidence = support / (total_time_orders / total_orders) if total_time_orders > 0 else 0
    conviction = (1 - rice_meal_probability) / (1 - confidence) if (1 - confidence) != 0 else float('inf')
    conviction_data.append((most_common_visit_time, rice_meal, round(conviction, 3)))

conviction_df = pd.DataFrame(conviction_data, columns=["Visit Time", "Rice Meal", "Conviction"])

# Display results
print("Most Frequent Age Group:", most_common_age_group)
print("Most Common Visit Time:", most_common_visit_time)
print("\nConviction Table:")
print(conviction_df)
