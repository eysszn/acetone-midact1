import pandas as pd
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "Downloads/FastFood.csv" 
df = pd.read_csv(file_path)

# Split multiple time selections and count time_list = df["What time do you usually go to McDonalds?"].dropna().str.split(", ")
time_counter = Counter([time for sublist in time_list for time in sublist])
time_count_df = pd.DataFrame(time_counter.items(), columns=["Time", "Count"])

# Sort by Count (Descending)
time_count_df = time_count_df.sort_values(by="Count", ascending=False).reset_index(drop=True)

# Display the results
print("Most Common Visit Times:")
print(time_count_df)

# Plot Visit Times
plt.figure(figsize=(10, 6))
sns.barplot(x="Count", y="Time", data=time_count_df, hue="Time", palette="magma", legend=False)
plt.xlabel("Count")
plt.ylabel("Visit Time")
plt.title("Most Common Visit Times at McDonald's")
plt.show()
