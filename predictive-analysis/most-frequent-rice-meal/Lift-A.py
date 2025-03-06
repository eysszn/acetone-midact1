import pandas as pd

df = pd.read_excel("C:/Users/eugen/OneDrive/Desktop/SixSigmas-FastFood.xlsx", sheet_name = "Clean")

# Ensure both columns are treated as lists, replacing NaN with ["None"]
df["Rice_Meal"] = df["Which rice meals do you usually order from McDonalds?"].str.split(", ")
df["Drink"] = df["Which drink/s do you usually order from McDonalds?"].apply(lambda x: x.split(", ") if pd.notna(x) else ["None"])

# Explode both columns to align them
df_exploded = df.explode("Rice_Meal").explode("Drink")

# Strip leading/trailing spaces
df_exploded["Rice_Meal"] = df_exploded["Rice_Meal"].str.strip()
df_exploded["Drink"] = df_exploded["Drink"].str.strip()

# Calculate the support of "Fried Chicken with Rice"
support_rice_meal = df_exploded[df_exploded["Rice_Meal"] == "Fried Chicken with Rice"].shape[0] / df_exploded.shape[0]

# Calculate the support of each drink
support_drinks = df_exploded[df_exploded["Drink"].isin(["McFloat", "Soft Drinks", "Cappuccino", "Americano", "Hot Chocolate"])].groupby("Drink").size() / df_exploded.shape[0]

# Calculate the support of the combination "Fried Chicken with Rice" and each drink
support_combinations = df_exploded[(df_exploded["Rice_Meal"] == "Fried Chicken with Rice") &
                                   (df_exploded["Drink"].isin(["McFloat", "Soft Drinks", "Cappuccino", "Americano", "Hot Chocolate"]))].groupby("Drink").size() / df_exploded.shape[0]

# Calculate the lift for each combination
lift_values = {}
for drink in support_drinks.index:
    support_drink = support_drinks[drink]
    support_combination = support_combinations.get(drink, 0)  # Default to 0 if the combination doesn't exist
    lift = support_combination / (support_rice_meal * support_drink)
    lift_values[drink] = lift

# Display the lift values
for drink, lift in lift_values.items():
    print(f"Lift for Fried Chicken with Rice -> {drink}: {lift:.2f}")