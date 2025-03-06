import pandas as pd
from collections import Counter

# Load the dataset
file_path = "C:/Users/Juduruu/Downloads/SixSigmas_FastFood_Clean.csv"  # Replace with the actual path to your file
df = pd.read_csv(file_path)

# Clean the types of promotions
def clean_promotion_types(column):
    promotion_types_str = column["What types of promotions are most likely to catch your attention? (Select all that apply)"]
    if isinstance(promotion_types_str, str):
        # Remove the unneccessary details
        promotion_types_str = promotion_types_str.replace('(e.g. Php 75 Meal Deals)', '')
        promotion_types_str = promotion_types_str.replace('(e.g., Meal Combos with Drink and Side)', '')
        promotion_types_str = promotion_types_str.replace('(e.g., 10% off, Buy One Get One Free)', '')
        promotion_types = [promo.strip() for promo in promotion_types_str.split(',')]

        cleaned_promotions = [promo for promo in promotion_types if promo in ["Combo Deals", "Percentage Discounts", "Limited Time Offers", "Fixed Price Promotions"]]
        return ', '.join(cleaned_promotions)
    else:
        return None

df["What types of promotions are most likely to catch your attention? (Select all that apply)"] = df.apply(clean_promotion_types, axis=1)

# Extract and count items from a column
def extract_and_count(df, column_name):
    item_list = []
    for items in df[column_name].dropna():
        item_list.extend([item.strip() for item in items.split(',')])
    return Counter(item_list)

# Find most frequent menu items
menu_item_counts = extract_and_count(df, "Which of the menu items do you usually order?")
most_frequent_menu_item = menu_item_counts.most_common(1)[0][0]
print(f"Most Frequent Menu Item: {most_frequent_menu_item}")

# Find 2 most frequent menu items
promotion_counts = extract_and_count(df, "What types of promotions are most likely to catch your attention? (Select all that apply)")
most_frequent_promotions = [item[0] for item in promotion_counts.most_common(2)]
print(f"Two Most Frequent Promotion Types: {most_frequent_promotions}")

# Calculate Lift for each promotion type
num_transactions = len(df)

for promotion_type in most_frequent_promotions:
    # Calculate support for X: Most Frequent Menu Item
    support_X_count = sum(1 for index, row in df.iterrows() if most_frequent_menu_item in row["Which of the menu items do you usually order?"].split(','))
    support_X = support_X_count / num_transactions

    # Calculate support for Y: Each individual promotion type
    support_Y_count = sum(1 for index, row in df.iterrows() if promotion_type in row["What types of promotions are most likely to catch your attention? (Select all that apply)"].split(','))
    support_Y = support_Y_count / num_transactions

    # Calculate support for X ∪ Y: Most Frequent Menu Item and the current promotion type
    support_X_and_Y_count = sum(1 for index, row in df.iterrows()
                                if most_frequent_menu_item in row["Which of the menu items do you usually order?"].split(',') and
                                promotion_type in row["What types of promotions are most likely to catch your attention? (Select all that apply)"].split(','))
    support_X_and_Y = support_X_and_Y_count / num_transactions

    # Calculate confidence and lift
    confidence_X_to_Y = support_X_and_Y / support_X if support_X > 0 else 0
    lift_X_to_Y = confidence_X_to_Y / support_Y if support_Y > 0 else 0

    # Print the results for the current promotion type
    print(f"Lift for {most_frequent_menu_item} --> {promotion_type}: {lift_X_to_Y:.4f}")
    print("-" * 30)
