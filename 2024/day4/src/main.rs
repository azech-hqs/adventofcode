use std::fs::read_to_string;

enum Direction {
    North,
    NorthEast,
    East,
    SouthEast,
    South,
    SouthWest,
    West,
    NorthWest,
}

struct Position {
    x: i32,
    y: i32,
}

impl Position {
    fn step_one(&self, direction: &Direction) -> Self {
        match direction {
            Direction::North => {
                return Position {
                    y: self.y - 1,
                    ..*self
                }
            }
            Direction::NorthEast => {
                return Position {
                    x: self.x + 1,
                    y: self.y - 1,
                }
            }
            Direction::East => {
                return Position {
                    x: self.x + 1,
                    ..*self
                }
            }
            Direction::SouthEast => {
                return Position {
                    x: self.x + 1,
                    y: self.y + 1,
                }
            }
            Direction::South => {
                return Position {
                    y: self.y + 1,
                    ..*self
                }
            }
            Direction::SouthWest => {
                return Position {
                    x: self.x - 1,
                    y: self.y + 1,
                }
            }
            Direction::West => {
                return Position {
                    x: self.x - 1,
                    ..*self
                }
            }
            Direction::NorthWest => {
                return Position {
                    x: self.x - 1,
                    y: self.y - 1,
                }
            }
        }
    }
}

struct WordMatrix {
    data: Vec<String>,
}

impl WordMatrix {
    fn x_max(&self) -> usize {
        return self.data.get(0).unwrap_or(&String::from("")).len();
    }

    fn y_max(&self) -> usize {
        return self.data.len();
    }

    fn get(&self, pos: &Position) -> Option<char> {
        let x0: usize = pos.x.try_into().unwrap_or(self.x_max());
        let y0: usize = pos.y.try_into().unwrap_or(self.y_max());
        if pos.x < 0 || x0 >= self.x_max() || pos.y < 0 || y0 >= self.y_max() {
            return None;
        }
        return self.data[y0].chars().nth(x0);
    }

    /*
     * 1. Start only from X
     * 2. Walk 3 steps in all directions (if possible -> boundaries!).
     * 3. Add +1 if walk yields XMAS.
     * 4. (not sure) store which X's have been visited yet (path-dependent).
     */
    fn evaluate_path(&self, start: &Position, direction: Direction) -> i32 {
        let is_x = match self.get(start) {
            Some(x) => x.eq(&'X'),
            None => return 0,
        };
        let mut next_pos = start.step_one(&direction);
        let is_m = match self.get(&next_pos) {
            Some(x) => x.eq(&'M'),
            None => return 0,
        };
        next_pos = next_pos.step_one(&direction);
        let is_a = match self.get(&next_pos) {
            Some(x) => x.eq(&'A'),
            None => return 0,
        };
        next_pos = next_pos.step_one(&direction);
        let is_s = match self.get(&next_pos) {
            Some(x) => x.eq(&'S'),
            None => return 0,
        };

        return if is_x && is_m && is_a && is_s { 1 } else { 0 };
    }

    fn count_xmas(&self) -> i32 {
        let mut count = 0;
        for y in 0usize..self.y_max() {
            for x in 0..self.x_max() {
                let pos = Position {
                    x: x as i32,
                    y: y as i32,
                };
                count += self.evaluate_path(&pos, Direction::North);
                count += self.evaluate_path(&pos, Direction::NorthEast);
                count += self.evaluate_path(&pos, Direction::East);
                count += self.evaluate_path(&pos, Direction::SouthEast);
                count += self.evaluate_path(&pos, Direction::South);
                count += self.evaluate_path(&pos, Direction::SouthWest);
                count += self.evaluate_path(&pos, Direction::West);
                count += self.evaluate_path(&pos, Direction::NorthWest);
                println!("count is {:?}", &count);
            }
        }
        return count;
    }
}

fn read_word_matrix() -> WordMatrix {
    let default = String::from(
        "MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX",
    );
    let raw_text = read_to_string("input.txt").unwrap_or(default);
    return WordMatrix {
        data: raw_text.lines().map(|l| l.to_owned()).collect(),
    };
}

fn main() {
    let mat = read_word_matrix();
    let count = mat.count_xmas();

    println!("The count is {:?}", count);
}
