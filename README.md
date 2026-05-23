# Parallel Sudoku Solver

This project contains a **parallelized Sudoku solver in C** (`file.c`).  
It implements both:
- **Sequential backtracking** (`h=0`).
- **Process-level parallelism** at recursion depth (`h=1`, `h=2`).

For testing, I used **easy, medium, and hard Sudoku puzzles** taken from the Kaggle dataset:  
[3 Million Sudoku Puzzles with Ratings](https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings/data).

Benchmarking scripts (`benchmark.py` + helpers) measure execution times and save results in JSON.

## Contributors

- Mithil Pechimuthu
- Husain Malwat

## Acknowledgement

This project was completed as part of the Operating Systems course under the guidance of Prof. Abhishek Bichhawat.