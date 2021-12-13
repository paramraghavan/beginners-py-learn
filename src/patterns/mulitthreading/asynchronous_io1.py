'''
ref: https://kamilwu.medium.com/a-guide-to-python-asyncio-7a280dee3fdb
'''


import asyncio
from datetime import datetime


def log(msg):
    print(f'{datetime.now():%H:%M:%S.%f} {msg}')


async def say_after(what, delay):
    log(f'"{what}" scheduled for execution')
    await asyncio.sleep(delay)
    log(what)

'''
the say_after calls are run in sequence,one after the other
'''
async def main():
    await say_after('Hello!', 2)
    await say_after('Hi!', 1)
    log('Done.')


'''
asyncio.create_task() creates a task from the coroutine object and schedules it on the event loop,
 but does not pause the caller. This is an important difference between creating a Task via 
 asyncio.create_task() and awaiting via await on a coroutine.
'''
async def main_create_task():
    task1 = asyncio.create_task(say_after('Hello!', 2))
    task2 = asyncio.create_task(say_after('Hi!', 1))
    await task1
    await task2
    log('Done.')

if __name__ == '__main__':
    # tasks invoked sequentially
    asyncio.run(main())
    print('*' * 70)
    print('*' * 70)
    # tasks run is interlaced.
    asyncio.run(main_create_task())
