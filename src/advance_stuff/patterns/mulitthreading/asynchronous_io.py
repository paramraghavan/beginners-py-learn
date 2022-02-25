'''
https://medium.com/@sh.hooshyari/introduction-to-asyncio-in-python-36983d6a715a
https://realpython.com/async-io-python/ **
python has a package asyncio for this purpose, it has two keywords:
 async to define coroutines and
 await to run coroutines
'''

import asyncio
async def process():
   return "done"

result = asyncio.run(process()) # correct way of executing async function
print(f'run complete {result}')

async def main():
    # entry point of our script
    pass
asyncio.run(main())

#
# '''
# Now what we do if we have multiple coroutines to run?
# simply use asyncio.gather
# '''
#
import asyncio
import time

async def task(run_id):
    await asyncio.sleep(1)
    print(f"done task {run_id}")

async def main():
    start = time.time()
    await asyncio.gather(task(1), task(2), task(3))
    print(f"all the tasks took {time.time() - start} to run")

asyncio.run(main())
