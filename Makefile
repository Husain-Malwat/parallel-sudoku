# Makefile for Multiple Sudoku Solvers
CC      := gcc
CFLAGS  := -O2 -Wall -Wextra -std=c11

# Source files and output binaries
SOLVER_DIR := solvers
BIN_DIR    := bin
SOURCES    := $(wildcard $(SOLVER_DIR)/*.c)
SOLVERS    := $(patsubst $(SOLVER_DIR)/%.c,$(BIN_DIR)/%,$(SOURCES))

# Default LDLIBS (can be overridden per solver)
LDLIBS  := -pthread

# All solvers
all: $(BIN_DIR) $(SOLVERS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

# Generic rule for building solvers
$(BIN_DIR)/%: $(SOLVER_DIR)/%.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

# Individual targets for specific solvers (useful for custom LDLIBS)
.PHONY: sequential fork pthread

sequential: $(BIN_DIR)/sequential
fork: $(BIN_DIR)/fork
pthread: $(BIN_DIR)/pthread

# Optional: Different LDLIBS for specific solvers
# Example: if fork.c doesn't need pthread
# $(BIN_DIR)/fork: $(SOLVER_DIR)/fork.c
#	$(CC) $(CFLAGS) -o $@ $< 

# List available solvers
.PHONY: list-solvers
list-solvers:
	@echo "Available solvers:"
	@for solver in $(SOLVERS); do echo "  - $$(basename $$solver)"; done

# Clean all
clean:
	rm -f $(SOLVERS)

# Clean specific solver
clean-%:
	rm -f $(BIN_DIR)/$*

.PHONY: all clean list-solvers
