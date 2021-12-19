import operator
from dataclasses import dataclass
from functools import reduce

@dataclass
class Packet:
    ''' Mutable packet data definition to recursively capture key problem information. '''
    version: int
    value: int = None
    end: int = None

def packet_data(bits : str, start_idx : int) -> Packet:
    ''' Summarize data for a packet starting at the given index in a bit stream. '''
    packet_summary = Packet(version=int(bits[start_idx:start_idx+3], 2))
    p_type_id = int(bits[start_idx+3:start_idx+6], 2)
    
    # Packets with type ID 4 represent a literal value
    if p_type_id == 4:
        packet_summary.end = start_idx + 6
        bit_str = ''
        while bits[packet_summary.end] == '1':
            bit_str += bits[packet_summary.end+1:packet_summary.end+5]
            packet_summary.end += 5

        bit_str += bits[packet_summary.end+1:packet_summary.end+5]
        packet_summary.value = int(bit_str, 2)
        packet_summary.end += 5
        return packet_summary

    subpacket_vals = []
    l_type_id = int(bits[start_idx + 6], 2)
    p_start = start_idx + 7

    # the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet
    if l_type_id == 0:
        bit_length = int(bits[p_start:p_start+15], 2)
        packet_summary.end = p_start + 15
        while packet_summary.end < p_start + 15 + bit_length:
            parsed_packet = packet_data(bits, packet_summary.end)
            subpacket_vals.append(parsed_packet.value)
            packet_summary.version += parsed_packet.version
            packet_summary.end = parsed_packet.end

    # the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet
    else:
        num_subpackets = int(bits[p_start:p_start+11], 2)
        packet_summary.end = p_start + 11
        for _ in range(num_subpackets):
            parsed_packet = packet_data(bits, packet_summary.end)
            subpacket_vals.append(parsed_packet.value)
            packet_summary.version += parsed_packet.version
            packet_summary.end = parsed_packet.end

    if p_type_id == 0:
        packet_summary.value = sum(subpacket_vals)
    elif p_type_id == 1:
        packet_summary.value = reduce(operator.mul, subpacket_vals, 1)
    elif p_type_id == 2:
        packet_summary.value = min(subpacket_vals)
    elif p_type_id == 3:
        packet_summary.value = max(subpacket_vals)
    elif p_type_id == 5:
        packet_summary.value = int(subpacket_vals[0] > subpacket_vals[1])
    elif p_type_id == 6:
        packet_summary.value = int(subpacket_vals[0] < subpacket_vals[1])
    else:
        packet_summary.value = int(subpacket_vals[0] == subpacket_vals[1])

    return packet_summary

def make_bits_from(transmission : str) -> str:
    ''' Convert hex string into a binary string. '''
    return ''.join('{0:b}'.format(int(t, 16)).zfill(4) for t in transmission)

def part1(transmission : str) -> int:
    ''' Solve part 1 '''
    return packet_data(make_bits_from(transmission), 0).version

def part2(transmission : str) -> int:
    ''' Solve part 2 '''
    return packet_data(make_bits_from(transmission), 0).value

with open('input/day16.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    print(part1(lines[0]))
    print(part2(lines[0]))

## Test cases
assert part1('8A004A801A8002F478') == 16
assert part1('620080001611562C8802118E34') == 12
assert part1('C0015000016115A2E0802F182340') == 23
assert part1('A0016C880162017C3686B18A3D4780') == 31
assert part2('C200B40A82') == 3
assert part2('04005AC33890') == 54
assert part2('880086C3E88112') == 7
assert part2('CE00C43D881120') == 9
assert part2('D8005AC2A8F0') == 1
assert part2('F600BC2D8F') == 0
assert part2('9C005AC2F8F0') == 0
assert part2('9C0141080250320F1802104A08') == 1