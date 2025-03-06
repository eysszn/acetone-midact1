import pandas as pd
from collections import defaultdict

# Load the clean dataset
df = pd.read_csv('C:/Users/Juduruu/Downloads/SixSigmas_FastFood_Clean.csv')

# Identify the most frequent age group
most_common_age = df['Age'].value_counts().idxmax()
age_filtered = df[df['Age'] == most_common_age]

# Find the most common visit time within this age group
time_counts = defaultdict(int)
for times in age_filtered['What time do you usually go to McDonalds?']:
    for time in [t.strip() for t in times.split(',')]:
        time_counts[time] += 1
most_common_time = max(time_counts, key=time_counts.get)

# Functions for conditions
def has_time(row, target_time):
    return target_time in [t.strip() for t in row['What time do you usually go to McDonalds?'].split(',')]

def has_specific_rice_meal(row, rice_meal):
    return isinstance(row['Which rice meals do you usually order from McDonalds?'], str) and rice_meal in row['Which rice meals do you usually order from McDonalds?']

# Compute Support Values for each specific rice meal
number_transactions = len(df)
rice_meals = ["Fried Chicken with Rice", "Chicken Fillet Ala King", "Pepper Steak", "McCrispy"]

results = []

for rice_meal in rice_meals:
    # Calculate for the Support(X)
    antecedent_group = age_filtered[age_filtered.apply(has_time, args=(most_common_time,), axis=1)]
    support_X = len(antecedent_group) / number_transactions

    # Calculate for Support(Y)
    rice_meal_group = df[df.apply(has_specific_rice_meal, args=(rice_meal,), axis=1)]
    support_Y = len(rice_meal_group) / number_transactions

    # Calculate for Support(X ∩ Y)
    support_X_and_Y = len(antecedent_group[antecedent_group.apply(has_specific_rice_meal, args=(rice_meal,), axis=1)]) / number_transactions

    # Calculate for Confidence(X → Y)
    confidence_X_to_Y = support_X_and_Y / support_X if support_X > 0 else 0

    # Calculate for Lift(X → Y)
    lift_X_to_Y = confidence_X_to_Y / support_Y if support_Y > 0 else 0

    # Store the results for each rice meal
    lift_value = round(lift_X_to_Y, 2)
    results.append(f"Lift({most_common_time} & {most_common_age} → {rice_meal}) : {lift_value}")

# Display results
print ("Lift of Most Common Visit Time of Most Frequent Age Group → Each Rice Meals Usually Ordered from McDonald's")
for result in results:
    print(result)
