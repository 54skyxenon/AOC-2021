from typing import List, Dict

## Map from number of segments to the decoded digit (as a string)
UNIQUE_SEGMENTS = {2: '1', 4: '4', 3 : '7', 7 : '8'}

def str_subset(a : str, b : str) -> bool:
    ''' Is a's character set of a subset of b's? '''
    return set(a).issubset(set(b))

def add_mappings(encode : Dict[str, str], decode : Dict[str, str], cipher : str, plain : str) -> None:
    ''' Adds mapping from plaintext to ciphertext and vice versa in encoding/decoding caches. '''
    encode[plain] = cipher
    decode[cipher] = plain

def part1(entries : List[str]) -> int:
    ''' Solve part 1 '''
    ans = 0

    for entry in entries:
        encoded_output = entry.split('|')[1]
        for encoded_digit in encoded_output.split():
            ans += len(encoded_digit) in UNIQUE_SEGMENTS

    return ans

def part2(entries : List[int]) -> int:
    ''' Solve part 2 '''
    ans = 0

    for entry in entries:
        encoded_signals, encoded_output = entry.split('|')
        encoded_signals = [''.join(sorted(signal)) for signal in encoded_signals.split()]
        encoded_output = [''.join(sorted(output)) for output in encoded_output.split()]
        encode, decode = dict(), dict()

        # decode the uniques first
        for encoded_signal in encoded_signals:
            if len(encoded_signal) in UNIQUE_SEGMENTS:
                add_mappings(encode, decode, encoded_signal, UNIQUE_SEGMENTS[len(encoded_signal)])

            # missing: [0, 2, 3, 5, 6, 9]

        # focus on 6 segment digits
        for encoded_signal in encoded_signals:
            if len(encoded_signal) == 6:
                # try to decode '9': it uses exactly 2 more segments than '4'
                if str_subset(encode['4'], encoded_signal):
                    add_mappings(encode, decode, encoded_signal, '9')
                # try to decode '0': it uses exactly 3 more segments than '7'
                elif str_subset(encode['7'], encoded_signal):
                    add_mappings(encode, decode, encoded_signal, '0')
                # '6' does not fulfill the above criterion and is the last candidate
                else:
                    add_mappings(encode, decode, encoded_signal, '6')

            # missing: [2, 3, 5]

        # focus on 5 segment digits
        for encoded_signal in encoded_signals:
            if len(encoded_signal) == 5:
                # try to decode '3': it uses exactly 3 more segments than '1'
                if str_subset(encode['1'], encoded_signal):
                    add_mappings(encode, decode, encoded_signal, '3')
                # try to decode '5': it uses exactly 1 less character than '9'
                elif str_subset(encoded_signal, encode['9']):
                    add_mappings(encode, decode, encoded_signal, '5')
                # '2' does not fulfill the above criterion and is the last candidate
                else:
                    add_mappings(encode, decode, encoded_signal, '2')

            # we're done!

        ans += int(''.join(decode[digit] for digit in encoded_output))

    return ans

with open('day8.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    print(part1(lines))
    print(part2(lines))