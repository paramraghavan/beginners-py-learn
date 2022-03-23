'''
Given a array of tuples find the tuple with max value based on the first tuple value.
There is an array of range of values [(10,20),(21,30),(40,60),(70,90),(91,100)]
In this case it should print (91,100)
'''

'''
max tuple based on the second tuple value.
'''
def print_max_value_tuple(tuple_list):
    return max(tuple_list, key= lambda tuple_item : tuple_item[1])


# max_tuple = lambda tuple_item, pos : tuple_item[pos]
def max_tuple(item, pos):
    return  item[pos]

'''
As built in function iterates over the list, we can use key to override the default funtion to find the
max value.
'''
def print_max_value_tuple_pos(tuple_list, pos):
    return max(tuple_list, key= lambda item: max_tuple(item, pos))


if __name__ == '__main__':
    tuple_list = [(10,20),(21,30),(99,100),(40,60),(70,90),(91,105)]

    # default max is based on first tuple position
    print(f'default print_max_value_tuple: {max(tuple_list)}')
    print(80 * '-')
    print(80 * '-')
    print(f'print_max_value_tuple: {print_max_value_tuple(tuple_list)}')

    print(80 * '-')
    print(80 * '-')

    print(f'print_max_value_tuple_pos 0: {print_max_value_tuple_pos(tuple_list, 0)}')
    print(f'print_max_value_tuple_pos 1: {print_max_value_tuple_pos(tuple_list, 1)}')
