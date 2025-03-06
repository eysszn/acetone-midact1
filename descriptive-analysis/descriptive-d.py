import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Common Visit Time by Age Group
# Load the CSV File
df = pd.read_csv('C:/Users/Lenovo/Downloads/Midterm1Clean.csv')

#Extract relevant columns
df_age_time = df[['Age', 'What time do you usually go to McDonalds?']]

# Expand rows for multiple time selections
df_age_time = df_age_time.assign(
    **{"What time do you usually go to McDonalds?": df_age_time[
        "What time do you usually go to McDonalds?"
    ].str.split(', ')}
).explode("What time do you usually go to McDonalds?")

# Count occurrences of visit times by age group
visit_counts = df_age_time.value_counts().reset_index(name='Count')
print(visit_counts)

# Plot the data
plt.figure(figsize=(10, 6))
sns.barplot(data=visit_counts, x="Age", y="Count", hue="What time do you usually go to McDonalds?", palette="magma")
plt.title("Common Visit Times by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Count of Visits")
plt.legend(title="Visit Time")
plt.show()