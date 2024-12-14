import gzip

from util import vec2, readlines


def parse_line(line: str) -> tuple[vec2, vec2]:
    p, v = line.strip().split()
    p = vec2(*map(int, p.split("=")[-1].split(",")))
    v = vec2(*map(int, v.split("=")[-1].split(",")))
    return p, v


robots = [parse_line(line) for line in readlines()]

BOUNDS = (11, 7) if len(robots) < 30 else (101, 103)


def move(pos: vec2, vel: vec2) -> vec2:
    new_pos = pos + vel
    return vec2(new_pos.x % BOUNDS[0], new_pos.y % BOUNDS[1])


def make_grid(robots: list[vec2]) -> str:
    grid: list[list[str]] = []
    for y in range(BOUNDS[1]):
        row = [" "] * BOUNDS[0]
        grid.append(row)
    for pos in robots:
        grid[pos.y][pos.x] = "#"
    return "\n".join("".join(row) for row in grid)


frames = []
frame_compressed_lengths = [0] * 10_000
seconds = 0
for i in range(10_000):
    frame_compressed_lengths[i] = len(gzip.compress(bytearray([pos.x for pos, _ in robots]))) + len(
        gzip.compress(bytearray([pos.y for pos, _ in robots]))
    )
    frames.append([pos for pos, _ in robots])
    robots = [(move(pos, vel), vel) for pos, vel in robots]
    seconds += 1

# import matplotlib.pyplot as plt

# plt.plot(range(10_000), frame_compressed_lengths)
# plt.show()

tree_frame_num = min(enumerate(frame_compressed_lengths), key=lambda x: x[1])[0]

print(make_grid(frames[tree_frame_num]))
print(tree_frame_num)
