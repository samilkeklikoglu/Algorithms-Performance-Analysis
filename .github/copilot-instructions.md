# Copilot instructions (Algorithms-Performance-Analysis)

## Big picture

- This repo is **dual-track**: Java is the **authoritative benchmark engine**, Python is a **GUI/visualizer** that launches Java and reads JSON.
- Java entrypoint: [src/main/java/edu/gidatarim/sortbench/Main.java](../src/main/java/edu/gidatarim/sortbench/Main.java)
  - Parses CLI args via [src/main/java/edu/gidatarim/sortbench/cli/Args.java](../src/main/java/edu/gidatarim/sortbench/cli/Args.java)
  - Runs benchmark via [src/main/java/edu/gidatarim/sortbench/measure/BenchmarkRunner.java](../src/main/java/edu/gidatarim/sortbench/measure/BenchmarkRunner.java)
  - Writes JSON via [src/main/java/edu/gidatarim/sortbench/export/JsonWriter.java](../src/main/java/edu/gidatarim/sortbench/export/JsonWriter.java)

## Critical workflows

- Build (Windows): `./gradlew.bat build` (Java target = 17; see [build.gradle](../build.gradle))
- Run benchmark (Windows): `./gradlew.bat run --args="--dataset random --size 20000 --reps 5 --seed 42"`
- Run GUI: `python python/main.py` (see [python/README.md](../python/README.md))

## Benchmarking conventions (important)

- **Paired reps:** For repetition `r`, the engine generates one dataset with `seed + r`, then benchmarks every algorithm on a fresh `base.clone()`.
- **Warmup:** `--warmup` runs untimed warmup sorts before measuring.
- **Verification:** `--verify` checks sortedness outside the timed region.
- **Allocation metric:** Collected during the timed sort region via [src/main/java/edu/gidatarim/sortbench/measure/AllocationMeasurer.java](../src/main/java/edu/gidatarim/sortbench/measure/AllocationMeasurer.java) (`thread allocated bytes` if available, otherwise heap-used delta).

## Results format + location

- Output directory is **hard-coded** to `results/` (Java writes there; Python reads from there).
- Java prints: `Wrote results: <absolute path>.json` (Python parses this in [python/parse_java_output.py](../python/parse_java_output.py)).
- File naming: `<dataset>_n<size>_r<reps>_s<seed>_<timestamp>.json` (see JsonWriter).
- JSON shape (top-level): `timestampUtc`, `engineVersion`, `jvm{...}`, `params{...}`, `resultsByAlgorithm{...}`.
  - Per algorithm: `timesNs[]`, `allocatedBytes[]`, plus stats: `minNs/maxNs/avgNs/medianNs` and `minAllocatedBytes/maxAllocatedBytes/avgAllocatedBytes/medianAllocatedBytes`.

## Windows/Gradle quoting quirk

- Gradle may pass args as a **single token** on Windows; Java arg parsing explicitly supports this (see `Args.parse`).
- Python runner uses `cmd.exe /c gradlew.bat run --args="..."` to avoid Gradle interpreting `--dataset` etc as Gradle flags (see [python/java_runner.py](../python/java_runner.py)).

## Adding/changing algorithms (project pattern)

- Algorithms are stateless utilities with `public static void sort(int[] a)` (examples: [src/main/java/edu/gidatarim/sortbench/algo/QuickSort.java](../src/main/java/edu/gidatarim/sortbench/algo/QuickSort.java), [src/main/java/edu/gidatarim/sortbench/algo/RadixSort.java](../src/main/java/edu/gidatarim/sortbench/algo/RadixSort.java)).
- If you add a new algorithm:
  - Add it to [src/main/java/edu/gidatarim/sortbench/cli/AlgorithmName.java](../src/main/java/edu/gidatarim/sortbench/cli/AlgorithmName.java)
  - Wire it in `BenchmarkRunner.sort(...)`
  - Ensure it can handle the dataset constraints (e.g., current random values are non-negative; Radix assumes `value >= 0`).
