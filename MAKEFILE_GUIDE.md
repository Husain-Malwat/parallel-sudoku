# Makefile Guide for Multiple Solvers

This guide explains how to use the Makefile when you have multiple solver implementations.

## Project Structure

```
solvers/              # Source directory
  ├── sequential.c    # Sequential solver implementation
  ├── fork.c          # Fork-based parallelization
  └── pthread.c       # Pthread-based parallelization
bin/                  # Build output directory
  ├── sequential      # Compiled sequential solver
  ├── fork            # Compiled fork solver
  └── pthread         # Compiled pthread solver
```

## How the Makefile Works

The Makefile uses:
- **`SOURCES`** - Automatically finds all `.c` files in `solvers/`
- **`SOLVERS`** - Creates corresponding binary names in `bin/`
- **Pattern rules** - Compiles each `.c` file to a corresponding executable

```makefile
SOURCES := $(wildcard $(SOLVER_DIR)/*.c)
SOLVERS := $(patsubst $(SOLVER_DIR)/%.c,$(BIN_DIR)/%,$(SOURCES))
```

This means if you add `hybrid.c`, it automatically becomes `bin/hybrid`.

## Makefile Commands

### Build all solvers
```bash
make
# or
make all
```

### Build specific solver
```bash
make sequential
make fork
make pthread
```

### List available solvers
```bash
make list-solvers
```

### Clean all solvers
```bash
make clean
```

### Clean specific solver
```bash
make clean-fork
make clean-pthread
```

## Adding a New Solver

1. **Create source file in `solvers/` folder:**
   ```bash
   cp solvers/sequential.c solvers/my_solver.c
   # Edit my_solver.c with your implementation
   ```

2. **Build it automatically:**
   ```bash
   make
   ```
   The Makefile automatically compiles it to `bin/my_solver`

3. **Use it with benchmark:**
   ```bash
   python3 benchmark.py --solver my_solver
   ```

## Customizing Compilation for Specific Solvers

If some solvers need different compiler flags or libraries:

```makefile
# Example: fork solver doesn't need pthread
$(BIN_DIR)/fork: $(SOLVER_DIR)/fork.c
	$(CC) $(CFLAGS) -o $@ $<

# Example: hybrid solver needs special optimization
$(BIN_DIR)/hybrid: $(SOLVER_DIR)/hybrid.c
	$(CC) $(CFLAGS) -O3 -march=native -o $@ $< $(LDLIBS)
```

Add these custom rules to the Makefile to override the default pattern rule.

## Common Makefile Patterns

### Build only if source changed
```bash
make
# Files only rebuild if .c file is newer than binary
```

### Force rebuild
```bash
make clean && make
```

### Check what would build
```bash
make --dry-run
```

## Using with Benchmarks

List available solvers:
```bash
python3 benchmark.py --list
```

Run benchmark on specific solver:
```bash
python3 benchmark.py --solver sequential
python3 benchmark.py --solver fork
python3 benchmark.py --solver pthread
```

## Tips

- **Always run `make` before benchmarking** to ensure binaries are up-to-date
- **Keep solver implementations in `solvers/`** folder for consistency
- **Use meaningful names** for solvers (e.g., `sequential`, `fork`, `pthread`)
- **Add custom Makefile rules** for solvers with special requirements
- **Use `make list-solvers`** to verify all solvers compiled successfully
