use anyhow::{Ok, Result};
use std::collections::HashMap;
use std::env;
use std::{cmp::Reverse, fs::read_to_string};

fn calculate_total_distance(left: &[i32], right: &[i32]) -> i32 {
    return left
        .into_iter()
        .zip(right.into_iter())
        .map(|(l, r)| (l - r).abs())
        .into_iter()
        .sum();
}

fn calculate_similarity_score(left: &[i32], right: &[i32]) -> i32 {
    let mut counter: HashMap<i32, i32> = HashMap::new();
    right.iter().for_each(|x| {
        counter
            .entry(*x)
            .and_modify(|count| *count += 1)
            .or_insert(1);
    });
    return left
        .iter()
        .map(|x| x * counter.get(x).copied().unwrap_or(0))
        .sum();
}

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

    let distance_sum = calculate_total_distance(&left, &right);
    println!("The total distance is {:?}", distance_sum);

    let similarity_score = calculate_similarity_score(&left, &right);
    println!("The similarity score is {:?}", similarity_score);

    return Ok(());
}
