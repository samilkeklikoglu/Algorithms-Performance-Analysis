package edu.gidatarim.sortbench.export;

import edu.gidatarim.sortbench.cli.AlgorithmName;
import edu.gidatarim.sortbench.measure.AlgorithmRun;
import edu.gidatarim.sortbench.measure.BenchmarkResult;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public final class JsonWriter {
  private JsonWriter() {
  }

  public static Path writeToResultsDir(BenchmarkResult result, Path resultsDir) throws IOException {
    Files.createDirectories(resultsDir);

    String safeTimestamp = result.timestampUtc
        .replace(":", "-")
        .replace(".", "-");

    String fileName = String.format(
        "%s_n%d_r%d_s%d_%s.json",
        result.datasetType.name().toLowerCase(),
        result.size,
        result.repetitions,
        result.seed,
        safeTimestamp);

    Path out = resultsDir.resolve(fileName);
    String json = toJson(result);
    Files.writeString(out, json, StandardCharsets.UTF_8);
    return out;
  }

  public static String toJson(BenchmarkResult r) {
    StringBuilder sb = new StringBuilder(16 * 1024);
    sb.append('{');

    field(sb, "timestampUtc", r.timestampUtc).append(',');
    field(sb, "engineVersion", r.engineVersion).append(',');

    sb.append("\"jvm\":{");
    field(sb, "javaVersion", r.javaVersion).append(',');
    field(sb, "vmName", r.vmName).append(',');
    field(sb, "osName", r.osName).append(',');
    field(sb, "osArch", r.osArch);
    sb.append('}').append(',');

    sb.append("\"params\":{");
    sb.append("\"algorithms\":[");
    for (int i = 0; i < r.algorithms.length; i++) {
      if (i > 0)
        sb.append(',');
      sb.append('"').append(r.algorithms[i].name().toLowerCase()).append('"');
    }
    sb.append("],");
    field(sb, "dataset", r.datasetType.name().toLowerCase()).append(',');
    numField(sb, "size", r.size).append(',');
    numField(sb, "repetitions", r.repetitions).append(',');
    numField(sb, "warmupRuns", r.warmupRuns).append(',');
    numField(sb, "seed", r.seed).append(',');
    field(sb, "allocationMetric", r.allocationMetric);
    sb.append('}').append(',');

    sb.append("\"resultsByAlgorithm\":{");
    int algoIndex = 0;
    for (AlgorithmName name : r.algorithms) {
      if (algoIndex++ > 0)
        sb.append(',');
      AlgorithmRun run = r.resultsByAlgorithm.get(name);
      sb.append('"').append(name.name().toLowerCase()).append('"').append(':');
      sb.append('{');

      sb.append("\"timesNs\":[");
      for (int i = 0; i < run.timesNs.length; i++) {
        if (i > 0)
          sb.append(',');
        sb.append(run.timesNs[i]);
      }
      sb.append("],");

      sb.append("\"allocatedBytes\":[");
      for (int i = 0; i < run.allocatedBytes.length; i++) {
        if (i > 0)
          sb.append(',');
        sb.append(run.allocatedBytes[i]);
      }
      sb.append("],");

      numField(sb, "minNs", run.stats.minNs).append(',');
      numField(sb, "maxNs", run.stats.maxNs).append(',');
      doubleField(sb, "avgNs", run.stats.avgNs).append(',');
      doubleField(sb, "medianNs", run.stats.medianNs).append(',');

      numField(sb, "minAllocatedBytes", run.allocationStats.minAllocatedBytes).append(',');
      numField(sb, "maxAllocatedBytes", run.allocationStats.maxAllocatedBytes).append(',');
      doubleField(sb, "avgAllocatedBytes", run.allocationStats.avgAllocatedBytes).append(',');
      doubleField(sb, "medianAllocatedBytes", run.allocationStats.medianAllocatedBytes);

      sb.append('}');
    }
    sb.append('}');

    sb.append('}');
    sb.append(System.lineSeparator());
    return sb.toString();
  }

  private static StringBuilder field(StringBuilder sb, String name, String value) {
    sb.append('"').append(escape(name)).append('"').append(':');
    sb.append('"').append(escape(value)).append('"');
    return sb;
  }

  private static StringBuilder numField(StringBuilder sb, String name, long value) {
    sb.append('"').append(escape(name)).append('"').append(':');
    sb.append(value);
    return sb;
  }

  private static StringBuilder doubleField(StringBuilder sb, String name, double value) {
    sb.append('"').append(escape(name)).append('"').append(':');
    if (Double.isFinite(value)) {
      sb.append(value);
    } else {
      sb.append("null");
    }
    return sb;
  }

  private static String escape(String s) {
    if (s == null) {
      return "";
    }
    StringBuilder out = new StringBuilder(s.length() + 16);
    for (int i = 0; i < s.length(); i++) {
      char c = s.charAt(i);
      switch (c) {
        case '"' -> out.append("\\\"");
        case '\\' -> out.append("\\\\");
        case '\b' -> out.append("\\b");
        case '\f' -> out.append("\\f");
        case '\n' -> out.append("\\n");
        case '\r' -> out.append("\\r");
        case '\t' -> out.append("\\t");
        default -> {
          if (c < 0x20) {
            out.append(String.format("\\u%04x", (int) c));
          } else {
            out.append(c);
          }
        }
      }
    }
    return out.toString();
  }
}
