import sys
import time
import subprocess
import glob
from rich.console import Console
from rich.table import Table
from tqdm import tqdm

def normalize_output(output):
    # Split the output into lines, strip whitespace, and sort
    return sorted(line.strip() for line in output.strip().split('\n') if line.strip())

def run_script(script_name, input_file):
    start_time = time.time()
    result = subprocess.run(['python', script_name, input_file], capture_output=True, text=True)
    end_time = time.time()
    return end_time - start_time, result.stdout

def benchmark(scripts, input_files):
    results = {script: {} for script in scripts}
    sanity_results = {}
    total_iterations = len(input_files) * len(scripts)

    # Run sanity check first
    print("Running sanity check...")
    for input_file in input_files:
        _, sanity_output = run_script("sanity_check.py", input_file)
        sanity_results[input_file] = normalize_output(sanity_output)

    with tqdm(total=total_iterations, desc="Overall Progress") as pbar:
        for script in scripts:
            for input_file in input_files:
                time_taken, output = run_script(script, input_file)
                normalized_output = normalize_output(output)
                results[script][input_file] = {
                    "time": time_taken,
                    "output": output,
                    "matches_sanity": normalized_output == sanity_results[input_file]
                }
                pbar.update(1)
                pbar.set_postfix_str(f"Current: {script} - {input_file}")

    return results

def create_table(results, input_files):
    table = Table(title="Script Performance Comparison")
    table.add_column("Script", style="cyan", no_wrap=True)
    for input_file in input_files:
        table.add_column(input_file, justify="right", style="magenta")
    table.add_column("Sanity Check", justify="center", style="yellow")

    all_times = [data["time"] for script_results in results.values() for data in script_results.values()]
    min_time = min(all_times)
    max_time = max(all_times)

    for script, file_results in results.items():
        row = [script]
        all_match = True
        for input_file in input_files:
            data = file_results[input_file]
            time = data["time"]
            if time == min_time:
                color = "green"
            elif time == max_time:
                color = "red"
            else:
                color = "white"
            row.append(f"[{color}]{time:.4f}s[/{color}]")
            all_match &= data["matches_sanity"]
        row.append("✅" if all_match else "❌")
        table.add_row(*row)

    return table

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python benchmark.py <input_file1> <input_file2> ...")
        sys.exit(1)

    input_files = sys.argv[1:]
    scripts = sorted(glob.glob("iteration_*.py"))

    if not scripts:
        print("No iteration_*.py scripts found in the current directory.")
        sys.exit(1)

    if "sanity_check.py" not in glob.glob("*.py"):
        print("sanity_check.py not found in the current directory.")
        sys.exit(1)

    print(f"Found {len(scripts)} script(s): {', '.join(scripts)}")
    print(f"Input files: {', '.join(input_files)}")
    print("Starting benchmark...")

    results = benchmark(scripts, input_files)

    print("\nGenerating results table...")
    table = create_table(results, input_files)

    console = Console()
    console.print(table)