import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_excel("C:/Users/markl/Downloads/SixSigmas-FastFood.xlsx", sheet_name="SixSigmas-FastFood")

# Ensure both columns are treated as lists, replacing NaN with ["None"]
df["Rice_Meal"] = df["Which rice meals do you usually order from McDonalds?"].str.split(", ")
df["Drink"] = df["Which drink/s do you usually order from McDonalds?"].apply(lambda x: x.split(", ") if pd.notna(x) else ["None"])

# Explode both columns to align them
df_exploded = df.explode("Rice_Meal").explode("Drink")

# Strip leading/trailing spaces
df_exploded["Rice_Meal"] = df_exploded["Rice_Meal"].str.strip()
df_exploded["Drink"] = df_exploded["Drink"].str.strip()

# Group by Rice Meal and Drink, then count occurrences
meal_drink_counts = df_exploded.groupby(["Rice_Meal", "Drink"]).size().reset_index(name="Count")

# Identify the highest-ordered rice meal
top_rice_meal = meal_drink_counts.groupby("Rice_Meal")["Count"].sum().idxmax()

# Filter only the highest-ordered rice meal and its drink combinations
top_meal_combinations = meal_drink_counts[meal_drink_counts["Rice_Meal"] == top_rice_meal]

# Get total count of the highest-ordered rice meal
highest_meal_total = top_meal_combinations["Count"].sum()

# Compute ratio of each combination to total orders of that rice meal (in percentage)
top_meal_combinations["Ratio (%)"] = round((top_meal_combinations["Count"] / highest_meal_total) * 100, 1)

# Sort by count for better visualization
top_meal_combinations = top_meal_combinations.sort_values(by="Count", ascending=False)

# Plot the filtered bar chart
plt.figure(figsize=(10, 6))
ax = sns.barplot(data=top_meal_combinations, x="Count", y="Drink", palette="muted")

# Extend x-axis limits to create more space for labels
max_x_value = top_meal_combinations["Count"].max()
plt.xlim(0, max_x_value + (max_x_value * 0.3))  # Add 30% more space to the right

# Add annotations **inside** the bars for better readability
for index, row in enumerate(top_meal_combinations.itertuples()):
    ax.text(
        row.Count + 1,  # Position text slightly outside the bar
        index, 
        f"{row.Count} ({row._4}%)",  # Show count and percentage
        va="center", 
        ha="left",
        color="black",  # Ensure visibility
        fontsize=11,
        fontweight="bold"
    )

# Add labels and title
plt.xlabel("Order Count")
plt.ylabel("Drink Pairing")
plt.title(f"Drink Combinations for Most Ordered Rice Meal: {top_rice_meal}")
plt.grid(axis="x", linestyle="--", alpha=0.5)

# Show results
print(top_meal_combinations[["Rice_Meal", "Drink", "Count", "Ratio (%)"]])
plt.show()

# Display summary
print(f"\nMost Ordered Rice Meal: {top_rice_meal}")
print(f"Total Count of {top_rice_meal}: {highest_meal_total}")
