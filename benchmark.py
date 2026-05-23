import subprocess, time, json, glob, os, sys, argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = f"{BASE_DIR}/bin"
OUTPUT_DIR = f"{BASE_DIR}/outputs"
RESULTS_JSON = f"{BASE_DIR}/timings.json"
ANALYSIS_JSON = f"{BASE_DIR}/analysis.json"
input_path = f"{BASE_DIR}/puzzles"

def get_available_solvers():
    """List all available solver executables"""
    if not os.path.exists(BIN_DIR):
        return []
    solvers = [f for f in os.listdir(BIN_DIR) if os.path.isfile(os.path.join(BIN_DIR, f)) and os.access(os.path.join(BIN_DIR, f), os.X_OK)]
    return sorted(solvers)

def run_solver(solver_path, input_file, h):
    base = os.path.basename(input_file).replace(".txt", f"_h{h}_sol.txt")
    output_file = os.path.join(OUTPUT_DIR, base)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    start = time.perf_counter()
    subprocess.run([solver_path, input_file, output_file, str(h)], check=True)
    end = time.perf_counter()
    
    return end - start

def main():
    parser = argparse.ArgumentParser(description='Benchmark Sudoku solvers')
    parser.add_argument('--solver', default='sequential', help='Name of the solver executable (default: sequential)')
    parser.add_argument('--list', action='store_true', help='List available solvers')
    args = parser.parse_args()
    
    # List available solvers if requested
    if args.list:
        available = get_available_solvers()
        if available:
            print("Available solvers in bin/:")
            for solver in available:
                print(f"  - {solver}")
        else:
            print("No solvers found. Please run 'make' to build solvers.")
        return
    
    solver_path = os.path.join(BIN_DIR, args.solver)
    
    if not os.path.exists(solver_path):
        print(f"Error: Solver '{args.solver}' not found at {solver_path}")
        available = get_available_solvers()
        if available:
            print("\nAvailable solvers:")
            for solver in available:
                print(f"  - {solver}")
        else:
            print("\nNo solvers available. Please run 'make' to build solvers.")
        return
    
    patterns = [f"{input_path}/easy*.txt",
                f"{input_path}/med*.txt",
                f"{input_path}/hard*.txt"]

    files = []
    for pat in patterns:
        files.extend(glob.glob(pat))
    files = sorted(files)
    if not files:
        print("No input files found.")
        return

    results = { "runs": [], "means": {}, "solver": args.solver }

    for h in [0, 1, 2]:
        times = []
        for f in files:
            print(f"[run] {f} with h={h}")
            t = run_solver(solver_path, f, h)
            times.append(t)
            results["runs"].append({
                "file": f,
                "h": h,
                "time_sec": t
            })
        results["means"][str(h)] = sum(times)/len(times)

    # save raw timings
    with open(RESULTS_JSON, "w") as f:
        json.dump(results, f, indent=2)

    # save summary analysis
    analysis = {
        "solver": args.solver,
        "mean_times": results["means"],
        "n_files": len(files),
        "note": "h=0 is sequential backtracking; h=1 is parallel fork at depth 1; h=2 is deeper parallelization"
    }
    with open(ANALYSIS_JSON, "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"[done] wrote {RESULTS_JSON} and {ANALYSIS_JSON}")

if __name__ == "__main__":
    main()
