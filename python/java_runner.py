from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class JavaRunConfig:
    dataset: str  # random|partially_sorted|reverse
    size: int
    reps: int
    seed: int = 42
    warmup: int = 5
    algorithms: str = "all"
    verify: bool = True


def run_java_benchmark(repo_root: Path, cfg: JavaRunConfig) -> subprocess.CompletedProcess[str]:
    gradlew = repo_root / "gradlew.bat"
    if not gradlew.exists():
        raise FileNotFoundError(f"Missing Gradle wrapper: {gradlew}")

    args_value = (
        f"--dataset {cfg.dataset} "
        f"--size {cfg.size} "
        f"--reps {cfg.reps} "
        f"--seed {cfg.seed} "
        f"--warmup {cfg.warmup} "
        f"--algorithms {cfg.algorithms} "
        f"--verify {'true' if cfg.verify else 'false'}"
    )

    # Important: Gradle interprets values that start with `--...` as options.
    # So `--args` must be passed in the `--args="..."` form (single token).
    # Also, execute the .bat via cmd.exe for reliable Windows behavior.
    cmd: List[str] = [
        "cmd.exe",
        "/c",
        str(gradlew),
        "run",
        f"--args=\"{args_value}\"",
    ]

    return subprocess.run(
        cmd,
        cwd=str(repo_root),
        text=True,
        capture_output=True,
        check=False,
    )
