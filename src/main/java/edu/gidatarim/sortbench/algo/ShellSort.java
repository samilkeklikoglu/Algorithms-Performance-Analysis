package edu.gidatarim.sortbench.algo;

public final class ShellSort {
  private ShellSort() {
  }

  public static void sort(int[] a) {
    int n = a.length;
    if (n < 2) {
      return;
    }

    // Simple Shell gap sequence: n/2, n/4, ..., 1
    for (int gap = n >>> 1; gap > 0; gap >>>= 1) {
      for (int i = gap; i < n; i++) {
        int tmp = a[i];
        int j = i;
        while (j >= gap && a[j - gap] > tmp) {
          a[j] = a[j - gap];
          j -= gap;
        }
        a[j] = tmp;
      }
    }
  }
}
