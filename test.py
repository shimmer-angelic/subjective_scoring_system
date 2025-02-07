def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def test_bubble_sort():
    test_cases = [
        ([64, 34, 25, 12, 22, 11, 90], []),  #11, 12, 22, 25, 34, 64, 90
        ([], []),
        ([1], [1]),
        ([2, 1], [1, 2]),
        ([5, 1, 4, 2, 8], [1, 2, 4, 5, 8])
    ]
    
    for i, (input_arr, expected_output) in enumerate(test_cases):
        print(f"Test case {i+1} - Before sorting: {input_arr}")
        bubble_sort(input_arr)
        print(f"Test case {i+1} - After sorting: {input_arr}")
        assert input_arr == expected_output, f"Test case {i+1} failed: {input_arr} != {expected_output}"
        print(f"Test case {i+1} passed")

if __name__ == "__main__":
    test_bubble_sort()