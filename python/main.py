from __future__ import annotations

import threading
from pathlib import Path

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from java_runner import JavaRunConfig, run_java_benchmark
from parse_java_output import parse_written_results_path
from results_loader import find_latest_result, load_result, parse_algorithm_stats


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


def _repo_root() -> Path:
    # python/main.py -> repo root
    return Path(__file__).resolve().parents[1]


class ProSortingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AlgoAnalyze")
        self.geometry("1200x800")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        # Keep controls top-aligned: let extra vertical space expand *after* our widgets.
        self.sidebar.grid_rowconfigure(99, weight=1)

        title_lbl = ctk.CTkLabel(
            self.sidebar,
            text="🚀 AlgoAnalyze",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_lbl.grid(row=0, column=0, padx=20, pady=(30, 20))

        ctk.CTkLabel(self.sidebar, text="Data Size (N):", anchor="w").grid(
            row=1, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self.size_entry = ctk.CTkEntry(self.sidebar, placeholder_text="1000")
        self.size_entry.insert(0, "10000")
        self.size_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(self.sidebar, text="Repetitions:", anchor="w").grid(
            row=3, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self.reps_entry = ctk.CTkEntry(self.sidebar, placeholder_text="5")
        self.reps_entry.insert(0, "50")
        self.reps_entry.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(self.sidebar, text="Dataset Type:", anchor="w").grid(
            row=9, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self.type_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["random", "partially_sorted", "reverse"],
        )
        self.type_menu.set("random")
        self.type_menu.grid(row=10, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.verify_var = ctk.BooleanVar(value=True)
        self.verify_check = ctk.CTkCheckBox(
            self.sidebar,
            text="Verify (sortedness)",
            variable=self.verify_var,
        )
        self.verify_check.grid(row=11, column=0, padx=20, pady=(0, 10), sticky="w")

        self.btn_run = ctk.CTkButton(
            self.sidebar,
            text="START ANALYSIS",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            height=40,
            font=("Arial", 14, "bold"),
            command=self.start_thread,
        )
        self.btn_run.grid(row=12, column=0, padx=20, pady=20)

        self.status_lbl = ctk.CTkLabel(self.sidebar, text="Status: Ready", text_color="gray")
        self.status_lbl.grid(row=13, column=0, padx=20, pady=10)

    def create_main_area(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        self.tab_dashboard = self.tabs.add("📈 Charts")
        self.tab_table = self.tabs.add("📋 Table")
        self.tab_logs = self.tabs.add("📝 Logs")

        self.setup_dashboard()
        self.setup_table()

        self.log_box = ctk.CTkTextbox(self.tab_logs, font=("Consolas", 13))
        self.log_box.pack(fill="both", expand=True, padx=5, pady=5)

    def setup_dashboard(self):
        self.chart_frame = ctk.CTkFrame(self.tab_dashboard)
        self.chart_frame.pack(fill="both", expand=True)

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=100)
        self.fig.patch.set_facecolor("#242424")

        self.ax1.set_facecolor("#2b2b2b")
        self.ax1.set_title("Average Time (ms)", color="white", fontsize=10)
        self.ax1.tick_params(colors="white", labelsize=8)

        self.ax2.set_facecolor("#2b2b2b")
        self.ax2.set_title("Heap Allocated During Sort (KB)", color="white", fontsize=10)
        self.ax2.tick_params(colors="white", labelsize=8)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def setup_table(self):
        headers = ["Algorithm", "Avg (ms)", "Median (ms)", "Avg Heap Alloc (KB)", "Status"]
        self.table_frame = ctk.CTkFrame(self.tab_table)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.table_frame,
                text=text,
                font=("Arial", 16, "bold"),
                fg_color="#333",
                corner_radius=5,
            )
            lbl.grid(row=0, column=col, sticky="ew", padx=2, pady=5, ipady=5)
            self.table_frame.grid_columnconfigure(col, weight=1)

    def start_thread(self):
        self.btn_run.configure(state="disabled")
        self.status_lbl.configure(text="Status: Running")
        self.log_box.delete("1.0", "end")
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        try:
            size = int(self.size_entry.get())
            reps = int(self.reps_entry.get())
            dataset = self.type_menu.get()
            verify = bool(self.verify_var.get())
        except Exception:
            self._log("ERROR: Invalid input! (size/reps/seed/warmup must be numbers)\n")
            self.reset_ui()
            return

        cfg = JavaRunConfig(
            dataset=dataset,
            size=size,
            reps=reps,
            seed=42,
            warmup=5,
            algorithms="all",
            verify=verify,
        )

        repo_root = _repo_root()
        self._log(f"PARAMETERS: dataset={dataset}, N={size}, reps={reps}, seed=42, warmup=5, verify={verify}\n")
        self._log("Running Java (Gradle Wrapper)...\n")

        proc = run_java_benchmark(repo_root, cfg)
        if proc.stdout:
            self._log(proc.stdout + "\n")
        if proc.stderr:
            self._log(proc.stderr + "\n")

        if proc.returncode != 0:
            self._log(f"ERROR: Java benchmark failed (exit={proc.returncode})\n")
            self.reset_ui()
            return

        try:
            results_path = parse_written_results_path(proc.stdout)
            if results_path is None:
                results_path = find_latest_result(repo_root / "results")
            result = load_result(results_path)
            stats = parse_algorithm_stats(result)
        except Exception as e:
            self._log(f"ERROR: Failed to read results file: {e}\n")
            self.reset_ui()
            return

        self._log(f"Loaded results: {results_path.name}\n")
        alloc_metric = (result.get("params") or {}).get("allocationMetric")
        if alloc_metric:
            self._log(
                f"Memory metric: {alloc_metric} (heap allocated during timed sort; in-place algorithms may show 0)\n"
            )

        self.update_dashboard(stats)
        self.update_table_view(stats)

        self._log("\nBenchmark completed successfully.")
        self.reset_ui()

    def update_dashboard(self, stats):
        self.after(0, lambda: self._draw_graphs(stats))

    def _draw_graphs(self, stats):
        names = list(stats.keys())
        avg = [stats[n].avg_ms for n in names]
        alloc = [stats[n].avg_allocated_kb for n in names]

        self.ax1.clear()
        self.ax1.set_facecolor("#2b2b2b")
        self.ax1.bar(names, avg, color="#3498db", alpha=0.85)
        self.ax1.set_title("Average Time (ms)", color="white", pad=10)
        self.ax1.tick_params(axis="x", rotation=20, colors="white")
        self.ax1.tick_params(axis="y", colors="white")

        self.ax2.clear()
        self.ax2.set_facecolor("#2b2b2b")
        alloc_values = [(v if v is not None else 0.0) for v in alloc]
        self.ax2.bar(names, alloc_values, color="#9b59b6", alpha=0.85)
        self.ax2.set_title("Heap Allocated During Sort (KB)", color="white", pad=10)
        self.ax2.tick_params(axis="x", rotation=20, colors="white")
        self.ax2.tick_params(axis="y", colors="white")

        self.fig.tight_layout()
        self.canvas.draw()

    def update_table_view(self, stats):
        self.after(0, lambda: self._draw_table(stats))

    def _draw_table(self, stats):
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        for i, (algo, s) in enumerate(stats.items()):
            bg_color = "#2b2b2b" if i % 2 == 0 else "#3a3a3a"
            ctk.CTkLabel(self.table_frame, text=algo, fg_color=bg_color).grid(row=i + 1, column=0, sticky="ew", padx=2, pady=2)
            ctk.CTkLabel(self.table_frame, text=f"{s.avg_ms:.3f}", fg_color=bg_color).grid(row=i + 1, column=1, sticky="ew", padx=2, pady=2)
            ctk.CTkLabel(self.table_frame, text=f"{s.median_ms:.3f}", fg_color=bg_color).grid(row=i + 1, column=2, sticky="ew", padx=2, pady=2)
            alloc_text = "-" if s.avg_allocated_kb is None else f"{s.avg_allocated_kb:.1f}"
            ctk.CTkLabel(self.table_frame, text=alloc_text, fg_color=bg_color).grid(row=i + 1, column=3, sticky="ew", padx=2, pady=2)
            ctk.CTkLabel(self.table_frame, text="OK", fg_color=bg_color, text_color="#2ecc71").grid(row=i + 1, column=4, sticky="ew", padx=2, pady=2)

    def _log(self, text: str):
        self.after(0, lambda: (self.log_box.insert("end", text), self.log_box.see("end")))

    def reset_ui(self):
        self.after(0, self._enable_button)

    def _enable_button(self):
        self.btn_run.configure(state="normal")
        self.status_lbl.configure(text="Status: Completed")


if __name__ == "__main__":
    app = ProSortingApp()
    app.mainloop()
