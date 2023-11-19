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

import asyncio

async def my_coroutine(id, delay):
    print(f"Coroutine {id} starting")
    await asyncio.sleep(delay)
    print(f"Coroutine {id} finished")
    return f"Result from coroutine {id}"

async def main():
    # List of coroutines
    tasks = [my_coroutine(1, 2), my_coroutine(2, 1), my_coroutine(3, 3)]

    # Waiting for all coroutines to complete
    results = await asyncio.gather(*tasks)

    # Print results
    for result in results:
        print(result)

# Run the main coroutine
asyncio.run(main())
