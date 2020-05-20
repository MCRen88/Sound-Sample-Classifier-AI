import numpy as np

a = np.array([1, 2, 3, 4, 5])

a = np.append(a, [a[-1]] * 5, 0)

print(a)
