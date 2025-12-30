from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


_WROTE_RESULTS_RE = re.compile(r"^Wrote results:\s*(?P<path>.+\.json)\s*$", re.MULTILINE)


def parse_written_results_path(stdout: str) -> Optional[Path]:
    if not stdout:
        return None
    m = _WROTE_RESULTS_RE.search(stdout)
    if not m:
        return None
    return Path(m.group("path").strip())
