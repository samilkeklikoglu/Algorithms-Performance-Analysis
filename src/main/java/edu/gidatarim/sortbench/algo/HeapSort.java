package edu.gidatarim.sortbench.algo;

public final class HeapSort {
  private HeapSort() {
  }

  public static void sort(int[] a) {
    int n = a.length;
    if (n < 2) {
      return;
    }

    for (int i = (n >>> 1) - 1; i >= 0; i--) {
      siftDown(a, i, n);
    }

    for (int end = n - 1; end > 0; end--) {
      int tmp = a[0];
      a[0] = a[end];
      a[end] = tmp;
      siftDown(a, 0, end);
    }
  }

  private static void siftDown(int[] a, int root, int size) {
    while (true) {
      int left = (root << 1) + 1;
      if (left >= size) {
        return;
      }
      int right = left + 1;
      int child = (right < size && a[right] > a[left]) ? right : left;
      if (a[root] >= a[child]) {
        return;
      }
      int tmp = a[root];
      a[root] = a[child];
      a[child] = tmp;
      root = child;
    }
  }
}
