import pandas as pd

df = pd.read_excel("C:/Users/eugen/OneDrive/Desktop/SixSigmas-FastFood.xlsx", sheet_name = "Clean")

# Ensure both columns are treated as lists, replacing NaN with ["None"]
df["Desserts"] = df["Which dessert/s do you usually order from McDonalds?"].str.split(", ")
df["OtherMeal"] = df["What other meal/s you usually order from McDonalds?"].str.split(", ")

# Explode both columns to align them
df_exploded = df.explode("Desserts").explode("OtherMeal")

# Strip leading/trailing spaces
df_exploded["Desserts"] = df_exploded["Desserts"].str.strip()
df_exploded["OtherMeal"] = df_exploded["OtherMeal"].str.strip()

# Calculate the support of "McFlurry"
support_desserts = df_exploded[df_exploded["Desserts"] == "McFlurry"].shape[0] / df_exploded.shape[0]

# Calculate the support of each other meal
support_otherMeals = df_exploded[df_exploded["OtherMeal"].isin(["Fries", "Chicken Sandwich", "Chicken McNuggets", "Hotcakes", "Apple Pie", "McSpaghetti", "McBurger", "Hash Browns", "Tuna Pie", "Cheese burger"])].groupby("OtherMeal").size() / df_exploded.shape[0]

# Calculate the support of the combination "McFlurry" and each other meal
support_combinations = df_exploded[(df_exploded["Desserts"] == "McFlurry") &
                                   (df_exploded["OtherMeal"].isin(["Fries", "Chicken Sandwich", "Chicken McNuggets", "Hotcakes", "Apple Pie", "McSpaghetti", "McBurger", "Hash Browns", "Tuna Pie", "Cheese burger"]))].groupby("OtherMeal").size() / df_exploded.shape[0]

# Calculate the lift for each combination
lift_values = {}
for otherMeal in support_otherMeals.index:
    support_otherMeal = support_otherMeals[otherMeal]
    support_combination = support_combinations.get(otherMeal, 0)  # Default to 0 if the combination doesn't exist
    lift = support_combination / (support_desserts * support_otherMeal)
    lift_values[otherMeal] = lift

# Display the lift values
for otherMeal, lift in lift_values.items():
    print(f"Lift for McFlurry -> {otherMeal}: {lift:.2f}")
