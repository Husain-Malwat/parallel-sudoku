import subprocess, time, json, glob, os

BIN = "/root/workspace/mithil/sudoku"
OUTPUT_DIR = "/root/workspace/mithil/outputs"
RESULTS_JSON = "/root/workspace/mithil/timings.json"
ANALYSIS_JSON = "/root/workspace/mithil/analysis.json"
input_path = "/root/workspace/mithil/puzzles"

def run_solver(input_file, h):
    base = os.path.basename(input_file).replace(".txt", f"_h{h}_sol.txt")
    output_file = os.path.join(OUTPUT_DIR, base)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    start = time.perf_counter()
    subprocess.run([BIN, input_file, output_file, str(h)], check=True)
    end = time.perf_counter()
    
    return end - start

def main():
    patterns = [f"{input_path}/easy*.txt",
                f"{input_path}/med*.txt",
                f"{input_path}/hard*.txt"]

    files = []
    for pat in patterns:
        files.extend(glob.glob(pat))
    files = sorted(files)
    if not files:
        print("No input files (hard*.txt) found.")
        return

    results = { "runs": [], "means": {} }

    for h in [0, 1, 2]:
        times = []
        for f in files:
            print(f"[run] {f} with h={h}")
            t = run_solver(f, h)
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
        "mean_times": results["means"],
        "n_files": len(files),
        "note": "h=0 is sequential backtracking; h=1 is parallel fork at depth 1; h=2 is deeper parallelization"
    }
    with open(ANALYSIS_JSON, "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"[done] wrote {RESULTS_JSON} and {ANALYSIS_JSON}")

if __name__ == "__main__":
    main()
