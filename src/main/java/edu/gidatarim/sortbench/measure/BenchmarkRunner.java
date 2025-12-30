package edu.gidatarim.sortbench.measure;

import edu.gidatarim.sortbench.algo.HeapSort;
import edu.gidatarim.sortbench.algo.MergeSort;
import edu.gidatarim.sortbench.algo.QuickSort;
import edu.gidatarim.sortbench.algo.RadixSort;
import edu.gidatarim.sortbench.algo.ShellSort;
import edu.gidatarim.sortbench.cli.AlgorithmName;
import edu.gidatarim.sortbench.cli.Args;
import edu.gidatarim.sortbench.data.DatasetGenerator;

import java.time.Instant;
import java.util.EnumMap;
import java.util.Map;

public final class BenchmarkRunner {
  private static final long WARMUP_SEED_MIX = 0x9E3779B97F4A7C15L;

  private BenchmarkRunner() {
  }

  public static BenchmarkResult run(Args args, String engineVersion) {
    warmup(args, engineVersion);

    Map<AlgorithmName, AlgorithmRun> results = new EnumMap<>(AlgorithmName.class);
    for (AlgorithmName name : args.algorithms) {
      results.put(name, new AlgorithmRun(new long[args.repetitions]));
    }

    for (int r = 0; r < args.repetitions; r++) {
      long repSeed = args.seed + r;
      int[] base = DatasetGenerator.generate(args.datasetType, args.size, repSeed);

      for (AlgorithmName name : args.algorithms) {
        int[] copy = base.clone();
        long start = System.nanoTime();
        sort(name, copy);
        long end = System.nanoTime();

        if (args.verify) {
          Sortedness.requireSortedAscending(copy, name.name().toLowerCase() + ", rep=" + r);
        }

        // Record measurement
        results.get(name).timesNs[r] = end - start;
      }
    }

    // Recompute stats with filled arrays
    Map<AlgorithmName, AlgorithmRun> finalized = new EnumMap<>(AlgorithmName.class);
    for (Map.Entry<AlgorithmName, AlgorithmRun> e : results.entrySet()) {
      finalized.put(e.getKey(), new AlgorithmRun(e.getValue().timesNs));
    }

    String timestampUtc = Instant.now().toString();

    return new BenchmarkResult(
        timestampUtc,
        engineVersion,
        System.getProperty("java.version"),
        System.getProperty("java.vm.name"),
        System.getProperty("os.name"),
        System.getProperty("os.arch"),
        args.algorithms.toArray(new AlgorithmName[0]),
        args.datasetType,
        args.size,
        args.repetitions,
        args.warmupRuns,
        args.seed,
        finalized);
  }

  private static void warmup(Args args, String engineVersion) {
    if (args.warmupRuns <= 0) {
      return;
    }

    int warmN = Math.max(1_000, Math.min(args.size / 10, 50_000));
    long warmSeedBase = args.seed ^ WARMUP_SEED_MIX;

    for (int w = 0; w < args.warmupRuns; w++) {
      long seed = warmSeedBase + w;
      int[] base = DatasetGenerator.generate(args.datasetType, warmN, seed);
      for (AlgorithmName name : args.algorithms) {
        int[] copy = base.clone();
        sort(name, copy);
      }
    }
  }

  private static void sort(AlgorithmName name, int[] a) {
    switch (name) {
      case QUICK -> QuickSort.sort(a);
      case HEAP -> HeapSort.sort(a);
      case SHELL -> ShellSort.sort(a);
      case MERGE -> MergeSort.sort(a);
      case RADIX -> RadixSort.sort(a);
    }
  }
}
