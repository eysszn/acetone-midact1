import pandas as pd
# Load the dataset
df = pd.read_csv("Downloads/FastFood.csv")

# Most frequent age group
age_group = df["Age"].mode()[0]

# Most common visit time of this age group
time = df[df["Age"] == age_group]["What time do you usually go to McDonalds?"].mode()[0]

# Filter transactions that occur at this visit time
visit = df[df["What time do you usually go to McDonalds?"] == time]

# Extract rice meal orders
meals = visit["Which rice meals do you usually order from McDonalds?"].str.split(",", expand=True)
meals = meals.stack().reset_index(drop=True)  # Flatten into a single column

# Clean values
meals = meals.str.strip().str.lower().str.title()

# Count occurrences of each rice meal
rm_counts = rice_meals.value_counts().reset_index()
rm_counts.columns = ["Rice Meal", "Count"]

# Add visit time column
rm_counts.insert(0, "Visit Time", time)

# Print results in table format
print(rm_counts.to_string(index=False))

# Calculate and print confidence values separately
total = visit.shape[0]
print("\nConfidence Values for Each Combination:")
for meal, count in zip(rm_counts["Rice Meal"], rm_counts["Count"]):
    confidence = (count / total) * 100
    print(f"Confidence({time} → {meal}): {confidence:.2f}%")
