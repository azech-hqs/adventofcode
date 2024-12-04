use anyhow::{Ok, Result};
use std::{env, fs::read_to_string};

struct Report {
    levels: Vec<i32>,
}

impl Report {
    fn is_safe(&self, levels: &[i32]) -> i32 {
        let diffvec: Vec<i32> = levels
            .iter()
            .zip(levels.iter().skip(1))
            .map(|(a, b)| b - a)
            .collect();

        if diffvec.contains(&0) {
            return 0;
        } else if !(diffvec.iter().sum::<i32>().abs()
            == diffvec.iter().map(|x| x.abs()).sum::<i32>())
        {
            return 0;
        } else if diffvec.iter().any(|&x| x.abs() > 3 || x.abs() < 1) {
            return 0;
        }
        return 1;
    }

    fn is_safe_as_num(&self) -> i32 {
        return self.is_safe(&self.levels);
    }

    fn is_safe_tolerate(&self) -> i32 {
        let safe_num = self.is_safe_as_num();

        if safe_num == 1 {
            return safe_num;
        }

        for i in 0..self.levels.len() {
            let mut tmp_levels = self.levels.clone();
            tmp_levels.remove(i);
            if self.is_safe(&tmp_levels) == 1 {
                return 1;
            }
        }
        return 0;
    }
}

fn main() -> Result<()> {
    let filename: String = env::args().nth(1).unwrap_or(String::from("input.txt"));

    let safe_sum: i32 = read_to_string(filename)?
        .lines()
        .map(|l| Report {
            levels: l
                .split_whitespace()
                .map(|x| x.parse::<i32>().unwrap())
                .into_iter()
                .collect::<Vec<i32>>(),
        })
        .map(|r| r.is_safe_tolerate())
        .sum();
    println!("There are {:?} safe reports.", safe_sum);

    Ok(())
}
