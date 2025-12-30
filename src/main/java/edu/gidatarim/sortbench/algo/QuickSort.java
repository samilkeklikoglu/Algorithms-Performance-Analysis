package edu.gidatarim.sortbench.algo;

public final class QuickSort {
  private QuickSort() {
  }

  public static void sort(int[] a) {
    if (a.length < 2) {
      return;
    }
    quickSort(a, 0, a.length - 1);
  }

  private static void quickSort(int[] a, int lo, int hi) {
    while (lo < hi) {
      int mid = lo + ((hi - lo) >>> 1);
      int pivot = medianOf3(a[lo], a[mid], a[hi]);

      // 3-way partition: [lo..lt-1] < pivot, [lt..gt] == pivot, [gt+1..hi] > pivot
      int lt = lo;
      int i = lo;
      int gt = hi;
      while (i <= gt) {
        int v = a[i];
        if (v < pivot) {
          swap(a, lt++, i++);
        } else if (v > pivot) {
          swap(a, i, gt--);
        } else {
          i++;
        }
      }

      // Tail recursion elimination: recurse into smaller side first.
      int leftLo = lo;
      int leftHi = lt - 1;
      int rightLo = gt + 1;
      int rightHi = hi;

      if (leftHi - leftLo < rightHi - rightLo) {
        if (leftLo < leftHi) {
          quickSort(a, leftLo, leftHi);
        }
        lo = rightLo;
        hi = rightHi;
      } else {
        if (rightLo < rightHi) {
          quickSort(a, rightLo, rightHi);
        }
        lo = leftLo;
        hi = leftHi;
      }
    }
  }

  private static void swap(int[] a, int i, int j) {
    if (i == j) {
      return;
    }
    int tmp = a[i];
    a[i] = a[j];
    a[j] = tmp;
  }

  private static int medianOf3(int x, int y, int z) {
    if (x < y) {
      if (y < z) {
        return y;
      }
      return (x < z) ? z : x;
    }
    if (x < z) {
      return x;
    }
    return (y < z) ? z : y;
  }
}
