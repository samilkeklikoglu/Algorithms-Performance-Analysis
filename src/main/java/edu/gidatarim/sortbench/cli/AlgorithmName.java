package edu.gidatarim.sortbench.cli;

import java.util.Locale;

public enum AlgorithmName {
  QUICK,
  HEAP,
  SHELL,
  MERGE,
  RADIX;

  public static AlgorithmName parse(String raw) {
    if (raw == null) {
      throw new IllegalArgumentException("Algorithm name is required");
    }
    String normalized = raw.trim().toLowerCase(Locale.ROOT);
    return switch (normalized) {
      case "quick", "quicksort", "quick_sort" -> QUICK;
      case "heap", "heapsort", "heap_sort" -> HEAP;
      case "shell", "shellsort", "shell_sort" -> SHELL;
      case "merge", "mergesort", "merge_sort" -> MERGE;
      case "radix", "radixsort", "radix_sort" -> RADIX;
      default -> throw new IllegalArgumentException("Unknown algorithm: " + raw);
    };
  }
}
