import pandas as pd

# Reading CSV files into DataFrames
df_order = pd.read_csv('order.csv')
df_order_line_item = pd.read_csv('order_line_item.csv')
df_order_line_item_details = pd.read_csv('order_line_item_detail.csv')

# Converting DataFrames to dictionaries
order_dict = df_order.to_dict(orient='records')
order_line_item_dict = df_order_line_item.to_dict(orient='records')
order_line_item_details_dict = df_order_line_item_details.to_dict(orient='records')

# Printing the dictionaries
print("Order Dictionary:")
print(order_dict)
print("\nOrder Line Item Dictionary:")
print(order_line_item_dict)
print("\nOrder Line Item Details Dictionary:")
print(order_line_item_details_dict)
