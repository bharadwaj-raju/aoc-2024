use std::{
    cmp::Ordering,
    collections::{BinaryHeap, HashMap},
    ops::{Add, Sub},
};

use itertools::Itertools;

#[derive(Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
struct Vec2 {
    x: i64,
    y: i64,
}

const CARDINALS: [Vec2; 4] = [
    Vec2 { x: 1, y: 0 },
    Vec2 { x: -1, y: 0 },
    Vec2 { x: 0, y: 1 },
    Vec2 { x: 0, y: -1 },
];

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

impl Vec2 {
    fn cardinal_neighbors(self) -> [Vec2; 4] {
        [
            self + CARDINALS[0],
            self + CARDINALS[1],
            self + CARDINALS[2],
            self + CARDINALS[3],
        ]
    }

    fn manhattan(self, other: Vec2) -> u64 {
        self.x.abs_diff(other.x) + self.y.abs_diff(other.y)
    }
}

type Grid<'a> = &'a [Vec<char>];

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = args.get(1).expect("arg");
    let text = std::fs::read_to_string(filename).unwrap();
    let grid = text
        .lines()
        .map(|line| line.chars().collect_vec())
        .collect_vec();
    let (start, end) = process_input(&grid);
    let (_, normal_path) = a_star(&grid, start, end).expect("path exists");

    println!("part 1 = {}", find_cheats(&normal_path, 2, 100));
    println!("part 2 = {}", find_cheats(&normal_path, 20, 100));
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

#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    position: Vec2,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other
            .cost
            .cmp(&self.cost)
            .then_with(|| self.position.cmp(&other.position))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn process_input(grid: Grid) -> (Vec2, Vec2) {
    let mut start = Vec2 { x: 0, y: 0 };
    let mut end = Vec2 { x: 0, y: 0 };
    for (y, row) in grid.iter().enumerate() {
        for (x, &cell) in row.iter().enumerate() {
            if cell == 'S' {
                start = Vec2 {
                    x: x.try_into().unwrap(),
                    y: y.try_into().unwrap(),
                };
            } else if cell == 'E' {
                end = Vec2 {
                    x: x.try_into().unwrap(),
                    y: y.try_into().unwrap(),
                };
            }
        }
    }
    (start, end)
}

fn a_star(grid: Grid, start: Vec2, end: Vec2) -> Option<(usize, Vec<Vec2>)> {
    let mut frontier = BinaryHeap::new();
    frontier.push(State {
        cost: 0,
        position: start,
    });
    let mut came_from = HashMap::new();
    let mut cost = HashMap::new();
    came_from.insert(start, None);
    cost.insert(start, 0);

    while !frontier.is_empty() {
        let current = frontier.pop().unwrap().position;
        if current == end {
            break;
        }
        for next in current.cardinal_neighbors() {
            if grid_get(grid, next, '#') == '#' {
                continue;
            }
            let new_cost = cost[&current] + 1;
            if !cost.contains_key(&next) || new_cost < cost[&next] {
                cost.insert(next, new_cost);
                frontier.push(State {
                    cost: new_cost + next.manhattan(end) as usize,
                    position: next,
                });
                came_from.insert(next, Some(current));
            }
        }
    }

    let mut path = vec![end];
    while *path.last().unwrap() != start {
        let Some(Some(prev)) = came_from.get(path.last().unwrap()) else {
            return None;
        };
        path.push(*prev);
    }

    Some((cost[&end], path))
}

fn find_cheats(path: &[Vec2], max_cheat_time: usize, min_savings: usize) -> usize {
    let mut viable = 0;
    for (start_time, cheat_start) in path.iter().enumerate() {
        if start_time > path.len() - min_savings {
            break;
        }
        for (normal_end_time, cheat_end) in path.iter().enumerate().skip(start_time + min_savings) {
            let cheat_dist = cheat_start.manhattan(*cheat_end) as usize;
            let cheat_end_time = start_time + cheat_dist;
            let savings = normal_end_time - cheat_end_time;
            if cheat_dist <= max_cheat_time && savings >= min_savings {
                viable += 1;
            }
        }
    }
    viable
}
