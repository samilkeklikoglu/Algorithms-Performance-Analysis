# Python GUI (Track A)

This folder contains the **current** Python GUI that reuses the legacy CustomTkinter UI but does **not** benchmark in Python.

- It runs the Java benchmark engine (Track B) and reads JSON results from `../results/`.
- The legacy exploratory implementation remains untouched in `../python-legacy/`.

Notes:

- Time is displayed in milliseconds (ms).
- "Memory" is displayed as heap allocation during the timed sort region (KB). In-place algorithms may show 0 KB.

## Setup (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r python\requirements.txt
```

## Run

```powershell
python python\main.py
```
