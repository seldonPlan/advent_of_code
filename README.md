https://adventofcode.com

## Overview ##

Advent of Code submissions. There is a numeric named directory for each day in the Advent of Code calendar (`01` through `25`). Each day has two steps (`a` and `b`). New days/steps can be added by running the `scripts/new_step.py` (no args needed, the script will know what to do). Code assumes a python version of at least 3.10 (some solutions use structural pattern matching).

All steps include at least the following files:
 - `problem.txt`: a statement of the problem to be solved (copied from adventofcode.com)
 - `input.txt`: problem input data
 - `solution.py`: python script to be run that solves the problem
 - `result.txt`: the answer to the problem, corresponds to what is input into the answer box on the adventofcode.com site
 - `output.txt`/`output.json`: full output of the problem calculations. Used to help troubleshoot, or see a view of all the data

## Setup Active AOC Directory ##

On first clone, create a plain text `.active_aoc` file in the root of the repo and populate with the directory to work from. For instance, run `echo "2021" > .active_aoc` to have `new_step.py` manage the **2021** files and directories located under the `/2021` prefix.