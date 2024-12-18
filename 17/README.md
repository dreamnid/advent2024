# Day 17

Mixed up xor's ^ with xor |

Part 2 algorithm

Noted that A is being shifted by 3
Since A has to be 0 at the last iteration, it's easier to work backwards (starting at the end of the program)

Manually solved 2 by finding where iteration fails where it can't pop, then going through the previous iteration that has poss_prev_a list size greater than one

## Performance
```bash
(advent2024) ~/w/a/17 ❯❯❯ time ./17.py                                                                                                                                                                                                         ⏎ main ✚ ✱ ◼
15 last_a try 0
out: [0]
out: [0]
i 15 poss_a [0, 7]
14 last_a try 0
14 last_a try 7
out: [3, 0]
out: [3, 0]
i 14 poss_a [2, 4]
13 last_a try 4
out: [5, 3, 0]
out: [5, 3, 0]
out: [5, 3, 0]
i 13 poss_a [2, 3, 6]
12 last_a try 6
out: [5, 5, 3, 0]
out: [5, 5, 3, 0]
i 12 poss_a [1, 6]
11 last_a try 1
out: [7, 5, 5, 3, 0]
i 11 poss_a [1]
10 last_a try 1
out: [1, 7, 5, 5, 3, 0]
i 10 poss_a [6]
9 last_a try 6
out: [4, 1, 7, 5, 5, 3, 0]
out: [4, 1, 7, 5, 5, 3, 0]
i 9 poss_a [0, 3]
8 last_a try 0
out: [4, 4, 1, 7, 5, 5, 3, 0]
out: [4, 4, 1, 7, 5, 5, 3, 0]
i 8 poss_a [4, 5]
7 last_a try 5
out: [3, 4, 4, 1, 7, 5, 5, 3, 0]
i 7 poss_a [2]
6 last_a try 2
out: [0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
out: [0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
out: [0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
i 6 poss_a [2, 5, 7]
5 last_a try 2
out: [5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
out: [5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
i 5 poss_a [0, 6]
4 last_a try 0
4 last_a try 6
out: [7, 5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
i 4 poss_a [2]
3 last_a try 2
out: [7, 7, 5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
i 3 poss_a [1]
2 last_a try 1
out: [1, 7, 7, 5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
out: [1, 7, 7, 5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
i 2 poss_a [0, 6]
1 last_a try 6
out: [4, 1, 7, 7, 5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
i 1 poss_a [3]
0 last_a try 3
out: [2, 4, 1, 7, 7, 5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
out: [2, 4, 1, 7, 7, 5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
i 0 poss_a [3, 5]
timer b:  0:00:00.006469
b output:  [2, 4, 1, 7, 7, 5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0]
b:  267265166222235
./17.py  0.05s user 0.02s system 78% cpu 0.097 total

```