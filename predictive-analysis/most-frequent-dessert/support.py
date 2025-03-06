import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_excel("C:/Users/markl/Downloads/SixSigmas-FastFood.xlsx", sheet_name="SixSigmas-FastFood")

# Ensure relevant columns are treated as lists, replacing NaN with ["None"]
df["Dessert"] = df["Which dessert/s do you usually order from McDonalds?"].apply(lambda x: x.split(", ") if pd.notna(x) else ["None"])
df["Other_Meals"] = df["What other meal/s you usually order from McDonalds?"].apply(lambda x: x.split(", ") if pd.notna(x) else ["None"])

# Explode lists for proper alignment
df_exploded = df.explode("Dessert").explode("Other_Meals")

# Strip spaces
df_exploded["Dessert"] = df_exploded["Dessert"].str.strip()
df_exploded["Other_Meals"] = df_exploded["Other_Meals"].str.strip()

# Filter only rows where McFlurry is ordered AND Other_Meals is valid
filtered_df = df_exploded[
    (df_exploded["Dessert"] == "McFlurry") & 
    (df_exploded["Other_Meals"].notna()) & 
    (df_exploded["Other_Meals"].str.strip() != "None") & 
    (df_exploded["Other_Meals"].str.strip() != "")
]

# Count occurrences of Other Meals paired with McFlurry
meal_counts = filtered_df["Other_Meals"].value_counts().reset_index()
meal_counts.columns = ["Meal", "Count"]

# Compute total count of McFlurry + meal combinations
total_meal_count = meal_counts["Count"].sum()

# Compute ratios for each meal pairing in percentage format
meal_counts["Ratio (%)"] = (meal_counts["Count"] / total_meal_count) * 100

# Identify highest ordered meal
highest_meal = meal_counts.iloc[0]["Meal"]
highest_meal_count = meal_counts.iloc[0]["Count"]
highest_meal_ratio = (highest_meal_count / total_meal_count) * 100

# Display the computed results
print(f"\n **McFlurry Meal Pairing Analysis** ")
print(f" Total meals paired with McFlurry: {total_meal_count}")
print(f" Most ordered meal paired with McFlurry: {highest_meal} ({highest_meal_count} orders)")
print(f" Ratio of highest ordered meal to total: {highest_meal_ratio:.2f}%\n")

# Print the ratio for all combinations
print(" **All McFlurry + Meal Pairing Ratios** ")
print(meal_counts.to_string(index=False))  # Display full table without truncation

# If no valid data is found, exit gracefully
if meal_counts.empty:
    print("\n No data found for McFlurry pairings.\n")
else:
    # Plot bar chart
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=meal_counts, x="Count", y="Meal", palette="muted")

    # Extend x-axis for better readability
    max_x_value = meal_counts["Count"].max()
    plt.xlim(0, max_x_value + (max_x_value * 0.3))  # Add 30% more space

    # Add annotations inside bars with counts and ratios in percentage
    for index, row in meal_counts.iterrows():
        ax.text(
            row["Count"] + 1,  # Slightly outside the bar
            index, 
            f"{row['Count']} ({row['Ratio (%)']:.2f}%)",
            va="center", 
            ha="left",
            color="black", 
            fontsize=11,
            fontweight="bold"
        )

    # Labels and title
    plt.xlabel("Order Count")
    plt.ylabel("Meals Paired with McFlurry")
    plt.title("Meal Combinations Ordered with McFlurry")
    plt.grid(axis="x", linestyle="--", alpha=0.5)

    # Show results
    plt.show()    
