from typing import List, Dict, Tuple
from collections import Counter
from copy import deepcopy

StrIntCounter = Dict[str, int]
PairRules = Dict[str, str]

def build_rules(rules : List[str]) -> PairRules:
    ''' Represent polymerization rules as a dictionary mapping pair insertion rules to results. '''
    rule_dict = dict()
    for rule in rules:
        pair, result = rule.split(' -> ')
        rule_dict[pair] = result
    
    return rule_dict

def step(state : StrIntCounter, element_count : StrIntCounter, rules : PairRules) -> Tuple[StrIntCounter, StrIntCounter]:
    ''' Count number of pairings and elements after one step. '''
    new_state = Counter()
    new_element_count = deepcopy(element_count)

    for pair in state:
        middle = rules[pair]
        new_state[pair[0] + middle] += state[pair]
        new_state[middle + pair[1]] += state[pair]
        new_element_count[middle] += state[pair]

    return new_state, new_element_count

def solve(template : str, rules : PairRules, num_steps : int) -> int:
    ''' Simulate the given number of steps to get the answer. '''
    state = Counter(template[i:i+2] for i in range(len(template) - 1))
    element_count = Counter(template)

    for _ in range(num_steps):
        state, element_count = step(state, element_count, rules)

    counts = element_count.most_common()
    return counts[0][1] - counts[-1][1]

def part1(template : str, rules : PairRules) -> int:
    ''' Solve part 1 '''
    return solve(template, rules, 10)
    

def part2(template : str, rules : PairRules) -> int:
    ''' Solve part 2 '''
    return solve(template, rules, 40)

with open('day14.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    template = lines[0]
    rules = build_rules(lines[2:])
    print(part1(template, rules))
    print(part2(template, rules))