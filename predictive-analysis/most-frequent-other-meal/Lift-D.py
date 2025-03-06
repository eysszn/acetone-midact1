import pandas as pd

df = pd.read_excel("C:/Users/eugen/OneDrive/Desktop/SixSigmas-FastFood.xlsx", sheet_name = "Clean 2")

df["Other"] = df["What other meal/s you usually order from McDonalds?"].str.split(", ")
df["Promo"] = df["What types of promotions are most likely to catch your attention? (Select all that apply)"].str.split(", ")

df_exploded = df.explode("Other").explode("Promo")

df_exploded["Other"] = df_exploded["Other"].str.strip()
df_exploded["Promo"] = df_exploded["Promo"].str.strip()

support_menu = df_exploded[df_exploded["Other"] == "Fries"].shape[0] / df_exploded.shape[0]

support_promos = df_exploded[df_exploded["Promo"].isin(["Combo Deals", "Percentage Discounts"])].groupby("Promo").size() / df_exploded.shape[0]

support_combinations = df_exploded[(df_exploded["Other"] == "Fries") &
                                   (df_exploded["Promo"].isin(["Combo Deals", "Percentage Discounts"]))].groupby("Promo").size() / df_exploded.shape[0]

lift_values = {}
for promo in support_promos.index:
    support_promo = support_promos[promo]
    support_combination = support_combinations.get(promo, 0)  # Default to 0 if the combination doesn't exist
    lift = support_combination / (support_menu * support_promo)
    lift_values[promo] = lift

for promo, lift in lift_values.items():
    print(f"Lift for Fries -> {promo}: {lift:.2f}")
