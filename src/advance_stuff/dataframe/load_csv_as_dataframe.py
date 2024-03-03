import pandas as pd

# Reading CSV files into DataFrames
df_order = pd.read_csv('order.csv')
df_order_line_item = pd.read_csv('order_line_item.csv')
df_order_line_item_details = pd.read_csv('order_line_item_detail.csv')

# Displaying the DataFrames
print("Order DataFrame:")
print(df_order)
print("\nOrder Line Item DataFrame:")
print(df_order_line_item)
print("\nOrder Line Item Details DataFrame:")
print(df_order_line_item_details)