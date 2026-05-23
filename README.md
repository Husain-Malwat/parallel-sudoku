# Parallel Sudoku Solver

This project contains **multiple Sudoku solver implementations in C**, including:
- `sequential.c` - Traditional sequential backtracking
- `fork.c` - Process-level parallelism using fork()
- `pthread.c` - Thread-based parallelism using pthreads

Each solver implements both:
- **Sequential backtracking** (`h=0`).
- **Process-level parallelism** at recursion depth (`h=1`, `h=2`).

For testing, I used **easy, medium, and hard Sudoku puzzles** taken from the Kaggle dataset:  
[3 Million Sudoku Puzzles with Ratings](https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings/data).

Benchmarking scripts (`benchmark.py` + helpers) measure execution times and save results in JSON.

## Building

To build **all solvers**:
```bash
make
```

To build a **specific solver**:
```bash
make sequential
make fork
make pthread
```

To list **available solvers**:
```bash
make list-solvers
```

To clean up builds:
```bash
make clean
```

To clean specific solver
```bash
make clean-fork    
```

## Running

To list available solvers:
```bash
python3 benchmark.py --list
```

To run the benchmark with a specific solver:
```bash
python3 benchmark.py --solver sequential
python3 benchmark.py --solver fork
python3 benchmark.py --solver pthread
```

To run with default solver (sequential):
```bash
python3 benchmark.py
```

All solver executables should be located in the `bin/` directory.

## Contributors

- Mithil Pechimuthu
- Husain Malwat

## Acknowledgement

This project was completed as part of the Operating Systems course under the guidance of Prof. Abhishek Bichhawat.