use regex::Regex;
use std::{env, fs::read_to_string, str::FromStr};

struct Multiply {
    a: i32,
    b: i32,
}

impl Multiply {
    fn run(&self) -> i32 {
        return self.a * self.b;
    }
}
#[derive(Debug, PartialEq, Eq)]
struct ParseMultiplyError;

impl FromStr for Multiply {
    type Err = ParseMultiplyError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let re = Regex::new(r"mul\((\d+),(\d+)\)").map_err(|_| ParseMultiplyError)?;
        let caps = re.captures(s).unwrap();
        return Ok(Multiply {
            a: caps[1].parse::<i32>().map_err(|_| ParseMultiplyError)?,
            b: caps[2].parse::<i32>().map_err(|_| ParseMultiplyError)?,
        });
    }
}

fn read_content() -> Result<String, std::io::Error> {
    let filename: String = env::args().nth(1).unwrap_or(String::from("simple.txt"));
    return read_to_string(filename);
}

fn evaluate_multiply(content: &str) -> i32 {
    let re = Regex::new(r"mul\(\d+,\d+\)").unwrap();
    let multiplied: i32 = re
        .find_iter(&content)
        .map(|x| Multiply::from_str(x.as_str()).unwrap().run())
        .sum();
    println!("The total sum is {:?}", &multiplied);
    return multiplied;
}

fn evaluate_multiply_range(content: &str) -> i32 {
    let re = Regex::new(r"mul\(\d+,\d+\)|do\(\)|don't\(\)").unwrap();
    let mut active: bool = true;
    let mut sum: i32 = 0;
    for cmd in re.find_iter(content) {
        let command = cmd.as_str();
        if command.starts_with("don") {
            active = false;
        } else if command.starts_with("do") {
            active = true;
        };

        if command.starts_with("mul") && active {
            sum += Multiply::from_str(command).unwrap().run();
        }
    }
    println!("The total sum of active commands is {:?}", &sum);
    return sum;
}

fn main() {
    let content = read_content().unwrap_or(String::from(
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
    ));
    evaluate_multiply(&content);
    evaluate_multiply_range(&content);
}
