import pandas as pd

# Load the dataset
df = pd.read_csv("Downloads/FastFood.csv")

# Filter only "Fried Chicken with Rice"
fried_chicken = df[
    df["Which rice meals do you usually order from McDonalds?"].str.contains("Fried Chicken with Rice", na=False)
]

# Count total orders of Fried Chicken with Rice
fc = fried_chicken.shape[0]

# Split multiple drink choices into separate rows
drinks = fried_chicken["Which drink/s do you usually order from McDonalds?"].str.split(",", expand=True)
drinks = drinks.stack().reset_index(drop=True) 

# Remove extra spaces and count occurrences of each drink
dcounts = drinks.str.strip().value_counts().reset_index()
dcounts.columns = ["Drink", "Count"]

# Add the "Rice Meal" column
dcounts.insert(0, "Rice_Meal", "Fried Chicken with Rice")

# Display the properly formatted output without confidence in the table
print(dcounts.to_string(index=False))
print("\nConfidence Values for Each Combination:")
for _, row in dcounts.iterrows():
    confidence = (row["Count"] / fc) * 100
    print(f"Confidence(Fried Chicken with Rice → {row['Drink']}): {confidence:.2f}%")
