package edu.gidatarim.sortbench.data;

import java.util.SplittableRandom;

public final class DatasetGenerator {
  private static final int RANDOM_UPPER_BOUND_EXCLUSIVE = 1_000_000;

  private DatasetGenerator() {
  }

  public static int[] generate(DatasetType type, int size, long seed) {
    return switch (type) {
      case RANDOM -> random(size, seed);
      case REVERSE -> reverse(size);
      case PARTIALLY_SORTED -> partiallySorted(size, seed);
    };
  }

  private static int[] random(int size, long seed) {
    SplittableRandom rng = new SplittableRandom(seed);
    int[] a = new int[size];
    for (int i = 0; i < size; i++) {
      a[i] = rng.nextInt(RANDOM_UPPER_BOUND_EXCLUSIVE);
    }
    return a;
  }

  private static int[] reverse(int size) {
    int[] a = new int[size];
    for (int i = 0; i < size; i++) {
      a[i] = size - i;
    }
    return a;
  }

  private static int[] partiallySorted(int size, long seed) {
    int[] a = new int[size];
    for (int i = 0; i < size; i++) {
      a[i] = i;
    }

    int swaps = (int) Math.floor(size * 0.10);
    if (size < 2 || swaps <= 0) {
      return a;
    }

    SplittableRandom rng = new SplittableRandom(seed);
    for (int s = 0; s < swaps; s++) {
      int i = rng.nextInt(size);
      int j = rng.nextInt(size);
      int tmp = a[i];
      a[i] = a[j];
      a[j] = tmp;
    }
    return a;
  }
}
