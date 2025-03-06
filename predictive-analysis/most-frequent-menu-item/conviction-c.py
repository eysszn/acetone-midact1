import pandas as pd
from collections import Counter

# Identify the most ordered menu item
menu_items = df["Which of the menu items do you usually order?"].dropna().str.split(", ").explode()
most_common_menu_item, _ = Counter(menu_items).most_common(1)[0]

# Identify the two most frequent promotion types
promotions = df["What types of promotions are most likely to catch your attention? (Select all that apply)"].dropna().str.split(", ").explode()
most_common_promotions = [item for item, _ in Counter(promotions).most_common(2)]

# Filter rows where the most ordered menu item is present
filtered_df = df[df["Which of the menu items do you usually order?"].str.contains(most_common_menu_item, na=False)]

total_orders = len(df)
total_menu_item_orders = len(filtered_df)

# Compute support for each promotion
promotion_counts = Counter(filtered_df["What types of promotions are most likely to catch your attention? (Select all that apply)"].dropna().str.split(", ").explode())
support_data = [(most_common_menu_item, promo, promotion_counts[promo] / total_orders) for promo in most_common_promotions]

support_df = pd.DataFrame(support_data, columns=["Menu Item", "Promotion", "Support"])

# Compute conviction
all_promotion_counts = Counter(df["What types of promotions are most likely to catch your attention? (Select all that apply)"].dropna().str.split(", ").explode())

conviction_data = []
for promo, support in zip(support_df["Promotion"], support_df["Support"]):
    promo_probability = all_promotion_counts[promo] / total_orders if promo in all_promotion_counts else 0
    confidence = support / (total_menu_item_orders / total_orders)
    conviction = (1 - promo_probability) / (1 - confidence) if (1 - confidence) != 0 else float('inf')
    conviction_data.append((most_common_menu_item, promo, round(conviction, 3)))

conviction_df = pd.DataFrame(conviction_data, columns=["Menu Item", "Promotion", "Conviction"])

# Display results
print("Most ordered menu item:", most_common_menu_item)
print("\nConviction Table:")
print(conviction_df)
