from util import readlines

from .day21common import complexity

if __name__ == "__main__":
    print(sum(complexity(code, 25) for code in readlines()))
