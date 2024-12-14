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


for _ in range(100):
    robots = [(move(pos, vel), vel) for pos, vel in robots]

q1 = q2 = q3 = q4 = 0

mid_x = BOUNDS[0] // 2
mid_y = BOUNDS[1] // 2

for robot in robots:
    pos, _ = robot
    if pos.x < mid_x and pos.y < mid_y:
        q1 += 1
    elif pos.x > mid_x and pos.y < mid_y:
        q2 += 1
    elif pos.x > mid_x and pos.y > mid_y:
        q3 += 1
    elif pos.x < mid_x and pos.y > mid_y:
        q4 += 1

print(BOUNDS)
print(q1, q2, q3, q4)
print(q1 * q2 * q3 * q4)
