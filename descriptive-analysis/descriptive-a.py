import pandas as pd
from collections import Counter
#Load the clean dataset
file_path = "C:/Users/Juduruu/Downloads/SixSigmas_FastFood_Clean.csv" #change the filepath where the file is located
df = pd.read_csv(file_path)

age_group = df["Age"]
age_group_counter = Counter(age_group)
age_group_counter_df = pd.DataFrame(age_group_counter.items(), columns=["Age Group", "Count"])

# Sort the Result by Count (Descending)
age_group_counter_df = age_group_counter_df.sort_values(by="Count", ascending=False).reset_index(drop=True)

# Display the Results
print("Most Frequent Customer Age Group that goes to McDonalds:")
print(age_group_counter_df)
