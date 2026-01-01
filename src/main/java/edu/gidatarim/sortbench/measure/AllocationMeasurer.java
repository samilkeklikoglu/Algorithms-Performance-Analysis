package edu.gidatarim.sortbench.measure;

import java.lang.management.ManagementFactory;

public final class AllocationMeasurer {
  public enum Metric {
    THREAD_ALLOCATED_BYTES,
    HEAP_USED_DELTA_BYTES
  }

  private final Metric metric;

  // Only used when Metric.THREAD_ALLOCATED_BYTES
  private final com.sun.management.ThreadMXBean threadBean;
  private final long threadId;

  // Only used when Metric.HEAP_USED_DELTA_BYTES
  private final java.lang.management.MemoryMXBean memoryBean;

  private AllocationMeasurer(
      Metric metric,
      com.sun.management.ThreadMXBean threadBean,
      long threadId,
      java.lang.management.MemoryMXBean memoryBean) {
    this.metric = metric;
    this.threadBean = threadBean;
    this.threadId = threadId;
    this.memoryBean = memoryBean;
  }

  @SuppressWarnings("deprecation")
  public static AllocationMeasurer create() {
    try {
      java.lang.management.ThreadMXBean base = ManagementFactory.getThreadMXBean();
      if (base instanceof com.sun.management.ThreadMXBean thread) {
        if (thread.isThreadAllocatedMemorySupported()) {
          if (!thread.isThreadAllocatedMemoryEnabled()) {
            thread.setThreadAllocatedMemoryEnabled(true);
          }
          return new AllocationMeasurer(Metric.THREAD_ALLOCATED_BYTES, thread, Thread.currentThread().getId(), null);
        }
      }
    } catch (Throwable ignored) {
      // Fall through to heap delta.
    }

    return new AllocationMeasurer(Metric.HEAP_USED_DELTA_BYTES, null, -1L, ManagementFactory.getMemoryMXBean());
  }

  public Metric metric() {
    return metric;
  }

  public long read() {
    return switch (metric) {
      case THREAD_ALLOCATED_BYTES -> threadBean.getThreadAllocatedBytes(threadId);
      case HEAP_USED_DELTA_BYTES -> memoryBean.getHeapMemoryUsage().getUsed();
    };
  }
}
