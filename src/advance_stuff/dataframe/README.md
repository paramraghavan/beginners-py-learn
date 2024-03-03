# Transform CSV
We are going to work with Order, Order Line Item and Order Line Item Details 

## CSV files
- Here we have CSV file, but the above transformation could be applied to  other file types
- Order
```csv
order_id,customer_id,order_date
1,101,2023-01-01
2,102,2023-01-02
3,103,2023-01-03
```
- Order Line Item
```csv
line_item_id,order_id,product_id,decription
10,1,1001,mouse
20,2,1002,camera
30,3,1003,keyboard
```
- Order Line Item Details 
```csv
line_item_id,quantity,price
10,2,10.5
20,3,20.0
30,1,15.0
```
## Transformations
- Read csv as a dataframe
- Read csv as a python dictionary
- To join three DataFrames - Order, Order Line Item and Order Line Item Details dataframes using pandas, you can use the
  merge function, you can join them based on common columns
- Delete unwanted columns order_date and line_item_id
  - When merging dataframes in pandas, you can't directly exclude columns during the merge operation itself.
  However, you can easily drop the unwanted columns immediately after merging.
