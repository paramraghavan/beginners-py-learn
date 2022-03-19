'''
Given a start, stop and step, generate a list of range tuples, so that
gen_range(100, 140, 10)  would produce output:

[(100, 110), (110, 120), (120, 130), (130, 140)]
'''


def gen_range(start, stop, step):
    for i in range(start,stop+1,step):
         yield (i,i+step)


def gen_range_values(start, stop, step):
    range_values = []
    for range in gen_range(start, stop, step):
        if range[0] == stop:
            break;
        range_values.append(range)
    print(f'range_values: {range_values}')


if __name__ == '__main__':
    start = 100
    stop = 190
    step = 10
    gen_range_values(start, stop,step)





