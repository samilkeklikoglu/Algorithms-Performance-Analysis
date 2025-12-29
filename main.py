import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import algorithms as algos
from utils import generate_data, measure_performance

class ProjectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Performance Analysis 2025")
        self.root.geometry("400x350")
        
        # Seçenekler
        tk.Label(root, text="Veri Boyutu Seç (n):", font=('Arial', 10, 'bold')).pack(pady=5)
        self.size_var = tk.StringVar(value="1000")
        ttk.Combobox(root, textvariable=self.size_var, values=["1000", "10000", "100000"]).pack() # [cite: 26, 27, 28]

        tk.Label(root, text="Veri Karakteristiği:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.type_var = tk.StringVar(value="random")
        ttk.Combobox(root, textvariable=self.type_var, values=["random", "partially_sorted", "reverse"]).pack()

        tk.Button(root, text="Analizi Başlat ve Grafikleri Çiz", command=self.run_analysis, 
                  bg="#2ecc71", fg="white", font=('Arial', 10, 'bold'), height=2).pack(pady=20)

    def run_analysis(self):
        size = int(self.size_var.get())
        d_type = self.type_var.get()
        data = generate_data(size, d_type)
        
        sorting_methods = {
            "Quick Sort": algos.quick_sort,
            "Heap Sort": algos.heap_sort,
            "Shell Sort": algos.shell_sort,
            "Merge Sort": algos.merge_sort,
            "Radix Sort": algos.radix_sort
        }

        times, memories = [], []
        names = list(sorting_methods.keys())

        for name in names:
            t, m = measure_performance(sorting_methods[name], data)
            times.append(t)
            memories.append(m)

        self.show_graphs(names, times, memories, size, d_type)

    def show_graphs(self, names, times, memories, size, d_type):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f"Performans Analizi (n={size}, Tip={d_type})")

        # Zaman Grafiği [cite: 43]
        ax1.bar(names, times, color='skyblue')
        ax1.set_title("Çalışma Süresi (Saniye)")
        ax1.set_ylabel("Saniye")

        # Bellek Grafiği [cite: 44]
        ax2.bar(names, memories, color='salmon')
        ax2.set_title("Bellek Kullanımı (MB)")
        ax2.set_ylabel("MB")

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectApp(root)
    root.mainloop()