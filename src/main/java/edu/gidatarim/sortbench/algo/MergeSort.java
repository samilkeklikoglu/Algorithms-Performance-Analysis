package edu.gidatarim.sortbench.algo;

public final class MergeSort {
  private MergeSort() {
  }

  public static void sort(int[] a) {
    int n = a.length;
    if (n < 2) {
      return;
    }
    int[] tmp = new int[n];
    mergeSort(a, tmp, 0, n);
  }

  private static void mergeSort(int[] a, int[] tmp, int lo, int hi) {
    int len = hi - lo;
    if (len <= 1) {
      return;
    }
    int mid = lo + (len >>> 1);
    mergeSort(a, tmp, lo, mid);
    mergeSort(a, tmp, mid, hi);

    // If already ordered, avoid merge.
    if (a[mid - 1] <= a[mid]) {
      return;
    }

    int i = lo;
    int j = mid;
    int k = lo;
    while (i < mid && j < hi) {
      if (a[i] <= a[j]) {
        tmp[k++] = a[i++];
      } else {
        tmp[k++] = a[j++];
      }
    }
    while (i < mid) {
      tmp[k++] = a[i++];
    }
    while (j < hi) {
      tmp[k++] = a[j++];
    }
    System.arraycopy(tmp, lo, a, lo, len);
  }
}
