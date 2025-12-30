package edu.gidatarim.sortbench.data;

import java.util.Locale;

public enum DatasetType {
  RANDOM,
  PARTIALLY_SORTED,
  REVERSE;

  public static DatasetType parse(String raw) {
    if (raw == null) {
      throw new IllegalArgumentException("Dataset type is required");
    }
    String normalized = raw.trim().toLowerCase(Locale.ROOT);
    return switch (normalized) {
      case "random" -> RANDOM;
      case "partially_sorted", "partial", "partiallysorted" -> PARTIALLY_SORTED;
      case "reverse", "reversed" -> REVERSE;
      default -> throw new IllegalArgumentException("Unknown dataset type: " + raw);
    };
  }
}
