from util import *
from collections import Counter

left, right = zip(*[map(int, line.split()) for line in readlines()])

left, right = (Counter(lst) for lst in zip(*[map(int, line.split()) for line in readlines()]))

print(sum(l * left[l] * right[l] for l in left))
