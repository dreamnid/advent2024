# Day 20

The description talking about the cheat lasting for 2 nanoseconds can be interpreted that you can 
travel through 2 wall blocks. 
After careful reading, it really means at the 2nd nano second, you must be back on the path so
you can only travel through 1 wall block.

### Part b struggles
* Didn't realize the cheat path can also go on '.'
* KG pointed out since cheat path can also go on '.', don't need to use A* anymore

### Part b wrong ansers
* 883350 - too low
* 1104707 - too high

## Performance
```bash
(advent2024) ~/w/a/20 ❯❯❯ ./20.py                                                                                                                                                                                                                main ✚ ✱ ◼
timer a:  0:00:00.068792
a 1363
timer b:  0:00:10.956533
b 1007186
```