package edu.gidatarim.sortbench.measure;

public final class AlgorithmRun {
  public final long[] timesNs;
  public final Stats stats;

  public final long[] allocatedBytes;
  public final AllocationStats allocationStats;

  public final long[] heapUsedDeltaBytes;
  public final AllocationStats heapUsedDeltaStats;

  public AlgorithmRun(long[] timesNs, long[] allocatedBytes, long[] heapUsedDeltaBytes) {
    this.timesNs = timesNs;
    this.stats = Stats.from(timesNs);

    this.allocatedBytes = allocatedBytes;
    this.allocationStats = AllocationStats.from(allocatedBytes);

    this.heapUsedDeltaBytes = heapUsedDeltaBytes;
    this.heapUsedDeltaStats = AllocationStats.from(heapUsedDeltaBytes);
  }
}
