package edu.gidatarim.sortbench.measure;

import java.util.Arrays;

public final class Stats {
  public final long minNs;
  public final long maxNs;
  public final double avgNs;
  public final double medianNs;

  private Stats(long minNs, long maxNs, double avgNs, double medianNs) {
    this.minNs = minNs;
    this.maxNs = maxNs;
    this.avgNs = avgNs;
    this.medianNs = medianNs;
  }

  public static Stats from(long[] timesNs) {
    if (timesNs.length == 0) {
      throw new IllegalArgumentException("timesNs must not be empty");
    }

    long min = timesNs[0];
    long max = timesNs[0];
    double sum = 0.0;
    for (long t : timesNs) {
      if (t < min)
        min = t;
      if (t > max)
        max = t;
      sum += t;
    }
    double avg = sum / timesNs.length;

    long[] sorted = Arrays.copyOf(timesNs, timesNs.length);
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

    return new Stats(min, max, avg, median);
  }
}
