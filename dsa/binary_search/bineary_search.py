def binary_search(arr, target):
    """
    Performs binary search on a sorted array.

    Args:
        arr: Sorted list of elements
        target: Element to search for

    Returns:
        Index of target if found, -1 if not found
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# Example usage
if __name__ == "__main__":
    # Test with a sorted array
    numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    # Search for existing elements
    print(binary_search(numbers, 7))  # Output: 3
    print(binary_search(numbers, 1))  # Output: 0
    print(binary_search(numbers, 19))  # Output: 9

    # Search for non-existing element
    print(binary_search(numbers, 8))  # Output: -1