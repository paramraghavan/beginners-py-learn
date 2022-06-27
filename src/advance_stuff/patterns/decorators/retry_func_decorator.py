import time
def retry(times, interval, exceptions):
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    attempt += 1
                    time.sleep(interval)
                    print(
                        'Exception thrown when attempting to run function \'%s\', attempt '
                        '%d of %d @%d seconds interval' % (func.__name__, attempt, times, interval)
                    )
            return func(*args, **kwargs)
        return newfn
    return decorator

count = 0
@retry(times=3, interval=10, exceptions=(ValueError, TypeError))
def run():
    print('Some code here ....')
    print('Oh no, we have exception')
    global count
    count = count + 1
    if count == 1:
        raise ValueError('Some error')
    if count == 2:
        raise TypeError('Some error')
    raise TypeError("test unhandled")
    print(f'count: {count}, all is well finally')


if __name__ == "__main__":
    run()