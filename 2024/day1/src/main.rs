use anyhow::{Ok, Result};
use std::env;
use std::{cmp::Reverse, fs::read_to_string};

fn main() -> Result<()> {
    let filename: String = env::args().nth(1).unwrap_or(String::from("input.txt"));

    let numbers = read_to_string(filename)?
        .lines()
        .flat_map(|l| {
            l.split_whitespace()
                .map(|x| x.parse::<i32>().unwrap())
                .into_iter()
        })
        .collect::<Vec<_>>();

    let mut left: Vec<i32> = numbers.iter().cloned().step_by(2).collect::<Vec<_>>();
    left.sort_by_key(|x| Reverse(*x));
    let mut right: Vec<i32> = numbers
        .iter()
        .cloned()
        .skip(1)
        .step_by(2)
        .collect::<Vec<_>>();
    right.sort_by_key(|x| Reverse(*x));

    let distance_sum: i32 = left
        .into_iter()
        .zip(right.into_iter())
        .map(|(l, r)| (l - r).abs())
        .into_iter()
        .sum();

    println!("The total distance is {:?}", distance_sum);

    return Ok(());
}
