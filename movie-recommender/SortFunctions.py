####
# Quicksort algorithm taken from:
# https://www.geeksforgeeks.org/quick-sort/
# accessed on 01/25/22
# license: none given
# author: Adnan Aliakbar
###
# CHANGELOG:
# - added if __name__ == "__main__" to driver code
####
# Python3 implementation of QuickSort
# This Function handles sorting part of quick sort
# start and end points to first and last element of
# an array respectively
def partition(start, end, array):
    pivot_index = start
    pivot = array[pivot_index]

    while start < end:

        while start < len(array) and array[start] <= pivot:
            start += 1

        while array[end] > pivot:
            end -= 1

        if start < end:
            array[start], array[end] = array[end], array[start]

    array[end], array[pivot_index] = array[pivot_index], array[end]

    return end


# The main function that implements QuickSort
def quick_sort(start, end, array):

    if start < end:
        p = partition(start, end, array)

        quick_sort(start, p - 1, array)
        quick_sort(p + 1, end, array)


if __name__ == "__main__":
    # Driver code
    array = [10, 7, 8, 9, 1, 5]
    quick_sort(0, len(array) - 1, array)

    print(f'Sorted array: {array}')