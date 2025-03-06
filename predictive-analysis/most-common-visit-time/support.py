import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_excel("G:/My Drive/3rd Year 2ndSem/Data Analytics/Midterms/2Copy of SixSigmas-FastFood.xlsx", sheet_name='Clean')

# Ensure "Rice Meals" is a list, replacing NaN with ["None"]
df["Rice_Meal"] = df["Which rice meals do you usually order from McDonalds?"].apply(lambda x: x.split(", ") if pd.notna(x) else ["None"])

# Strip spaces
df["Rice_Meal"] = df["Rice_Meal"].apply(lambda meals: [meal.strip() for meal in meals])

# Explode lists to count individual items
df_exploded = df.explode("Rice_Meal")

# Count occurrences of each age group
age_counts = df_exploded["Age"].value_counts().reset_index()
age_counts.columns = ["Age Group", "Count"]

# Get the most frequent age group
most_frequent_age_group = age_counts.iloc[0]["Age Group"]
most_frequent_age_count = age_counts.iloc[0]["Count"]

# Filter dataset to include only the most frequent age group
filtered_df = df_exploded[df_exploded["Age"] == most_frequent_age_group]

# Split visit times into separate entries using commas as delimiters
filtered_df["Visit_Times"] = filtered_df["What time do you usually go to McDonalds?"].apply(
    lambda x: [time.strip() for time in x.split(",")] if pd.notna(x) else []
)

# Explode visit times to count them individually
df_visit_exploded = filtered_df.explode("Visit_Times")

# Count occurrences of visit times
visit_time_counts = df_visit_exploded["Visit_Times"].value_counts().reset_index()
visit_time_counts.columns = ["Visit Time", "Count"]

# Get the most common visit time
most_common_visit_time = visit_time_counts.iloc[0]["Visit Time"]
most_common_visit_count = visit_time_counts.iloc[0]["Count"]

# Filter dataset to include only the most frequent age group and most common visit time
filtered_df = df_visit_exploded[df_visit_exploded["Visit_Times"] == most_common_visit_time]

# Count occurrences of rice meals
rice_meal_counts = filtered_df["Rice_Meal"].value_counts().reset_index()
rice_meal_counts.columns = ["Rice Meal", "Count"]

# Compute total orders
total_rice_meal_count = rice_meal_counts["Count"].sum()

# Compute ratio (%) for each rice meal
rice_meal_counts["Ratio (%)"] = (rice_meal_counts["Count"] / total_rice_meal_count) * 100

# Display Results
print(f"\n **Most Frequent Age Group:** {most_frequent_age_group} ({most_frequent_age_count} people)\n")
print(f" **Most Common Visit Time for This Age Group:** {most_common_visit_time} ({most_common_visit_count} visits)\n")

if not rice_meal_counts.empty:
    most_common_rice_meal = rice_meal_counts.iloc[0]["Rice Meal"]
    most_common_rice_meal_count = rice_meal_counts.iloc[0]["Count"]
    print(f" **Most Ordered Rice Meal at This Time:** {most_common_rice_meal} ({most_common_rice_meal_count} orders)\n")
else:
    print("\n No rice meal data found for this visit time.\n")

# If no valid data is found, exit gracefully
if rice_meal_counts.empty:
    print("\n No rice meal data found for this visit time.\n")
else:
    # Modify labels to include both count and percentage
    rice_meal_counts["Label"] = rice_meal_counts.apply(lambda row: f"{row['Rice Meal']} ({row['Ratio (%)']:.2f}%)", axis=1)

    # Plot bar chart for rice meals
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=rice_meal_counts, x="Count", y="Label", palette="muted")

    # Extend x-axis for better readability
    max_x_value = rice_meal_counts["Count"].max()
    plt.xlim(0, max_x_value + (max_x_value * 0.3))  # Add 30% more space

    # Add annotations inside bars with counts and ratios in percentage
    for index, row in rice_meal_counts.iterrows():
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
    plt.xlabel("Order Count")
    plt.ylabel("Rice Meal")
    plt.title(f"Rice Meals Ordered During {most_common_visit_time} for {most_frequent_age_group}")
    plt.grid(axis="x", linestyle="--", alpha=0.5)

    # Show results
    plt.show()
