use std::{
    collections::{HashMap, HashSet},
    ops::{Add, Sub},
};

use itertools::Itertools;

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
struct Vec2 {
    x: i64,
    y: i64,
}

impl Add for Vec2 {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Self {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
        }
    }
}

impl Sub for Vec2 {
    type Output = Self;

    fn sub(self, rhs: Self) -> Self::Output {
        Self {
            x: self.x - rhs.x,
            y: self.y - rhs.y,
        }
    }
}

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
enum Direction {
    Up,
    Down,
    Right,
    Left,
}

impl Direction {
    fn turn_right(self) -> Self {
        match self {
            Direction::Up => Direction::Right,
            Direction::Down => Direction::Left,
            Direction::Right => Direction::Down,
            Direction::Left => Direction::Up,
        }
    }
}

impl From<Direction> for Vec2 {
    fn from(value: Direction) -> Self {
        match value {
            Direction::Up => Vec2 { x: 0, y: -1 },
            Direction::Down => Vec2 { x: 0, y: 1 },
            Direction::Right => Vec2 { x: 1, y: 0 },
            Direction::Left => Vec2 { x: -1, y: 0 },
        }
    }
}

type ObstacleSkipList = HashMap<usize, Vec<usize>>;
type Grid<'a> = &'a [Vec<char>];

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = args.get(1).expect("arg");
    let text = std::fs::read_to_string(filename).unwrap();
    let grid = text
        .lines()
        .map(|line| line.chars().collect_vec())
        .collect_vec();
    let (mut obstacles_by_row, mut obstacles_by_col, guard) = process_input(&grid);
    println!("part 1 = {}", part1(&grid, guard));
    println!(
        "part 2 = {}",
        part2(&grid, &mut obstacles_by_row, &mut obstacles_by_col, guard)
    );
}

fn grid_get(grid: Grid, pos: Vec2, default: char) -> char {
    let Ok(row): Result<usize, _> = pos.y.try_into() else {
        return default;
    };
    let Ok(col): Result<usize, _> = pos.x.try_into() else {
        return default;
    };
    *grid.get(row).and_then(|r| r.get(col)).unwrap_or(&default)
}

fn process_input(grid: Grid) -> (ObstacleSkipList, ObstacleSkipList, Vec2) {
    let mut guard_pos = Vec2 { x: -1, y: -1 };
    let mut obstacles_by_row: ObstacleSkipList = HashMap::new();
    let mut obstacles_by_col: ObstacleSkipList = HashMap::new();
    for (y, row) in grid.iter().enumerate() {
        for (x, &cell) in row.iter().enumerate() {
            if cell == '^' {
                guard_pos = Vec2 {
                    x: x as i64,
                    y: y as i64,
                };
            } else if cell == '#' {
                obstacles_by_row.entry(y).or_default().push(x);
                obstacles_by_col.entry(x).or_default().push(y);
            }
        }
    }
    (obstacles_by_row, obstacles_by_col, guard_pos)
}

fn walk(grid: Grid, guard: Vec2) -> Vec<Vec2> {
    let mut facing = Direction::Up;
    let mut path: Vec<Vec2> = Vec::new();
    path.push(guard);
    let mut guard = guard;
    loop {
        let in_front = grid_get(grid, guard + facing.into(), 'O');
        if in_front == 'O' {
            break;
        }
        if in_front == '#' {
            while grid_get(grid, guard + facing.into(), 'O') == '#' {
                facing = facing.turn_right();
            }
        }
        guard = guard + facing.into();
        path.push(guard);
    }
    path
}

fn part1(grid: Grid, guard: Vec2) -> usize {
    walk(grid, guard).iter().unique().count()
}

fn check_loop(
    grid: Grid,
    obstacles_by_row: &ObstacleSkipList,
    obstacles_by_col: &ObstacleSkipList,
    placed_obstacle: Vec2,
    guard: Vec2,
) -> bool {
    let mut facing = Direction::Up;
    let mut guard = guard;
    let mut seen: HashSet<(Vec2, Direction)> = HashSet::new();
    seen.insert((guard, facing));
    loop {
        let row = guard.y as usize;
        let col = guard.x as usize;
        guard = match facing {
            Direction::Up => {
                let Some(y) = obstacles_by_col
                    .get(&col)
                    .unwrap()
                    .iter()
                    .filter(|&&y| y < row)
                    .max()
                else {
                    break false;
                };
                Vec2 {
                    x: guard.x,
                    y: *y as i64,
                }
            }
            Direction::Down => {
                let Some(y) = obstacles_by_col
                    .get(&col)
                    .unwrap()
                    .iter()
                    .filter(|&&y| y > row)
                    .min()
                else {
                    break false;
                };
                Vec2 {
                    x: guard.x,
                    y: *y as i64,
                }
            }
            Direction::Right => {
                let Some(x) = obstacles_by_row
                    .get(&row)
                    .unwrap()
                    .iter()
                    .filter(|&&x| x > col)
                    .min()
                else {
                    break false;
                };
                Vec2 {
                    x: *x as i64,
                    y: guard.y,
                }
            }
            Direction::Left => {
                let Some(x) = obstacles_by_row
                    .get(&row)
                    .unwrap()
                    .iter()
                    .filter(|&&x| x < col)
                    .max()
                else {
                    break false;
                };
                Vec2 {
                    x: *x as i64,
                    y: guard.y,
                }
            }
        };
        let curr = grid_get(grid, guard, 'O');
        if curr == 'O' {
            break false;
        }
        if curr == '#' || guard == placed_obstacle {
            guard = guard - facing.into();
            let mut spot_turns = 0;
            while grid_get(grid, guard + facing.into(), 'O') == '#'
                || guard + facing.into() == placed_obstacle
            {
                facing = facing.turn_right();
                spot_turns += 1;
                if spot_turns == 4 {
                    return true;
                }
            }
        }
        if seen.contains(&(guard, facing)) {
            break true;
        }
        seen.insert((guard, facing));
    }
}

fn part2(
    grid: Grid,
    obstacles_by_row: &mut ObstacleSkipList,
    obstacles_by_col: &mut ObstacleSkipList,
    guard: Vec2,
) -> usize {
    let mut looping_obstacles: HashSet<Vec2> = HashSet::new();
    for would_step in walk(grid, guard).iter().skip(1).unique() {
        obstacles_by_col
            .entry(would_step.x.try_into().unwrap())
            .or_default()
            .push(would_step.y.try_into().unwrap());
        obstacles_by_row
            .entry(would_step.y.try_into().unwrap())
            .or_default()
            .push(would_step.x.try_into().unwrap());
        if check_loop(grid, obstacles_by_row, obstacles_by_col, *would_step, guard) {
            looping_obstacles.insert(*would_step);
        }
        obstacles_by_col
            .get_mut(&would_step.x.try_into().unwrap())
            .unwrap()
            .pop();
        obstacles_by_row
            .get_mut(&would_step.y.try_into().unwrap())
            .unwrap()
            .pop();
    }
    looping_obstacles.len()
}
