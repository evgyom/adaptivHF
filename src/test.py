import numpy
import numpy as np

a = np.array([[0, 1, 2], [3, 4, 5], [9, 7, 9]])
print(a)
b = np.array([[0.9, 0.8, 0.1], [0.1, 0.0, 0.4], [0.1, 0.0, 0.9]])

c = np.random.rand(b.shape[0], b.shape[1])

update_mask = (a<3) & (b>c)

a = a + update_mask
print(a)