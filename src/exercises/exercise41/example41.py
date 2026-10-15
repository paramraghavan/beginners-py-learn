def sliding_window(iterable, n):
    if n < 1:
        raise ValueError("Window size must be at least 1")
    window = []


    for item in range(0, len(iterable), 1):
        if item <= (len(iterable)-n):
            yield iterable[item:(item+n)]


if __name__ == '__main__':
            arr = [1,3,5,7,9,10,11,12]
            x= sliding_window(arr,3)
            for item in x:
                print(item)