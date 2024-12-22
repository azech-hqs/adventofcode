use std::{collections::HashMap, fs::read_to_string};

#[derive(Debug)]
enum ReadDataError {
    ReadFileError,
    InvalidRule,
    ParseError,
    MapError,
}

fn read_data() -> Result<(Rules, Vec<Vec<i32>>), ReadDataError> {
    let default_text = String::from(
        "47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47",
    );
    let raw_text = read_to_string("./input.txt").unwrap_or(default_text);
    let (rules, numbers) = raw_text
        .split_once("\n\n")
        .ok_or(ReadDataError::ReadFileError)?;

    let mut rules_map: HashMap<i32, Vec<i32>> = HashMap::new();
    for line in rules.lines() {
        let (a, b) = line.split_once('|').ok_or(ReadDataError::InvalidRule)?;
        let a = a.parse::<i32>().map_err(|_| ReadDataError::ParseError)?;
        let b = b.parse::<i32>().map_err(|_| ReadDataError::ParseError)?;

        if rules_map.contains_key(&a) {
            rules_map
                .get_mut(&a)
                .ok_or(ReadDataError::MapError)?
                .push(b);
        } else {
            rules_map.insert(a, vec![b]);
        }
    }

    let numbers: Vec<_> = numbers
        .lines()
        .map(|line| {
            let result = line
                .split(',')
                .into_iter()
                .filter_map(|n| n.parse::<i32>().ok())
                .collect::<Vec<i32>>();
            return result;
        })
        .collect();

    return Ok((Rules { data: rules_map }, numbers));
}

struct Rules {
    data: HashMap<i32, Vec<i32>>,
}

impl Rules {
    fn is_ordered(&self, a: &i32, b: &i32) -> bool {
        return self.data.get(a).map(|v| v.contains(b)).unwrap_or(false);
    }

    fn quick_sort(&self, v: &mut Vec<i32>) -> Vec<i32> {
        self._qs(v, 0, v.len() - 1);
        println!("sorted array: {:?}", &v);
        return v.to_vec();
    }

    fn _qs(&self, v: &mut Vec<i32>, left_index: usize, right_index: usize) -> Option<()> {
        if right_index as i32 - left_index as i32 <= 0 {
            return Some(());
        }
        let pivot_index = self._partition_array(v, left_index, right_index)?;
        self._qs(v, left_index, pivot_index.saturating_sub(1));
        self._qs(v, pivot_index + 1, right_index);
        return Some(());
    }

    fn _partition_array(
        &self,
        v: &mut Vec<i32>,
        left_index: usize,
        right_index: usize,
    ) -> Option<usize> {
        let pivot_index = right_index;
        let pivot = v.get(pivot_index)?.clone();
        let mut right_ptr = right_index.saturating_sub(1);
        let mut left_ptr = left_index;

        loop {
            while self.is_ordered(&v[left_ptr], &pivot) {
                left_ptr += 1;
            }

            while self.is_ordered(&pivot, &v[right_ptr]) && right_ptr != 0 {
                right_ptr = right_ptr.saturating_sub(1);
            }

            if left_ptr >= right_ptr {
                break;
            } else {
                v.swap(left_ptr, right_ptr);
                left_ptr += 1;
            }
        }

        v.swap(left_ptr, pivot_index);
        return Some(left_ptr);
    }
}

fn main() -> Result<(), ReadDataError> {
    /*
     * General idea:
     *  - always compare pairs of numbers
     *  - possible to compare tuple of i32?
     *  - comparison function fn compare(a, b) -> bool
     */

    let (rules, arrays) = read_data()?;

    let mut middle: i32 = 0;
    let mut middle_unsorted: i32 = 0;
    for array in &arrays[..] {
        let is_ordered = array.windows(2).all(|w| rules.is_ordered(&w[0], &w[1]));
        if is_ordered {
            let i = array.len() / 2;
            middle += array[i];
        } else {
            let mut sorted = array.clone();
            rules.quick_sort(&mut sorted);
            let i = sorted.len() / 2;
            middle_unsorted += sorted[i];
        }
    }

    println!("there are {:?} rules", rules.data.len());
    println!("there are {:?} arrays", arrays.len());
    println!("the sum of middle values is {:?}", &middle);
    println!(
        "the sum of middle values (unsorted) is {:?}",
        &middle_unsorted
    );

    return Ok(());
}
