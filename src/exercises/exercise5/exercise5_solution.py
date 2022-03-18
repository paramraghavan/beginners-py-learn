'''
 There is an array of range of values [(10,20),(21,30),(40,60),(70,90),(91,100)] and a
 list of values [10,23,65,89,32,45,67,89,90,27,99]. Identify list of acceptable values
 for the range tuples.
'''

loop_counter = 0

'''
BigO is range items count X values items count --> mXn, n^2
Can we reduce the BigO from the order of n^2 ?
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



from math import ceil

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



if __name__ == '__main__':
    list_range = [(0,9), (10, 20), (21, 30), (40, 60), (70, 90), (91, 100)]
    list_values = [10, 13, 23, 65, 71, 32, 45, 67, 89, 90, 27, 99, 101]

    ''' 
    You will notice that the number for iterations have reduced with function map_range_values_alt
    map_of_range_values: {(10, 20): [10, 13], (21, 30): [23, 27], (40, 60): [45], (70, 90): [89, 89, 90], (91, 100): [99]}, loop_counter: 70        
    '''
    print(f'map_of_range_values: {map_range_values(list_range, list_values)}, loop_counter: {loop_counter}')
    print(f'map_of_range_values: {map_range_values_alt(list_range, list_values)}, loop_counter: {loop_counter}')