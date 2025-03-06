import pandas as pd
# Load the dataset
df = pd.read_csv("Downloads/FastFood.csv")

# Convert all text columns to strings and remove extra spaces
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Filter "McFlurry"
mcflurry = df[df["Which dessert/s do you usually order from McDonalds?"].str.contains("McFlurry", case=False, na=False)]

# Count "McFlurry"
count = mcflurry.shape[0]

# Split multiple "Other Meals" into separate rows
other = mcflurry["What other meal/s you usually order from McDonalds?"].str.split(",", expand=True)
other = other.stack().reset_index(drop=True)  
# Strip spaces and force lowercase for consistency
other = other.str.strip().str.lower()

# Restore proper capitalization
other = other.str.title()

# Remove empty values from the 'other' column
other = other[other != ""]

# Count occurrences of each meal
meal = other.value_counts().reset_index()
meal.columns = ["Other Meal", "Count"]

# Add a column for the dessert (McFlurry)
meal.insert(0, "Dessert", "McFlurry")

# Print table if there are valid combinations
if not meal.empty:
    print(meal.to_string(index=False))

    # Calculate confidence values
    confidence_values = (meal["Count"] / count) * 100

    # Print confidence values separately
    print("\nConfidence Values for Each Combination:")
    for meal_name, conf in zip(meal["Other Meal"], confidence_values):
        print(f"Confidence(McFlurry → {meal_name}): {conf:.2f}%")
