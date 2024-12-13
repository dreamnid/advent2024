# Day 13

Wrong answers for part 2
* 92443512440894
* 86556292278088
* 80479614230959

Biggest problem for part 2 is I was using int to convert to int when I should be using round to account for .99999 -> 1

## Performance
```bash
(advent2024) ~/w/a/13 ❯❯❯ ./13.py                                                                                                                                                                                                           main ⬆ ✚ ✱ ◼
a 26005
timer a:  0:00:00.062180
b 105620095782547
timer b:  0:00:00.062948
```