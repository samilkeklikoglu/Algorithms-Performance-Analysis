package edu.gidatarim.sortbench.cli;

import edu.gidatarim.sortbench.data.DatasetType;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.EnumSet;
import java.util.List;
import java.util.Locale;

public final class Args {
  public final EnumSet<AlgorithmName> algorithms;
  public final DatasetType datasetType;
  public final int size;
  public final int repetitions;
  public final int warmupRuns;
  public final long seed;
  public final boolean verify;

  private Args(
      EnumSet<AlgorithmName> algorithms,
      DatasetType datasetType,
      int size,
      int repetitions,
      int warmupRuns,
      long seed,
      boolean verify) {
    this.algorithms = algorithms;
    this.datasetType = datasetType;
    this.size = size;
    this.repetitions = repetitions;
    this.warmupRuns = warmupRuns;
    this.seed = seed;
    this.verify = verify;
  }

  public static Args parse(String[] argv) {
    String datasetRaw = null;
    String algorithmsRaw = "all";
    Integer size = null;
    Integer reps = null;
    int warmup = 5;
    long seed = 12345L;
    boolean verify = true;

    List<String> tokens = new ArrayList<>(Arrays.asList(argv));
    for (int i = 0; i < tokens.size(); i++) {
      String t = tokens.get(i);
      if (!t.startsWith("--")) {
        throw new IllegalArgumentException("Unexpected token: " + t);
      }
      String key = t.substring(2).toLowerCase(Locale.ROOT);
      if (key.equals("help") || key.equals("h")) {
        throw new IllegalArgumentException("HELP");
      }
      if (i + 1 >= tokens.size()) {
        throw new IllegalArgumentException("Missing value for --" + key);
      }
      String value = tokens.get(++i);

      switch (key) {
        case "dataset" -> datasetRaw = value;
        case "algorithms" -> algorithmsRaw = value;
        case "size" -> size = parsePositiveInt("--size", value);
        case "reps", "repetitions" -> reps = parsePositiveInt("--reps", value);
        case "warmup" -> warmup = parseNonNegativeInt("--warmup", value);
        case "seed" -> seed = parseLong("--seed", value);
        case "verify" -> verify = parseBoolean("--verify", value);
        default -> throw new IllegalArgumentException("Unknown flag: --" + key);
      }
    }

    if (datasetRaw == null) {
      throw new IllegalArgumentException("Missing required flag: --dataset");
    }
    if (size == null) {
      throw new IllegalArgumentException("Missing required flag: --size");
    }
    if (reps == null) {
      throw new IllegalArgumentException("Missing required flag: --reps");
    }

    DatasetType datasetType = DatasetType.parse(datasetRaw);
    EnumSet<AlgorithmName> algorithms = parseAlgorithms(algorithmsRaw);

    if (size < 1) {
      throw new IllegalArgumentException("--size must be >= 1");
    }
    if (reps < 1) {
      throw new IllegalArgumentException("--reps must be >= 1");
    }
    if (warmup < 0) {
      throw new IllegalArgumentException("--warmup must be >= 0");
    }

    return new Args(algorithms, datasetType, size, reps, warmup, seed, verify);
  }

  private static boolean parseBoolean(String flag, String raw) {
    String v = raw.trim().toLowerCase(Locale.ROOT);
    return switch (v) {
      case "true", "t", "1", "yes", "y" -> true;
      case "false", "f", "0", "no", "n" -> false;
      default -> throw new IllegalArgumentException("Invalid boolean for " + flag + ": " + raw);
    };
  }

  private static EnumSet<AlgorithmName> parseAlgorithms(String raw) {
    if (raw == null || raw.isBlank()) {
      return EnumSet.allOf(AlgorithmName.class);
    }
    String normalized = raw.trim().toLowerCase(Locale.ROOT);
    if (normalized.equals("all")) {
      return EnumSet.allOf(AlgorithmName.class);
    }
    String[] parts = normalized.split(",");
    EnumSet<AlgorithmName> set = EnumSet.noneOf(AlgorithmName.class);
    for (String part : parts) {
      if (part.isBlank())
        continue;
      set.add(AlgorithmName.parse(part));
    }
    if (set.isEmpty()) {
      throw new IllegalArgumentException("--algorithms must be 'all' or a comma-separated list");
    }
    return set;
  }

  private static int parsePositiveInt(String flag, String raw) {
    int value = parseInt(flag, raw);
    if (value <= 0) {
      throw new IllegalArgumentException(flag + " must be > 0");
    }
    return value;
  }

  private static int parseNonNegativeInt(String flag, String raw) {
    int value = parseInt(flag, raw);
    if (value < 0) {
      throw new IllegalArgumentException(flag + " must be >= 0");
    }
    return value;
  }

  private static int parseInt(String flag, String raw) {
    try {
      return Integer.parseInt(raw.trim());
    } catch (NumberFormatException e) {
      throw new IllegalArgumentException("Invalid integer for " + flag + ": " + raw);
    }
  }

  private static long parseLong(String flag, String raw) {
    try {
      return Long.parseLong(raw.trim());
    } catch (NumberFormatException e) {
      throw new IllegalArgumentException("Invalid long for " + flag + ": " + raw);
    }
  }

  public static String usage() {
    return String.join(System.lineSeparator(),
        "Java Sorting Benchmark Engine (authoritative)",
        "",
        "Usage:",
        "  sortbench --dataset <random|partially_sorted|reverse> --size <N> --reps <R> [--warmup <W>] [--seed <S>] [--algorithms <all|list>] [--verify <true|false>]",
        "",
        "Examples:",
        "  sortbench --dataset random --size 100000 --reps 10",
        "  sortbench --dataset reverse --size 200000 --reps 7 --seed 42",
        "  sortbench --dataset partially_sorted --size 50000 --reps 10 --algorithms quick,merge,radix",
        "  sortbench --dataset random --size 100000 --reps 10 --verify false",
        "",
        "Notes:",
        "  - Outputs JSON to ./results/ (hard-coded).",
        "  - Benchmarks are paired: each repetition generates one dataset, then every algorithm sorts a fresh copy.",
        "  - Verification (default true) checks sortedness outside the timed region.");
  }
}
