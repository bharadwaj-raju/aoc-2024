from ..util import *

print(
    sum(
        abs(l - r)
        for (l, r) in zip(
            *(
                sorted(lst)
                for lst in zip(*[map(int, line.split()) for line in readlines()])
            )
        )
    )
)
