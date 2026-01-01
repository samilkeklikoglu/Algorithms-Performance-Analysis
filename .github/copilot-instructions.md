# Copilot instructions (Algorithms-Performance-Analysis)

## Big picture

- This repo is **dual-track**: Python is a GUI/visualization client; Java is the **authoritative benchmark engine**.
- Data flow: Python launches Java via Gradle Wrapper → Java writes a single JSON file into `results/` → Python loads/parses it for charts/table.
  - Java prints `Wrote results: <absolute path>.json`; Python prefers that, otherwise falls back to “latest file” in `results/`.

## Key code map

- Java CLI entrypoint: `src/main/java/edu/gidatarim/sortbench/Main.java`
- CLI args + quirks: `src/main/java/edu/gidatarim/sortbench/cli/Args.java`
  - Supports a Windows/Gradle quoting case where all args arrive as **one string** (`argv.length == 1`).
- Benchmark loop + invariants: `src/main/java/edu/gidatarim/sortbench/measure/BenchmarkRunner.java`
  - Per repetition `r`: dataset seed is `seed + r`; every algorithm sorts a **fresh clone** of the same base array.
  - `--verify` checks sortedness **outside** the timed region.
- JSON schema writer (hand-rolled): `src/main/java/edu/gidatarim/sortbench/export/JsonWriter.java`
- Python launcher: `python/java_runner.py` (uses `cmd.exe /c gradlew.bat run --args="..."` for reliable Windows behavior)
- Python results parsing: `python/results_loader.py`, `python/parse_java_output.py`

## Developer workflows (Windows)

- Build Java: `./gradlew.bat build`
- Run Java benchmark directly:
  - `./gradlew.bat run --args="--dataset random --size 20000 --reps 5 --seed 42 --warmup 5 --algorithms all --verify true"`
- Run the Python GUI (after venv + deps; see `python/README.md`): `python python\main.py`

## Project-specific conventions

- Java targets **Java 17 bytecode** (`build.gradle` uses `options.release = 17`). Prefer language features compatible with 17.
- Results output directory is effectively **fixed** to `results/` (see `Main.java` → `JsonWriter.writeToResultsDir(..., Path.of("results"))`).
- JSON fields consumed by Python include `params.allocationMetric` and `resultsByAlgorithm[*].{avgNs,medianNs,minNs,maxNs,avgAllocatedBytes,...}`.
  - Python displays time in **ms** and memory as **KB allocated during timed sort**; in-place algorithms may show `0`/`None`.

## When changing/adding algorithms

- Add/modify sorter implementations under `src/main/java/edu/gidatarim/sortbench/algo/`.
- Update algorithm selection + parsing in `src/main/java/edu/gidatarim/sortbench/cli/AlgorithmName.java` and the dispatch `switch` in `BenchmarkRunner.sort(...)`.
- Keep `JsonWriter` schema stable or update Python parsers (`python/results_loader.py`) in the same change.
