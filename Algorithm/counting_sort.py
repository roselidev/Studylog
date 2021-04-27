
import time
import random

# O(n*lg(n))
def counting_sort(A, m):
    tmp = [0]*(m+1)
    ret = [0]*len(A)
    for i in A:
        tmp[i] += 1
    for i in range(2, m+1):
        tmp[i] = tmp[i] + tmp[i-1]
    j = 0
    for i in reversed(range(len(A))):
        ret[tmp[A[i]]-1] = A[i]
        tmp[A[i]] -= 1
    return ret

def compare(arr):
    A = [3, 31, 48, 73, 8, 11, 20, 29, 65, 15] if arr == None else arr
    A_t = A.copy() # to compare with default python sort

    m = max(A)
    ### My merge sort
    s_time = time.time()
    A = counting_sort(A, m)
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

N = 6
compare(random.sample(range(1, 10), N))