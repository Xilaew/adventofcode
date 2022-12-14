use std::io::{self, BufRead, Stdin};
//use std::collections::HashMap;

#[derive(Debug)]
struct Monkey {
    items: Vec<u64>,
    operation: Operation,
    operand_1: Operand,
    operand_2: Operand,
    div_test: u64,
    true_mokey_id: usize,
    false_monkey_id: usize,
    inspect_counter: u32,
}

#[derive(Debug)]
enum Operation {
    Add,
    Mult,
}

#[derive(Debug)]
enum Operand {
    Integer(u64),
    Old,
}

impl Monkey {
    fn inspect(self: &mut Self) -> Option<(u64, usize)> {
        if self.items.len() == 0 {
            return None;
        }
        let w_pre = self.items.remove(0);
        let op1 = match self.operand_1 {
            Operand::Old => w_pre,
            Operand::Integer(i) => i,
        };
        let op2 = match self.operand_2 {
            Operand::Old => w_pre,
            Operand::Integer(i) => i,
        };
        let w_inspect = match self.operation {
            Operation::Add => op1 + op2,
            Operation::Mult => op1 * op2,
        };
        let w_cooldown = w_inspect / 3;
        let next_monkey_index = match w_cooldown % self.div_test {
            0 => self.true_mokey_id,
            _ => self.false_monkey_id,
        };
        return Some((w_cooldown, next_monkey_index));
    }
}

fn main() -> io::Result<()> {
    //let mut user_input = String::new();
    let mut monkeys: Vec<Monkey> = Vec::<Monkey>::new();
    let stdin: Stdin = io::stdin();
    let mut lines = stdin.lock().lines();
    while let Some(_l) = lines.next() {
        let s2 = lines.next().unwrap().unwrap();
        let mut items = Vec::<u64>::new();
        for s in s2.split(':').nth(1).unwrap().split(',') {
            let i: u64 = s.trim().parse().unwrap();
            items.push(i);
        }
        let s3 = lines.next().unwrap().unwrap();
        let mut s3_it = s3.split('=').nth(1).unwrap().trim().split(' ');
        let operand_1 = match s3_it.next() {
            Some("old") => Operand::Old,
            Some(i) => Operand::Integer(i.trim().parse().unwrap()),
            None => panic!("hier fliegt gleich alles in die Luft"),
        };
        let operation = match s3_it.next() {
            Some("+") => Operation::Add,
            Some("*") => Operation::Mult,
            Some(_) => panic!("hier fliegt gleich alles in die Luft"),
            None => panic!("hier fliegt gleich alles in die Luft"),
        };
        let operand_2 = match s3_it.next() {
            Some("old") => Operand::Old,
            Some(i) => Operand::Integer(i.trim().parse().unwrap()),
            None => panic!("hier fliegt gleich alles in die Luft"),
        };
        let div_test: u64 = lines.next().unwrap().unwrap()[21..].parse().unwrap();
        let true_monkey_id: usize = lines.next().unwrap().unwrap()[29..].parse().unwrap();
        let false_monkey_id: usize = lines.next().unwrap().unwrap()[30..].parse().unwrap();
        lines.next();
        let m: Monkey = Monkey {
            items: items,
            operation: operation,
            operand_1: operand_1,
            operand_2: operand_2,
            div_test: div_test,
            true_mokey_id: true_monkey_id,
            false_monkey_id: false_monkey_id,
            inspect_counter: 0,
        };
        monkeys.push(m);
    }
    println!("{:?},", monkeys);
    let rounds = 20;
    for _r in 0..rounds {
        for i in 0..monkeys.len() {
            while let Some((val, m_id)) = monkeys[i].inspect() {
                println!("{:?}->{:?} : {:?}", i, m_id, val);
                monkeys[i].inspect_counter += 1;
                monkeys[m_id].items.push(val);
            }
        }
    };
    monkeys.sort_by(|a,b| a.inspect_counter.cmp(&b.inspect_counter));

    println!("{:?}",monkeys[monkeys.len()-1]);
    println!("{:?}",monkeys[monkeys.len()-2]);
    let monkey_bussiness = monkeys[monkeys.len()-1].inspect_counter * monkeys[monkeys.len()-2].inspect_counter;
    println!("monkey business = {}",monkey_bussiness);
    Ok(())
}
