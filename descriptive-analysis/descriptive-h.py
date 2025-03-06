import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Most ordered "Other Meals"
# Load the CSV File
df = pd.read_csv('C:/Users/Lenovo/Downloads/Midterm1Clean.csv')

# Extract relevant column and drop NaN values
df_other_meals = df[['What other meal/s you usually order from McDonalds?']].dropna()

# Expand rows for multiple selections and standardize text formatting
df_other_meals = df_other_meals.assign(
    **{"What other meal/s you usually order from McDonalds?": df_other_meals[
        "What other meal/s you usually order from McDonalds?"
    ].str.split(',')}
).explode("What other meal/s you usually order from McDonalds?")

# Standardize meal names: strip spaces, convert to lowercase, and remove duplicate spaces
df_other_meals["What other meal/s you usually order from McDonalds?"] = df_other_meals[
    "What other meal/s you usually order from McDonalds?"
].str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)

# **Remove blank or NaN values**
df_other_meals = df_other_meals[df_other_meals["What other meal/s you usually order from McDonalds?"] != ""]

# Count occurrences of other meals
other_meal_counts = df_other_meals["What other meal/s you usually order from McDonalds?"].value_counts().reset_index()
other_meal_counts.columns = ["Other Meal", "Count"]

# Capitalize the first letter of each word for better readability
other_meal_counts["Other Meal"] = other_meal_counts["Other Meal"].str.title()
print(other_meal_counts)

# Plot the data
plt.figure(figsize=(10, 6))
sns.barplot(data=other_meal_counts, x="Count", y="Other Meal", palette="magma")
plt.title("Most Ordered Other Meals")
plt.xlabel("Count of Orders")
plt.ylabel("Other Meals")
plt.show()