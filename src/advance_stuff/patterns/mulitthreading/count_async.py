'''
https://realpython.com/async-io-python/ **

 At the heart of async IO are coroutines. A coroutine is a specialized version of a Python generator function.
 A coroutine is a function that can suspend its execution before reaching return, and it can indirectly pass control
 to another coroutine for some time.

 The order of this output is the heart of async IO. Talking to each of the calls to count() is a single event loop, or coordinator.
  When each task reaches await asyncio.sleep(1), the function yells up to the event loop and yields/gives control back to it, saying,
 “I’m going to be sleeping for 1 second. Go ahead and let something else meaningful be done in the meantime.”

 The keyword await passes function control back to the event loop. (It suspends the execution of the surrounding coroutine.)
 If Python encounters an await f() expression in the scope of g(), this is how await tells the event loop, “Suspend execution of g() until
 whatever I’m waiting on—the result of f()—is returned. In the meantime, go let something else run.”

'''
import asyncio

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")