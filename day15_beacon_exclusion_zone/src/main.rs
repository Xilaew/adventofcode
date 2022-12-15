use range_set::RangeSet;
use std::io::{self, BufRead};
use std::ops::RangeInclusive;
//use std::collections::HashMap;

#[derive(Debug)]
struct Beacon {
    x: i64,
    y: i64,
}

#[derive(Debug)]
struct Sensor {
    x: i64,
    y: i64,
    beacon: Beacon,
}

fn dist(s: &Sensor) -> i64 {
    return (s.x - s.beacon.x).abs() + (s.y - s.beacon.y).abs();
}

fn parse_input(reader: &mut dyn BufRead) -> Vec<Sensor> {
    let mut lines = reader.lines();
    let mut sensors = Vec::<Sensor>::new();
    while let Some(l) = lines.next() {
        let s = l.unwrap();
        let mut it1 = s.split(':');
        let mut its = it1.next().unwrap().split(',');
        let mut itb = it1.next().unwrap().split(',');
        let sx = its.next().unwrap().split('=').nth(1).unwrap();
        let sy = its.next().unwrap().split('=').nth(1).unwrap();
        let bx = itb.next().unwrap().split('=').nth(1).unwrap();
        let by = itb.next().unwrap().split('=').nth(1).unwrap();
        let b: Beacon = Beacon {
            x: bx.parse().unwrap(),
            y: by.parse().unwrap(),
        };
        let sensor: Sensor = Sensor {
            x: sx.parse().unwrap(),
            y: sy.parse().unwrap(),
            beacon: b,
        };
        // println!("{:?}: {}",&sensor,dist(&sensor));
        sensors.push(sensor);
    }
    return sensors;
}

fn part1(sensors: &Vec<Sensor>, const_y: i64) -> i64 {
    let mut rset = RangeSet::<[RangeInclusive<i64>; 10]>::new();
    for sen in sensors {
        let dist_beacon = dist(&sen);
        let dist_line = (sen.y - const_y).abs();
        if dist_line <= dist_beacon {
            let u = sen.x + dist_beacon - dist_line;
            let l = sen.x - dist_beacon + dist_line;
            rset.insert_range(l..=u);
            if sen.beacon.y == const_y {
                // println!("beacon at {:?}",(sen.beacon.x,sen.beacon.y));
                rset.remove(sen.beacon.x);
            }
            // println!("Sensor at ({},{}) with distance {}, covers [{},{}]",sen.x,sen.y,dist_beacon,l,u);
        }
    }
    return rset.iter().count().try_into().unwrap();
}

fn part2(sensors: &Vec<Sensor>, range: &RangeInclusive<i64>) -> i64 {
    let mut result :i64 = 0;
    let target_range_set = RangeSet::<[RangeInclusive<i64>; 1]>::from((*range).clone());
    for const_y in (*range).clone() {
        let mut rset = RangeSet::<[RangeInclusive<i64>; 1]>::new();
        for sen in sensors {
            let dist_beacon = dist(&sen);
            let dist_line = (sen.y - const_y).abs();
            if dist_line <= dist_beacon {
                let u = sen.x + dist_beacon - dist_line;
                let l = sen.x - dist_beacon + dist_line;
                rset.insert_range(l..=u);
            }
        }
        let cutoutrangeset = rset.remove_range(range.clone()).unwrap();
        if cutoutrangeset != target_range_set {
            println!("{}: {:?}",const_y,cutoutrangeset);
            let vec = rset.into_smallvec();
            let r1 = vec.get(0).unwrap().end()+1;
            result = (r1 * 4000000) + const_y;
        } else if const_y % 500000 == 0 {
            println!("{}",const_y);
        }
    }
    return result;
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let sensors = parse_input(&mut stdin.lock());
    let res1 = part1(&sensors, 2000000);
    let res2 = part2(&sensors, &(0..=4000000));
    println!("part1: {}, part2: {}",res1,res2);
    Ok(())
}
