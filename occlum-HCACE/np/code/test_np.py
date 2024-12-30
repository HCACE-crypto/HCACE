import os

os.environ['OMP_NUM_THREADS'] = '1'
import numpy as np

print(np.__file__)

arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr)


print("sum:", arr.sum())
print("mean:", arr.mean())
print("max:", arr.max())
print("min:", arr.min())


arr_T = arr.T
print(arr_T)
