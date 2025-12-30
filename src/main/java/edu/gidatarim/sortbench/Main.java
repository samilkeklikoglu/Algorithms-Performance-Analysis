package edu.gidatarim.sortbench;

import edu.gidatarim.sortbench.cli.Args;
import edu.gidatarim.sortbench.export.JsonWriter;
import edu.gidatarim.sortbench.measure.BenchmarkResult;
import edu.gidatarim.sortbench.measure.BenchmarkRunner;

import java.nio.file.Path;

public final class Main {
  private static final String ENGINE_VERSION = "1.0.0";

  private Main() {
  }

  public static void main(String[] argv) {
    if (argv.length == 0) {
      System.out.println(Args.usage());
      return;
    }
    Args args;
    try {
      args = Args.parse(argv);
    } catch (IllegalArgumentException e) {
      if ("HELP".equals(e.getMessage())) {
        System.out.println(Args.usage());
        System.exit(0);
        return;
      }
      System.err.println("Argument error: " + e.getMessage());
      System.err.println();
      System.err.println(Args.usage());
      System.exit(2);
      return;
    }

    BenchmarkResult result = BenchmarkRunner.run(args, ENGINE_VERSION);

    try {
      Path out = JsonWriter.writeToResultsDir(result, Path.of("results"));
      System.out.println("Wrote results: " + out.toAbsolutePath());
    } catch (Exception e) {
      System.err.println("Failed to write results: " + e.getMessage());
      System.exit(3);
    }
  }
}
