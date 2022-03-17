'''
 There is an array of range of values [(10,20),(21,30),(40,60),(70,90),(91,100)] and a
 list of values [10,23,65,89,32,45,67,89,90,27,99]. Identify list of acceptable values
 for the range tuples.
'''

'''
BigO is range items count X values items count --> mXn, n^2
Can we reduce the BigO from the order of n^2 ?
'''
def map_range_values(range, values):
    map_of_range_values = {}

    # range loop
    for range_value in range:
        print(f' start: {range_value[0]}, stop: {range_value[1]}' )

        values_list = []
        # values loop
        for num in values:
            if range_value[0] <= num <= range_value[1]:
                values_list.append(num)

        map_of_range_values[range_value]= values_list

    return map_of_range_values


if __name__ == '__main__':
    list_range = [(10, 20), (21, 30), (40, 60), (70, 90), (91, 100)]
    list_values = [10, 13, 23, 65, 89, 32, 45, 67, 89, 90, 27, 99, 101]

    print(f'map_of_range_values: {map_range_values(list_range, list_values)}')