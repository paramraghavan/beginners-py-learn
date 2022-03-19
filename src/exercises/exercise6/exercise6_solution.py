'''
Given a start, stop and step, generate a list of range tuples, so that
gen_range(100, 140, 10)  would produce output:

[(100, 110), (110, 120), (120, 130), (130, 140)]
'''

'''
Solution 1
'''
def gen_range_values(start, stop, step):
    range_values = []
    for item in range(start, stop, step):
        range_values.append((item,item+step))

    print(f'range_values: {range_values}')
    return range_values

'''
Alternate solution 2. Solution 1 is simple and best
Another solution to create range list using python 'generator'
'''
def gen_range_values_alt(start, stop, step):
    range_values = []
    for range in gen_range(start, stop, step):
        if range[0] == stop:
            break;
        range_values.append(range)

    print(f'range_values: {range_values}')
    return range_values

'''
Creating generator function using yield
'''
def gen_range(start, stop, step):
    for i in range(start,stop+1,step):
         yield (i,i+step)



if __name__ == '__main__':
    start = 100
    stop = 190
    step = 10
    range_values = gen_range_values(start, stop,step)
    range_values_alt = gen_range_values_alt(start, stop, step)
    assert range_values == range_values_alt, 'Error one or both of the range generators are incorrect.'




