import time
import random

# O(n^2)
def merge(A, B):
    i = 0
    j = 0
    ret = []
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            ret.append(A[i])
            i += 1
        else:
            ret.append(B[j])
            j += 1
    while i < len(A):
        ret.append(A[i])
        i += 1
    while j < len(B):
        ret.append(B[j])
        j += 1
    return ret

def merge_sort(A):
    if len(A) <= 1 : return A
    m = round(len(A)/2)
    B = merge_sort(A[0:m])
    C = merge_sort(A[m:len(A)])
    return merge(B, C)

def compare(arr):
    A = [3, 31, 48, 73, 8, 11, 20, 29, 65, 15] if arr == None else arr
    A_t = A.copy() # to compare with default python sort
    s_time = time.time()
    A = merge_sort(A)
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