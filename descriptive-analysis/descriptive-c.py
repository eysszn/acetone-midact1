import pandas as pd
from collections import Counter

# Load the clean dataset
file_path = "C:/Users/Juduruu/Downloads/SixSigmas_FastFood_Clean.csv"  #change the filepath where the file is located
df = pd.read_csv(file_path)

# Get menu items
menu_items_series = df["Which of the menu items do you usually order?"]

# Split each entry by comma, then extend the list
menu_items_list = []
for items in menu_items_series.dropna():
    menu_items_list.extend([item.strip() for item in items.split(',')])

# Count the frequency of each menu item
menu_items_counter = Counter(menu_items_list)

# Create a Dataframe for the Frequency Table
menu_items_counter_df = pd.DataFrame(menu_items_counter.items(), columns=["Menu Item", "Count"])

# Sort the result by Count (Descending)
menu_items_counter_df = menu_items_counter_df.sort_values(by="Count", ascending=False).reset_index(drop=True)

# Display the results
print("Most Frequently Ordered Menu Items:")
print(menu_items_counter_df)
