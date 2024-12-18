#!/usr/bin/env python3
from enum import IntEnum
import pprint

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='17-input.txt'
# INPUT_FILE='17a-example.txt'
# INPUT_FILE='17b-example.txt'

input_contents = get_file_contents(INPUT_FILE)


registers: list[int] = []
for line in input_contents[0]:
    line_split = line.split(': ')
    registers.append(int(line_split[1]))


program = [int(x) for x in input_contents[1][0].split(': ')[1].split(',')]


class OpCode(IntEnum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7

def get_combo_operand(val, cur_registers):
    match val:
        case 0 | 1 | 2 | 3:
            return val
        case 4:
            return cur_registers[0]
        case 5:
            return cur_registers[1]
        case 6:
            return cur_registers[2]
        case 7:
            raise ValueError()

def run(program, cur_registers):
    ip = 0
    out = []
    while ip < len(program):
        cur_op = program[ip]
        operand = program[ip+1]
        jump = False

        match cur_op:
            case OpCode.adv:
                cur_registers[0] >>= get_combo_operand(operand, cur_registers)
            case OpCode.bxl:
                cur_registers[1] ^= operand
            case OpCode.bst:
                cur_registers[1] = get_combo_operand(operand, cur_registers) % 8
            case OpCode.jnz:
                if cur_registers[0] != 0:
                    jump = True
                    ip = operand
            case OpCode.bxc:
                cur_registers[1] ^= cur_registers[2]
            case OpCode.out:
                out.append(get_combo_operand(operand, cur_registers) % 8)
            case OpCode.bdv:
                cur_registers[1] = cur_registers[0] >> get_combo_operand(operand, cur_registers)
            case OpCode.cdv:
                cur_registers[2] = cur_registers[0] >> get_combo_operand(operand, cur_registers)
            case _:
                raise ValueError('Unknown opcode')

        if not jump:
            ip += 2
    # print('a', cur_registers[0])
    # print('out', out)
    return out

# print('a:', ','.join(str(x) for x in run(program, registers.copy())))
# exit

# print(len(program))
# with PrintTiming('b'):
#     new_a = 0
#     while True:
#         registers_to_try = registers.copy()
#         registers_to_try[0] = new_a
#         if program == (cur_res := run(program, registers_to_try)):
#             break
#         print('trying ', new_a)
#         pprint.pprint(cur_res)
#         new_a += 128
# print('b: ', new_a)

# new_a = 10000002
# index = 0
# found = False
# cur_a = new_a
# while not found:
#     if new_a % 8 == program[index]:
#         print(program[index], end='')
#         index += 1
#         cur_a //= 8
#     else:
#         if index:
#             print()
#         index = 0
#         new_a += 10
#         cur_a = new_a

# for new_a in range(8):
#     registers_to_try = registers.copy()
#     registers_to_try[0] = (7 << 3) + new_a
#     print(run(program, registers_to_try))
#
# exit()

force_last_a = {
    # 14: 4,
    13: 4,
    12: 6,
    7: 5,
    1: 6
}


with PrintTiming('b'):
    res = []
    cur_total = 0
    prev_total = 0
    last_poss_a = [0]
    for i in reversed(range((program_len := len(program)))):
        while True:
            last_a = force_last_a.get(i) or last_poss_a.pop(0)
            print(i, 'last_a try', last_a)
            next_poss_a = []
            cur_total = (last_a + prev_total) << 3
            for new_a in range(8):
                registers_to_try = registers.copy()
                # print('trying ', new_a)
                # new_a <<= 3
                registers_to_try[0] = cur_total + new_a
                # if not res:
                #     registers_to_try[0] <<= 3
                cur_res = run(program, registers_to_try)

                if program[i:] == cur_res:
                    next_poss_a.append(new_a)
                    # res.append(new_a)
                    # cur_total += new_a
                    # cur_total <<= 3
                    print(f'out: {cur_res}')
                    # pprint.pprint(res)

            if next_poss_a:
                prev_total = cur_total
                last_poss_a = next_poss_a
                # print(f'{prev_total:b}')
                # print(f'{prev_total + new_a:b}')
                break

        if not last_poss_a:
            print('nope')
        else:
            print('i', i, 'poss_a', last_poss_a)
registers_to_try = registers.copy()
registers_to_try[0] = (prev_total + 3)
print('b output: ', run(program, registers_to_try))
print('b: ', (prev_total + 3))
