import numpy as np
import math

a = np.asarray([1, 2, 3, 4])
y1 = lambda x: math.log2(x)
y = lambda x: x * 2
print(y(a), y1(a))