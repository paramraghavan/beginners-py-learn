'''
 There is an array of range of values [(10,20),(21,30),(40,60),(70,90),(91,100)] and a
 list of values [10,23,65,89,32,45,67,89,90,27,99]. Identify list of acceptable values
 for the range tuples.
'''

loop_counter = 0

# 1st Implementation assuming  range values and list values both are not sorted
'''
BigO is range items count X values items count --> mXn, n^2
Can we reduce the BigO from the order of n^2 ?
Plain vanilla implementation
'''
def map_range_values(range, values):
    map_of_range_values = {}
    global loop_counter
    loop_counter = 0
    # range loop
    for range_value in range:
        loop_counter += 1
        print(f' start: {range_value[0]}, stop: {range_value[1]}' )

        values_list = []
        # values loop
        for num in values:
            loop_counter += 1
            if range_value[0] <= num <= range_value[1]:
                values_list.append(num)

        map_of_range_values[range_value]= values_list

    return map_of_range_values


# 2nd Implementation with range values sorted

'''
BigO is range items count X values items count --> mXn, n^2
Can we reduce the BigO from the order of n^2 ?
Assuming Range values start/stop are exclusive to each tuple and are in sorted order
ref: https://www.tutorialspoint.com/python_data_structure/python_divide_and_conquer.htm
'''
def divide_conquer(num, range):
    range_len = len(range)
    # start index
    idx0 = 0
    # end index
    idxn = range_len - 1
    global loop_counter
    while idx0 <= idxn:
        loop_counter += 1
        # mid value
        idxm = (idx0 + idxn)//2

        if range[idxm][0] <= num <= range[idxm][1]:
            return range[idxm]
        if  num > range[idxm][0]:
            idx0= idxm +1
        else:
            idxn = idxm - 1
        if idx0 > idxn:
            return None

'''
Uses divide_conquer on sorted range values
'''
def map_range_values_alt(range, values):
    map_of_range_values = {}
    global loop_counter
    loop_counter = 0
    # values loop
    range_length = len(range)
    for num in values:
        loop_counter += 1
        range_matched = divide_conquer(num, range)
        if range_matched == None:
            print(f'No match found for num: {num}')
            continue # no match found for num
        if  map_of_range_values.get(range_matched, None) == None:
            map_of_range_values[range_matched] = [num]
        else:
            map_of_range_values[range_matched].append(num)

    return map_of_range_values


# 3rd Implementation assuming  range values and list values both are sorted

'''
BigO is range items count X values items count --> mXn, n^2
Can we reduce the BigO from the order of n^2 ?
Assuming:
 1. Range values start/stop are exclusive to each tuple and are in sorted order
 2. The values in list_values are also sorted
'''

def check_in_range(num, range_values):
    match = None
    for range in range_values:
        if range[0] <= num <= range[1]:
            match = range
            break

    return match
'''
Uses check_in_range
'''
def map_range_values_both_sorted(range, values):
    map_of_range_values = {}
    global loop_counter
    loop_counter = 0
    # values loop
    range_length = len(range)
    for num in values:
        loop_counter += 1
        range_matched = check_in_range(num, range)
        # once the num value is more than the upper value of range,
        # then remove this range tuple
        if range_matched is not None and num >= range_matched[1]:
            #range.remove(range_matched) or  del range[0]
            # we know for sure this is the first item
            del range[0]
            if len(range) == 0:
                break;
        if range_matched == None:
            print(f'No match found for num: {num}')
            continue # no match found for num
        if  map_of_range_values.get(range_matched, None) == None:
            map_of_range_values[range_matched] = [num]
        else:
            map_of_range_values[range_matched].append(num)

    return map_of_range_values





if __name__ == '__main__':
    list_range = [(0,9), (10, 20), (21, 30), (40, 60), (70, 90), (91, 100)]
    list_values = [10, 13, 23, 65, 71, 32, 45, 67, 89, 90, 27, 99, 101]

    ''' 
    You will notice that the number for iterations have reduced:
    Original: Quadratic growth
     map_of_range_values: {(0, 9): [], (10, 20): [10, 13], (21, 30): [23, 27], (40, 60): [45], (70, 90): [71, 89, 90], (91, 100): [99]}, loop_counter: 84 --> bigO NXM
     
    Assuming range sorted: Log-Linear growth
     map_of_range_values_sorted: {(10, 20): [10, 13], (21, 30): [23, 27], (70, 90): [71, 89, 90], (40, 60): [45], (91, 100): [99]}, loop_counter: 45 --> bigO NXlogM 
    
    Assuming range and values both sorted: Linear growth
    map_range_values_both_sorted: {(10, 20): [10, 13], (21, 30): [23, 27], (40, 60): [45], (70, 90): [71, 89, 90], (91, 100): [99]}, loop_counter: 13 --> bogO N      
    '''
    print(f'map_of_range_values: {map_range_values(list_range, list_values)}, loop_counter: {loop_counter}')
    print(f'map_of_range_values_sorted: {map_range_values_alt(list_range, list_values)}, loop_counter: {loop_counter}')
    list_values_in_sort_order = [10, 13, 23, 27, 32, 45, 65, 71, 67, 89, 90, 99, 101]
    print(f'map_range_values_both_sorted: {map_range_values_both_sorted(list_range, list_values_in_sort_order)}, loop_counter: {loop_counter}')