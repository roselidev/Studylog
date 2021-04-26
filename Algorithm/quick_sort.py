
import time
import random

# O(n*lg(n))
def partition(A, pivot):
    smaller = []
    larger = []
    for i in A:
        if i <= pivot:
            smaller.append(i)
        else: 
            larger.append(i)
    return smaller + [pivot] + larger, len(smaller)

def quick_sort(A):
    if len(A) <= 1 : return A
    pivot = A[-1]
    A, index = partition(A[0:-1], pivot)
    return quick_sort(A[:index]) + quick_sort(A[index:])

def compare(arr):
    A = [3, 31, 48, 73, 8, 11, 20, 29, 65, 15] if arr == None else arr
    A_t = A.copy() # to compare with default python sort

    ### My merge sort
    s_time = time.time()
    A = quick_sort(A)
    m_time = time.time() - s_time

    ### Python default sort
    s_time = time.time()
    A_t.sort()
    d_time = time.time() - s_time
    
    if A == A_t:
        print("Correct")
    else:
        print("Incorrect")

    if s_time > d_time:
        print("Faster")
    else:
        print("Slower")

N = 10
compare(random.sample(range(1, 1000), N))