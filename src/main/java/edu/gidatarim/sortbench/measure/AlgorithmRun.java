package edu.gidatarim.sortbench.measure;

public final class AlgorithmRun {
  public final long[] timesNs;
  public final Stats stats;

  public AlgorithmRun(long[] timesNs) {
    this.timesNs = timesNs;
    this.stats = Stats.from(timesNs);
  }
}
