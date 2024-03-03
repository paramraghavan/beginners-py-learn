import pandas as pd

# order_data = {
#     'order_id': [1, 2, 3],
#     'customer_id': [101, 102, 103],
#     'order_date': ['2023-01-01', '2023-01-02', '2023-01-03']
# }
# order_line_item_data = {
#     'line_item_id': [10, 20, 30],
#     'order_id': [1, 2, 3],
#     'product_id': [1001, 1002, 1003],
#     'description': ['mouse','camera','keyboard']
# }
# order_line_item_details_data = {
#     'line_item_id': [10, 20, 30],
#     'quantity': [2, 3, 1],
#     'price': [10.5, 20.0, 15.0]
# }
#
# # Creating DataFrames
# df_order = pd.DataFrame(order_data)
# df_order_line_item = pd.DataFrame(order_line_item_data)
# df_order_line_item_details = pd.DataFrame(order_line_item_details_data)

# Reading CSV files into DataFrames
df_order = pd.read_csv('order.csv')
df_order_line_item = pd.read_csv('order_line_item.csv')
df_order_line_item_details = pd.read_csv('order_line_item_detail.csv')

# Joining the DataFrames
merged_df = pd.merge(df_order, df_order_line_item, on='order_id')
# merged_df = merged_df.drop(columns=['product_id'])
merged_df = pd.merge(merged_df, df_order_line_item_details, on='line_item_id')
# final_df = merged_df.drop(columns=['line_item_id'])
print(merged_df)

# Delete unwanted columns order_date and line_item_id
# Removing unwanted columns
final_df = merged_df.drop(columns=['product_id', 'line_item_id'])

print(final_df)
