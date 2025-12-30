package edu.gidatarim.sortbench.measure;

import edu.gidatarim.sortbench.cli.AlgorithmName;
import edu.gidatarim.sortbench.data.DatasetType;

import java.util.Map;

public final class BenchmarkResult {
  public final String timestampUtc;
  public final String engineVersion;

  public final String javaVersion;
  public final String vmName;
  public final String osName;
  public final String osArch;

  public final AlgorithmName[] algorithms;
  public final DatasetType datasetType;
  public final int size;
  public final int repetitions;
  public final int warmupRuns;
  public final long seed;

  public final Map<AlgorithmName, AlgorithmRun> resultsByAlgorithm;

  public BenchmarkResult(
      String timestampUtc,
      String engineVersion,
      String javaVersion,
      String vmName,
      String osName,
      String osArch,
      AlgorithmName[] algorithms,
      DatasetType datasetType,
      int size,
      int repetitions,
      int warmupRuns,
      long seed,
      Map<AlgorithmName, AlgorithmRun> resultsByAlgorithm) {
    this.timestampUtc = timestampUtc;
    this.engineVersion = engineVersion;
    this.javaVersion = javaVersion;
    this.vmName = vmName;
    this.osName = osName;
    this.osArch = osArch;
    this.algorithms = algorithms;
    this.datasetType = datasetType;
    this.size = size;
    this.repetitions = repetitions;
    this.warmupRuns = warmupRuns;
    this.seed = seed;
    this.resultsByAlgorithm = resultsByAlgorithm;
  }
}
