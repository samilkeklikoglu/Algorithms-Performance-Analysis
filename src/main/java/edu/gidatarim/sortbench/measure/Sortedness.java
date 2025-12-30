package edu.gidatarim.sortbench.measure;

public final class Sortedness {
  private Sortedness() {
  }

  /**
   * Returns -1 if sorted ascending, else returns the first index i where a[i-1] >
   * a[i].
   */
  public static int firstInversionIndex(int[] a) {
    for (int i = 1; i < a.length; i++) {
      if (a[i - 1] > a[i]) {
        return i;
      }
    }
    return -1;
  }

  public static void requireSortedAscending(int[] a, String context) {
    int idx = firstInversionIndex(a);
    if (idx >= 0) {
      int left = a[idx - 1];
      int right = a[idx];
      throw new IllegalStateException(
          "Sort verification failed" + (context == null ? "" : " (" + context + ")") +
              ": a[" + (idx - 1) + "]=" + left + " > a[" + idx + "]=" + right);
    }
  }
}
