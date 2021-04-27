import time
import random
# O(n^2)

def insertion_sort(arr=None):
    A = [3, 31, 48, 73, 8, 11, 20, 29, 65, 15] if arr == None else arr
    A_t = A.copy() # to compare with default python sort

    ### My insertion sort
    s_time = time.time()

    for i in range(1, len(A)):
        for j in range(0, i):
            if A[i] < A[j]:
                A.insert(j,A[i])
                del A[i+1]

    m_time = time.time() - s_time

    ### Python default sort
    s_time = time.time()
    A_t.sort()
    d_time = time.time() - s_time
    
    if A == A_t:
        print("Correct")
    else:
        print("Incorrect")

    if m_time > d_time:
        print("Faster")
    else:
        print("Slower")

N = 100
insertion_sort(random.sample(range(1, 1000), N))