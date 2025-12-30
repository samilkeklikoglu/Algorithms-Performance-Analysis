package edu.gidatarim.sortbench.algo;

public final class RadixSort {
  private RadixSort() {
  }

  /**
   * LSD radix sort for non-negative 32-bit integers using base 256 (4 passes).
   */
  public static void sort(int[] a) {
    int n = a.length;
    if (n < 2) {
      return;
    }

    int[] out = new int[n];
    int[] count = new int[256];

    for (int shift = 0; shift < 32; shift += 8) {
      // reset counts
      for (int i = 0; i < 256; i++) {
        count[i] = 0;
      }

      for (int value : a) {
        // Assumes value >= 0.
        int bucket = (value >>> shift) & 0xFF;
        count[bucket]++;
      }

      int sum = 0;
      for (int i = 0; i < 256; i++) {
        int c = count[i];
        count[i] = sum + c;
        sum += c;
      }

      for (int i = n - 1; i >= 0; i--) {
        int v = a[i];
        int bucket = (v >>> shift) & 0xFF;
        out[--count[bucket]] = v;
      }

      System.arraycopy(out, 0, a, 0, n);
    }
  }
}
