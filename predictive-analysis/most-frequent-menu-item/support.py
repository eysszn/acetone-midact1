import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Load dataset
df = pd.read_excel("G:/My Drive/3rd Year 2ndSem/Data Analytics/Midterms/2Copy of SixSigmas-FastFood.xlsx", sheet_name='Clean')

# Ensure relevant columns are treated as lists, replacing NaN with ["None"]
df["Menu_Item"] = df["Which of the menu items do you usually order?"].apply(lambda x: x.split(", ") if pd.notna(x) else ["None"])

# **Fix Promotion Type column: Remove Parentheses BEFORE Splitting**
df["Promotion_Type"] = df["What types of promotions are most likely to catch your attention? (Select all that apply)"].apply(
    lambda x: re.sub(r"\(.*?\)", "", x).strip() if pd.notna(x) else "None"
)

# Now split the cleaned Promotion_Type column into lists
df["Promotion_Type"] = df["Promotion_Type"].apply(lambda x: x.split(", "))

# Explode lists for proper counting
df_exploded = df.explode("Menu_Item").explode("Promotion_Type")

# Strip spaces for consistency
df_exploded["Menu_Item"] = df_exploded["Menu_Item"].str.strip()
df_exploded["Promotion_Type"] = df_exploded["Promotion_Type"].str.strip()

# Count occurrences of each Menu Item
menu_counts = df_exploded["Menu_Item"].value_counts().reset_index()
menu_counts.columns = ["Menu Item", "Count"]

# Get the Most Frequently Ordered Menu Item
most_frequent_menu_item = menu_counts.iloc[0]["Menu Item"]
most_frequent_menu_count = menu_counts.iloc[0]["Count"]

# Filter dataset for the most ordered menu item
filtered_df = df_exploded[df_exploded["Menu_Item"] == most_frequent_menu_item]

# Count occurrences of Promotion Types related to the most ordered menu item
promo_counts = filtered_df["Promotion_Type"].value_counts().reset_index()
promo_counts.columns = ["Promotion Type", "Count"]

# Compute total promotion count for that menu item
total_promo_count = promo_counts["Count"].sum()

# Compute ratio (%) for each promotion type
promo_counts["Ratio (%)"] = (promo_counts["Count"] / total_promo_count) * 100

# Get the Top 2 Promotion Types
top_two_promos = promo_counts.head(2)

# Display Results
print(f"\n **Most Frequently Ordered Menu Item:** {most_frequent_menu_item} ({most_frequent_menu_count} orders)\n")

print(" **Top 2 Promotion Types for This Menu Item:**")
for _, row in top_two_promos.iterrows():
    print(f" {row['Promotion Type']}: {row['Count']} times used ({row['Ratio (%)']:.2f}%)")

# If no valid data is found, exit gracefully
if promo_counts.empty:
    print("\n No promotion data found for this menu item.\n")
else:
    # Modify labels to include both count and percentage
    promo_counts["Label"] = promo_counts.apply(lambda row: f"{row['Promotion Type']} ({row['Ratio (%)']:.2f}%)", axis=1)

    # Plot bar chart for promotion types related to the most ordered menu item
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=promo_counts, x="Count", y="Label", palette="muted")

    # Extend x-axis for better readability
    max_x_value = promo_counts["Count"].max()
    plt.xlim(0, max_x_value + (max_x_value * 0.3))  # Add 30% more space

    # Add annotations inside bars with counts and ratios in percentage
    for index, row in promo_counts.iterrows():
        ax.text(
            row["Count"] + 1,  # Slightly outside the bar
            index, 
            f"{row['Count']} ({row['Ratio (%)']:.2f}%)",  # Show both count and percentage
            va="center", 
            ha="left",
            color="black", 
            fontsize=11,
            fontweight="bold"
        )

    # Labels and title
    plt.xlabel("Count")
    plt.ylabel("Promotion Type")
    plt.title(f"Promotion Types Related to {most_frequent_menu_item}")
    plt.grid(axis="x", linestyle="--", alpha=0.5)

    # Show results
    plt.show()
