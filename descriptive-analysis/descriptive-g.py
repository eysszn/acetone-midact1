import pandas as pd
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "Downloads/FastFood.csv"
df = pd.read_csv(file_path)

# Filter only Afternoon Snack time
afternoon_snack_df = df[df["What time do you usually go to McDonalds?"].str.contains("Afternoon Snack", na=False)]

# Split multiple dessert selections and count each 
dessert_list = afternoon_snack_df["Which dessert/s do you usually order from McDonalds?"].dropna().str.split(", ")
dessert_counter = Counter([dessert for sublist in dessert_list for dessert in sublist])

# Convert to DataFrame
dessert_count_df = pd.DataFrame(dessert_counter.items(), columns=["Dessert", "Count"])

# Sort by Count (Descending) and Reset Index
dessert_count_df = dessert_count_df.sort_values(by="Count", ascending=False).reset_index(drop=True)

print("\nMost Common Desserts as an Afternoon Snack:")
print(dessert_count_df)

# Plot Desserts
plt.figure(figsize=(10, 6))
sns.barplot(x="Count", y="Dessert", data=dessert_count_df, hue="Dessert", palette="magma", legend=False)
plt.xlabel("Count")
plt.ylabel("Dessert")
plt.title("Most Common Desserts Ordered at McDonald's")
plt.show()
