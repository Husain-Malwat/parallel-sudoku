# Makefile
CC      := gcc
CFLAGS  := -O2 -Wall -Wextra -std=c11
# pthread is required for unnamed POSIX semaphores; -lrt is usually not needed on modern glibc
LDLIBS  := -pthread

# Change this if your file isn't named file.c
SRC     := file.c
BIN     := sudoku

all: $(BIN)

$(BIN): $(SRC)
	$(CC) $(CFLAGS) -o $(BIN) $(SRC) $(LDLIBS)

clean:
	rm -f $(BIN)
