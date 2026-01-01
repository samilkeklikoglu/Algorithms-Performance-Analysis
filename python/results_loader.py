from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class AlgorithmStats:
    avg_ms: float
    median_ms: float
    min_ms: float
    max_ms: float

    avg_allocated_kb: float | None = None
    median_allocated_kb: float | None = None
    min_allocated_kb: float | None = None
    max_allocated_kb: float | None = None

    avg_heap_used_delta_kb: float | None = None
    median_heap_used_delta_kb: float | None = None
    min_heap_used_delta_kb: float | None = None
    max_heap_used_delta_kb: float | None = None


def _bytes_to_kb(b: float) -> float:
    return b / 1024.0


def find_latest_result(results_dir: Path) -> Path:
    if not results_dir.exists():
        raise FileNotFoundError(f"Results directory not found: {results_dir}")

    candidates = sorted(results_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError(f"No JSON results found in: {results_dir}")
    return candidates[0]


def load_result(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_algorithm_stats(result: dict) -> Dict[str, AlgorithmStats]:
    by_algo = result.get("resultsByAlgorithm") or {}
    stats: Dict[str, AlgorithmStats] = {}

    for algo_name, payload in by_algo.items():
        avg_ns = float(payload.get("avgNs"))
        median_ns = float(payload.get("medianNs"))
        min_ns = float(payload.get("minNs"))
        max_ns = float(payload.get("maxNs"))

        avg_alloc = payload.get("avgAllocatedBytes")
        median_alloc = payload.get("medianAllocatedBytes")
        min_alloc = payload.get("minAllocatedBytes")
        max_alloc = payload.get("maxAllocatedBytes")

        avg_heap = payload.get("avgHeapUsedDeltaBytes")
        median_heap = payload.get("medianHeapUsedDeltaBytes")
        min_heap = payload.get("minHeapUsedDeltaBytes")
        max_heap = payload.get("maxHeapUsedDeltaBytes")

        def _to_kb(v) -> float | None:
            if v is None:
                return None
            try:
                f = float(v)
            except (TypeError, ValueError):
                return None
            if f < 0:
                return None
            return _bytes_to_kb(f)

        stats[algo_name] = AlgorithmStats(
            avg_ms=avg_ns / 1_000_000.0,
            median_ms=median_ns / 1_000_000.0,
            min_ms=min_ns / 1_000_000.0,
            max_ms=max_ns / 1_000_000.0,

            avg_allocated_kb=_to_kb(avg_alloc),
            median_allocated_kb=_to_kb(median_alloc),
            min_allocated_kb=_to_kb(min_alloc),
            max_allocated_kb=_to_kb(max_alloc),

            avg_heap_used_delta_kb=_to_kb(avg_heap),
            median_heap_used_delta_kb=_to_kb(median_heap),
            min_heap_used_delta_kb=_to_kb(min_heap),
            max_heap_used_delta_kb=_to_kb(max_heap),
        )

    return stats
