# Algorithms-Performance-Analysis (Dual Track)

This repository is structured as a dual-track algorithms course project:

- **Track A (Python / legacy)**: GUI + visualization only (exploratory, not authoritative for benchmarking)
- **Track B (Java / authoritative)**: deterministic dataset generation + repeatable benchmarking + JSON export

## Track A — Python (preserved)

Location: [python-legacy/](python-legacy)

Purpose:

- GUI (CustomTkinter)
- Visualization (Matplotlib)
- User interaction

Non-goals:

- Authoritative benchmarking and dataset control (kept in Java to avoid timing instability)

## Track B — Java (authoritative benchmark engine)

### Why Java is authoritative

Benchmarking must be isolated from GUI rendering, Python allocation noise, and interpreter/runtime variability.
The Java CLI engine is designed for:

- deterministic inputs (seeded)
- JVM warmup
- `System.nanoTime()` timing
- repeated trials + aggregated statistics
- machine-readable export (JSON)

### Environment prerequisites (Windows-friendly)

- **JDK 17+** recommended (project compiles to Java 17 bytecode).
  - Your current machine can use JDK 21; teammates with JDK 17 will still run outputs.
- **No Gradle install required for teammates**: the repo includes the **Gradle Wrapper**.

Verify Java:

- `java -version`
- `javac -version`

### How to run

From repo root:

- Build:

  - `./gradlew build` (Linux/macOS)
  - `./gradlew.bat build` (Windows)

- Run a benchmark (defaults to **all** algorithms):
  - `./gradlew.bat run --args="--dataset random --size 20000 --reps 5 --seed 42"`

Optional flags:

- `--warmup <W>` (default: 5)
- `--algorithms all|quick,heap,shell,merge,radix` (default: all)
- `--verify <true|false>` (default: true; checks sortedness outside timed region)

### Output

Results are written **only** to the hard-coded directory:

- [results/](results)

Each run produces a single JSON file containing results for multiple algorithms.

Key properties:

- `params.seed` is the experiment seed.
- **Paired repetitions**: for repetition `r`, the engine generates one dataset using `seed + r`, then benchmarks every algorithm on a fresh copy of that dataset.
- Statistics include `minNs`, `maxNs`, `avgNs` (double), `medianNs` (double).

## Notes for future Python GUI integration (discussion only)

The intended workflow is:

1. Python GUI collects parameters.
2. Python launches the Java CLI process.
3. Python reads the newest JSON file in [results/](results) and visualizes it.

This avoids the instability seen when timing and visualization share the same process.
