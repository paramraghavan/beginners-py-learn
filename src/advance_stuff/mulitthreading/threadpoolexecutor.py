'''
When you run this code, all 10 items will be sent out to be worked on but as we limit of 3 worker threads
there will 3 items processed concurrently,  as the worker completes the process on the item it is working on,
it will pickup the next item in queue
'''

from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from typing import List


def process_item(item: int) -> dict:
    """
    Simulate processing an item with random delay to demonstrate async behavior.
    """
    # Simulate some work
    time.sleep(random.uniform(0.1, 0.5))

    # Simulate occasional failures
    if random.random() < 0.1:  # 10% chance of failure
        raise ValueError(f"Processing failed for item {item}")

    return {
        "item": item,
        "result": item * item,
        "processed_at": time.strftime("%H:%M:%S")
    }


def process_batch(items: List[int], max_workers: int = 3) -> tuple:
    """
    Process a batch of items using ThreadPoolExecutor.
    Returns tuple of (successful results, errors).
    """
    successful_results = []
    errors = []

    # Use context manager to ensure proper cleanup
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and get future objects
        future_to_item = {
            executor.submit(process_item, item): item
            for item in items
        }

        # Process completed futures as they finish
        for future in as_completed(future_to_item):
            item = future_to_item[future]
            try:
                result = future.result()
                successful_results.append(result)
                print(f"Successfully processed item {item}")
            except Exception as e:
                errors.append({
                    "item": item,
                    "error": str(e)
                })
                print(f"Error processing item {item}: {e}")

    return successful_results, errors


def main():
    # Example usage
    items = list(range(10))
    print(f"Processing {len(items)} items...")

    start_time = time.time()
    results, errors = process_batch(items)
    end_time = time.time()

    print("\nResults:")
    for result in results:
        print(f"Item {result['item']}: {result['result']} (processed at {result['processed_at']})")

    print("\nErrors:")
    for error in errors:
        print(f"Item {error['item']}: {error['error']}")

    print(f"\nTotal time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
