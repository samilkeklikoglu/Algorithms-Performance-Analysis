package edu.gidatarim.sortbench.measure;

public final class AlgorithmRun {
  public final long[] timesNs;
  public final Stats stats;

  public final long[] allocatedBytes;
  public final AllocationStats allocationStats;

  public AlgorithmRun(long[] timesNs, long[] allocatedBytes) {
    this.timesNs = timesNs;
    this.stats = Stats.from(timesNs);

    this.allocatedBytes = allocatedBytes;
    this.allocationStats = AllocationStats.from(allocatedBytes);
  }
}
