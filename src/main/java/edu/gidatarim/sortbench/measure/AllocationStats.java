package edu.gidatarim.sortbench.measure;

import java.util.Arrays;

public final class AllocationStats {
  public final long minAllocatedBytes;
  public final long maxAllocatedBytes;
  public final double avgAllocatedBytes;
  public final double medianAllocatedBytes;

  private AllocationStats(long min, long max, double avg, double median) {
    this.minAllocatedBytes = min;
    this.maxAllocatedBytes = max;
    this.avgAllocatedBytes = avg;
    this.medianAllocatedBytes = median;
  }

  public static AllocationStats from(long[] bytes) {
    if (bytes.length == 0) {
      throw new IllegalArgumentException("allocated bytes array must not be empty");
    }

    long min = bytes[0];
    long max = bytes[0];
    double sum = 0.0;
    for (long b : bytes) {
      if (b < min)
        min = b;
      if (b > max)
        max = b;
      sum += b;
    }
    double avg = sum / bytes.length;

    long[] sorted = Arrays.copyOf(bytes, bytes.length);
    Arrays.sort(sorted);
    double median;
    int n = sorted.length;
    if ((n & 1) == 1) {
      median = sorted[n >>> 1];
    } else {
      long a = sorted[(n >>> 1) - 1];
      long b = sorted[n >>> 1];
      median = (a + b) / 2.0;
    }

    return new AllocationStats(min, max, avg, median);
  }
}
